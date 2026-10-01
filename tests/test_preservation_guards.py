"""Reproduce independent-review failures in every shipped preservation engine."""
import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / 'output/final/09-capabilities.pptx'
EDITIONS = {
    'Codex': ROOT / 'skills/paper-figure',
    'Claude': ROOT / 'ports/claude/paper-figure',
    'Antigravity': ROOT / 'ports/antigravity/plugin/skills/paper-figure',
}


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def reordered_parts(P, second='ppt/slides/slide2.xml'):
    """A real two-slide OPC package: displayed slide 1 has the second part name."""
    parts = P.load(SAMPLE)
    parts[second] = parts['ppt/slides/slide1.xml']
    parts[str(Path(second).parent / '_rels' / (Path(second).name + '.rels'))] = parts['ppt/slides/_rels/slide1.xml.rels']
    presentation = P.xml(parts['ppt/presentation.xml'])
    ids = presentation.find('p:sldIdLst', P.NS)
    entry = copy.deepcopy(ids[0])
    entry.set('id', str(int(entry.get('id')) + 1))
    entry.set('{' + P.REL + '}id', 'rIdReviewSecond')
    ids.insert(0, entry)
    parts['ppt/presentation.xml'] = P.serial(presentation)
    rels = P.xml(parts['ppt/_rels/presentation.xml.rels'])
    relationship = P.E.SubElement(rels, '{' + P.PACKAGE_REL + '}Relationship')
    relationship.attrib.update({'Id': 'rIdReviewSecond', 'Type': P.REL + '/slide', 'Target': '/' + second})
    parts['ppt/_rels/presentation.xml.rels'] = P.serial(rels)
    types = P.xml(parts['[Content_Types].xml'])
    override = copy.deepcopy(next(x for x in types if x.get('PartName') == '/ppt/slides/slide1.xml'))
    override.set('PartName', '/' + second)
    types.append(override)
    parts['[Content_Types].xml'] = P.serial(types)
    return parts


class GuardCases:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = Path(self.tmp.name)
        self.P = module(self.edition / 'scripts/pptx.py', 'review_pptx_' + self.__class__.__name__)
        self.source = self.dir / 'source.pptx'
        self.source.write_bytes(SAMPLE.read_bytes())
        self.output = self.dir / 'revised.pptx'
        self.planfile = self.dir / 'plan.json'
        self.write_plan()

    def plan(self, source=None, **operation):
        inspected = self.P.inspect(source or self.source)
        obj = next(x for x in inspected['slides'][0]['objects'] if x['name'] == 'encoder')
        return {'sourceSha256': inspected['sha256'], 'operations': [{
            'slide': 1, **{k: obj[k] for k in ('id', 'name', 'fingerprint')},
            'action': 'replace_text', 'old': 'Encoder', 'new': 'Reviewed encoder', **operation,
        }]}

    def write_plan(self, **operation):
        self.planfile.write_text(json.dumps(self.plan(**operation)))

    def cli(self, *args, script='pptx.py', env=None):
        return subprocess.run([sys.executable, str(self.edition / 'scripts' / script), *map(str, args)],
                              text=True, capture_output=True, env=env)

    def patch_cli(self, receipt):
        return self.cli('patch', self.source, self.output, '--plan', self.planfile, '--receipt', receipt)

    def assert_rejected_without_changes(self, command, protected):
        before = {p: p.read_bytes() for p in protected}
        result = command()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertFalse(self.output.exists())
        for path, data in before.items():
            self.assertEqual(path.read_bytes(), data, str(path))

    def test_inspection_report_cannot_overwrite_source(self):
        self.assert_rejected_without_changes(
            lambda: self.cli('inspect', self.source, '--output', self.source), [self.source])

    def test_patch_receipt_collisions_rejected_before_writing(self):
        for receipt in (self.source, self.output, self.planfile):
            with self.subTest(receipt=receipt.name):
                self.assert_rejected_without_changes(lambda: self.patch_cli(receipt), [self.source, self.planfile])

    def test_existing_report_is_preserved_before_patch(self):
        report = self.dir / 'existing.json'
        report.write_text('original report')
        self.assert_rejected_without_changes(lambda: self.patch_cli(report), [self.source, report])

    def test_source_aliases_are_preserved(self):
        for kind in ('symlink', 'hardlink'):
            with self.subTest(kind=kind):
                alias = self.dir / kind
                alias.symlink_to(self.source) if kind == 'symlink' else os.link(self.source, alias)
                self.assert_rejected_without_changes(lambda: self.patch_cli(alias), [self.source, alias])
                self.assert_rejected_without_changes(
                    lambda: self.cli('inspect', self.source, '--output', alias), [self.source, alias])

    def test_future_output_alias_is_rejected(self):
        alias = self.dir / 'future-output.json'
        alias.symlink_to(self.output)
        self.assert_rejected_without_changes(lambda: self.patch_cli(alias), [self.source])
        self.assertTrue(alias.is_symlink())

    def test_dangling_report_link_is_not_followed(self):
        target = self.dir / 'missing.json'
        alias = self.dir / 'report.json'
        alias.symlink_to(target)
        self.assert_rejected_without_changes(lambda: self.patch_cli(alias), [self.source])
        self.assertFalse(target.exists())
        self.assertTrue(alias.is_symlink())

    def test_unavailable_report_directory_prevents_patch(self):
        self.assert_rejected_without_changes(lambda: self.patch_cli(self.dir / 'absent/report.json'), [self.source])

    def test_failed_patch_cleans_reserved_report(self):
        plan = self.plan()
        plan['sourceSha256'] = 'stale'
        self.planfile.write_text(json.dumps(plan))
        receipt = self.dir / 'receipt.json'
        self.assert_rejected_without_changes(lambda: self.patch_cli(receipt), [self.source, self.planfile])
        self.assertFalse(receipt.exists())

    def test_successful_patch_receipt_and_stdout_inspection(self):
        receipt = self.dir / 'receipt.json'
        result = self.patch_cli(receipt)
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = json.loads(receipt.read_text())
        self.assertEqual(saved['outputSha256'], self.P.sha(self.output.read_bytes()))
        self.assertEqual(saved['changed'][0]['part'], 'ppt/slides/slide1.xml')
        inspected = self.cli('inspect', self.output)
        self.assertEqual(inspected.returncode, 0, inspected.stderr)
        self.assertEqual(next(x for x in json.loads(inspected.stdout)['slides'][0]['objects'] if x['name'] == 'encoder')['text'], 'Reviewed encoder')

    def test_reordered_and_renamed_slide_patch_preserves_other_parts(self):
        for second in ('ppt/slides/slide2.xml', 'ppt/slides/method-state.xml'):
            with self.subTest(second=second):
                parts = reordered_parts(self.P, second)
                source = self.dir / (Path(second).stem + '.pptx')
                self.P.save(parts, source)
                inspection = self.P.inspect(source)
                self.assertEqual([(s['slide'], s['part']) for s in inspection['slides']], [(1, second), (2, 'ppt/slides/slide1.xml')])
                output = source.with_name(source.stem + '-patched.pptx')
                receipt = self.P.patch(source, output, self.plan(source, part=second))
                after = self.P.load(output)
                self.assertEqual(receipt['changedParts'], [second])
                self.assertEqual(self.P.text(self.P.lookup(self.P.xml(after[second]), 'encoder')), 'Reviewed encoder')
                for part in parts:
                    if part != second:
                        self.assertEqual(after[part], parts[part], part)

    def test_orphan_slide_is_not_a_displayed_slide(self):
        parts = self.P.load(self.source)
        parts['ppt/slides/slide99.xml'] = parts['ppt/slides/slide1.xml']
        self.assertEqual(self.P.slides(parts), ['ppt/slides/slide1.xml'])

    def test_relative_and_absolute_relationship_targets(self):
        parts = reordered_parts(self.P)
        for target in ('slides/slide2.xml', '/ppt/slides/slide2.xml', 'slides/slide%32.xml'):
            rels = self.P.xml(parts['ppt/_rels/presentation.xml.rels'])
            rels[-1].set('Target', target)
            parts['ppt/_rels/presentation.xml.rels'] = self.P.serial(rels)
            self.assertEqual(self.P.slides(parts), ['ppt/slides/slide2.xml', 'ppt/slides/slide1.xml'])

    def test_invalid_relationships_fail_before_patch(self):
        for change in ('external', 'missing', 'duplicate', 'escape', 'non-slide'):
            with self.subTest(change=change):
                parts = reordered_parts(self.P)
                rels = self.P.xml(parts['ppt/_rels/presentation.xml.rels'])
                if change == 'external': rels[-1].set('TargetMode', 'External')
                elif change == 'missing': rels.remove(rels[-1])
                elif change == 'duplicate': rels[-1].set('Target', 'slides/slide1.xml')
                elif change == 'escape': rels[-1].set('Target', '../../missing.xml')
                else: rels[-1].set('Target', 'presentation.xml')
                parts['ppt/_rels/presentation.xml.rels'] = self.P.serial(rels)
                source = self.dir / (change + '.pptx')
                self.P.save(parts, source)
                plan = self.plan()
                plan['sourceSha256'] = self.P.sha(source.read_bytes())
                with self.assertRaises(ValueError): self.P.patch(source, self.output, plan)
                self.assertFalse(self.output.exists())

    def test_slide_index_and_optional_part_are_checked(self):
        for value in (0, -1, 2, True, '1'):
            with self.subTest(slide=value), self.assertRaises(ValueError):
                self.P.patch(self.source, self.output, self.plan(slide=value))
        with self.assertRaisesRegex(ValueError, 'Slide part'):
            self.P.patch(self.source, self.output, self.plan(part='ppt/slides/stale.xml'))
        self.assertFalse(self.output.exists())

    def test_prepare_uses_displayed_order(self):
        source = self.dir / 'reordered.pptx'
        self.P.save(reordered_parts(self.P), source)
        manifest = {'slides': [
            {'groups': [{'name': 'first-visible-group', 'children': ['encoder']}]},
            {'groups': [{'name': 'second-visible-group', 'children': ['encoder']}]},
        ]}
        self.P.prepare(source, self.output, manifest)
        outputs = [self.output]
        if (self.edition / 'scripts/materialize.py').exists():
            manifest_path = self.dir / 'manifest.json'
            manifest_path.write_text(json.dumps(manifest))
            materialized = self.dir / 'materialized.pptx'
            result = self.cli(source, materialized, '--manifest', manifest_path, script='materialize.py')
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(materialized)
        for output in outputs:
            saved = self.P.load(output)
            self.assertEqual(self.P.name(self.P.lookup(self.P.xml(saved['ppt/slides/slide2.xml']), 'first-visible-group')), 'first-visible-group')
            self.assertEqual(self.P.name(self.P.lookup(self.P.xml(saved['ppt/slides/slide1.xml']), 'second-visible-group')), 'second-visible-group')

    def test_flow_audit_reports_displayed_order_and_part(self):
        source = self.dir / 'reordered.pptx'
        self.P.save(reordered_parts(self.P), source)
        result = self.cli(source, script='flow_audit.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)['connectors']
        self.assertTrue(rows)
        self.assertEqual({(r['slide'], r['part']) for r in rows}, {(1, 'ppt/slides/slide2.xml'), (2, 'ppt/slides/slide1.xml')})

    def test_transformed_or_unsupported_peer_move_rejected(self):
        for change in ('rotation', 'flip', 'ellipse', 'site', 'connector-rotation', 'custom-route'):
            with self.subTest(change=change):
                parts = self.P.load(self.source)
                root = self.P.xml(parts['ppt/slides/slide1.xml'])
                peer = self.P.lookup(root, 'input')
                conn = self.P.lookup(root, 'input-encoder')
                if change == 'rotation': self.P.xfrm(peer).set('rot', '1800000')
                elif change == 'flip': self.P.xfrm(peer).set('flipH', 'true')
                elif change == 'ellipse': peer.find('p:spPr/a:prstGeom', self.P.NS).set('prst', 'ellipse')
                elif change == 'site': conn.find('.//a:stCxn', self.P.NS).set('idx', '9')
                elif change == 'connector-rotation': self.P.xfrm(conn).set('rot', '60000')
                else: conn.find('p:spPr/a:prstGeom', self.P.NS).tag = self.P.q('a:custGeom')
                parts['ppt/slides/slide1.xml'] = self.P.serial(root)
                source = self.dir / (change + '.pptx')
                self.P.save(parts, source)
                before = source.read_bytes()
                with self.assertRaises(ValueError):
                    self.P.patch(source, self.output, self.plan(source, action='move', dx=10, dy=10))
                self.assertEqual(source.read_bytes(), before)
                self.assertFalse(self.output.exists())

    def test_supported_straight_move_updates_both_connector_anchors(self):
        self.P.patch(self.source, self.output, self.plan(action='move', dx=12, dy=20))
        root = self.P.xml(self.P.load(self.output)['ppt/slides/slide1.xml'])
        self.assertEqual(self.P.node_record(self.P.lookup(root, 'encoder'))['boundsPx'][:2], [273, 120])
        result = self.cli(self.output, script='flow_audit.py')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['summary']['requiringRenderedReview'], 0)


for edition, path in EDITIONS.items():
    globals()[edition + 'Guards'] = type(edition + 'Guards', (GuardCases, unittest.TestCase), {'edition': path})


if __name__ == '__main__':
    unittest.main(verbosity=2)

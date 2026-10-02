"""Real schema failures, lossless normalization and offline validation in all ports."""
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from test_preservation_guards import EDITIONS, SAMPLE, module


class PackageCases:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        from pathlib import Path
        self.dir = Path(self.tmp.name)
        self.P = module(self.edition / 'scripts/pptx.py', 'package_' + self.__class__.__name__)
        self.parts = self.P.load(SAMPLE)
        self.source, self.output = self.dir / 'source.pptx', self.dir / 'fixed.pptx'

    def bad_order(self):
        root = self.P.xml(self.parts['ppt/presentation.xml'])
        notes = root.find('p:notesMasterIdLst', self.P.NS)
        root.remove(notes)
        root.insert(root.index(root.find('p:sldIdLst', self.P.NS)) + 1, notes)
        self.parts['ppt/presentation.xml'] = self.P.serial(root)

    def write(self):
        self.P.save(self.parts, self.source)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(self.edition / 'scripts/pptx.py'), *map(str, args)],
                              text=True, capture_output=True)

    def test_order_failure_caught_by_inspect_and_official_schema(self):
        self.bad_order(); self.write()
        self.assertFalse(self.P.inspect(self.source)['passed'])
        result = self.P.validate(self.source)
        self.assertFalse(result['passed'])
        self.assertTrue(any(e['part'] == 'ppt/presentation.xml' and 'notesMasterIdLst' in e['message'] for e in result['errors']))

    def test_normalization_preserves_all_other_parts_and_source(self):
        self.bad_order()
        self.parts = {'ppt/': b'', 'custom/opaque.bin': b'keep\x00\xff', **self.parts}
        self.write(); before = self.source.read_bytes()
        result = self.P.normalize(self.source, self.output)
        self.assertEqual(result['changedParts'], ['ppt/presentation.xml'])
        self.assertEqual(self.source.read_bytes(), before)
        with zipfile.ZipFile(self.output) as z:
            self.assertEqual(z.namelist()[0], '[Content_Types].xml')
            self.assertFalse(any(n.endswith('/') for n in z.namelist()))
            for name, data in self.parts.items():
                if not name.endswith('/') and name != 'ppt/presentation.xml':self.assertEqual(z.read(name), data)
        self.assertTrue(self.P.validate(self.output)['passed'])
        again = self.dir / 'again.pptx'
        second = self.P.normalize(self.output, again)
        self.assertEqual(second['changedParts'], [])
        self.assertEqual(self.P.load(self.output), self.P.load(again))

    def test_prepare_normalizes_and_validates_before_save(self):
        self.bad_order(); self.write()
        self.P.prepare(self.source, self.output, {'slides': [{}]})
        self.assertTrue(self.P.validate(self.output)['passed'])
        with zipfile.ZipFile(self.output) as z:self.assertEqual(z.namelist()[0], '[Content_Types].xml')

    def test_prepare_rejects_schema_invalid_shape_before_save(self):
        root = self.P.xml(self.parts['ppt/slides/slide1.xml'])
        root.find('.//a:xfrm/a:ext', self.P.NS).set('cx', '-1')
        self.parts['ppt/slides/slide1.xml'] = self.P.serial(root)
        self.write()
        with self.assertRaisesRegex(ValueError, 'XSD'):self.P.prepare(self.source, self.output, {'slides': [{}]})
        self.assertFalse(self.output.exists())

    def test_patch_does_not_implicitly_normalize_human_file(self):
        self.bad_order(); self.parts = {'ppt/': b'', **self.parts}; self.write()
        info = self.P.inspect(self.source)
        obj = next(o for o in info['slides'][0]['objects'] if o['name'] == 'encoder')
        plan = {'sourceSha256': info['sha256'], 'operations': [{
            'slide': 1, **{k: obj[k] for k in ('id', 'name', 'fingerprint')},
            'action': 'replace_text', 'old': 'Encoder', 'new': 'Reviewed'}]}
        self.P.patch(self.source, self.output, plan)
        saved = self.P.load(self.output)
        self.assertEqual(list(saved), list(self.parts))
        for name, data in self.parts.items():
            if name != 'ppt/slides/slide1.xml':self.assertEqual(saved[name], data)

    def test_unknown_or_duplicate_presentation_children_are_not_repaired(self):
        for tag in ('p:sldSz', '{urn:test}unknown'):
            with self.subTest(tag=tag):
                parts = self.parts.copy(); root = self.P.xml(parts['ppt/presentation.xml'])
                self.P.E.SubElement(root, self.P.q(tag) if tag.startswith('p:') else tag)
                parts['ppt/presentation.xml'] = self.P.serial(root)
                with self.assertRaises(ValueError):self.P.normalized_parts(parts)

    def test_unrecognized_xml_is_explicitly_incomplete(self):
        self.parts['custom/unknown.xml'] = b'<extra xmlns="urn:unknown"/>'
        result = self.P.validate_parts(self.parts)
        self.assertFalse(result['passed']); self.assertFalse(result['complete'])
        self.assertEqual(result['uncheckedParts'][0]['part'], 'custom/unknown.xml')

    def test_content_type_declared_xml_is_checked_without_xml_suffix(self):
        root = self.P.xml(self.parts['[Content_Types].xml'])
        self.P.E.SubElement(root, '{http://schemas.openxmlformats.org/package/2006/content-types}Override',
                           PartName='/custom/payload.dat', ContentType='application/custom+xml')
        self.parts['[Content_Types].xml'] = self.P.serial(root)
        self.parts['custom/payload.dat'] = b'<broken'
        result = self.P.validate_parts(self.parts)
        self.assertFalse(result['passed'])
        self.assertTrue(any(e['part'] == 'custom/payload.dat' for e in result['errors']))

    def test_lax_extensions_are_not_silently_counted_as_validated(self):
        root = self.P.xml(self.parts['ppt/presentation.xml'])
        ext = self.P.sub(self.P.sub(root, 'p:extLst'), 'p:ext', uri='urn:example')
        self.P.E.SubElement(ext, '{urn:unknown}unvalidated')
        self.parts['ppt/presentation.xml'] = self.P.serial(root)
        result = self.P.validate_parts(self.parts)
        self.assertTrue(result['passed'])
        self.assertTrue(any(e['part'] == 'ppt/presentation.xml' for e in result['unvalidatedExtensions']))

    def test_validate_does_not_resolve_document_external_entities(self):
        secret = self.dir / 'private.txt'; secret.write_text('MUST_NOT_APPEAR')
        self.parts['custom/entity.xml'] = ('<!DOCTYPE x [<!ENTITY leak SYSTEM "'+secret.as_uri()+'">]><x>&leak;</x>').encode()
        result = self.P.validate_parts(self.parts)
        self.assertFalse(result['passed']); self.assertNotIn('MUST_NOT_APPEAR', json.dumps(result))

    def test_missing_schema_bundle_fails_explicitly(self):
        self.P.SCHEMA_DIR = self.dir / 'absent'
        with self.assertRaisesRegex(ValueError, 'schemas are missing'):self.P.validate_parts(self.parts)

    def test_cli_normalize_refuses_colliding_receipts_and_existing_output(self):
        self.bad_order(); self.write(); before = self.source.read_bytes()
        for path in (self.source, self.output):
            result = self.cli('normalize', self.source, self.output, '--receipt', path)
            self.assertNotEqual(result.returncode, 0); self.assertFalse(self.output.exists())
            self.assertEqual(self.source.read_bytes(), before)
        self.output.write_bytes(b'keep')
        receipt = self.dir / 'receipt.json'
        result = self.cli('normalize', self.source, self.output, '--receipt', receipt)
        self.assertNotEqual(result.returncode, 0); self.assertEqual(self.output.read_bytes(), b'keep')
        self.assertFalse(receipt.exists())

    def test_cli_validate_exit_codes_and_report_preservation(self):
        self.bad_order(); self.write()
        result = self.cli('validate', self.source)
        self.assertEqual(result.returncode, 1); self.assertFalse(json.loads(result.stdout)['passed'])
        before = self.source.read_bytes()
        result = self.cli('validate', self.source, '--output', self.source)
        self.assertNotEqual(result.returncode, 0); self.assertEqual(self.source.read_bytes(), before)
        result = self.cli('normalize', self.source, self.output, '--receipt', self.dir / 'receipt.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli('validate', self.output)
        self.assertEqual(result.returncode, 0, result.stderr); self.assertTrue(json.loads(result.stdout)['passed'])


for name, edition in EDITIONS.items():
    globals()['TestPackage' + name] = type('TestPackage' + name, (PackageCases, unittest.TestCase), {'edition': edition})

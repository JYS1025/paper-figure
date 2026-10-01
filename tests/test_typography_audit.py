"""Regression checks against saved output and explicit PDF character metrics."""
import hashlib
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/paper-figure/scripts'))
import typography_audit as T


def region(**updates):
    result = {'name': 'formula', 'page': 1, 'boundsPt': [0, 0, 100, 100], 'expectedText': 'xi',
              'expectedFonts': ['ArialMT'], 'minSizePt': 6, 'minRelativeSize': .6}
    result.update(updates)
    return result


def plan(source, regions):
    return {'pdfSha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'publicationWidthMm': 177.8, 'regions': regions}


class TypographyAudit(unittest.TestCase):
    def test_detects_actual_too_small_scripts(self):
        source = ROOT / 'output/unseen-suite-05/spatial-assignment/figure.pdf'
        spec = region(boundsPt=[260, 30, 504, 54], expectedFonts=['LiberationSans'],
                      expectedText='aci = area(Cc ∩ Di) / area(Di)')
        result = T.audit(source, plan(source, [spec]))
        r = result['regions'][0]
        self.assertAlmostEqual(r['minPublicationSizePt'], 4.089, places=3)
        self.assertIn('below_selected_minimum_size', r['reviewReasons'])
        self.assertIn('below_selected_relative_size', r['reviewReasons'])
        self.assertNotIn('character_inventory_mismatch', r['reviewReasons'])
        self.assertNotIn('passed', result)

    def test_detects_fallback_despite_declared_arial(self):
        source = ROOT / 'output/hybrid-assets-test-06/figure.pdf'
        result = T.audit(source, plan(source, [region(boundsPt=[150, 178, 201, 205], expectedText='s(tₖ)')]))
        r = result['regions'][0]
        self.assertIn('LinuxLibertineG', r['unexpectedFonts'])
        self.assertIn('unexpected_rendered_font', r['reviewReasons'])
        self.assertNotIn('character_inventory_mismatch', r['reviewReasons'])

    def test_partial_missing_script_is_not_hidden_by_extractable_base(self):
        char = {'text': 'x', 'fontname': 'ABCDEF+ArialMT', 'size': 10,
                'x0': 5, 'x1': 15, 'top': 5, 'bottom': 15}
        r = T.region_report([char], region(expectedText='xi'), 1)
        self.assertEqual(r['missingCharacters'], {'i': 1})
        self.assertIn('character_inventory_mismatch', r['reviewReasons'])

    def test_publication_scaling_changes_absolute_size_not_ratio(self):
        chars = [{'text': 'x', 'fontname': 'ABCDEF+ArialMT', 'size': 10,
                  'x0': 5, 'x1': 15, 'top': 5, 'bottom': 15},
                 {'text': 'i', 'fontname': 'ABCDEF+ArialMT', 'size': 7,
                  'x0': 15, 'x1': 20, 'top': 12, 'bottom': 19}]
        full = T.region_report(chars, region(), 1)
        half = T.region_report(chars, region(), .5)
        self.assertEqual(full['reviewReasons'], [])
        self.assertEqual(half['minPublicationSizePt'], 3.5)
        self.assertEqual(full['minToMaxSizeRatio'], half['minToMaxSizeRatio'])
        self.assertIn('below_selected_minimum_size', half['reviewReasons'])

    def test_region_without_text_is_unmeasured_not_passed(self):
        r = T.region_report([], region(), 1)
        self.assertIn('no_extractable_text_inside_region', r['reviewReasons'])
        self.assertIsNone(r['minToMaxSizeRatio'])

    def test_boundary_glyph_is_not_silently_excluded(self):
        char = {'text': 'k', 'fontname': 'ABCDEF+OtherFont', 'size': 7,
                'x0': 99, 'x1': 104, 'top': 5, 'bottom': 12}
        r = T.region_report([char], region(), 1)
        self.assertEqual(len(r['boundaryCharacters']), 1)
        self.assertIn('characters_cross_region_boundary', r['reviewReasons'])
        self.assertIn('unexpected_rendered_font', r['reviewReasons'])

    def test_stale_render_rejected(self):
        source = ROOT / 'output/hybrid-assets-test-06/figure.pdf'
        spec = plan(source, [region()]); spec['pdfSha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'changed'):
            T.audit(source, spec)

    def test_audit_leaves_pdf_unchanged(self):
        source = ROOT / 'output/hybrid-assets-test-06/figure.pdf'
        before = source.read_bytes()
        T.audit(source, plan(source, [region(boundsPt=[150, 178, 201, 205])]))
        self.assertEqual(before, source.read_bytes())

    def test_bad_coordinates_and_overlap_are_rejected(self):
        source = ROOT / 'output/hybrid-assets-test-06/figure.pdf'
        invalid = [[0, 0, float('nan'), 30], [0, 0, -1, 3]]
        for box in invalid:
            with self.assertRaises(ValueError):
                T.validate_plan(plan(source, [region(boundsPt=box)]))
        with self.assertRaisesRegex(ValueError, 'overlap'):
            T.validate_plan(plan(source, [region(), region(name='duplicate-area')]))

    def test_cli_refuses_overwriting_source(self):
        source = ROOT / 'output/hybrid-assets-test-06/figure.pdf'
        before = source.read_bytes()
        script = ROOT / 'skills/paper-figure/scripts/typography_audit.py'
        result = subprocess.run([sys.executable, str(script), str(source),
                                 '--plan', 'unused.json', '--output', str(source)],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, source.read_bytes())


if __name__ == '__main__':
    unittest.main()

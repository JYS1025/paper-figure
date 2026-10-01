"""Keep runtime recovery guidance inside the shipped package."""
import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('skill_package', ROOT / 'scripts/skill_package.py')
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)


class PackageReferences(unittest.TestCase):
    def test_all_editions_include_linked_guides(self):
        for relative in ('skills/paper-figure', 'ports/claude/paper-figure', 'ports/antigravity/plugin/skills/paper-figure'):
            with self.subTest(edition=relative):
                root = ROOT / relative
                counts = K.validate_references(root, K.skill_files(root))
                self.assertGreater(counts['markdownLinks'], 0)

    def test_missing_script_guide_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'scripts').mkdir()
            (root / 'scripts/render.py').write_text("raise SystemExit('See references/missing-environment.md')")
            with self.assertRaisesRegex(ValueError, 'missing-environment.md'):
                K.validate_references(root, K.skill_files(root))

    def test_excluded_or_external_guide_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'SKILL.md').write_text('[guide](.private/guide.md)')
            (root / '.private').mkdir()
            (root / '.private/guide.md').write_text('not shipped')
            with self.assertRaises(ValueError): K.validate_references(root, K.skill_files(root))

    def test_antigravity_missing_renderer_points_to_shipped_guide(self):
        skill = ROOT / 'ports/antigravity/plugin/skills/paper-figure'
        with tempfile.TemporaryDirectory() as directory:
            env = os.environ.copy()
            env['PATH'] = directory
            env.pop('FIGURE_SOFFICE', None)
            env.pop('FIGURE_PDFTOPPM', None)
            result = subprocess.run([sys.executable, str(skill / 'scripts/render.py'),
                                     str(ROOT / 'output/final/09-capabilities.pptx'), directory + '/render'],
                                    env=env, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            guides = re.findall(r'references/[\w.-]+\.md', result.stdout + result.stderr)
            self.assertTrue(guides, result.stderr)
            self.assertTrue(all((skill / guide).is_file() for guide in guides), guides)


if __name__ == '__main__':
    unittest.main(verbosity=2)

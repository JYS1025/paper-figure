"""Default authoring preflight must not invoke the optional credential helper."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PORTS = ('ports/claude/paper-figure', 'ports/antigravity/plugin/skills/paper-figure')


class PreflightDisclosure(unittest.TestCase):
    def run_preflight(self, edition, requested):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            shutil.copy2(ROOT / edition / 'scripts/preflight.mjs', work / 'preflight.mjs')
            # Isolate authoring-package availability, preserving the real subprocess logic.
            (work / 'runtime.mjs').write_text(
                "export const python=process.env.FIGURE_PYTHON;\n"
                "export const pptxgen=()=>class {version='test-engine'};\n")
            marker = work / 'credential-helper-called'
            (work / 'gemini_image.py').write_text(
                'from pathlib import Path\n'
                "Path(__file__).with_name('credential-helper-called').write_text('status')\n"
                'print(\'{"configured":true,"verifiedWithProvider":false}\')\n')
            env = os.environ.copy()
            env.update(FIGURE_PYTHON=sys.executable, PAPER_FIGURE_GEMINI_API_KEY='fixture-secret-never-display')
            node = env.get('FIGURE_NODE') or shutil.which('node')
            if not node: self.skipTest('Node.js is required for the portable preflight test')
            command = [node, str(work / 'preflight.mjs')]
            if requested: command.append('--check-gemini-api')
            result = subprocess.run(command, env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(env['PAPER_FIGURE_GEMINI_API_KEY'], result.stdout + result.stderr)
            return json.loads(result.stdout), marker.exists()

    def test_default_does_not_call_or_disclose_credentials_even_with_key_configured(self):
        for edition in PORTS:
            with self.subTest(edition=edition):
                result, invoked = self.run_preflight(edition, False)
                self.assertFalse(invoked)
                self.assertNotIn('imageGeneration', result)
                self.assertTrue(result['engine']['available'])

    def test_explicit_check_invokes_helper_without_claiming_provider_access(self):
        for edition in PORTS:
            with self.subTest(edition=edition):
                result, invoked = self.run_preflight(edition, True)
                self.assertTrue(invoked)
                self.assertTrue(result['imageGeneration']['credentialStatus']['configured'])
                self.assertFalse(result['imageGeneration']['providerVerified'])


if __name__ == '__main__':
    unittest.main(verbosity=2)

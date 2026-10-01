"""Offline transport, credential and packaging tests; never call a paid API."""
import base64
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from unittest.mock import patch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
def load_client(script, name):
    spec = importlib.util.spec_from_file_location(name, script)
    client = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(client)
    return client

sys.path.insert(0, str(ROOT / 'scripts'))
from skill_package import skill_files

class ImageClientCases:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.key = 'fixture-private-token-not-a-real-key'
        self.env = patch.dict(os.environ, {'PAPER_FIGURE_GEMINI_KEY_FILE': str(self.root/'key')}, clear=True)
        self.env.start()
        data = io.BytesIO();Image.new('RGB', (2, 3), 'teal').save(data, format='PNG');self.png = data.getvalue()
        self.reply = {'responseId':'fixture-response', 'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':'explanation'}, {'inlineData':{'mimeType':'image/png','data':base64.b64encode(self.png).decode()}}]}}]}
        self.calls = []

    def tearDown(self):
        self.env.stop();self.tmp.cleanup()

    def transport(self, url, key, payload, timeout):
        self.calls.append((url, key, payload, timeout));return self.reply

    def generate(self, **kw):
        os.environ['PAPER_FIGURE_GEMINI_API_KEY'] = self.key
        return self.G.generate('An illustrative composition.', self.root/'out', purpose='draft', transport=self.transport, **kw)

    def test_saved_image_and_manifest_match_actual_response(self):
        result = self.generate()
        self.assertEqual((self.root/'out/image-01.png').read_bytes(), self.png)
        self.assertEqual(result['images'][0]['dimensions'], [2,3])
        self.assertFalse(result['imageInspectedByAgent'])
        self.assertEqual(result['purpose'], 'draft')
        self.assertEqual(len(self.calls), 1)
        url, key, payload, timeout = self.calls[0]
        self.assertEqual(url, 'https://generativelanguage.googleapis.com/v1/models/gemini-3.1-flash-image:generateContent')
        self.assertEqual(key, self.key)
        self.assertEqual(payload['generationConfig']['responseFormat']['image']['aspectRatio'], '16:9')
        for p in (self.root/'out').iterdir():self.assertNotIn(self.key.encode(), p.read_bytes())

    def test_selected_reference_is_encoded_and_hashed(self):
        ref=self.root/'reference.png';ref.write_bytes(self.png)
        result=self.generate(references=[ref])
        self.assertEqual(result['references'][0]['mimeType'], 'image/png')
        self.assertEqual(base64.b64decode(self.calls[0][2]['contents'][0]['parts'][1]['inlineData']['data']), self.png)

    def test_missing_key_makes_no_request_or_success_output(self):
        with self.assertRaises(self.G.ImageError):self.G.generate('Figure', self.root/'out', purpose='draft', transport=self.transport)
        self.assertEqual(self.calls, []);self.assertFalse((self.root/'out').exists())

    def test_existing_output_is_preserved_without_request(self):
        out=self.root/'out';out.mkdir();(out/'keep').write_text('original')
        with self.assertRaises(self.G.ImageError):self.generate()
        self.assertEqual(self.calls, []);self.assertEqual((out/'keep').read_text(), 'original')

    def test_text_only_is_failure_not_a_draft(self):
        self.reply={'candidates':[{'content':{'parts':[{'text':'Cannot create an image'}]}}]}
        with self.assertRaises(self.G.ImageError):self.generate()
        self.assertFalse((self.root/'out/generation.json').exists())
        self.assertTrue((self.root/'out/failure.json').exists());self.assertEqual(len(self.calls), 1)

    def test_blocked_candidate_does_not_count_as_success(self):
        self.reply['promptFeedback']={'blockReason':'SAFETY'}
        with self.assertRaises(self.G.ImageError):self.generate()
        self.assertFalse((self.root/'out/generation.json').exists())

    def test_thought_image_is_not_a_final_image(self):
        self.reply['candidates'][0]['content']['parts'][1]['thought']=True
        with self.assertRaises(self.G.ImageError):self.generate()

    def test_truncated_candidate_is_not_delivered(self):
        self.reply['candidates'][0]['finishReason']='MAX_TOKENS'
        with self.assertRaises(self.G.ImageError):self.generate()

    def test_malformed_response_produces_safe_failure(self):
        self.reply={'candidates':[None]}
        with self.assertRaises(self.G.ImageError):self.generate()
        self.assertFalse((self.root/'out/generation.json').exists())

    def test_invalid_image_content_rejected(self):
        self.reply['candidates'][0]['content']['parts'][1]['inlineData']['data']=base64.b64encode(b'not an image').decode()
        with self.assertRaises(self.G.ImageError):self.generate()

    def test_mime_mismatch_rejected(self):
        self.reply['candidates'][0]['content']['parts'][1]['inlineData']['mimeType']='image/jpeg'
        with self.assertRaises(self.G.ImageError):self.generate()

    def test_model_url_cannot_redirect_credentials(self):
        with self.assertRaises(self.G.ImageError):self.generate(model='https://example.invalid/image')
        self.assertEqual(self.calls, [])

    def test_embedded_credential_rejected_before_recording_prompt(self):
        os.environ['PAPER_FIGURE_GEMINI_API_KEY']=self.key
        with self.assertRaises(self.G.ImageError):self.G.generate(self.key, self.root/'out', purpose='draft', transport=self.transport)
        self.assertFalse((self.root/'out').exists());self.assertEqual(self.calls, [])

    def test_error_bodies_never_reveal_keys(self):
        error=urllib.error.HTTPError('https://generativelanguage.googleapis.com', 403, self.key, {}, io.BytesIO(self.key.encode()))
        with patch.object(urllib.request.OpenerDirector, 'open', side_effect=error):
            with self.assertRaises(self.G.ImageError) as caught:self.G.request_json(self.G.API_ROOT+'model:generateContent',self.key,{},1)
        self.assertNotIn(self.key, str(caught.exception))

    def test_key_is_header_only_and_redirects_disabled(self):
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self,n):return b'{}'
        with patch.object(urllib.request.OpenerDirector,'open',return_value=Response()) as call:
            self.G.request_json(self.G.API_ROOT+'model:generateContent',self.key,{'contents':[]},1)
        request=call.call_args.args[0]
        self.assertNotIn(self.key,request.full_url);self.assertNotIn(self.key.encode(),request.data)
        self.assertEqual(dict(request.header_items())['X-goog-api-key'],self.key)
        self.assertIsNone(self.G.NoRedirect().redirect_request(request,None,302,'',{},'https://example.invalid'))

    def test_key_file_registration_private_and_not_overwritten(self):
        file=self.root/'keys/api';self.G.save_key(self.key,file)
        if os.name!='nt':self.assertEqual(stat.S_IMODE(file.stat().st_mode),0o600)
        self.assertEqual(self.G.stored_key(file),self.key)
        with self.assertRaises(self.G.ImageError):self.G.save_key('other-value',file)
        self.assertEqual(self.G.stored_key(file),self.key)
        self.G.save_key('other-value',file,replace=True);self.assertEqual(self.G.stored_key(file),'other-value')

    @unittest.skipIf(os.name=='nt','POSIX file modes')
    def test_public_key_file_and_symlink_rejected(self):
        file=self.root/'key';file.write_text(self.key);file.chmod(0o644)
        with self.assertRaises(self.G.ImageError):self.G.stored_key(file)
        file.chmod(0o600);link=self.root/'link';link.symlink_to(file)
        with self.assertRaises(self.G.ImageError):self.G.stored_key(link)

    def test_environment_precedence_and_status_do_not_expose_key(self):
        os.environ['GEMINI_API_KEY']='low-priority';os.environ['GOOGLE_API_KEY']='sdk-priority'
        self.assertEqual(self.G.credentials()[0],'sdk-priority')
        os.environ['PAPER_FIGURE_GEMINI_API_KEY']=self.key
        self.assertEqual(self.G.credentials()[0],self.key)
        self.assertNotIn(self.key,json.dumps(self.G.status()));self.assertFalse(self.G.status()['verifiedWithProvider'])

    def test_cli_rejects_key_argument_without_echoing_it(self):
        result=subprocess.run([sys.executable,str(self.script),'generate','--api-key',self.key],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0);self.assertNotIn(self.key,result.stderr+result.stdout)

    def test_setup_requires_a_human_terminal(self):
        result=subprocess.run([sys.executable,str(self.script),'setup'],input=self.key,capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0);self.assertNotIn(self.key,result.stderr+result.stdout)
        self.assertFalse((self.root/'key').exists())

    def test_packaging_omits_local_credentials_and_dependencies(self):
        for name in ['SKILL.md','scripts/helper.py','scripts/.env','scripts/gemini-api-key','secret.key','.env','node_modules/pkg/index.js','references/options.md']:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('fixture')
        self.assertEqual([str(p.relative_to(self.root)) for p in skill_files(self.root)],['SKILL.md','references/options.md','scripts/helper.py'])

for edition, relative in {
    'Codex': 'skills/paper-figure',
    'Claude': 'ports/claude/paper-figure',
    'Antigravity': 'ports/antigravity/plugin/skills/paper-figure',
}.items():
    script = ROOT / relative / 'scripts/gemini_image.py'
    globals()[edition + 'ImageClientTests'] = type(
        edition + 'ImageClientTests', (ImageClientCases, unittest.TestCase),
        {'script': script, 'G': load_client(script, 'gemini_' + edition.lower())})

if __name__=='__main__':unittest.main()

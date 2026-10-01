#!/usr/bin/env python3
"""Optional Gemini image drafts/assets. Credentials never enter command arguments.

status is offline; setup is for a human terminal; generate makes one API request.
"""
import argparse
import base64
import binascii
import getpass
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

DEFAULT_MODEL = 'gemini-3.1-flash-image'
API_ROOT = 'https://generativelanguage.googleapis.com/v1/models/'
MAX_BYTES = 64 * 1024 * 1024
ENV_KEYS = ('PAPER_FIGURE_GEMINI_API_KEY', 'GOOGLE_API_KEY', 'GEMINI_API_KEY')
RATIOS = ('1:1', '1:4', '1:8', '2:3', '3:2', '3:4', '4:1', '4:3', '4:5', '5:4', '8:1', '9:16', '16:9', '21:9')
MIMES = {'PNG': 'image/png', 'JPEG': 'image/jpeg', 'WEBP': 'image/webp'}
EXTENSIONS = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/webp': '.webp'}


class ImageError(Exception):
    """Only fixed, non-secret diagnostics may be exposed to the CLI."""


def key_path():
    override = os.environ.get('PAPER_FIGURE_GEMINI_KEY_FILE')
    if override:
        return Path(override).expanduser()
    base = Path(os.environ.get('APPDATA', Path.home() / '.config')) if os.name == 'nt' else Path.home() / '.config'
    return base / 'paper-figure' / 'gemini-api-key'


def valid_key(value):
    if not isinstance(value, str) or not value or len(value) > 512 or not re.fullmatch(r'[!-~]+', value):
        raise ImageError('Invalid key format. Register the key locally; do not paste it into chat.')
    return value


def stored_key(path):
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, 'r', encoding='utf8') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or (os.name != 'nt' and (info.st_mode & 0o077 or info.st_uid != os.getuid())):
                raise ImageError('The local key file must be owned by you and private (chmod 600).')
            return valid_key(stream.read(514).strip())
    except ImageError:
        raise
    except (OSError, UnicodeError):
        raise ImageError('Cannot read the private key file. Check its location and permissions.') from None


def credentials():
    for name in ENV_KEYS:
        if os.environ.get(name):
            return valid_key(os.environ[name]), name
    path = key_path()
    if path.exists() or path.is_symlink():
        return stored_key(path), 'local key file'
    raise ImageError('Gemini key is not configured. Run setup in your own terminal, set PAPER_FIGURE_GEMINI_API_KEY, or choose no-API mode.')


def status():
    try:
        _, source = credentials()
        return {'configured': True, 'source': source, 'model': DEFAULT_MODEL, 'verifiedWithProvider': False}
    except ImageError as error:
        return {'configured': False, 'model': DEFAULT_MODEL, 'verifiedWithProvider': False, 'guidance': str(error)}


def save_key(value, path, replace=False):
    value = valid_key(value)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    flags = os.O_WRONLY | os.O_CREAT | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    if not replace:
        flags |= os.O_EXCL
    try:
        fd = os.open(path, flags, 0o600)
        with os.fdopen(fd, 'w', encoding='utf8') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or (os.name != 'nt' and info.st_uid != os.getuid()):
                raise ImageError('Key was not saved. Use a regular file owned by you.')
            if os.name != 'nt':
                os.fchmod(stream.fileno(), 0o600)
            stream.truncate(0)
            stream.write(value + '\n')
    except OSError:
        raise ImageError('Key was not saved. Check permissions; use setup --replace only to replace your existing key.') from None


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_json(url, key, payload, timeout):
    data = json.dumps(payload).encode('utf8')
    if len(data) > MAX_BYTES:
        raise ImageError('Request is too large. Use fewer or smaller reference images.')
    request = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=timeout) as response:
            raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ImageError('Image response exceeded the supported size limit.')
        return json.loads(raw)
    except urllib.error.HTTPError as error:
        reasons = {400: 'Request rejected; check the model, prompt and reference formats.', 401: 'Authentication failed; register a valid key.', 403: 'Access denied; check key restrictions and model access.', 404: 'Model not found; select an available image model with --model.', 429: 'Quota or rate limit reached; check your Gemini project quota.'}
        reason = reasons.get(error.code, 'Provider request failed. No automatic retry was made.')
        raise ImageError(f'Gemini HTTP {error.code}. {reason}') from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ImageError('Gemini network request failed or timed out. No automatic retry was made; a timed-out request may still have been processed.') from None
    except (json.JSONDecodeError, UnicodeError):
        raise ImageError('Gemini returned an unreadable response.') from None


def image_info(data):
    from PIL import Image
    try:
        with Image.open(io.BytesIO(data)) as image:
            fmt, size = image.format, image.size
            image.verify()
        if fmt not in MIMES:
            raise ImageError('Only PNG, JPEG and WebP images are supported.')
        return MIMES[fmt], list(size)
    except ImageError:
        raise
    except Exception:
        raise ImageError('Invalid image bytes. No successful image output was recorded.') from None


def decode_images(response):
    if not isinstance(response, dict):
        raise ImageError('Gemini returned an unexpected response structure.')
    if response.get('promptFeedback', {}).get('blockReason'):
        raise ImageError('Gemini blocked this image request. Review the prompt; no automatic retry was made.')
    result = []
    for candidate in response.get('candidates', []):
        if candidate.get('finishReason') not in (None, 'STOP'):
            continue
        for part in candidate.get('content', {}).get('parts', []):
            item = part.get('inlineData')
            if part.get('thought') or not item:
                continue
            if item.get('mimeType') not in EXTENSIONS:
                raise ImageError('Gemini returned an unsupported image type.')
            try:
                data = base64.b64decode(item.get('data', ''), validate=True)
            except (ValueError, TypeError, binascii.Error):
                raise ImageError('Gemini returned invalid image encoding.') from None
            mime, dimensions = image_info(data)
            if mime != item['mimeType']:
                raise ImageError('Gemini image format did not match its declared type.')
            result.append((data, mime, dimensions))
    if not result:
        raise ImageError('Gemini returned no final image. Text-only or blocked responses do not count as a generated draft.')
    return result


def generate(prompt, output_dir, *, purpose, model=DEFAULT_MODEL, aspect_ratio='16:9', references=(), timeout=180, transport=request_json):
    try:
        from PIL import Image  # Check decoding support before a billable request.
    except ImportError:
        raise ImageError('Install Pillow before making an image request.') from None
    if purpose not in ('draft', 'asset') or aspect_ratio not in RATIOS:
        raise ImageError('Choose purpose draft/asset and a supported aspect ratio.')
    if not re.fullmatch(r'[a-z0-9][a-z0-9._-]{1,100}', model) or 'image' not in model:
        raise ImageError('Use an image model ID, without a URL or path.')
    if not isinstance(prompt, str) or not prompt.strip():
        raise ImageError('The prompt file is empty.')
    key, _ = credentials()
    if key in prompt or key in str(output_dir) or key in model:
        raise ImageError('A credential appeared in task input. Remove it before generating an image.')
    parts, refs = [{'text': prompt}], []
    if len(references) > 14:
        raise ImageError('Use at most fourteen selected reference images.')
    for reference in references:
        try:
            with Path(reference).open('rb') as stream:
                data = stream.read(MAX_BYTES + 1)
        except OSError:
            raise ImageError('Cannot read a selected reference image.') from None
        if len(data) > MAX_BYTES:
            raise ImageError('Reference image is too large.')
        mime, dimensions = image_info(data)
        parts.append({'inlineData': {'mimeType': mime, 'data': base64.b64encode(data).decode('ascii')}})
        refs.append({'sha256': hashlib.sha256(data).hexdigest(), 'mimeType': mime, 'dimensions': dimensions})
    payload = {'contents': [{'role': 'user', 'parts': parts}], 'generationConfig': {'responseModalities': ['TEXT', 'IMAGE'], 'responseFormat': {'image': {'aspectRatio': aspect_ratio}}}}
    output = Path(output_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        output.mkdir(mode=0o700)
    except FileExistsError:
        raise ImageError('Output directory already exists. Choose a new directory before making an API call.') from None
    (output / 'prompt.txt').write_text(prompt, encoding='utf8')
    try:
        response = transport(API_ROOT + model + ':generateContent', key, payload, timeout)
        try:
            images = decode_images(response)
        except (AttributeError, TypeError, KeyError):
            raise ImageError('Gemini returned an unexpected response structure.') from None
        files = []
        for i, (data, mime, dimensions) in enumerate(images, 1):
            name = f'image-{i:02d}' + EXTENSIONS[mime]
            with (output / name).open('xb') as stream:
                stream.write(data)
            files.append({'file': name, 'mimeType': mime, 'dimensions': dimensions, 'sha256': hashlib.sha256(data).hexdigest()})
        response_id = response.get('responseId')
        safe_id = response_id if isinstance(response_id, str) and re.fullmatch(r'[\w.-]{1,200}', response_id) and key not in response_id else None
        record = {'provider': 'Google Gemini API', 'api': 'generateContent v1', 'model': model, 'purpose': purpose, 'createdAt': datetime.now(timezone.utc).isoformat(), 'responseId': safe_id, 'promptFile': 'prompt.txt', 'aspectRatio': aspect_ratio, 'references': refs, 'images': files, 'imageInspectedByAgent': False}
        (output / 'generation.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf8')
        return record
    except ImageError as error:
        (output / 'failure.json').write_text(json.dumps({'success': False, 'message': str(error), 'automaticRetries': 0}) + '\n', encoding='utf8')
        raise


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, 'Invalid command arguments. Use --help; provide credentials through setup or environment variables, never CLI arguments.\n')


def main():
    parser = SafeParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('status', help='Offline credential-presence check; no API call.')
    setup = commands.add_parser('setup', help='Register a key privately in your own terminal.')
    setup.add_argument('--replace', action='store_true')
    gen = commands.add_parser('generate', help='Make one image API request after selecting Gemini mode.')
    gen.add_argument('--prompt-file', required=True)
    gen.add_argument('--output-dir', required=True)
    gen.add_argument('--purpose', choices=('draft', 'asset'), required=True)
    gen.add_argument('--model', default=DEFAULT_MODEL)
    gen.add_argument('--aspect-ratio', choices=RATIOS, default='16:9')
    gen.add_argument('--reference', action='append', default=[])
    args = parser.parse_args()
    try:
        if args.command == 'status':
            print(json.dumps(status(), indent=2))
        elif args.command == 'setup':
            if not sys.stdin.isatty():
                raise ImageError('Run setup yourself in an interactive terminal. Never send the key through an agent chat or command argument.')
            print('Create/manage your Gemini key: https://aistudio.google.com/apikey')
            print('The key will be saved outside the project; Gemini API usage may be billed by Google.')
            value = getpass.getpass('Gemini API key (hidden): ')
            save_key(value, key_path(), replace=args.replace)
            print('Key registered. Run status to check local availability; it does not verify model access.')
        else:
            prompt = Path(args.prompt_file).read_text(encoding='utf8')
            result = generate(prompt, args.output_dir, purpose=args.purpose, model=args.model, aspect_ratio=args.aspect_ratio, references=args.reference)
            print(json.dumps(result, indent=2))
    except (ImageError, OSError, UnicodeError, ImportError) as error:
        message = str(error) if isinstance(error, ImageError) else 'Local file or dependency error. Check the selected paths and install Pillow if needed.'
        print(message, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""Explicit distributable-file allowlist shared by portable skill packaging."""
from pathlib import Path

def skill_files(root):
    root = Path(root)
    files = []
    for file in sorted(root.rglob('*')):
        parts = file.relative_to(root).parts
        if not file.is_file() or file.is_symlink():
            continue
        if any(p.startswith('.') or p in {'node_modules', '__pycache__', 'venv'} for p in parts):
            continue
        if file.name == 'gemini-api-key' or file.suffix in {'.pyc', '.pyo', '.pem', '.key'}:
            continue
        if parts[0] in {'scripts', 'references', 'assets', 'examples'} or parts == ('SKILL.md',) or parts == ('package.json',) or parts == ('requirements.txt',):
            files.append(file)
    return files

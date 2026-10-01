"""Distributable-file allowlist and local-reference validation for skill packages."""
import re
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


def validate_references(root, files):
    """Resolve documentation links against files actually included in the ZIP."""
    root = Path(root).resolve()
    included = {file.resolve() for file in files}
    counts = {'markdownLinks': 0, 'scriptGuideReferences': 0}
    for file in files:
        targets = []
        if file.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', file.read_text()):
                target = target.split('#')[0]
                if not target or '://' in target or target.startswith('mailto:'):
                    continue
                targets.append((file.parent / target, target, 'markdownLinks'))
        elif file.suffix in {'.py', '.mjs'}:
            # Runtime error messages commonly point to skill-root-relative guides.
            for target in re.findall(r'(?<![\w/])references/[\w./-]+\.md', file.read_text()):
                targets.append((root / target, target, 'scriptGuideReferences'))
        for resolved, target, kind in targets:
            if resolved.resolve() not in included:
                raise ValueError(f'Unpackaged local reference: {file.resolve().relative_to(root)} → {target}')
            counts[kind] += 1
    return counts

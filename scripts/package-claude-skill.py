#!/usr/bin/env python3
"""Validate local references and package the Claude port, excluding caches/deps."""
import hashlib,json,re,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'ports/claude/paper-figure'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=sorted(p for p in SKILL.rglob('*') if p.is_file() and not any(x in {'__pycache__','node_modules','.venv','.DS_Store'} for x in p.relative_to(SKILL).parts) and p.suffix not in {'.pyc','.pyo'})
checked_links=0
for p in files:
    if p.suffix in {'.md','.py','.mjs','.json','.txt','.html','.svg'}:
        text=p.read_text()
        for token in ['/Users/','@oai/artifact-tool','load_workspace_dependencies','PRESENTATIONS_SKILL_DIR','ARTIFACT_NODE_MODULES']:
            if token in text:raise ValueError(f'Host-specific dependency in {p.relative_to(SKILL)}: {token}')
    if p.suffix=='.md':
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            target=target.split('#')[0]
            if not target or '://' in target or target.startswith('mailto:'):continue
            resolved=(p.parent/target).resolve()
            if not resolved.is_relative_to(SKILL.resolve()) or not resolved.exists():raise ValueError(f'Broken/outside local link: {p.relative_to(SKILL)} → {target}')
            checked_links+=1
output=ROOT/'output/paper-figure-claude-skill.zip';output.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
    for p in files:archive.write(p,Path('paper-figure')/p.relative_to(SKILL))
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(files)==len(set(archive.namelist()))
    assert 'paper-figure/SKILL.md' in archive.namelist()
    for p in files:assert archive.read(str(Path('paper-figure')/p.relative_to(SKILL)))==p.read_bytes()
shutil.copy2(ROOT/'ports/claude/INSTALL.txt',ROOT/'output/paper-figure-claude-install.txt')
manifest={'source':'skills/paper-figure','port':'ports/claude/paper-figure','date':'2026-10-01','canonicalFileHashes':{str(p.relative_to(ROOT/'skills/paper-figure')):digest(p) for p in sorted((ROOT/'skills/paper-figure').rglob('*')) if p.is_file() and '__pycache__' not in p.parts},'portFileHashes':{str(p.relative_to(SKILL)):digest(p) for p in files},'zip':str(output.relative_to(ROOT)),'zipSha256':digest(output),'zipBytes':output.stat().st_size,'zipFiles':len(files),'validatedLocalLinks':checked_links}
(ROOT/'ports/claude/port-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:manifest[k] for k in ['zip','zipSha256','zipBytes','zipFiles','validatedLocalLinks']}))

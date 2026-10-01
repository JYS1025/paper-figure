#!/usr/bin/env python3
"""Package portable Claude skills and Antigravity plugins without caches/deps."""
import hashlib,json,re,shutil,zipfile,argparse
from pathlib import Path
from skill_package import skill_files
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Package a self-contained portable skill edition.')
parser.add_argument('--edition',choices=['claude','antigravity'],default='claude')
edition=parser.parse_args().edition
is_plugin=edition=='antigravity'
SKILL=ROOT/('ports/antigravity/plugin/skills/paper-figure' if is_plugin else 'ports/claude/paper-figure')
package_root=ROOT/'ports/antigravity/plugin' if is_plugin else SKILL
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=skill_files(SKILL)
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
kind='plugin' if is_plugin else 'skill'
output=ROOT/f'output/paper-figure-{edition}-{kind}.zip';output.parent.mkdir(exist_ok=True)
package_files=([package_root/'plugin.json'] if is_plugin else [])+files
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
    for p in package_files:archive.write(p,Path('paper-figure')/p.relative_to(package_root))
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(package_files)==len(set(archive.namelist()))
    assert str(Path('paper-figure')/SKILL.relative_to(package_root)/'SKILL.md') in archive.namelist()
    for p in package_files:assert archive.read(str(Path('paper-figure')/p.relative_to(package_root)))==p.read_bytes()
shutil.copy2(ROOT/f'ports/{edition}/INSTALL.txt',ROOT/f'output/paper-figure-{edition}-install.txt')
manifest={'source':'skills/paper-figure','port':str(SKILL.relative_to(ROOT)),'date':'2026-10-01','canonicalFileHashes':{str(p.relative_to(ROOT/'skills/paper-figure')):digest(p) for p in sorted((ROOT/'skills/paper-figure').rglob('*')) if p.is_file() and '__pycache__' not in p.parts},'portFileHashes':{str(p.relative_to(SKILL)):digest(p) for p in files},'packageFileHashes':{str(p.relative_to(package_root)):digest(p) for p in package_files},'zip':str(output.relative_to(ROOT)),'zipSha256':digest(output),'zipBytes':output.stat().st_size,'zipFiles':len(package_files),'validatedLocalLinks':checked_links}
(ROOT/f'ports/{edition}/port-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:manifest[k] for k in ['zip','zipSha256','zipBytes','zipFiles','validatedLocalLinks']}))

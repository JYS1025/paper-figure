#!/usr/bin/env python3
"""Package Codex/Claude skills and Antigravity plugins without caches/deps."""
import hashlib,json,shutil,zipfile,argparse
from datetime import date
from pathlib import Path
from skill_package import skill_files,validate_references
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Package a self-contained portable skill edition.')
parser.add_argument('--edition',choices=['codex','claude','antigravity'],default='claude')
edition=parser.parse_args().edition
is_plugin=edition=='antigravity'
SKILL=ROOT/({'codex':'skills/paper-figure','claude':'ports/claude/paper-figure','antigravity':'ports/antigravity/plugin/skills/paper-figure'}[edition])
package_root=ROOT/'ports/antigravity/plugin' if is_plugin else SKILL
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=skill_files(SKILL)
references=validate_references(SKILL,files)
for p in files:
    if edition!='codex' and p.suffix in {'.md','.py','.mjs','.json','.txt','.html','.svg'}:
        text=p.read_text()
        for token in ['/Users/','@oai/artifact-tool','load_workspace_dependencies','PRESENTATIONS_SKILL_DIR','ARTIFACT_NODE_MODULES']:
            if token in text:raise ValueError(f'Host-specific dependency in {p.relative_to(SKILL)}: {token}')
kind='plugin' if is_plugin else 'skill'
output=ROOT/('output/paper-figure-skill.zip' if edition=='codex' else f'output/paper-figure-{edition}-{kind}.zip');output.parent.mkdir(exist_ok=True)
package_files=([package_root/'plugin.json'] if is_plugin else [])+files
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as archive:
    for p in package_files:archive.write(p,Path('paper-figure')/p.relative_to(package_root))
with zipfile.ZipFile(output) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist())==len(package_files)==len(set(archive.namelist()))
    assert str(Path('paper-figure')/SKILL.relative_to(package_root)/'SKILL.md') in archive.namelist()
    for p in package_files:assert archive.read(str(Path('paper-figure')/p.relative_to(package_root)))==p.read_bytes()
if edition!='codex':shutil.copy2(ROOT/f'ports/{edition}/INSTALL.txt',ROOT/f'output/paper-figure-{edition}-install.txt')
manifest={'source':'skills/paper-figure','port':str(SKILL.relative_to(ROOT)),'date':date.today().isoformat(),'canonicalFileHashes':{str(p.relative_to(ROOT/'skills/paper-figure')):digest(p) for p in skill_files(ROOT/'skills/paper-figure')},'portFileHashes':{str(p.relative_to(SKILL)):digest(p) for p in files},'packageFileHashes':{str(p.relative_to(package_root)):digest(p) for p in package_files},'zip':str(output.relative_to(ROOT)),'zipSha256':digest(output),'zipBytes':output.stat().st_size,'zipFiles':len(package_files),'validatedLocalLinks':references['markdownLinks'],'validatedScriptGuideReferences':references['scriptGuideReferences']}
manifest_path=ROOT/('docs/validation/codex-package.json' if edition=='codex' else f'ports/{edition}/port-manifest.json')
manifest_path.parent.mkdir(parents=True,exist_ok=True);manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:manifest[k] for k in ['zip','zipSha256','zipBytes','zipFiles','validatedLocalLinks','validatedScriptGuideReferences']}))

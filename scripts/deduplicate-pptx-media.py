#!/usr/bin/env python3
"""Share byte-identical media parts without merging native picture objects.

Run on an authoring candidate before finalization; never rewrite a delivered file.
"""
import hashlib
import posixpath
import sys
import zipfile
from pathlib import Path
from lxml import etree as ET

source, destination = map(Path, sys.argv[1:])
with zipfile.ZipFile(source) as archive:
    parts = {name: archive.read(name) for name in archive.namelist()}
canonical, redirects = {}, {}
for name, data in parts.items():
    if not name.startswith('ppt/media/'):
        continue
    identity = (Path(name).suffix, hashlib.sha256(data).hexdigest())
    first = canonical.setdefault(identity, name)
    if first != name:
        assert parts[first] == data
        redirects[name] = first
for name, data in list(parts.items()):
    if not name.endswith('.rels'):
        continue
    tree = ET.fromstring(data)
    owner_dir = posixpath.dirname(posixpath.dirname(name))
    changed = False
    for relation in tree:
        if relation.get('TargetMode') == 'External':
            continue
        target = relation.get('Target', '')
        resolved = posixpath.normpath(posixpath.join(owner_dir, target)).lstrip('/')
        if resolved in redirects:
            relation.set('Target', posixpath.relpath(redirects[resolved], owner_dir or '.'))
            changed = True
    if changed:
        parts[name] = ET.tostring(tree, encoding='UTF-8', xml_declaration=True, standalone=True)
types = ET.fromstring(parts['[Content_Types].xml'])
for entry in list(types):
    if entry.get('PartName', '').lstrip('/') in redirects:
        types.remove(entry)
parts['[Content_Types].xml'] = ET.tostring(types, encoding='UTF-8', xml_declaration=True, standalone=True)
with zipfile.ZipFile(destination, 'x', zipfile.ZIP_DEFLATED) as archive:
    for name, data in parts.items():
        if name not in redirects:
            archive.writestr(name, data)
print(f'Shared {len(redirects)} byte-identical media parts; picture objects unchanged.')

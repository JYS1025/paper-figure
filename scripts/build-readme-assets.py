#!/usr/bin/env python3
"""Build README install/download buttons. Counters use update-repo-badges.py.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/images/readme'
OUT.mkdir(parents=True, exist_ok=True)

for filename, label, fill in [('codex', 'Get Codex skill', '#A6CBBB'), ('claude', 'Get Claude skill', '#B8ADCE')]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="204" height="44" viewBox="0 0 204 44" role="img" aria-label="Download the {filename} skill ZIP">
<title>Download the {filename} skill ZIP</title>
<rect x="0.5" y="0.5" width="203" height="43" rx="6" fill="{fill}" stroke="#617078" stroke-opacity="0.25"/>
<path d="M23 13v14m-5-5 5 5 5-5m-12 9h14" stroke="#17242C" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<text x="43" y="27" fill="#17242C" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="600">{label}</text>
<path d="m185 19 3 3-3 3" stroke="#17242C" stroke-width="1.4" fill="none" stroke-linecap="round"/>
</svg>'''
    (OUT / f'download-{filename}.svg').write_text(svg)

install = (OUT / 'download-codex.svg').read_text().replace('Download the codex skill ZIP', 'Install via CLI').replace('Get Codex skill', 'Install via CLI')
install = install.replace('M23 13v14m-5-5 5 5 5-5m-12 9h14', 'M17 16l6 6-6 6m10 0h9')
(OUT / 'install-cli.svg').write_text(install)
print(f'Wrote install/download buttons to {OUT.relative_to(ROOT)}')

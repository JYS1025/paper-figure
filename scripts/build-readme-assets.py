#!/usr/bin/env python3
"""Build self-contained README badges and download buttons from verified facts.

These are static capability labels, not live CI, download or popularity counters.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/images/readme'
OUT.mkdir(parents=True, exist_ok=True)

BADGES = [
    ('codex', 'CODEX', 'SKILL', '#A6CBBB'),
    ('claude', 'CLAUDE', 'SKILL', '#B8ADCE'),
    ('powerpoint', 'OUTPUT', 'PPTX', '#AEC8DE'),
    ('color-books', 'COLOR BOOKS', '16', '#DCB56C'),
    ('image-first', 'WORKFLOW', 'IMAGE FIRST', '#A6CBBB'),
    ('checks', 'LOCAL CHECKS', '38', '#C0CFAC'),
    ('node', 'NODE.JS', '20+', '#C0CFAC'),
    ('python', 'PYTHON', '3.10+', '#AEC8DE'),
]

for filename, label, value, accent in BADGES:
    left, right = len(label) * 6.7 + 22, len(value) * 6.7 + 22
    w, h = round(left + right), 26
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}: {escape(value)}">
<title>{escape(label)}: {escape(value)}</title>
<defs><clipPath id="edge"><rect width="{w}" height="{h}" rx="4"/></clipPath></defs>
<g clip-path="url(#edge)"><rect width="{w}" height="{h}" fill="#26343E"/><rect x="{left}" width="{right}" height="{h}" fill="{accent}"/></g>
<g font-family="DejaVu Sans Mono,Consolas,monospace" font-size="10" font-weight="600" text-anchor="middle" letter-spacing="0.4">
<text x="{left/2}" y="17" fill="#F4F2E9">{escape(label)}</text>
<text x="{left+right/2}" y="17" fill="#17242C">{escape(value)}</text></g>
</svg>'''
    (OUT / f'badge-{filename}.svg').write_text(svg)

for filename, label, fill in [('codex', 'Get Codex skill', '#A6CBBB'), ('claude', 'Get Claude skill', '#B8ADCE')]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="204" height="44" viewBox="0 0 204 44" role="img" aria-label="Download the {filename} skill ZIP">
<title>Download the {filename} skill ZIP</title>
<rect x="0.5" y="0.5" width="203" height="43" rx="6" fill="{fill}" stroke="#617078" stroke-opacity="0.25"/>
<path d="M23 13v14m-5-5 5 5 5-5m-12 9h14" stroke="#17242C" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<text x="43" y="27" fill="#17242C" font-family="Arial,Helvetica,sans-serif" font-size="15" font-weight="600">{label}</text>
<path d="m185 19 3 3-3 3" stroke="#17242C" stroke-width="1.4" fill="none" stroke-linecap="round"/>
</svg>'''
    (OUT / f'download-{filename}.svg').write_text(svg)

print(f'Wrote {len(BADGES)} capability badges and 2 download buttons to {OUT.relative_to(ROOT)}')

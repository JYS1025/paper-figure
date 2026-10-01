#!/usr/bin/env python3
"""Build the bundled color-book catalog from its single JSON source (stdlib only)."""
import argparse
import html
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET


def luminance(value):
    rgb = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    return sum(v * w for v, w in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + .05) / (lo + .05)


def validate(catalog):
    results, ids = [], set()
    if catalog['schema_version'] != 1:
        raise ValueError('Unsupported catalog schema')
    for book in catalog['books']:
        if book['id'] in ids or not re.fullmatch(r'[a-z][a-z0-9-]*', book['id']):
            raise ValueError('Invalid or duplicate book ID')
        ids.add(book['id'])
        n = book['neutral']
        preview = book.get('preview', {})
        if preview.get('mode', 'families') not in ('families', 'solid-primary', 'colored-flow', 'filter', 'monochrome'):
            raise ValueError(f'Unknown preview mode: {book["id"]}')
        if preview.get('output') and preview['output'] not in book['colors']:
            raise ValueError(f'Unknown output family: {book["id"]}')
        for value in list(n.values()) + [v for family in book['colors'].values() for v in family.values()]:
            if not re.fullmatch(r'#[0-9A-F]{6}', value):
                raise ValueError(f'Invalid RGB value {value}')
        pairs = [('ink/canvas', n['ink'], n['canvas'], 4.5),
                 ('secondary/canvas', n['secondary_text'], n['canvas'], 4.5),
                 ('ink/surface', n['ink'], n['surface'], 4.5),
                 ('stroke/surface', n['stroke'], n['surface'], 3.0)]
        for name, c in book['colors'].items():
            pairs += [(f'{name}: ink/fill', n['ink'], c['fill'], 4.5),
                      (f'{name}: stroke/fill', c['stroke'], c['fill'], 3.0),
                      (f'{name}: accent/fill', c['accent'], c['fill'], 3.0)]
        if preview.get('mode') == 'solid-primary':
            first = next(iter(book['colors'].values()))
            pairs.append(('solid module: white/accent', '#FFFFFF', first['accent'], 4.5))
        values = [{'pair': label, 'ratio': round(contrast(a, b), 2), 'target': target,
                   'meets_target': contrast(a, b) >= target} for label, a, b, target in pairs]
        results.append({'id': book['id'], 'pairs': values})
    return {'scope': 'sRGB contrast heuristics for intended pairs, not journal requirements or CVD certification',
            'all_pairs_meet_targets': all(v['meets_target'] for r in results for v in r['pairs']),
            'books': results}


def text(x, y, value, size=14, color='#242424', weight='normal', anchor='start'):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(value)}</text>'


def rect(x, y, w, h, fill, stroke='none', width=1, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def svg(inner, w, h, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(title, quote=True)}"><title>{html.escape(title)}</title><g font-family="Arial, Helvetica, sans-serif">{inner}</g></svg>'


def card(book, index):
    n, families = book['neutral'], list(book['colors'].items())
    ink = n['ink']
    a, b = families[0][1], families[1][1]
    preview = book.get('preview', {})
    mode = preview.get('mode', 'families')
    c = book['colors'][preview['output']] if preview.get('output') else (families[2][1] if len(families) > 2 else a)
    source = book['inspiration'][0]['name'].split(':')[0].split(',')[0]
    if len(source) > 45:
        source = 'Design references in catalog'
    parts = [rect(0, 0, 588, 374, '#FFFFFF', '#D6D9DD', rx=5),
             text(22, 32, f'{index:02d}   {book["name"]}', 22, ink, 'bold'),
             text(22, 55, book['id'], 12, n['secondary_text']),
             text(566, 55, source, 11, n['secondary_text'], anchor='end')]
    for j, (name, col) in enumerate(families):
        x = 22 + j * 183
        parts.append(text(x, 81, name.upper(), 11, n['secondary_text'], 'bold'))
        for k, role in enumerate(('fill', 'stroke', 'accent')):
            sx = x + k * 57
            parts += [rect(sx, 90, 52, 29, col[role]),
                      text(sx, 134, col[role], 10, ink),
                      text(sx, 147, role, 10, n['secondary_text'])]
    captions = {'families':'Color use: related families with light fills and stronger details',
                'solid-primary':'Color use: a solid primary module against a light counterpart',
                'colored-flow':'Color use: route colors on a quiet background',
                'filter':'Color use: neutral pool, curated seed, explicit rejection mark',
                'monochrome':'Color use: gray models, white operations, dark structure'}
    parts += [text(22, 174, captions[mode], 11, n['secondary_text'])]
    # Original teaching examples demonstrate allocations, not the cited architectures.
    enclosure_role = preview.get('enclosure', 'neutral' if book['id'] == 'ink-cobalt' else 'tinted')
    enclosure = {'neutral':n['surface'], 'white':n['canvas'], 'tinted':a['fill']}[enclosure_role]
    parts += [rect(148, 191, 269, 136, enclosure, n['stroke'], .9, 3),
              text(160, 211, 'Shared model', 12, ink, 'bold')]
    for y, family, letter in ((225, a, 'A'), (285, b, 'B')):
        route = family['accent'] if mode == 'colored-flow' else n['connector']
        token_fill = n['canvas'] if mode == 'monochrome' else family['fill']
        for i in range(4):
            parts.append(rect(22 + i * 23, y - 12, 17, 17, token_fill, family['stroke'], 1.2))
        label = ('Pool (X: remove)' if letter == 'A' else 'Curated seed') if mode == 'filter' else f'Input {letter}'
        parts += [text(22, y + 22, label, 11, ink),
                  f'<path d="M112 {y-3}H169" fill="none" stroke="{route}" stroke-width="2"/>',
                  f'<path d="M169 {y-3}l-7 -4v8z" fill="{route}"/>']
    if mode == 'filter':
        reject = book['colors']['vermilion']['accent']
        parts.append(f'<path d="M24 215l13 13m0 -13l-13 13" stroke="{reject}" stroke-width="2.5"/>')
    fill_a = a['accent'] if mode == 'solid-primary' else a['fill']
    fill_b = a['fill'] if mode == 'monochrome' else b['fill']
    color_a = '#FFFFFF' if mode == 'solid-primary' else ink
    labels = ('Dedup', 'Retrieve', 'Merge') if mode == 'filter' else ('Encode A', 'Encode B', 'Integrate')
    route_a = a['accent'] if mode == 'colored-flow' else n['connector']
    route_b = b['accent'] if mode == 'colored-flow' else n['connector']
    parts += [rect(172, 219, 82, 24, fill_a, a['stroke'], 1.1),
              text(213, 235, labels[0], 10, color_a, anchor='middle'),
              rect(172, 279, 82, 24, fill_b, b['stroke'], 1.1),
              text(213, 295, labels[1], 10, ink, anchor='middle'),
              f'<path d="M254 231H271V261" fill="none" stroke="{route_a}" stroke-width="2"/>',
              f'<path d="M254 291H271V261" fill="none" stroke="{route_b}" stroke-width="2"/>',
              f'<path d="M271 261H294" fill="none" stroke="{n["connector"]}" stroke-width="2"/>',
              f'<path d="M294 261l-7 -4v8z" fill="{n["connector"]}"/>',
              rect(297, 240, 96, 42, a['fill'] if book['id'] == 'ink-cobalt' else n['canvas'], a['stroke'] if book['id'] == 'ink-cobalt' else n['stroke'], 1.1),
              text(345, 265, labels[2], 12, ink, anchor='middle'),
              f'<path d="M393 261H445" fill="none" stroke="{n["connector"]}" stroke-width="2"/>',
              f'<path d="M445 261l-7 -4v8z" fill="{n["connector"]}"/>']
    for i in range(4):
        parts.append(rect(451 + i * 25, 250, 18, 22, c['accent'], c['stroke'], 1))
    parts += [text(451, 292, 'Output', 11, ink),
              rect(22, 343, 13, 13, n['ink']), text(41, 354, f'Ink {n["ink"]}', 11, ink),
              rect(183, 343, 13, 13, n['surface'], n['stroke']), text(202, 354, 'Neutral structure', 11, ink),
              text(400, 354, 'Illustrative color-use example', 10, n['secondary_text'])]
    return ''.join(parts)


def sheet(books, first=1):
    height = 172 + ((len(books) + 1) // 2) * 400
    parts = [rect(0, 0, 1240, height, '#FFFFFF'),
             text(28, 48, 'Research figure color books', 32, weight='bold'),
             text(28, 78, f'Books {first:02d}–{first+len(books)-1:02d} · fills, boundaries and accents in use', 16, '#52575F'),
             text(28, 104, 'Author-curated adaptations. Reference names identify design evidence, not official palette specifications.', 12, '#52575F')]
    for i, book in enumerate(books):
        x, y = 28 + (i % 2) * 612, 127 + (i // 2) * 400
        parts.append(f'<g transform="translate({x},{y})">{card(book,first+i)}</g>')
    parts.append(text(28, height-22, 'Preserve semantic roles. Use the source principle that fits the method; do not copy its architecture.', 14, '#52575F'))
    return svg(''.join(parts), 1240, height, 'Research figure color books')


def compact_index(books):
    height = 145 + ((len(books)+3)//4)*196
    parts = [rect(0,0,1240,height,'#FFFFFF'), text(28,44,f'{len(books)} research figure color books',30,weight='bold'),
             text(28,72,'Each family: light fill / boundary / accent. Reference-inspired, author-curated RGB values.',15,'#51565D'),
             text(28,96,'01–06 original collection · 07–16 added from direct visual study of 10 paper figures',13,'#51565D')]
    for i,b in enumerate(books):
        x,y = 28+(i%4)*304,118+(i//4)*196
        parts += [rect(x,y,286,178,'#FFFFFF','#D6D9DD',rx=4),text(x+14,y+26,f'{i+1:02d}  {b["name"]}',16,weight='bold')]
        ref = b['inspiration'][0]['name'].split(':')[0].split(',')[0]
        if i<6:ref=['RLDX-1','SAM / Transformer','MAE','CLIP','spinDrop','CUD adaptation'][i]
        parts.append(text(x+14,y+48,ref,12,'#51565D'))
        for j,(name,c) in enumerate(b['colors'].items()):
            sx=x+14+j*88
            parts += [rect(sx,y+63,80,27,c['fill']),rect(sx,y+90,80,12,c['stroke']),rect(sx,y+102,80,22,c['accent']),
                      text(sx,y+141,name,11,'#51565D')]
        mode=b.get('preview',{}).get('mode','families')
        parts.append(text(x+14,y+164,mode.replace('-',' '),11,'#51565D'))
    return svg(''.join(parts),1240,height,'Color-book index')


def build(source, output):
    catalog = json.loads(source.read_text())
    report = validate(catalog)
    if not report['all_pairs_meet_targets']:
        failed = [(b['id'], p) for b in report['books'] for p in b['pairs'] if not p['meets_target']]
        raise ValueError(f'Contrast target failures: {failed}')
    output.mkdir(parents=True, exist_ok=True)
    if source.resolve() != (output / 'color-books.json').resolve():
        (output / 'color-books.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    individual = output / 'color-books'
    individual.mkdir(exist_ok=True)
    cards, sections = [], []
    for i, book in enumerate(catalog['books'], 1):
        inner = card(book, i)
        image = svg(inner, 588, 374, book['name'])
        ET.fromstring(image)
        (individual / f'{book["id"]}.svg').write_text(image + '\n')
        x, y = 28 + ((i - 1) % 2) * 612, 127 + ((i - 1) // 2) * 400
        cards.append(f'<g transform="translate({x},{y})">{inner}</g>')
        links = ', '.join(f'<a href="{html.escape(s["url"], quote=True)}">{html.escape(s["name"])}</a>' for s in book['inspiration'])
        observations = ''.join(f'<p>{html.escape(s["observation"])}</p>' for s in book['inspiration'] if s.get('observation'))
        sections.append(f'<article id="{book["id"]}">{image}<div class="notes"><h2>{html.escape(book["name_ko"])}</h2><p><b>적용:</b> {html.escape(book["allocation"])}</p><p><b>검토:</b> {html.escape(book["caution"])}</p><details><summary>참고 figure와 관찰 근거</summary><p>{links}</p>{observations}</details></div></article>')
    height = 172 + ((len(catalog['books']) + 1) // 2) * 400
    header = rect(0, 0, 1240, height, '#FFFFFF') + text(28, 48, 'Research figure color books', 32, weight='bold') + text(28, 78, f'{len(catalog["books"])} curated combinations · pale fills, visible boundaries, concentrated accents', 16, '#52575F') + text(28, 104, 'Palette adaptations, not official paper colors. The examples isolate color; they are not layout templates.', 12, '#52575F')
    footer = text(28, height - 22, 'Start with semantic roles. Use only the needed hues. Keep labels dark and check the final publication size.', 14, '#52575F')
    overview = svg(header + ''.join(cards) + footer, 1240, height, 'Research figure color books')
    ET.fromstring(overview)
    (output / 'color-books.svg').write_text(overview + '\n')
    index_svg = compact_index(catalog['books'])
    ET.fromstring(index_svg)
    (output / 'color-books-index.svg').write_text(index_svg + '\n')
    pages = output / 'color-books' / 'pages'
    pages.mkdir(exist_ok=True)
    for start in range(0,len(catalog['books']),4):
        page_svg = sheet(catalog['books'][start:start+4],start+1)
        ET.fromstring(page_svg)
        (pages/f'page-{start//4+1:02d}.svg').write_text(page_svg+'\n')
    page = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Research figure color books</title><style>
body{margin:0;background:#F5F6F7;color:#24272B;font:15px/1.6 system-ui,sans-serif}main{max-width:1240px;margin:auto;padding:32px 24px}h1{font-size:32px;line-height:1.2;margin:0 0 12px}h2{font-size:19px;margin:0 0 8px}.intro{max-width:930px}nav{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0}a{color:#245B90}nav a{border:1px solid #A8AEB6;padding:6px 12px;border-radius:4px;text-decoration:none;background:white}.toolbar{display:flex;gap:22px;margin:18px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{background:white;border:1px solid #D6D9DD;border-radius:5px;overflow:hidden}article svg{display:block;width:100%;height:auto}.notes{padding:18px 22px 24px}.notes p{margin:7px 0}body.gray svg{filter:grayscale(1)}footer{margin-top:24px;font-size:13px;color:#51565D}@media(max-width:850px){.grid{grid-template-columns:1fr}}@media print{body{background:white}nav,.toolbar{display:none}.grid{display:block}article{break-inside:avoid;margin-bottom:22px}.notes{font-size:12px}article svg{max-height:360px}}
</style><main><h1>Research figure color books</h1><div class="intro"><p>__COUNT__개 조합의 면색·경계색·강조색과 사용 예시를 제공합니다. 07–16번에는 추가로 직접 살펴본 논문 figure와 배색 관찰을 기록했습니다. 진한 모듈, 색 경로, 회색 중심 등 그림에 맞는 배분 방식도 함께 선택하세요.</p><p>원본 figure의 배색 원리를 참고해 직접 설계한 값입니다. 원본에서 추출한 공식 팔레트가 아니며, 논문 전체의 색상 사용 통계를 뜻하지 않습니다.</p></div>'''
    page = page.replace('__COUNT__', str(len(catalog['books'])))
    page += '<nav>' + ''.join(f'<a href="#{b["id"]}">{html.escape(b["name"])}</a>' for b in catalog['books']) + '</nav>'
    page += '<div class="toolbar"><label><input type="checkbox" id="gray"> 흑백으로 비교</label><span>같은 의미에는 같은 색 · 필요한 색만 선택</span></div>'
    page += '<div class="grid">' + ''.join(sections) + '</div><footer>흑백 비교는 색각 시뮬레이션이 아닙니다. 실제 figure의 크기·선·라벨·색 외 구분을 함께 검토하세요. 색상 데이터: <a href="color-books.json">color-books.json</a></footer></main><script>document.getElementById("gray").addEventListener("change",e=>document.body.classList.toggle("gray",e.target.checked));</script></html>'
    (output / 'color-books.html').write_text(page + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    assets = Path(__file__).resolve().parents[1] / 'assets'
    parser.add_argument('--source', type=Path, default=assets / 'color-books.json')
    parser.add_argument('--output-dir', type=Path, default=assets)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = build(args.source, args.output_dir)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n')
    print(f'Built {len(result["books"])} color books; intended contrast pairs meet the catalog targets.')

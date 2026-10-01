#!/usr/bin/env python3
"""Read-only rendered-text diagnostics for selected regions of a saved figure PDF.

Requires pdfplumber. Thresholds are author-chosen review triggers, not a quality
score. No math semantics, native editability, or PowerPoint appearance is inferred.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import unicodedata


def font_name(name):
    """Remove only a PDF subset prefix; do not equate different font families."""
    return re.sub(r'^[A-Z]{6}\+', '', name or '')


def number(value, label, positive=True):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{label} must be a finite number')
    if not math.isfinite(value) or (positive and value <= 0):
        raise ValueError(f'{label} must be a finite positive number')
    return value


def region_report(chars, region, scale):
    """Measure extracted character metrics, retaining partial boundary hits."""
    x0, top, x1, bottom = region['boundsPt']
    inside, boundary = [], []
    for char in chars:
        if not char.get('text', '').strip():
            continue
        intersects = (char['x0'] < x1 and char['x1'] > x0
                      and char['top'] < bottom and char['bottom'] > top)
        if not intersects:
            continue
        full = (char['x0'] >= x0 and char['x1'] <= x1
                and char['top'] >= top and char['bottom'] <= bottom)
        item = {
            'text': char['text'], 'font': font_name(char['fontname']),
            'pdfSizePt': round(char['size'], 4),
            'publicationSizePt': round(char['size'] * scale, 4),
            'boundsPt': [round(char[k], 4) for k in ('x0', 'top', 'x1', 'bottom')],
            'upright': char.get('upright', True),
        }
        (inside if full else boundary).append(item)
    reasons = []
    if not inside:
        reasons.append('no_extractable_text_inside_region')
    if boundary:
        reasons.append('characters_cross_region_boundary')
    # PDF character order can differ for scripts; compare inventory, not order.
    inventory = lambda text: Counter(c for c in unicodedata.normalize('NFC', text) if not c.isspace())
    expected = inventory(region['expectedText'])
    extracted = inventory(''.join(c['text'] for c in inside))
    missing, extra = expected - extracted, extracted - expected
    if missing or extra:
        reasons.append('character_inventory_mismatch')
    observed = inside + boundary
    unexpected = sorted({c['font'] for c in observed} - set(region['expectedFonts']))
    if unexpected:
        reasons.append('unexpected_rendered_font')
    if any(not c['upright'] for c in observed):
        reasons.append('rotated_text_requires_visual_review')
    if any(not math.isfinite(c['pdfSizePt']) or c['pdfSizePt'] <= 0 for c in observed):
        reasons.append('invalid_character_size')
    sizes = [c['publicationSizePt'] for c in inside if math.isfinite(c['publicationSizePt']) and c['publicationSizePt'] > 0]
    minimum, maximum = (min(sizes), max(sizes)) if sizes else (None, None)
    ratio = minimum / maximum if sizes else None
    if minimum is not None and minimum < region['minSizePt']:
        reasons.append('below_selected_minimum_size')
    if ratio is not None and ratio < region['minRelativeSize']:
        reasons.append('below_selected_relative_size')
    return {
        'name': region['name'], 'page': region['page'], 'boundsPt': region['boundsPt'],
        'reviewReasons': reasons, 'unexpectedFonts': unexpected,
        'expectedText': region['expectedText'],
        'missingCharacters': dict(missing), 'extraCharacters': dict(extra),
        'minPublicationSizePt': minimum, 'maxPublicationSizePt': maximum,
        'minToMaxSizeRatio': round(ratio, 4) if ratio is not None else None,
        'thresholds': {k: region[k] for k in ('minSizePt', 'minRelativeSize', 'expectedFonts')},
        'characters': inside, 'boundaryCharacters': boundary,
    }


def validate_plan(plan):
    if not isinstance(plan, dict):
        raise ValueError('Plan must be a JSON object')
    if not re.fullmatch(r'[0-9a-f]{64}', plan.get('pdfSha256', '')):
        raise ValueError('pdfSha256 must identify the saved PDF')
    number(plan.get('publicationWidthMm'), 'publicationWidthMm')
    regions = plan.get('regions')
    if not isinstance(regions, list) or not regions:
        raise ValueError('At least one selected region is required')
    names = set()
    for region in regions:
        if not isinstance(region, dict):
            raise ValueError('Each selected region must be a JSON object')
        name = region.get('name')
        if not isinstance(name, str) or not name or name in names:
            raise ValueError('Region names must be nonempty and unique')
        names.add(name)
        if not isinstance(region.get('expectedText'), str) or not region['expectedText'].strip():
            raise ValueError(f'{name}: expectedText must identify the complete expression')
        page = region.get('page')
        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError(f'{name}: page must be a positive integer')
        box = region.get('boundsPt')
        if not isinstance(box, list) or len(box) != 4:
            raise ValueError(f'{name}: boundsPt must contain four coordinates')
        for value in box:
            number(value, 'boundsPt coordinate', positive=False)
        if box[0] < 0 or box[1] < 0 or box[2] <= box[0] or box[3] <= box[1]:
            raise ValueError(f'{name}: invalid region bounds')
        fonts = region.get('expectedFonts')
        if not isinstance(fonts, list) or not fonts or any(not isinstance(f, str) or not f.strip() for f in fonts):
            raise ValueError(f'{name}: explicitly supply approved rendered font names')
        number(region.get('minSizePt'), 'minSizePt')
        relative = number(region.get('minRelativeSize'), 'minRelativeSize')
        if relative > 1:
            raise ValueError('minRelativeSize cannot exceed 1')
    for i, a in enumerate(regions):
        for b in regions[i + 1:]:
            if a['page'] != b['page']:
                continue
            x, y, xx, yy = a['boundsPt']
            bx, by, bxx, byy = b['boundsPt']
            if max(x, bx) < min(xx, bxx) and max(y, by) < min(yy, byy):
                raise ValueError('Selected regions must not overlap')


def audit(source, plan):
    import pdfplumber
    validate_plan(plan)
    source = Path(source)
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != plan['pdfSha256']:
        raise ValueError('PDF changed since region selection; inspect the current render')
    reports = []
    with pdfplumber.open(source) as pdf:
        for region in plan['regions']:
            if region['page'] > len(pdf.pages):
                raise ValueError(f"Unknown PDF page: {region['page']}")
            page = pdf.pages[region['page'] - 1]
            # Ambiguous origins need explicit visual handling, not guessed offsets.
            if page.bbox[:2] != (0, 0) or page.rotation:
                raise ValueError('Rotated pages or nonzero page origins are unsupported')
            box = region['boundsPt']
            if box[2] > page.width or box[3] > page.height:
                raise ValueError(f"{region['name']}: region extends beyond the PDF page")
            scale = plan['publicationWidthMm'] / (page.width * 25.4 / 72)
            report = region_report(page.chars, region, scale)
            report['pdfPageSizePt'] = [page.width, page.height]
            report['publicationScale'] = scale
            reports.append(report)
    return {
        'source': str(source.resolve()), 'sourceSha256': digest, 'readOnly': True,
        'publicationWidthMm': plan['publicationWidthMm'],
        'scope': 'Selected PDF text metrics only; inspect mathematical typography and native editability separately.',
        'summary': {
            'regions': len(reports),
            'requiringReview': sum(bool(r['reviewReasons']) for r in reports),
            'unmeasuredRegions': sum(not r['characters'] for r in reports),
        },
        'regions': reports,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('--plan', required=True)
    parser.add_argument('--output')
    args = parser.parse_args()
    if args.output:
        output = Path(args.output)
        if output.resolve() in {Path(args.source).resolve(), Path(args.plan).resolve()} or output.exists():
            parser.error('Output must be a new file distinct from the PDF and plan')
    try:
        result = audit(args.source, json.loads(Path(args.plan).read_text()))
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            with Path(args.output).open('x') as stream:
                stream.write(rendered)
        else:
            print(rendered, end='')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()

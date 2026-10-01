# Editable mathematical typography

Read this when formulas, subscripts or superscripts occur. Native text is editable, but that alone does not establish good mathematical typography. Keep mathematical meaning and styling consistent with the manuscript; do not change notation merely to match a reference's appearance.

## Choose a notation system

Separate ordinary labels from mathematical roles. Under conventional scientific typesetting, variables and running indices are italic, while descriptive indices (such as `now`), numbers and named operators (such as `area`) are upright. Preserve an established manuscript convention when it differs. Apply vector/matrix weight only when the notation calls for it; bolding only the final occurrence of a variable for emphasis can suggest a different mathematical object. Prefer emphasis on its containing region instead.

Use a compatible, available math/text font combination with the necessary glyph coverage. A serif math font can pair with sans-serif labels, as in the DiT example; sans-serif mathematics can also be appropriate. Arial is not inherently wrong, and serif type is not a universal quality rule. The governing requirements are consistent roles, spacing, glyph shapes and readable scripts. [NIST typeface guidance](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-10-more-printing-and-using-symbols-and-numbers) and [DiT Figure 3](https://arxiv.org/html/2212.09748v2#S1.F3) provide useful reference points.

## Author scripts without accidental double shrinking

Use ordinary characters with native sub/superscript formatting for a notation family. Do not mix literal underscores, precomposed Unicode scripts (`ₖ`, `₁`, `⁺`) and unrelated manually lowered runs within that family. Ordinary Greek and operator characters remain useful; the concern is inconsistent script construction and missing glyph coverage, not Unicode in general. Preserve existing author notation unless the requested edit or a confirmed defect warrants changing it.

Two editable approaches are viable:

- A native equation object, if the available authoring path actually supports it and its saved editability/rendering are verified.
- For simple labels, native formatted text runs or deliberately positioned native text objects. Use one tested recipe for font, size, baseline, spacing and repeated occurrences. Individually positioned components must remain easy to select as a logical group and should not attach semantic arrows to invisible captions.

Treat script size and baseline as coupled renderer behavior. In the reviewed LibreOffice export, a 6.98pt run with a lowered baseline beside a 9.30pt base rendered at 4.09pt, roughly 44% of the base. Pre-reducing the font and applying script formatting had compounded the reduction. This is an observed failure in that path, not a universal Office scaling constant. Do not copy its baseline value or compensate with a global inverse multiplier. For automatic script formatting, begin without a second manual size reduction, render, and tune to the actual result. For independently positioned text, set the intended script size explicitly without also applying automatic script reduction.

The current `Figure.label()` helper styles a whole textbox and is not a math parser or an equation API. Do not pass LaTeX strings or unimplemented rich-text options and assume they were typeset. Use a verified native text/equation path for mixed styles. Stacked fractions, nested scripts, matrices and aligned derivations need a suitable equation path; rasterizing the formula or outlining it as an SVG does not preserve text editability. Report the capability limitation if no compliant route is available.

Inline solidus fractions and right-positioned sum indices can be valid. Choose layout according to space and mathematical scope rather than forcing display-style fractions or limits into every label. Check minus signs, operator spacing, parentheses, accents and multi-character indices as part of the same notation system.

## Small native subscript recipe

For a simple `X` with index `t`, the following creates two editable text objects and one selectable group. Coordinates and sizes are CSS pixels; they are starting values for the selected font and width, not a universal math layout. No automatic script scaling is applied a second time. Choose a font actually available in the renderer, and use upright styling for descriptive indices.

```js
const style = {
  typeface: 'Times New Roman', fontSize: 22, italic: true,
  color: '#233947', alignment: 'left', verticalAlignment: 'top',
  wrap: 'none', insets: {left: 0, right: 0, top: 0, bottom: 0}
};
const base = f.label('state-base', 'X', 410, 208, 23, 28);
base.text.style = style;
const index = f.label('state-index', 't', 428, 219, 17, 21);
index.text.style = {...style, fontSize: 15};
f.group('state-label', ['state-base', 'state-index']);
```

Keep these offsets consistent for repeated occurrences of this notation, then check the saved PDF's actual font sizes and the reduced preview. Wider indices, accents, nested scripts and operators require fresh spacing decisions; this recipe is not an equation parser. Include both text objects and their group in the content contract. Connect semantic arrows to the represented module or data, not this label group.

## Review the saved output

Render the latest saved PPTX using the intended output path. Compare representative expressions with a relevant original figure at comparable publication width and base-text size. Inspect a single index, multi-character index and any superscript or operator used by the method. Check baseline alignment, spacing, repeated-symbol consistency and legibility, including the smallest essential index.

Check both the PPTX's encoded runs and the exported PDF's actual fonts and sizes. A declared Arial run can still render a missing Unicode subscript with a fallback font. Likewise, an encoded 6.98pt run need not render at 6.98pt. A font allow-list check on PPTX XML cannot prove absence of fallback.

Use the read-only `scripts/typography_audit.py` on selected mathematical regions when a PDF with text is available. It requires `pdfplumber` from the workspace runtime. Supply tight, nonoverlapping regions in PDF points (top-left origin), expected characters from the native expression, the intended publication width, approved **rendered PostScript font names** and review thresholds chosen for this figure. Inspect the preview to select regions; do not guess from stale coordinates. An example plan for one region is:

```json
{
  "pdfSha256": "<hash of the PDF being checked>",
  "publicationWidthMm": 177.8,
  "regions": [{
    "name": "state-label", "page": 1, "expectedText": "s(tnow)",
    "boundsPt": [380, 178, 442, 205],
    "expectedFonts": ["ArialMT"],
    "minSizePt": 6.0,
    "minRelativeSize": 0.60
  }]
}
```

These thresholds are illustrative review triggers, not publisher requirements. `minRelativeSize` compares the smallest and largest extracted font sizes within the region; select one expression with a comparable base size. `minSizePt` applies after scaling to the stated publication width. PDF subset prefixes are ignored, but font families are not silently aliased. Explicitly approve intended math fonts and styles; do not approve a fallback just to clear a finding.

```sh
python scripts/typography_audit.py figure.pdf --plan math-regions.json --output typography-audit.json
```

The report flags unexpectedly small text, fonts outside the approved set, region-boundary characters, missing/extra characters and regions with no extractable text. `expectedText` contains the ordinary character sequence (not LaTeX markup); whitespace is ignored and characters are compared by count because PDF script order can differ. This can expose a missing index even when the base text is extractable, but it does not verify ordering, mathematical meaning, kerning or native equation editability. Font-size metadata is not the visible ink height of a precomposed Unicode script. Outlined or rasterized text is unmeasured, never a pass. Pair the report with the original content contract and a visual check. Diagnose flagged cases rather than replacing fonts or resizing all scripts automatically.

Name the renderer in validation notes. LibreOffice/PDF results do not establish native PowerPoint appearance. When output engines disagree, inspect the target application and preserve the verified export separately. Never claim reference-level typography from structural checks alone.

# Review and preservation

## Confirm the selected creation route

Read the selected mode from task notes; see [image options](image-options.md). In image-draft mode, inspect the [draft-stage evidence](image-first.md#completion-evidence): actual full-figure draft and prompt, its review and transfer plan before PPTX authoring, and the draft-to-saved-render comparison. An asset-only image call or post-hoc image does not meet that route's requirements. In no-API mode, those artifacts are not required: review the content contract, references, palette decisions and native construction instead, and record that no image-model draft was generated. In every mode, keep full raster drafts out of the delivered PPTX and verify native explanatory objects. Local edits to a saved PPTX follow the preservation path below.

## Two independent review passes

Content: compare required labels, nodes and directed relationships against the exported objects. Preserve training/inference scope, repeated-block meaning and parameter-sharing distinctions. Explicitly check what is absent as well as present. The contract is written from the brief, not inferred from the finished picture.

Appearance: render the saved PPTX, inspect each figure enlarged, then at its declared publication width. Check text clipping, manual breaks, padding, hierarchy, association of labels, intersections, arrow direction, contrast and available fonts. Inspect the whole figure after local changes. Structural checks cannot settle these questions. Stop after a small bounded number of rounds (usually three), preserving a record of remaining issues rather than claiming success by exhaustion.

For the draft-based creation route, compare that saved-file render with the selected full draft at equal width. Verify the useful composition, visual hierarchy and spacing survived native reconstruction; distinguish justified semantic corrections from accidental loss of visual quality. This comparison is required even when all structure checks pass.

For icons, review their [abstraction level and role](visual-assets.md#choose-abstraction-by-role), not merely whether a picture was inserted. For formulas and indices, use [mathematical typography review](math-typography.md#review-the-saved-output), including the rendered PDF's actual font names and script sizes. A PPTX font declaration and a legible enlarged preview can both miss fallback glyphs or scripts that are too small at publication width.

For labeled review, check whether decision symbols and state encodings can be interpreted from the figure plus its intended adjacent caption. Standalone figures need their own essential definitions; do not duplicate a complete caption as a glossary. If a fill changes after an observation, verify that it denotes the stated classification/status rather than an unintended physical transformation. Review all essential statuses at the actual intended width and in grayscale, especially pale unmeasured/pending marks beside empty or negative marks. Record a failed contrast check as a local finishing issue when the underlying flow remains clear.

Use [relationship planning and review](relationship-review.md) for endpoint, set-scope, identity, expansion and matrix-axis checks. Run `scripts/flow_audit.py` on the saved file to locate suspicious anchors or unsupported geometry, then resolve its flags in the render. Valid object IDs can still connect to a transparent caption box far from the depicted data. The audit is read-only and its warnings are not automatic aesthetic failures.

LibreOffice, host preview services and PowerPoint are different renderers. If their output disagrees, inspect PowerPoint when available and record which renderer produced the preview. Do not call a LibreOffice or host-rendered PNG a PowerPoint screenshot. Use an available renderer or the host-supported rendering wrapper, and record which one ran. Do not install a desktop application merely to hide a missing renderer. Pixel dimensions and physical preview dimensions must both be clear; browser print at 100% is more reliable for physical sizing than screen pixels alone.

## Inspect

```
python scripts/pptx.py inspect latest.pptx --contract contract.json --output inspect.json
```

Slide numbers are one-based **presentation order**, as displayed in PowerPoint, not the numbers in ZIP part filenames. Inspection and connector audits report both `slide` and the resolved `part`; contracts and generation manifests use that same displayed order. Reinspect after reordering or replacing slides.

Reports must use a new path. `inspect --output` and `patch --receipt` refuse existing files, links and collisions with inputs or the revised PPTX. Receipt availability is checked before patching; a failed patch removes its newly reserved receipt. Omit the report option to print JSON to standard output.

Contracts have `slides:[{nodes:{name:exactText},edges:[[from,to]],groups:[name]}]`. Newlines in labels are significant. `exactEdges` and `nativeOnly` default to true. A contract checks only what it specifies; the author must add all scientifically essential content. Counts of native shapes alone do not prove their correctness.

For mixed image/native figures, follow the explicit asset inventory in [visual assets](visual-assets.md). `nativeOnly:false` permits necessary picture objects; it does not establish that the rest of the diagram is editable. Verify that the named inserted assets are present, match their saved media and are individually replaceable, while required labels, semantic marks and connections remain native. Generated icons and illustrations are valid assets, not limited to photographs.

## Local patch of the latest file

Save and close the user's current file or confirm it is not changing during the operation. Inspect **that file**, not an old manifest. A plan contains:

```json
{
  "sourceSha256":"<from latest inspection>",
  "operations":[{
    "slide":1,"part":"<part from latest inspection>","id":"<current ID>","name":"encoder",
    "fingerprint":"<current object fingerprint>",
    "action":"replace_text","old":"Encoder","new":"Temporal encoder"
  }]
}
```

```
python scripts/pptx.py patch latest.pptx revised.pptx --plan edit.json --receipt receipt.json
```

The optional `part` field verifies that the numbered slide still maps to the inspected ZIP part. The receipt records both. The source hash prevents a stale edit; the current ID/name/fingerprint prevents an ambiguous target. Numeric IDs and names are not identities across arbitrary edits. If two objects have the same name after duplication, use the latest ID and visual context; never choose the first match. A failed precondition requires a fresh inspection, not disabling the check.

Supported text edits replace a unique substring in one text run, retaining that run's formatting. Cross-run replacement is rejected rather than flattening rich text. `move` uses CSS-pixel `dx`/`dy` for a top-level unrotated, unflipped shape or unconnected group. Attached straight connectors are recomputed only when both endpoints are top-level, unrotated, unflipped rectangles/rounded rectangles with supported connection sites. A rotated or flipped peer, grouped endpoint, transformed connector, custom route or connected-group move is rejected before saving; use native PowerPoint for those edits. The patcher refuses to overwrite its source or an existing output.

`style_connector` changes only a native connector's stroke width, existing destination arrow size, cap and join. Supply `widthPx` (positive and at most 12), `arrowWidth` and `arrowLength` (`sm`, `med`, `lg`) in addition to the usual source/target preconditions. It retains direction, endpoints, geometry, color and dash. It refuses non-connectors and absent/non-directional destination arrows. Inspect and render the saved result; it does not repair routing or overlapping content.

All untouched ZIP-entry payloads remain byte-identical. Within an edited slide, review the changed XML objects and compare the preview; XML serialization may change prefixes, but unrelated subtree content must stay equivalent. Media, unknown package parts, comments and styles are preserved when they were not targeted. No import/export model round trip is used for these edits. Do not run the original generator after a person has changed the file.

Reinspect the patched file, render it, compare changed and unchanged regions, and open it in PowerPoint where possible. For an intentional content change update the relevant contract with the user's new requirement. A patch receipt is evidence of change scope, not a proof of visual quality.

# Generated visual assets with editable explanations

Choose the mode with [image options](image-options.md). In API mode, first generate and inspect the full composition draft, then generate meaningful inserted imagery separately. Composition exploration and final pictorial assets have different purposes. In **no-API mode**, do not invoke an image provider: use authorized existing images or appropriate native pictograms, and state any missing photographic asset honestly. All modes preserve native explanatory text and geometry.

## Assign an authoring method to each element

| Element | Authoring method |
|---|---|
| Representative equipment, specimen illustration, scene, material appearance or pictorial icon | Generate or source an appropriate raster asset; insert it as an independent picture. |
| Labels, captions, equations, legends, arrows, axes, channels, state marks, correspondence cells and module boundaries | Native editable objects. Do not bake these into an image-generation request. |
| Exact measured sample or experimental result | Use supplied/authorized source data. Generated appearance is illustrative, not a substitute for evidence. |
| An icon's internal part that encodes an editable scientific relation | Separate that part into native objects, or draw the whole semantic icon natively. |

List the needed assets and their roles before authoring. Choose a small useful set rather than an arbitrary icon quota. For example, a camera image can establish the source of visual observations, while the observation timestamp and outgoing data path stay native. A generic object illustration need not specify a manufacturer's product or the experiment's exact hardware; label it as representative where that distinction matters.

Do not equate editability with zero images. Do not replace every physical input with a labeled rectangle to pass a `nativeOnly` check. Conversely, illustrative assets cannot repair missing relationships or justify invented measurements.

## Choose abstraction by role

For a small icon identifying a source, function or category, prefer an abstract pictogram: recognizable silhouette, limited palette, consistent outline or solid-fill treatment, and little or no shading. A camera used to mean visual input usually needs its body and lens, not reflective glass, screws and material texture. Judge useful detail at the intended printed size; extra detail is not automatically extra quality. Keep the visual weight compatible with adjacent native shapes.

Use photographs or richer illustrations when appearance itself is informative: an actual input scene, specimen, apparatus geometry or reconstruction. Preserve a user's specified illustration style. Do not impose pictograms on real observations or treat every research figure as a flat-icon diagram. BLIP-2 and Flamingo use simple frozen-state symbols alongside photographic inputs; RLDX-1 and CLIP use sample images and abstract internal representations. These are role-based observations from selected references, not a prevalence study or an AI-authorship test. See [reference observations](reference-cards.md#icon-role-and-mathematical-typography).

For generated concept icons, a useful prompt specification is: “One isolated flat pictogram of [subject], representing [role]. Simple silhouette, consistent [outline/solid] style, [palette], readable at [printed size]. Transparent background. No photorealistic materials, glossy reflections, product-render lighting, decorative shadows or fine hardware details.” Append the exclusions below. Perspective or restrained depth may be appropriate when it explains geometry; it is not a default embellishment.

## Generate independent final assets

The exclusions in this section apply to **asset prompts**, not to the preceding full-figure composition draft. That draft may depict the complete layout, including provisional text and arrows, solely for reconstruction. Final explanatory text, mathematics and diagram geometry must still be native.

In API mode, use `scripts/gemini_image.py --help` and its `generate --purpose asset` command, or the actual image provider already selected by the user; see [image options](image-options.md). Do not assume the host exposes a built-in bitmap-generation tool. Give each asset its subject, view, style, palette role, printed size, and composition/crop requirements. Keep style consistent across a set. Request a transparent background when the provider supports it, verify actual alpha, and preserve it. Gemini output is not guaranteed to contain an alpha channel; use appropriate native pictograms or another explicitly selected asset route if transparency is required. Do not treat a white or checkerboard background as transparency. Generate independent assets in separate calls when they need separate placement or replacement.

Explicitly exclude text, labels, numerals, logos, arrows, axes, connectors, legends, surrounding panels and complete diagram layouts. Add these later as native objects. If an unwanted label or diagram fragment appears inside a generated asset, correct it with the image tool or select another result; covering it with editable text is not the preferred construction.

Inspect each asset at the actual intended size: silhouette, legibility, clutter, transparency edges and compatibility with the figure. Save the selected source image and actual prompt in the project. Record which image is generated and what it represents. Do not vectorize a raster into thousands of tiny shapes merely to claim editability.

## Assemble and verify

Insert every asset as its own named picture object. Preserve aspect ratio and useful transparency; cropping belongs to the picture object, not to the scientific geometry. Put annotations, region outlines and arrows above/beside it as separate native objects. Bind data connectors to a visible native source boundary or port associated with the asset, rather than treating a remote caption as its endpoint.

For mixed figures, set `nativeOnly:false` on the relevant slide in the content contract (`slides[i].nativeOnly`, not at the top level) and verify an explicit picture inventory alongside the required native labels/nodes/edges. Check picture names, count and media identity; allowed raster assets do not authorize a flattened diagram or hidden full-figure background. The current inspector does not itself enforce that inventory, so verify the saved package separately.

Render the saved PPTX and verify that raster assets survived, all required explanatory elements remain native, and the images add useful visual context without obscuring text or endpoints. A test of asset insertion fails if generation was performed but no requested asset appears in the final figure.

Describe editability precisely: pictures can be moved, resized, cropped and replaced independently; their internal pixels are not editable vector parts. Text, mathematical notation, diagram structure and arrows remain individually editable. Save the assets separately so the user can replace them later.

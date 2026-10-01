# Represent the method, not just its module names

The first implementation produced technically editable but generic flowcharts. It flattened samples, operations and representations into equally important labeled rectangles. The corrections below address that observed failure; they are not a mandatory visual template.

## Study what is actually visible

Open the source figure, not only its caption. Look for the concrete sample, the representation that changes, the key relationship, the organizing spatial metaphor, the reading order, and the smallest labels. Decide which elements explain something and which are only styling. Compare the new draft with the reference at a similar publication width. State when the source image itself could not be inspected.

MAE's input patches and latent tokens are different visual objects. CLIP carries concrete image/text examples into an indexed correspondence matrix. U-Net uses feature-map dimensions and paired levels to encode architecture. The Transformer uses nested operations and precise residual joins; a photograph would add nothing there. See the [source cards](reference-cards.md).

## Choose marks by information type

| Information in the brief | Useful representation | Avoid |
|---|---|---|
| Visual input, crop, specimen, reconstruction | Actual supplied sample, or a clearly illustrative generated/source image when appropriate, with separate native region marks and captions | A generic "Image" box when spatial content matters; synthetic output presented as measured evidence |
| Source category or function, such as a camera input | A restrained pictogram with a recognizable silhouette and native labels/connections; generate the asset when appropriate | Glossy product detail that carries no information at the intended size; baking labels or arrows into the icon |
| Apparatus, material or specimen whose appearance matters | A meaningful independent photograph or illustration, with native explanatory annotations | Substituting a generic pictogram for scientifically relevant appearance or geometry |
| Feature channels and spatial hierarchy | Sized feature planes, short stacks, dimension annotations, matched skip levels | Arbitrary 3D thickness implying a channel count; identical boxes with scale written beneath |
| Patch/token selection | Stable position identities, visible masked/kept states, a clearly reduced sequence | Arbitrarily recoloring token identities between stages |
| Correspondence or pairwise operations | Indexed rows/columns, complete relevant pairs, meaningful diagonal or grouping, a compact formula | Decorative heatmaps with no defined axes or fabricated scores |
| Temporal alignment or uncertainty | Observed samples, intervals, uncertainty marks and aligned support; measured data when supplied | Invented curves that imply an accuracy gain |
| Hierarchy or repetition | One expanded unit plus the state sequence or a repeat enclosure; explicit weight sharing/separation | Filling space with extra modules or confusing repetition with a feedback loop |
| Retrieval, evidence or documents | Candidate snippets/stacks, provenance, a worked scoring decomposition | Generic icons that merely repeat the adjacent label |

Use only the representations the method needs. This is not a quota for photos, panels, token strips or a standard number of visual layers. If inputs are abstract and relationships are the core idea, a restrained diagram may be correct.

## Composition and restraint

Follow the selected [image mode](image-options.md). In image-draft mode, explore the whole composition with the [image-model draft](image-first.md) before native PPTX construction; a simple diagram still needs that route's draft. Keep effective visual relationships from the inspected image and correct scientific errors against the content contract. In no-API mode, apply these design principles directly to native authoring after reference and palette review, without requiring a generated draft.

Give the central contribution enough room to be inspected. Let support elements use less contrast and space. A large slide-style heading is often unnecessary in a paper figure that already has a caption. Use asymmetry when the method is asymmetric. Empty space should separate semantic groups, not substitute for missing detail. Choose meaningful color roles and keep them stable across views; the method determines how many are needed.

Use [color books](color-books.md) for several compatible palettes and their fill/stroke/accent recipes. Select by semantic roles and emphasis, not by a blanket preference for or against pastel. Large pale regions, stronger small marks and dark structure can coexist, as the RLDX reference illustrates. Colors supplied by a user or established elsewhere in the manuscript take precedence over the catalog.

Do not imitate a reference's surface style by adding gradients, shadows, random heatmap cells or tiny equations. Ask whether a reader can learn something from the marks before reading every label. Also ask whether replacing the method names would leave the figure unchanged; if so, method-specific information may be missing.

Separate raster media from editable explanations using [visual assets](visual-assets.md). Keep photos, generated object illustrations and suitable icons as independent picture objects, not thousands of traced shapes. Keep text, formulas, scientific geometry, cells, contours, annotations and arrows native when they need editing. "Zero pictures" is not a quality metric. Do not flatten the whole composition into an image or an SVG.

## Give the flow a visual hierarchy

Inspect connectors at publication width, not only while zoomed in. In the reviewed 177.8 mm examples, 1.3 px shafts (0.975 pt) with the smallest arrowheads made the flow recede behind the boxes. A useful starting point for this scale is 2.6 px (1.95 pt) for the main flow, 1.7–1.9 px for secondary/conditioning/update paths, and about 0.8–1 px for object borders. These are adjustable starting values, not publication standards.

Choose the shaft, arrowhead width/length, color, dash and join together. A thicker shaft with the old tiny arrowhead can still look weak; making every path equally heavy removes hierarchy. The revised helper exposes arrowhead sizes and preserves them on export. Check short gaps, merge points, arrow tips touching shapes, nearly-horizontal diagonals and unnecessary elbow detours. Native round joins soften corners without rasterizing them. Keep the main route visually continuous, reserve secondary lanes, and use dashed lines only for a defined role.

Thickness alone cannot fix a generic composition. Evaluate it alongside module proportions, semantic detail, spacing and typography. To isolate its effect, compare the same saved figure before and after restyling its connectors.

## Make relationships traceable without reading every label

Use [relationship planning and review](relationship-review.md) to define the unit represented by each mark, visible edge endpoints, collection scope and identity across views before arranging the diagram. This addresses the observed endpoint and correspondence gaps that persisted after the arrows were thicker. A simple overview can be adequate, and a generated figure can be comparable to a published one. Add only the detail that resolves a demonstrated explanatory gap; keep successful regions.

## Honest worked examples

Use real data when provided. When an example is necessary but no data exist, clearly identify it as illustrative and choose only the detail needed to explain the operation. Do not claim that a hand-drawn curve or generated image came from the method. Indicate when feature planes have unspecified channel counts. A colored feature glyph is schematic, not an activation measurement.

## Review the actual result

Inspect every final figure at full size and intended publication width. Check whether the contribution, data transitions and correspondence are legible; whether detail supports the story; and whether photographs, native marks and type form a coherent composition. Fix clipping, collisions and ambiguous paths. Structure checks establish neither visual quality nor source fidelity. Do not report aesthetic scores or reference-level equivalence without an actual evaluation.

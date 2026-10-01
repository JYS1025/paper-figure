# Graph pooling — gallery example

Original illustrative hard-assignment example, created in Codex on 2026-10-01. Visual reference: [Hierarchical Graph Representation Learning with Differentiable Pooling](https://arxiv.org/abs/1806.08804). DiffPool learns soft assignments; the displayed one-hot matrix is a toy construction for explaining pooling, not a learned result.

The [content contract](content-contract.json) and [reference observations](reference-observations.md) preceded image generation. The built-in image model produced the [full draft](image-draft.png) from the [saved prompt](draft-prompt.txt). After inspection, the [transfer plan](transfer-plan.md) was saved before native construction. Every final explanatory element was rebuilt with native PowerPoint objects; no raster asset was needed.

## Delivered output

- [Editable PPTX](figure-v2.pptx), [saved-file PNG](preview.png), [PDF](figure.pdf).
- [Equal-width draft comparison](draft-vs-pptx.png), [publication preview](publication-preview.png), [grayscale preview](grayscale-preview.png).
- 107 native shapes/text objects, 2 native process connectors, 2 math groups, zero pictures. Undirected graph edges are native paths. Equations are grouped native text with explicit superscript placement, not OMML equation-editor objects.

## Validation

Package integrity, slide geometry and import validation passed. Exact labels, matrix values and stipulated connector pairs passed the [structural check](structure-check.json). All eleven graph-edge identities and their saved geometric endpoints were checked. Independently computing SᵀAS gives `[[6,2,1],[2,6,1],[1,1,2]]`, matching the saved native cells. Each internal undirected edge contributes twice to diagonal mass. The graph displays cross-cluster edges while the matrix retains that mass. See [arithmetic record](graph-arithmetic.json).

The [connector audit](connector-check.json) flagged two transparent graph-region boundaries. Full-render review confirmed that the arrows connect the three explanatory regions without crossing a node or a matrix label. They show the explanatory sequence, not a claim that S alone determines the pooled graph. All attachment offsets are below 0.01 px.

The bundled renderer initially substituted fonts. A render-local Fontconfig file pointed to the existing macOS fonts. The final PDF uses Arial/Arial Bold and Times New Roman regular/italic. Both full mathematical expressions passed the [rendered typography check](typography-check.json): minimum script size 9.411 pt; script/body ratio 0.6587 at 177.8 mm width. The smallest other text is 8.107 pt. Full-size and grayscale previews were inspected; IDs, matrix values and graph structure remain readable without color.

These are package, semantic and rendered-output checks, not a manual PowerPoint editing test, a blind quality score, or an end-to-end Claude run. See [machine-readable validation](validation.json).

# Masked image modeling — gallery example

Original illustrative training schematic, created in Codex on 2026-10-01. Visual reference: [Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377). The generated wildlife photo is an illustrative input; coral prediction cells are symbolic, not a measured reconstruction.

The [content contract](content-contract.json) and [reference observations](reference-observations.md) preceded image generation. The built-in image model produced the [full draft](image-draft.png) from the [saved prompt](draft-prompt.txt). After inspection, the [transfer plan](transfer-plan.md) was saved before native construction. The source photograph was generated in a separate call; its prompt and source inventory are in `assets/`.

## Delivered output

- [Editable PPTX](figure-v2.pptx), [saved-file PNG](preview.png), [PDF](figure.pdf).
- [Equal-width draft comparison](draft-vs-pptx.png), [publication preview](publication-preview.png), [grayscale preview](grayscale-preview.png).
- 103 native shapes/text objects, 8 native connectors, 9 picture objects using one shared source image. The full draft is absent from the PPTX. Picture crops remain independent; sharing identical media bytes reduces the file from approximately 24.5 MB to 2.7 MB.

## Validation

Package integrity, slide geometry and import validation passed. Exact native text and the eight stipulated connector pairs passed the [structural check](structure-check.json). All nine pictures match the generated source bytes; the eight patch crops preserve the same row-major IDs 2, 5, 10 and 15. Twelve masked positions and all sixteen restored/predicted cells match the independent contract.

The [connector audit](connector-check.json) flagged four connectors attached to transparent sequence boundaries. Full-render review confirmed that these boundaries enclose the visible photo or latent stacks, and the arrows terminate at those stack boundaries. All attachment offsets are below 0.01 px. This is a resolved visual review, not a claim of zero audit flags.

The bundled LibreOffice initially substituted fonts. A render-local Fontconfig file pointed to the existing macOS Arial and Times New Roman fonts; no font installation or system configuration change was made. The final PDF uses Arial/Arial Bold, with a smallest rendered text size of 8.107 pt at 177.8 mm width. Full-size and grayscale previews were inspected; patch identity remains visible without color. The label intersecting the loss-branch connector in the first version was moved before delivery.

These are package, semantic and rendered-output checks, not a manual PowerPoint editing test, a blind quality score, or an end-to-end Claude run. See [machine-readable validation](validation.json).

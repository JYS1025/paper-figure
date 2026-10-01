# Image-model draft → editable PPTX

This route applies when using the built-in Antigravity image tool or another selected available image provider for a new figure or substantial redesign: **full-figure image-model draft → reviewed transfer plan → native PPTX reconstruction → saved-file comparison and validation**. Choose the mode using [image options](image-options.md) first. In **no-API mode**, author directly from the content contract and references and retain saved-file checks; the generation, transfer and comparison steps below do not apply. Separate icon/illustration generation follows [visual assets](visual-assets.md); it satisfies a different requirement and cannot replace the full composition draft.

Local text, color or geometry edits to the latest human-edited PPTX preserve that file and do not restart this design process. If the user explicitly requests direct authoring without a draft, honor and record that instruction. If the task is exact reconstruction of a supplied raster, inspect that image and use it as the design source without inventing a new composition; identify it as supplied, not image-model-generated. These routes do not establish that a new image-model draft was made.

## Generate the composition before building

1. Complete the scientific content contract, reference inspection, intended paper width/aspect ratio and color-role mapping first. Keep content authoritative outside the image.
2. Use the callable built-in `generate_image` tool for `antigravity-native`, the bundled `scripts/gemini_image.py` client only for selected Gemini API mode, or another explicitly selected provider (see [image options](image-options.md)) to generate at least one full composition for the current figure. Include its required entities and relationships, main visual explanation, exact notation as guidance, role colors, target proportions and the requirement for legible paper-scale hierarchy. Do not ask merely for an isolated icon, a palette swatch or a generic style board. Do not create the PPTX first and generate a matching image afterward.
3. Save the actual prompt and resulting draft in the task workspace, then view the image. Inspect the whole composition and its small labels, branches and repeated items against the contract. A successful tool call alone is not a reviewed draft. If it is unusable, make a targeted revision before proceeding; normally keep draft review within three rounds. On a failed API call, report the concrete failure and offer retry/setup or no-API mode; do not change modes silently.
4. Write the transfer decisions below **before PPTX construction**. Use the draft's effective composition rather than merely saving it and independently drawing the same old box layout. If major errors make most of the composition unsuitable, revise the draft; do not claim it informed the final layout when it did not.

The full draft may contain rendered text, mathematical notation, arrows and schematic geometry to explore their visual placement. They are provisional pixels only. Re-enter final text and mathematics from the content contract and rebuild final diagram elements natively. This permission to depict them in a draft does not permit embedding raster explanations in the delivered editable figure.

A useful prompt structure is:

```text
Create a complete visual composition draft for a research-paper figure.
Scientific content: [required entities, directed relationships, states, notation].
Primary explanation: [what the reader should understand from the marks].
Canvas: [aspect ratio and intended publication width].
Visual direction: [applicable reference observations, color roles, hierarchy].
Preserve: [identity, correspondence, quantities and required distinctions].
Avoid: invented stages/data, illegible dense labels, decorative complexity.
This is a design reference for later editable PPTX reconstruction.
```

## Separate scientific meaning from visual reference

The content contract governs labels, entities, direction, state, scope and scientific claims. The raster is a reference for composition, proportions, hierarchy, spacing and applicable visual cues. An attractive reference can contain duplicated stages, impossible connections, misleading states or invented measurements.

Trace required data/material paths, control paths, repeated items, state distinctions and quantities against the contract. Decide whether a shade or fill is cosmetic or encodes a state. Check essential status differences at publication size and without hue. Add symbol definitions and timing correspondence only as required by the brief and intended caption.

Record a compact transfer plan:

- **Preserve:** useful composition, relative scale, density and visual devices.
- **Correct:** semantic mistakes, unsupported details and inconsistent encodings.
- **Create/source as an asset:** appropriate pictorial content, as independently replaceable images with clear provenance and role. Generate requested pictograms/illustrations separately; the composition draft alone is not their final asset.
- **Rebuild natively:** labels, equations, semantic marks, module/channel geometry and explanatory connections.

Match meaningful proportions and negative space before small details. Keep the full raster reference out of the final editable diagram, including hidden/background objects. Do not cover it with native labels, insert it as one picture/SVG, or trace thousands of shapes. Equally, do not discard useful pictorial content just to make the picture count zero. Generated imagery remains illustrative, not experimental evidence.

## Verify the saved result

Run the ordinary contract, saved-file render, typography and relationship checks. Compare the selected draft and the render of the saved PPTX side by side at equal intended publication widths for hierarchy, relative scale, density, clearances, palette allocation and typography. Check the expected native objects and individual raster assets separately. Correct reconstruction losses that flatten the visual hierarchy or weaken the useful composition; semantic corrections take precedence over pixel fidelity. Native object checks do not replace this visual comparison or an interactive application test.

## Completion evidence

Keep a compact workflow record with paths to the content contract, actual image-generation prompt, selected full draft, pre-authoring transfer plan, final PPTX and its rendered preview. Record the comparison outcome and deliberate corrections; identify the actual renderer. Existing task notes can hold this record—no extra report format is required. Do not infer execution from a planned prompt, an icon-generation call, an old task's draft, or the final image's appearance.

In image-draft mode, the work is incomplete until the full draft has been generated and inspected before authoring, reconstructed, and compared with the saved-file render, unless the user chooses another route. No-API mode is complete after its native authoring and saved-file checks; it does not require an image draft. In the handoff, link the selected draft as well as the final PPTX/preview and name any such exception. A missing required stage is a workflow failure even when the final file is structurally valid. Do not retroactively relabel earlier direct-authored samples as image-model-draft tests.

When a comparison is requested, distinguish source-reference quality, fidelity of the editable reconstruction and superiority over another authoring route. Follow [blind review](blind-review.md) with truthful classes; two generated candidates are not a published/generated pair. Disclose unequal briefs, prompts, review budgets or prior feedback that prevent a controlled comparison.

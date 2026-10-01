# Image workflow for this task

Use direct native authoring by default in Claude; do not start with an image-provider menu or key-registration question. Reuse a route already selected by the user. Existing PPTX edits and exact reconstruction of a supplied image need no new composition draft or onboarding.

Only when the user explicitly requests use or setup of the external Gemini image API, read [the requested integration guide](gemini-image-api.md). Before that request, do not advertise the option, offer it as a fallback, inspect credentials or run setup. A saved key, an ordinary request for an image, or a missing tool is not a provider choice. If the user expressly selected another available image provider, follow its actual interface rather than switching providers.

In an explicitly selected image-generation route, follow [image-first.md](image-first.md), then reconstruct native PowerPoint objects. Record the actual provider/model only for calls that occurred. A generic request for a generated photograph does not authorize enabling a new external service: explain the available capability and use supplied imagery or a suitable native representation when appropriate.

## Direct native authoring (`no-api`)

Proceed directly from the content contract, visually inspected references, relationship plan and color roles to native PowerPoint authoring. **This is a normal supported mode, not a missing-stage failure.** Skip image-provider setup, image-model drafting, raster transfer plans and draft-to-render comparison. Do not call this an image-model workflow or invent a generated draft.

Maintain the same relationship, typography, saved-PPTX rendering, paper-scale and grayscale checks. Use informative native pictograms, spatial structures, matrix cells and data states when appropriate. Use user-supplied or otherwise authorized existing photographs where they are needed; do not invent experimental imagery or describe native drawings as generated photographs. If a requested new raster illustration cannot be made without an image API, explain that limitation and offer an appropriate native representation or supplied asset. Do not quietly switch to a different image provider.

Deliver the editable PPTX, its actual saved-file preview and validation note describing direct native authoring. Do not label the default result with an unrequested API option; do not claim an image-model draft was generated.

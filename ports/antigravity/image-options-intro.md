# Image workflow for this task

For a new figure or substantial redesign, use Antigravity's callable built-in `generate_image` by default when available. Use the host's account access and quota; do not present an image-provider menu or require external credentials. The tool must actually be exposed in the current session: documentation or local dependency checks do not establish tool/account access.

An existing user-selected route persists within the task. “No separate API key” still permits built-in image generation; an explicit request for no image generation selects direct native authoring. Local PPTX edits and supplied-image reconstruction need no new draft or onboarding.

## Built-in image generation

Resolve the actual tool and schema. Save the complete composition prompt and returned image, inspect it before authoring, and follow [image-first.md](image-first.md). Preserve transfer decisions and compare the draft with the saved-PPTX render. Generate needed pictorial assets separately. Record the actual tool and returned model information without inferring it from the chat model or fabricating another client's receipt.

If the tool is absent or fails, report the specific limitation. Continue independent preparation; discuss a supported retry, supplied image, or direct native authoring when appropriate. Do not introduce an external API as an unsolicited fallback. Missing credentials for an unrequested integration are irrelevant to this route.

## Explicit integration request only

Read [Gemini image API setup](gemini-image-api.md) only after the user explicitly asks to use or configure that external API. Before the request, do not advertise the integration, ask for registration, inspect credentials, or show an API/no-API choice. A generic image request, a stored key, a native-tool failure, exhausted quota or the host name Gemini does not select the external API. Reuse an explicit task-level choice without repeated onboarding.

## Direct native authoring (`no-api`)

When the user explicitly skips image generation, proceed from the contract, original references, relationship plan and color roles to editable native objects. Use authorized supplied imagery and appropriate native pictograms. State that no image-model draft was generated. Keep saved-file rendering, typography, paper-scale and grayscale checks; do not invent an image-generation record.

Official host references, checked 2026-10-01: [built-in image tool](https://antigravity.google/docs/hooks#interaction-and-media), [account authentication](https://antigravity.google/docs/cli/install/), [plans and quota](https://antigravity.google/docs/plans/). Use the actual session's capabilities rather than changing its authentication or region.

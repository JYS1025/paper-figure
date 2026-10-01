# Choose the image workflow

Antigravity CLI has a built-in `generate_image` tool. For a new figure or substantial redesign, prefer that tool when it is actually exposed in the current agent session and the user has not selected another route. **A separate Gemini API key is not a prerequisite for the account-authenticated built-in path.** The host's account access, permissions and quota still apply. Check capabilities without making a paid generation call solely as a probe. A local dependency/credential check cannot establish native-tool availability.

| Route | Use | Separate Gemini API key |
|---|---|---|
| `antigravity-native` | Default when available: built-in image draft, review, then native PPTX reconstruction. | Not required for the account-authenticated host tool. |
| `gemini-api` | Optional explicitly chosen external API client. | Required by the included client. |
| Direct native authoring (`no-api`) | Explicitly skip image-model generation; use native shapes/text and authorized existing assets. | Not required. |

Do not interpret “without registering an API key” as a request to omit the image draft. Use the built-in tool when available. If the user explicitly requests no image generation, honor that choice. Reuse prior choices without repeated onboarding. Existing PPTX edits and supplied-image reconstruction follow their own routes.

## Built-in Antigravity image mode

1. Resolve `generate_image` from the current session's tools and follow its actual schema. Official documentation lists it, but do not invent a shell command or tool call when it is not exposed. Do not extract host credentials or feed them to the separate API client.
2. Save the complete composition prompt, call the host image tool, and preserve its returned image. Inspect that image before native authoring. Follow [image-first.md](image-first.md) for the transfer plan and saved-PPTX comparison. Generate final pictorial assets separately when needed.
3. Record the route and actual tool/provider. Record a model ID only when known from the tool result; do not infer it from the chat model or copy the external client's default. Preserve available generation metadata without fabricating a `gemini_image.py` receipt. Keep all final explanatory labels, formulas, diagram shapes and arrows editable.
4. If the tool is unavailable or returns an access/quota/error result, report the specific observation. Offer a supported retry, optional Gemini API, or direct native authoring. Do not change routes silently or require API registration merely because local API-key status is unconfigured.

When a fallback choice is needed, ask in the user's language, for example: “현재 세션에서 내장 이미지 생성을 사용할 수 없습니다. 별도 Gemini API를 연결할까요, 아니면 이미지 생성 없이 편집형 도형으로 제작할까요?” Continue the independent content/reference preparation while awaiting the choice. Never request a secret in chat.

Official host references, checked 2026-10-01: [built-in image tool](https://antigravity.google/docs/hooks#interaction-and-media), [account login and optional API authentication](https://antigravity.google/docs/cli/install/), [account plans and quota](https://antigravity.google/docs/plans/). Enterprise regional endpoints can have different capabilities; use the actual session result rather than changing its authentication or region.

The following API registration instructions apply only to the separately selected `gemini-api` route.

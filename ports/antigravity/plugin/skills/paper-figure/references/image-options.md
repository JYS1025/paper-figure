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

## Gemini API mode

1. Explain once that the draft prompt and any specifically selected reference images will be sent to Google. The API has its own access, quota and billing; an Antigravity login or chat subscription does not establish image API access.
2. Run `python3 scripts/gemini_image.py status` from the installed skill folder (use the configured Python executable if different). It reports local credential presence only, never a key or a successful provider check.
3. If missing, direct the user to [Google AI Studio](https://aistudio.google.com/apikey) and let them create/manage the key. In **their own interactive terminal**, from this skill folder:

   ```sh
   python3 scripts/gemini_image.py setup
   ```

   Input is hidden. The helper writes a private key file outside the repository: `~/.config/paper-figure/gemini-api-key` on macOS/Linux, or `%APPDATA%/paper-figure/gemini-api-key` on Windows. POSIX permissions are 0600; Windows inherits the user's profile permissions. `setup --replace` explicitly replaces an existing key. The agent must not run an interactive setup in its tool session or request the secret through chat.
4. Existing secret management can instead supply `PAPER_FIGURE_GEMINI_API_KEY`, `GOOGLE_API_KEY` or `GEMINI_API_KEY`, in that precedence order; the dedicated variable avoids changing the host agent's authentication. `PAPER_FIGURE_GEMINI_KEY_FILE` selects a private key file. Do not inspect unrelated credential stores, write keys in the skill directory, print environment values, or pass a key as a CLI argument. An inherited environment variable takes precedence over the saved file; restart the agent after changing its environment.
5. Save the actual composition prompt, then call the included client:

   ```sh
   python3 scripts/gemini_image.py generate \
     --prompt-file /path/to/task/draft-prompt.txt \
     --output-dir /path/to/task/draft-01 \
     --purpose draft --aspect-ratio 16:9
   ```

   Use a new output directory per call. The client makes one request to Google's fixed HTTPS endpoint and does not retry automatically or follow redirects. It saves the prompt, decoded image files and `generation.json`; the model default is `gemini-3.1-flash-image`, checked against official documentation on 2026-10-01. `--model` selects another available image model. Use `--reference /path/to/image.png` only for selected images the task calls for sending; inspect them first. No project folder is uploaded.
6. Inspect the actual returned image and follow [image-first.md](image-first.md). A successful API response is not a reviewed draft. Generate appropriate final illustrations separately with `--purpose asset`; keep all explanatory geometry, labels and math native. The helper does not promise an alpha channel. For isolated pictograms, check the actual background; use native pictograms or an appropriate available asset tool when transparency is required.

Missing credentials or access: continue independent preparation and offer registration or no-API mode. Authentication, quota, timeout, blocked or text-only responses are failures, not permission to switch modes silently. Explain the concrete failure without echoing response bodies or credentials; let the user choose another mode or retry. Do not start repeated paid requests to probe model availability.

## Direct native authoring without image generation (`no-api`)

Proceed directly from the content contract, visually inspected references, relationship plan and color roles to native PowerPoint authoring. **This is a normal supported mode, not a missing-stage failure.** Skip image-provider setup, image-model drafting, raster transfer plans and draft-to-render comparison. Do not call this an image-model workflow or invent a generated draft.

Maintain the same relationship, typography, saved-PPTX rendering, paper-scale and grayscale checks. Use informative native pictograms, spatial structures, matrix cells and data states when appropriate. Use user-supplied or otherwise authorized existing photographs where they are needed; do not invent experimental imagery or describe native drawings as generated photographs. If a requested new raster illustration cannot be made without an image API, explain that limitation and offer an appropriate native representation or supplied asset. Do not quietly switch to a different image provider.

Deliver the editable PPTX, its actual saved-file preview and validation note with “No-API mode; no image-model draft generated.”

Official references: [Gemini image API](https://ai.google.dev/gemini-api/docs/generate-content/image-generation), [Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key), [image model](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image).

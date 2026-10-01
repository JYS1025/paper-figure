# Choose the image workflow

For a new figure or substantial redesign, offer two supported modes unless the user already chose one. Reuse the current task's choice; do not ask again for every asset or revision. A local PPTX edit or exact reconstruction of a supplied image does not need this onboarding.

Ask in the user's language. For example:

> 이미지 초안을 어떤 방식으로 준비할까요?
> 1. Gemini API 활용 — 이미지 모델로 구도를 탐색한 뒤 편집형 PPTX로 재구성합니다. API 키가 필요하며 Google API 요금이 발생할 수 있습니다.
> 2. API 없이 제작 — 레퍼런스와 배색을 검토하고 편집 가능한 도형·텍스트로 바로 만듭니다. API 키가 필요 없습니다.

In English: “Use Gemini API for a visual draft, or build native editable objects without an image API?” Do not ask the user to paste a key into chat. If the user says “without API,” that choice is sufficient: do not ask for a second waiver. Keep the question pending when the choice is needed; meanwhile prepare the independent content contract and reference observations. An existing key alone is not a mode choice. Honor an already requested, available image provider rather than forcing a switch.

Record `gemini-api`, `no-api`, `supplied-image`, `existing-pptx-edit`, or the explicitly chosen host provider in task notes. Save the model and generation records only for calls that actually occurred.

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

## No-API mode

Proceed directly from the content contract, visually inspected references, relationship plan and color roles to native PowerPoint authoring. **This is a normal supported mode, not a missing-stage failure.** Skip image-provider setup, image-model drafting, raster transfer plans and draft-to-render comparison. Do not call this an image-model workflow or invent a generated draft.

Maintain the same relationship, typography, saved-PPTX rendering, paper-scale and grayscale checks. Use informative native pictograms, spatial structures, matrix cells and data states when appropriate. Use user-supplied or otherwise authorized existing photographs where they are needed; do not invent experimental imagery or describe native drawings as generated photographs. If a requested new raster illustration cannot be made without an image API, explain that limitation and offer an appropriate native representation or supplied asset. Do not quietly switch to a different image provider.

Deliver the editable PPTX, its actual saved-file preview and validation note with “No-API mode; no image-model draft generated.”

Official references: [Gemini image API](https://ai.google.dev/gemini-api/docs/generate-content/image-generation), [Gemini API keys](https://ai.google.dev/gemini-api/docs/api-key), [image model](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image).

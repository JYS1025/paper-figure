# Gemini image API — explicit requests only

Read this reference only after the user explicitly asks to use or configure the external Gemini image API for this task. An ordinary figure/image request, mentioning Gemini as the host, a saved key, a missing native tool or exhausted native quota is not that request. Do not surface this integration as a default choice, suggest it as an unsolicited fallback, inspect its credentials, or start setup before that request. Reuse the explicit choice within the current task; do not ask for approval again merely because another draft or asset is needed.

This client is bundled in the Codex, Claude and Antigravity editions. Use the chosen host's Python runtime with Pillow available; it needs Python 3.10+ and no provider SDK. Codex keeps its existing PPTX authoring runtime. Selecting this image provider changes only the image-generation step, not the editable figure engine. The image-model draft, semantic transfer and saved-file checks still apply.

A request for setup information authorizes explanation/setup guidance, not an unrelated generation call. Never request a secret in chat or read the host's own credential stores. Use the following steps only for the requested integration.

## Requested setup and generation

1. Explain once that the draft prompt and any specifically selected reference images will be sent to Google. The API has its own access, quota and billing; an Antigravity login or chat subscription does not establish image API access.
2. Run `python3 scripts/gemini_image.py status` from the installed skill folder (use the configured Python executable if different). It reports local credential presence only, never a key or a successful provider check. In the Claude and Antigravity editions, `node scripts/preflight.mjs --check-gemini-api` includes this local credential check alongside authoring dependencies; use that flag only after this integration was explicitly requested. The default preflight does not check credentials.
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

Official references: [Gemini image API](https://ai.google.dev/gemini-api/docs/generate-content/image-generation), [API keys](https://ai.google.dev/gemini-api/docs/api-key), [image model](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image).

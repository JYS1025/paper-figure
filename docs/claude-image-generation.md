# Image options for Claude and Antigravity CLI

Both portable editions support **Gemini API** and **no-API** modes. When creating a new figure, the skill offers that choice unless the user already selected it. The choice is reused within the task. Existing PPTX edits and exact reproduction of a supplied image do not repeat onboarding.

| Mode | What happens | Required image access |
|---|---|---|
| Gemini API | Generate and inspect a complete visual draft; rebuild native PowerPoint objects; generate needed illustrations separately. | A Google Gemini API key, model access and network access. API quota and billing apply. |
| No API | Review references, color roles and scientific relationships, then author native shapes, labels, math and connectors directly. | None. Supplied images and native pictograms can still be used. |

Both modes require the authoring dependencies and a saved-PPTX renderer for visual verification. No-API mode is a supported route, not an incomplete image-model workflow. It does not synthesize photographic assets or claim a generated draft.

## Register a Gemini key when choosing API mode

The included `scripts/gemini_image.py` client implements the connection. No MCP server or additional Gemini SDK is required. It uses Python's standard library and Pillow. The default image model is `gemini-3.1-flash-image`, based on [Google's model documentation](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-flash-image); `--model` can select another available image model.

1. Open [Google AI Studio](https://aistudio.google.com/apikey) and create or select a key for your Google project. Do not paste the key into an agent chat.
2. In **your own interactive terminal**, open the installed Claude or Antigravity skill folder and run:

   ```sh
   python3 scripts/gemini_image.py setup
   python3 scripts/gemini_image.py status
   ```

   Use your configured Python executable instead of `python3` when needed. Input is hidden. The helper stores the key outside the repository in `~/.config/paper-figure/gemini-api-key` on macOS/Linux, or `%APPDATA%/paper-figure/gemini-api-key` on Windows. POSIX permissions are 0600; Windows inherits profile permissions. To replace a saved key explicitly, use `setup --replace`.
3. Tell the agent the setup is complete. It checks local availability, then calls the image API for the current task's saved prompt and selected references. `status` alone does not validate a key, model access, billing or quota.

Existing secret management can provide `PAPER_FIGURE_GEMINI_API_KEY`, `GOOGLE_API_KEY`, or `GEMINI_API_KEY`, in that order of precedence. `PAPER_FIGURE_GEMINI_KEY_FILE` selects a private key file. An inherited environment value overrides the saved file; restart your agent after changing its environment. The dedicated variable avoids changing Antigravity CLI authentication. Keys are never command arguments, prompt fields or generation metadata.

An Antigravity CLI login or subscription is separate from image API access. See [Google's key guidance](https://ai.google.dev/gemini-api/docs/api-key). The selected prompt and explicitly chosen reference images are sent to Google; whole project folders are not uploaded. Network-restricted claude.ai/API containers may prevent calls even with a valid key.

## How the image step works

Claude plans the composition and calls the optional Gemini client. Google's image model returns the raster draft; Claude inspects it and writes native PowerPoint objects with PptxGenJS. Antigravity CLI uses the same portable authoring engine and image client. Claude's own image understanding is separate from photo/illustration generation; see [Anthropic's explanation](https://support.claude.com/en/articles/9002504-can-claude-produce-images).

The helper saves actual image bytes, prompt, provider/model and hashes in a new output directory. It does not follow redirects, retry paid requests automatically, log server response bodies, or mark the returned draft as visually inspected. A blocked or text-only response is reported as a failure. The agent offers setup/retry or no-API mode and does not switch silently. Gemini output does not guarantee a transparent alpha channel.

## Installation and verification

[Install the correct edition](installation.md). Environment details: [Claude](../ports/claude/paper-figure/references/claude-environment.md), [Antigravity CLI](../ports/antigravity/plugin/skills/paper-figure/references/antigravity-environment.md). The shared [mode-selection instructions](../ports/claude/paper-figure/references/image-options.md) define onboarding and delivery evidence.

The client has offline tests for request encoding, response decoding, failures, secret handling and output preservation. Antigravity CLI plugin validation and packaged portable-engine output are checked separately. A live paid Gemini image call and an end-to-end agent figure task are not claimed without such a run. See [validation record](portable-image-validation.json).

## 한국어 안내

스킬을 처음 사용하는 신규 figure 작업에서는 **Gemini API 활용 / API 없이 제작** 중 하나를 고릅니다. 이미 지정한 방식은 같은 작업에서 다시 묻지 않습니다.

API를 고르면 Google AI Studio의 키 발급 페이지를 안내하고, 사용자가 본인 터미널에서 `python3 scripts/gemini_image.py setup`으로 등록합니다. 키를 채팅에 보내지 않으며 프로젝트 밖 개인 설정 폴더에 저장합니다. API 키와 이미지 모델 접근 권한·요금은 Antigravity CLI 로그인과 별개입니다.

API 없이도 레퍼런스·배색·관계를 검토한 뒤 도형·텍스트·수식으로 바로 제작하고 저장된 PPTX를 검증합니다. 이미지 모델 초안을 만든 것처럼 표시하지 않으며, 새 사진 생성이 필요한 경우에는 제공된 이미지나 적절한 네이티브 표현을 활용합니다.

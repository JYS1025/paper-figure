# Image options for Claude and Antigravity CLI

Claude offers optional **Gemini API** drafting or direct native authoring without image generation. **Antigravity CLI uses its built-in `generate_image` first when available**, without separate Gemini API key registration for the account-authenticated host route. An explicitly chosen external API or direct-native route is also supported. Choices persist within the task; existing PPTX edits and supplied-image reconstruction do not repeat onboarding. See Google’s [built-in tool documentation](https://antigravity.google/docs/hooks#interaction-and-media) and [account/API authentication distinction](https://antigravity.google/docs/cli/install/).

| Mode | What happens | Required image access |
|---|---|---|
| Antigravity built-in | Generate and inspect a composition draft with the current session’s `generate_image`; rebuild native editable objects. | Host tool availability and account permissions/quota; no separate image API key for account login. |
| Gemini API | Generate and inspect a complete visual draft; rebuild native PowerPoint objects; generate needed illustrations separately. | A Google Gemini API key, model access and network access. API quota and billing apply. |
| Direct native, no image generation | Review references, color roles and scientific relationships, then author native shapes, labels, math and connectors directly. | None. Supplied images and native pictograms can still be used. |

All routes require the authoring dependencies and a saved-PPTX renderer for visual verification. No-API mode is a supported route, not an incomplete image-model workflow. It does not synthesize photographic assets or claim a generated draft.

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

The optional direct Gemini API client has its own credentials and quota. Its setup is not required for Antigravity’s built-in tool. See [Google's key guidance](https://ai.google.dev/gemini-api/docs/api-key). The selected prompt and explicitly chosen reference images are sent to Google; whole project folders are not uploaded. Network-restricted claude.ai/API containers may prevent calls even with a valid key.

## How the image step works

Claude plans the composition and calls the optional Gemini client. Google's image model returns the raster draft; Claude inspects it and writes native PowerPoint objects with PptxGenJS. Antigravity CLI uses its built-in image tool by default and the same portable authoring engine. It uses the included API client only when that route is selected. If the built-in tool is absent or fails, the agent explains the result and offers a fallback instead of silently switching providers. Claude's own image understanding is separate from photo/illustration generation; see [Anthropic's explanation](https://support.claude.com/en/articles/9002504-can-claude-produce-images).

The helper saves actual image bytes, prompt, provider/model and hashes in a new output directory. It does not follow redirects, retry paid requests automatically, log server response bodies, or mark the returned draft as visually inspected. A blocked or text-only response is reported as a failure. The agent offers setup/retry or no-API mode and does not switch silently. Gemini output does not guarantee a transparent alpha channel.

## Installation and verification

[Install the correct edition](installation.md). Environment details: [Claude](../ports/claude/paper-figure/references/claude-environment.md), [Antigravity CLI](../ports/antigravity/plugin/skills/paper-figure/references/antigravity-environment.md). The host-specific mode guides define onboarding and delivery evidence: [Claude](../ports/claude/paper-figure/references/image-options.md) and [Antigravity](../ports/antigravity/plugin/skills/paper-figure/references/image-options.md). Local preflight cannot discover the agent’s native image tools, and an absent optional API key does not prove native generation is unavailable.

The client has offline tests for request encoding, response decoding, failures, secret handling and output preservation. Antigravity CLI plugin validation and packaged portable-engine output are checked separately. A live paid Gemini image call and an end-to-end agent figure task are not claimed without such a run. See the [API-client validation record](portable-image-validation.json) and [Antigravity native-route correction](antigravity-native-image-validation.json). The latter checks guidance, packaging and offline key-independent preflight; it does not claim a live native image call.

## 한국어 안내

Claude의 신규 figure 작업에서는 **Gemini API 활용 / 이미지 생성 없이 직접 제작** 중 하나를 고릅니다. Antigravity는 현재 세션의 **내장 이미지 생성**을 우선 사용하며, 계정 로그인 경로에서는 별도 API 키를 등록하지 않습니다. 내장 기능을 사용할 수 없거나 별도 API를 선택한 경우에만 해당 설정을 안내합니다. 이미 지정한 방식은 같은 작업에서 다시 묻지 않습니다.

API를 고르면 Google AI Studio의 키 발급 페이지를 안내하고, 사용자가 본인 터미널에서 `python3 scripts/gemini_image.py setup`으로 등록합니다. 키를 채팅에 보내지 않으며 프로젝트 밖 개인 설정 폴더에 저장합니다. API 키와 이미지 모델 접근 권한·요금은 Antigravity CLI 로그인과 별개입니다.

이미지 생성 없이도 레퍼런스·배색·관계를 검토한 뒤 도형·텍스트·수식으로 바로 제작하고 저장된 PPTX를 검증합니다. 이미지 모델 초안을 만든 것처럼 표시하지 않으며, 새 사진 생성이 필요한 경우에는 제공된 이미지나 적절한 네이티브 표현을 활용합니다.

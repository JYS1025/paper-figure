# How image generation works in the Claude edition

The Claude skill is an authoring workflow, not a bundled image-generation service. Claude can inspect images and write the code that builds editable PowerPoint objects. An external image tool supplies the raster composition draft.

Anthropic distinguishes HTML/SVG diagrams from generated photos or illustrations in its [image-generation guidance](https://support.claude.com/en/articles/9002504-can-claude-produce-images). External tools are executed by the host application or integration; see [Anthropic's tool-use documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

## Default new-figure workflow

1. Claude records the scientific content, studies reference figures and chooses color roles.
2. Claude calls an available image-generation tool to produce the full composition draft. The integration must return an image Claude can inspect and save with the actual prompt.
3. Claude reviews that draft and records which visual decisions to transfer or correct.
4. Claude uses the bundled PptxGenJS helpers to build editable text, equations, shapes and connectors. Any needed pictorial assets are generated separately and remain replaceable picture objects.
5. A renderer opens the saved PPTX; Claude inspects the resulting preview and checks content, relationships and typography.

The tool may be exposed through the host, an MCP server, or an explicitly authorized API integration. Availability depends on that host and connection. This repository does **not** select or install a provider, supply credentials, or include a provider-specific client. Installing the skill alone does not enable step 2.

## What happens without an image connection?

| Request | Supported behavior |
|---|---|
| Create a new figure using the default workflow | Prepare the content, references and palette, then report the missing image capability before native construction. |
| Explicitly skip image drafting | Build native objects and record that the image-first stage was waived. This does not become evidence that an image draft was generated. |
| Reproduce an image supplied by the user | Inspect the supplied image and follow the exact-reconstruction route. Preserve native editability where required. |
| Make a local edit to an existing PPTX | Preserve the latest file and modify the requested objects; a new composition draft is not normally needed. |

Writing an SVG or HTML sketch does not satisfy the default image-model drafting step. Likewise, an image created outside the session can be a supplied reference, but should not be described as a tool call that occurred in the session.

## Installation and verification boundary

The [installation guide](installation.md) installs the skill. The [Claude environment guide](../ports/claude/paper-figure/references/claude-environment.md) describes the public authoring dependencies and renderers. `scripts/preflight.mjs` checks those local dependencies; it cannot check a host's MCP connections or image-provider access.

The repository validates the Claude authoring engine and its output checks locally. It does not claim a complete Claude Code or claude.ai run with an external image provider. The new masked-image and graph-pooling gallery examples were produced in Codex.

## 한국어 요약

Claude 자체의 이미지 이해 기능과 이미지 생성 모델은 다릅니다. 현재 Claude 스킬은 **외부 이미지 도구로 초안을 생성하고 → Claude가 이를 검토한 뒤 → PptxGenJS로 편집형 PPTX를 만드는 구조**입니다. 저장소에는 이미지 서비스 연결이나 인증 설정이 포함되어 있지 않습니다.

외부 도구가 없으면 기본 신규 제작 과정은 준비 단계 후 필요한 연결을 안내하고 멈춥니다. 사용자가 명시적으로 초안을 생략하도록 요청했거나, 재현할 이미지를 직접 제공한 경우에는 해당 경로로 제작할 수 있습니다. 기존 PPTX의 부분 수정은 보통 새 이미지 초안 없이 처리합니다.

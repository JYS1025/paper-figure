# Image workflows by host

Start with the host’s default workflow; no external-service selection or registration question is part of ordinary figure creation.

| Host | Default behavior |
|---|---|
| Codex | Generate and inspect a full composition with the available host image tool, then rebuild editable PowerPoint objects. |
| Antigravity CLI | Use the current session’s built-in image tool, inspect its draft, and reconstruct native objects. |
| Claude | Review references, palette and relationships, then author native editable objects directly. |

Retain a route the user already explicitly selected for the current task. A generic image request or failure of the current tool does not select a different provider. Explain missing capabilities accurately; use a supplied image or discuss an appropriate direct-native route when needed. Do not silently skip a required draft or claim that native drawings came from an image model.

Every route preserves editable explanatory text, formulas, shapes and connectors. Images remain independent, replaceable objects. Review the actual saved PPTX at the intended publication width; native object counts do not establish visual quality.

[Installation](installation.md) · [Claude environment](../ports/claude/paper-figure/references/claude-environment.md) · [Antigravity environment](../ports/antigravity/plugin/skills/paper-figure/references/antigravity-environment.md)

## 한국어 안내

Codex·Antigravity는 사용 가능한 내장 이미지 도구를 우선 사용합니다. Claude는 기본적으로 레퍼런스·배색 검토 후 편집 가능한 도형·텍스트로 직접 제작합니다. 일반 작업을 별도 서비스 선택이나 등록 질문으로 시작하지 않습니다.

사용자가 이미 명시한 방식은 같은 작업에서 유지합니다. 도구 실패나 단순한 이미지 제작 요청만으로 다른 제공자를 선택한 것으로 간주하지 않습니다. 실제 생성한 초안과 직접 제작한 도형을 구분하여 기록합니다.

# 논문 피규어 제작 도구 — 범위와 근거

2026-09-29. 새 빈 프로젝트에서 시작. 상위/프로젝트 경로에 적용되는 AGENTS.md 없음. 기존 파일 없음. Git 초기화·글로벌 설치·외부 게시를 하지 않는다.

## 목표

논문의 모델 구조·방법론·추상 설명 그림을 개별 편집 가능한 PPTX로 만든다. PowerPoint가 편집기다. AI가 내용과 게재 크기를 고려해 구도, 타이포그래피, 색, 간격을 결정하며, 프로그램은 의미 보존·연결·편집 가능성을 검사한다. 통계 차트, 발표 덱, 웹 편집기, 대형 DSL, 래스터 그림을 넣은 PPT는 이 단계의 대상이 아니다.

## 구현 단계

A. 실제 export/reopen probe → B. 최소 제작 요소 및 참고 카드 → C. 재사용 스킬과 생성·검사·부분 수정 → D. 8개 과제의 기능·시각·편집 검증 → E. MCP 필요성 판단.

배포물은 로컬 스킬, 네이티브 PPTX 예제, 실제 파일의 재렌더링 PNG, 검증 기록, 사용법이다. 별도 모델 실험을 수행하지 않았다면 성능 향상을 주장하지 않는다. 별도 에이전트 생성은 요청받지 않았으므로 사용하지 않는다.

## 연구의 근거와 한계

- [AutoPresent, CVPR 2025](https://arxiv.org/html/2501.00912v2), [코드](https://github.com/para-lost/AutoPresent): PPTX를 유지하면서 SlidesLib로 평균 생성 코드를 170→13줄로 줄였다. 표3 detailed instructions + images, GPT-4o의 layout은 53.7→70.5, executability는 89.2%→86.7%. 레이아웃 점수는 모델 평가이며 실행 가능한 결과를 대상으로 한다. 모든 지표가 좋아졌다는 결론은 잘못이다. 지시·코드·렌더링을 함께 보고 반복 개선하는 방법을 참고했다.
- [PPTAgent, EMNLP 2025](https://aclanthology.org/2025.emnlp-main.728/), [PDF](https://aclanthology.org/2025.emnlp-main.728.pdf): 표7 Qwen full은 성공률95.0%, design3.27; w/o CodeRender는 74.6%, 3.34. 생성 안정성의 근거로 해석한다. 미관 향상 증명으로 해석하지 않는다. Guo et al. 방식으로 교체한 대조군으로, raw XML vs HTML만 통제한 실험이 아니다.
- [PaperBanana, 2026 preprint](https://arxiv.org/html/2601.23265v1): 참고 선택→계획→스타일링→렌더링→비평의 흐름을 참고했다. 스타일링 중 기술 내용이 빠질 수 있으므로 내용 검사를 따로 둔다. 방법론 그림은 래스터 출력이며 편집 어려움이 한계다. 출력 방식을 그대로 채택하지 않는다.

이 논문들은 논문 구조도용 네이티브 PPT의 유효성을 직접 검증하지 않았다. PPTX 형식 자체가 디자인 문제의 원인이라는 증거도 여기서 얻을 수 없다. 작은 보조 도구와 시각 피드백이 도움이 될 것이라는 설계 가설이며 이 프로젝트 결과로 검증해야 한다.

## 구현 참고

- 이 환경의 Presentations 스킬: Artifact Tool JS, 96dpi CSS px와 pt 구분, export/import 검증. 일반 덱의 16:9·큰 글자 기본값 대신 논문 폭을 사용한다.
- [Anthropic PPTX skill](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md): 내용/시각/수정 전후 비교의 아이디어만 참고. 코드를 복제하지 않았다.
- [K-Dense scientific-schematics](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/skills/scientific-schematics/SKILL.md): 명시적인 구성요소·관계·라벨을 참고. PNG 의존성을 가져오지 않았다.
- [공식 스킬 문서](https://developers.openai.com/codex/skills), [평가 방법](https://developers.openai.com/blog/eval-skills): 짧은 진입점, 필요한 상세 자료, 실제 실행 결과와 단계별 검증을 사용한다.

## 최초 호환성 발견

번들 26.905.11957의 Artifact Tool 시험에서 첫 도형 `input`의 cNvPr ID가 1→7로 export되었으나 stCxn은 1을 참조해 dangling endpoint가 생겼다. 재import 렌더링에서 선이 사라졌다. head 옵션은 OOXML headEnd(출발점), tail 옵션은 tailEnd(도착점)에 대응했다. 목적지 화살표에는 tail을 사용한다.

`pptx.py prepare`는 새 파일에 한해 manifest 이름으로 실제 ID를 다시 연결한다. 추측으로 첫 ID를 고치지 않는다. 모호한 이름은 오류다. native grpSp를 조립하고 noGrp 잠금을 해제한다. 기존 사용자 파일에는 prepare를 쓰지 않는다. 이 발견은 일반적인 모든 PPTX 또는 다른 버전의 Artifact Tool 문제로 일반화하지 않는다.

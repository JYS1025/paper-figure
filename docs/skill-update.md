# paper-figure 스킬 업데이트

## 전체 이미지 초안 → 네이티브 재구성을 필수로 고정 — 2026-10-01

사용자의 명시적인 요청에 따라, 새 figure 및 전체 구도 재설계의 제작 순서를 **이미지 모델로 전체 시각 초안 생성 → 실제 초안 검토·재구성 계획 → 편집형 PPTX 제작 → 저장된 출력과 초안 비교·검증**으로 고정했습니다. 이 변경은 제작 방식에 대한 요구를 반영하며, 특정 방식의 시각적 우위가 새로 입증되었다는 뜻은 아닙니다.

- [스킬 진입점](../skills/paper-figure/SKILL.md)에 필수 순서와 완료 조건을 직접 명시하고, [전체 초안 지침](../skills/paper-figure/references/image-first.md)을 새 제작 전에 읽도록 연결했습니다.
- 아이콘만 생성하기, 이전 과제의 초안을 가져오기, PPTX를 먼저 만든 뒤 이미지를 생성하기는 이 단계를 충족하지 못합니다. 실제 프롬프트·선택 초안·제작 전 재구성 결정·저장된 출력과의 비교 기록을 남기고 초안도 결과와 함께 연결합니다.
- 전체 초안에는 구도를 검토하기 위한 글자·수식·화살표가 보일 수 있습니다. 최종 설명 객체는 내용 명세에서 다시 네이티브로 작성하며, 전체 초안을 배경이나 숨겨진 그림으로 넣지 않습니다. 삽입용 아이콘·삽화는 별도 생성 단계로 유지합니다.
- [작성](../skills/paper-figure/references/authoring.md), [시각 설계](../skills/paper-figure/references/visual-design.md), [시각 자료](../skills/paper-figure/references/visual-assets.md), [검토](../skills/paper-figure/references/review-and-editing.md)의 상충되던 안내를 함께 수정했습니다. 도구 예제만 실행하는 것은 전체 제작 흐름을 완료한 것으로 간주하지 않습니다.
- 최신 PPTX의 라벨·색상 등 국소 수정은 기존 원본 보존 절차를 유지합니다. 사용자가 초안을 명시적으로 생략하도록 하거나 제공한 래스터의 정확한 재구성을 요구하면 그 경로를 사실대로 기록합니다. 이미지 생성이 막히면 직접 제작으로 조용히 대체하지 않습니다.

직전 [센서 보정 샘플](../output/pictogram-math-test-09/report.txt)과 [교차로 새 과제](../output/unseen-crossing-10/report.txt)는 전체 이미지 초안 없이 아이콘만 생성했던 실행입니다. 이력을 변경하거나 새 필수 흐름을 검증한 사례로 재분류하지 않았습니다. 이번 변경은 지침·참조 연결·배포 패키지를 검증하며, 추가 figure 생성이나 블라인드 평가는 포함하지 않습니다. [검증 기록](validation/required-image-draft-11/package-check.json).

## 아이콘 추상화와 수식 출력 검증 — 2026-09-30

원본 논문 figure와 현재 결과를 비교한 [분석 기록](validation/icon-math-audit-07/audit.json)을 재사용 가능한 지침과 읽기 전용 검증 도구로 반영했습니다. 이번 작업은 스킬 개선이며 기존 figure는 수정하지 않았습니다.

| 확인한 원인 | 반영한 변경 |
|---|---|
| 입력 종류를 나타내는 작은 아이콘에 제품 렌더링·재질 묘사를 요구함 | 개념·기능 표시는 단순한 픽토그램을 우선 검토하고, 실제 관측·장비 외형이 중요한 경우에는 사진·상세 삽화를 사용하도록 구분했습니다. 생성 프롬프트 예시와 최종 크기 검토 기준을 추가했습니다. |
| 유니코드 첨자와 서로 다른 수동 첨자 형식을 혼용함 | 같은 수식 계열의 글꼴·크기·기준선·기호 스타일을 하나의 검증된 방식으로 유지하도록 했습니다. 일반 변수, 설명용 첨자, 연산자의 역할과 원고 규약을 구분합니다. |
| 이미 줄인 글자에 첨자 처리를 적용해 최종 출력에서 더 작아짐 | 첨자 글자 크기와 기준선 처리를 함께 검증하며, 출력 엔진의 자동 축소와 수동 축소를 중복 적용하지 않도록 안내합니다. 관찰된 비율을 모든 프로그램에 적용하는 상수로 만들지 않습니다. |
| PPTX의 Arial 선언만 확인해 실제 출력의 글꼴 대체를 놓침 | 최종 PDF의 실제 글꼴, 문자별 크기, 내용 누락을 선택한 수식 영역에서 검사하는 `typography_audit.py`를 추가했습니다. |

새 [수식 조판 지침](../skills/paper-figure/references/math-typography.md)을 진입점·작성·검토 지침에 연결했습니다. [시각 자료 지침](../skills/paper-figure/references/visual-assets.md)과 [참고 사례](../skills/paper-figure/references/reference-cards.md)에는 BLIP-2·Flamingo·RLDX-1·CLIP·DiT의 관찰을 추가했습니다. 모든 논문이 같은 아이콘이나 서체를 사용한다는 규칙으로 일반화하지 않았습니다. 수식·다이어그램·라벨의 native 편집성은 유지해야 합니다.

검증 도구는 사용자가 정한 영역·예상 문자·허용 글꼴·최소 크기 기준으로 진단합니다. 게재 폭을 반영하고, PDF 해시가 달라지거나 출력 경로가 원본을 덮어쓰면 거부합니다. 그림의 품질 점수나 합격 판정을 내리지는 않습니다. 글자가 추출되지 않는 영역과 일부 문자 누락도 검토 대상으로 남깁니다.

기존 공간 집계 PDF에서 4.089pt 첨자와 5.2pt 합계식 인덱스를, 센서 융합 PDF에서 `ₖ`의 Linux Libertine 대체를 재현해 표시했습니다. [공간 집계 검사](validation/icon-math-skill-update-08/spatial-audit.json), [센서 융합 검사](validation/icon-math-skill-update-08/temporal-audit.json). 예시에 적용한 6pt·상대 크기 0.60은 이번 검토용 기준이며 출판사 표준이 아닙니다.

[새 회귀 검사 10개](validation/icon-math-skill-update-08/tests.log)가 통과했습니다. 실제 결함 검출, 게재 폭에 따른 크기 변화, 누락 문자, 빈 영역, 경계 밖 문자, 오래된 파일 거부, 원본 보존을 확인했습니다. 스킬 형식·내부 링크·배포 ZIP의 원본 일치 결과는 [패키지 검증](validation/icon-math-skill-update-08/skill-package.json)에 기록합니다. 이 검증은 지침과 진단 도구에 관한 것이며 새 figure의 품질 향상이나 PowerPoint 직접 편집을 시험한 결과는 아닙니다.

## 생성 이미지·아이콘과 편집형 설명의 분리 — 2026-09-30

사용자가 지적한 문제는 이미지 모델을 사용했더라도 최종 결과에서 시각 자료를 모두 도형으로 바꿔 버린다는 점이었습니다. 스킬의 기본 안내를 **필요한 이미지·아이콘은 생성해 삽입하고, 텍스트·수식·상태 표시·다이어그램·화살표는 native 객체로 작성**하는 방식으로 수정했습니다. [시각 자료 제작·삽입 지침](../skills/paper-figure/references/visual-assets.md)을 추가했습니다.

생성 프롬프트에는 텍스트·축·화살표·다이어그램을 제외하도록 명시합니다. 투명 배경과 일관된 스타일을 사용하고, 각 이미지는 독립된 picture로 저장합니다. `nativeOnly:false`를 사용할 때에는 허용한 이미지의 이름·개수·원본 일치를 따로 확인하도록 했습니다. 생성한 이미지를 최종 PPTX에 실제로 넣지 않은 결과는 삽입 시험의 성공으로 취급하지 않습니다.

기존 래스터 참조를 재구성하는 [참고 이미지 변환 지침](../skills/paper-figure/references/image-first.md)도 이 구분에 맞춰 정리했습니다. 편집성을 위해 사진·삽화·아이콘까지 모두 단순 도형으로 대체하거나, 그림 개수 0개를 품질 지표로 삼지 않습니다. 이미지 내부 픽셀과 native 설명 객체의 편집 가능성도 구분해 설명합니다.

[적용 예시](../output/hybrid-assets-test-06/report.md)는 저장된 센서 융합 PPTX에 새로 생성한 카메라·관성 센서 아이콘 두 개를 독립 객체로 삽입합니다. 기존 예시 파일은 보존하고, 생성 원본과 프롬프트를 함께 제공합니다.

## 라벨 공개 평가 피드백과 새 과제 생성 — 2026-09-30

[라벨을 유지한 블라인드 평가](../output/image-first-blind-test-04/report.md)의 남은 제안을 스킬에 반영했습니다. 결정 기호와 상태 표시는 그림 또는 인접 캡션에서 정의하고, 단독 사용 그림에는 필요한 정의를 포함합니다. 미측정·대기 상태와 음성·빈 상태가 게재 크기 및 흑백에서 구별되는지 확인합니다. 측정 후 채움 변화가 실제 물질 변화인지 판정 상태인지도 구분합니다.

검출과 작동 위치가 떨어져 있다는 이유만으로 시간 보정 모듈을 추가하지 않습니다. 지연 대응이 실제 방법에 명시되고 설명에 필요할 때만 어떤 시료·시각에 적용되는지 보여주도록 했습니다. 모든 화살표를 두껍게 만드는 규칙은 추가하지 않았습니다. 변경은 [관계 검토](../skills/paper-figure/references/relationship-review.md), [렌더링 검토](../skills/paper-figure/references/review-and-editing.md), [이미지 초안 변환](../skills/paper-figure/references/image-first.md)에 연결되어 있습니다.

새 주제 세 개를 작성하여 각각 새 맥락에서 이미지 초안과 편집형 PPTX를 만들도록 했습니다. 기존 액적 선별 예시와 평가 원문은 생성자에게 전달하지 않았습니다. 여기서 unseen은 이 프로젝트의 기존 생성 예시와 대화에 없는 과제라는 뜻이며, 모델 학습 데이터에 없다는 뜻은 아닙니다. [과제·실행 조건](validation/unseen-suite-05/session.json), [적용한 스킬 스냅샷](validation/unseen-suite-05/skill-snapshot.json), [배포 ZIP 검사](validation/unseen-suite-05/skill-package.json).

[새 과제 결과](../output/unseen-suite-05/report.md)에서는 시간 지연 보정, 공간 면적 집계, 비동기 실험 상태 전이를 다뤘습니다. 최초 생성 뒤의 렌더 검토에서 수식 인덱스의 literal underscore가 두 과제에 남아 있는 점을 확인해 native 아래첨자로 수정했습니다. 이 관찰을 [작성 지침](../skills/paper-figure/references/authoring.md)에 추가했습니다. 최초 생성에 사용한 스냅샷과 이 후속 보완이 포함된 최종 스냅샷은 구분해 보존합니다.

## 이미지 초안 → 편집형 PPTX 선택 경로 — 2026-09-30

이 절은 당시의 선택 경로 시험 기록입니다. 현재 적용 정책은 위 2026-10-01 필수 제작 절차로 변경되었습니다.

사용자의 아이디어를 실제 액적 선별 과제에 시험하고, [image-first 지침](../skills/paper-figure/references/image-first.md)을 선택 경로로 추가했습니다. 이미지 모델은 시각 구도의 참고 자료를 만들고, 원래 내용 명세는 과학적 의미의 기준으로 유지합니다. [시험 결과와 한계](../output/image-first-test-03/report.md), [초안](../output/image-first-test-03/image-draft.png), [재구성한 PPTX](../output/image-first-test-03/figure.pptx).

제어 단계 중복, 정의되지 않은 입자 표현, 불명확한 상태·출구 배색을 수정하면서 초안의 구도와 밀도를 참고했습니다. 최종 파일은 87개 native shape, 2개 native connector, 1개 group, picture 0개입니다. 필수 내용과 저장 연결 검사, 렌더링 검토를 수행했습니다. 이 방식의 시각적 우위에 관한 독립 블라인드 비교는 수행하지 않았으므로 기본 제작 경로를 강제로 대체하지 않습니다. [검토 기록](validation/image-first-test-03/result.json).

스킬 형식·내부 참조 검사 후 46개 파일을 포함한 배포 ZIP을 갱신했습니다. [패키지 검사](validation/image-first-test-03/skill-package.json).

## Color book 확장: 6 → 16개 — 2026-09-30

기존 6개 조합을 보존하고, 논문 10편의 원본 figure를 직접 시각 검토해 10개를 추가했습니다. [16개 전체 색상표](../output/color-books/color-books.png), [적용 예시와 근거를 담은 카탈로그](../skills/paper-figure/assets/color-books.html), [색상 선택 지침](../skills/paper-figure/references/color-books.md), [업데이트된 스킬 ZIP](../output/paper-figure-skill.zip)을 제공합니다.

| 추가한 조합 | 직접 검토한 원본 | 응용한 배색 원리 |
|---|---|---|
| Royal & Wheat | BLIP-2 Figure 1 | 진한 파랑·흰 글자의 backbone과 밝은 크림색 bridge |
| Periwinkle & Orchid | Flamingo Figure 3 | 고정된 모듈과 학습하는 모듈의 색을 반복해서 유지 |
| Pistachio & Rose | SAM 2 Figure 3 | 반복되는 기능 모듈의 연두·하늘·분홍 정체성 |
| Cyan & Lilac | Mask2Former Figure 2 | 시안 decoder·라일락 특징 평면·크림색 head의 대비 |
| Amethyst & Honey | RT-2 Figure 1 | 중립 배경 위 금색 언어 모듈·파란 시각 모듈·보라 출력 |
| Graphite & Ochre | DINOv2 Figure 3 | 회색 pool·황토색 curated seed·명시적인 빨간 제외 표시 |
| Celadon & Blush | Latent Diffusion Figure 3 | 표현 공간을 큰 녹색·분홍색 영역으로 구분 |
| Sky & Leaf | DiT Figure 3 | 회색 블록 내부에서 파랑·녹색·호박색 연산을 반복 |
| Olive & Copper | Mamba Figure 1 | 흰 배경 위 올리브·구리색 상태 경로와 파란 선택 경로 |
| Graphite & Silver | DINO Figure 2 | 회색 모델·흰 연산·짙은 관계선으로 설명하는 무채색 구성 |

각 항목에 원본 figure 링크와 실제 관찰을 기록했습니다. 원본에서 일부 역할을 선택하거나 강도를 조정한 응용 배색이며, HEX 값을 원본에서 추출했다는 의미는 아닙니다. 색의 이름뿐 아니라 넓은 면·진한 모듈·색 있는 경로·무채색 구조 등 배정 방식으로 선택하도록 지침을 확장했습니다. 카탈로그의 간단한 공통 구조는 배색 확인용이며 실제 연구 figure의 구조를 지시하지 않습니다.

- 전체 16개를 비교하는 색상표와 4개씩 담은 상세 시트, 개별 SVG, HTML 및 JSON을 재생성했습니다.
- 의도한 글자/면·경계/면·강조/면 조합의 대비 검사를 통과했습니다. 일반 글자/유색 면 최소 10.21:1, 경계/유색 면 최소 3.04:1, BLIP-2식 진한 모듈의 흰 글자 5.39:1입니다. [검사 결과](validation/color-books/contrast.json). 이는 국소 대비 검사이며 색각 접근성이나 전체 figure 품질 인증이 아닙니다.
- 색상·흑백 렌더링을 시각 검토하고, 스킬 형식·로컬 참조·기존 6개 데이터 보존·45개 배포 파일의 일치를 확인했습니다. [배포 검사](validation/color-books/package-check.json).
- HTML의 실제 브라우저 조작은 검증하지 않았습니다. 기존 연구 figure 수정이나 독립 검증모델의 품질 평가는 이번 범위에 포함하지 않았습니다.

## 이전 단계: Color book 6개 추가 — 2026-09-30

사용자의 요청에 따라 하나의 기본 배색 대신 6개 조합을 선택할 수 있게 했습니다. [색상 지침](../skills/paper-figure/references/color-books.md), [시각 카탈로그](../skills/paper-figure/assets/color-books.html), [전체 미리보기](../output/color-books/color-books.png), [RGB 데이터](../skills/paper-figure/assets/color-books.json)를 제공합니다.

- 세이지·라벤더 / 블루·살구 / 청록·코럴 / 플럼·샌드 / 모스·클레이 / 잉크·코발트.
- 각 색 계열에 면색·경계색·강조색을 따로 정의했습니다. 스킬은 그림의 의미에 맞춰 색을 배정하고, 기존 원고의 배색이 있으면 우선합니다.
- RLDX-1의 [Figure 2](https://arxiv.org/html/2605.03269v2/fig2_overview_rldx.png)와 [Figure 3](https://arxiv.org/html/2605.03269v2/fig3_overview_architecture.png)를 브라우저에서 직접 확인했습니다. Figure 2는 같은 라벤더로 세 스트림을 묶고, Figure 3은 민트·라벤더 계열을 큰 영역과 세부 토큰에서 다른 강도로 사용합니다. 이 원리를 참고한 직접 설계 값이며 원본 HEX의 추출본은 아닙니다.
- JSON에서 재생성하는 표준 Python 도구를 포함했습니다. 색상칩과 동일 구조의 적용 예시를 SVG·HTML로 보여주며, HTML에는 흑백 비교 기능이 있습니다.
- 여섯 조합의 색상 형식과 의도한 글자/면·경계/면·강조/면의 대비 검사를 통과했습니다. [검사 결과](validation/color-books/contrast.json). 모든 일반 글자/유색 면 조합의 최소 대비는 11.11:1, 경계/유색 면은 3.21:1입니다. 이 수치는 국소 대비 검사이며 색각 접근성이나 그림 전체의 품질 인증이 아닙니다.
- 렌더링한 전체 카탈로그를 색상·흑백으로 시각 검토했습니다. 스킬 형식과 로컬 참조 검사를 통과했고, 배포 ZIP의 30개 파일이 현재 스킬과 일치하는 것을 확인했습니다. [배포 검사](validation/color-books/package-check.json). HTML의 실제 브라우저 조작 검증은 로컬 파일 URL 제한으로 수행하지 못했습니다. 기존 연구 figure의 재색칠이나 새로운 독립 모델 품질 평가는 이번 범위에 포함하지 않았습니다.

## 이전 관계 검토 업데이트

2026-09-30. 사용자가 제공한 [블라인드 평가 피드백](validation/feedback-revision/user-feedback.txt)을 재사용 가능한 생성·검토 절차에 반영했습니다. 이번 변경 대상은 스킬이며, 예제 figure를 새로 만들거나 수정하지 않았습니다.

## 반영한 결정

| 관찰 | 스킬의 변경 |
|---|---|
| 얇은 화살표만으로 원인을 설명할 수 없음 | 선 두께보다 연결 대상·출발/도착 위치·집합 범위를 먼저 확인합니다. |
| ID 검사를 통과해도 선이 투명한 라벨 상자에 연결될 수 있음 | 저장된 PPTX의 실제 연결 대상과 좌표를 읽기 전용으로 진단합니다. 경고는 렌더링 검토 대상으로 취급하며 자동 품질 판정으로 쓰지 않습니다. |
| 전체 구조와 확대 영역, 선택 전후 항목, 두 입력과 행렬 축의 대응이 불명확 | 생성 전에 표현 단위·항목/집합 범위·정체성·확대 범위를 정의하고, 해당 구조가 있는 경우 추적 가능성을 확인합니다. |
| 단순한 개요도가 충분하거나 양쪽 품질이 비슷할 수 있음 | 비판 개수를 강제하지 않습니다. 구조 결함·조건부 설명 개선·마무리 조정을 구분하고 잘된 영역을 보존합니다. 정의되지 않은 연산을 추가하지 않습니다. |
| 유명한 논문 구도를 기억하면 출처를 쉽게 맞힐 수 있음 | 출처 정답률·구도 기억·시각적 품질을 분리합니다. 중립 프롬프트, 가린 정보의 범위, 평가자 맥락과 실제 실행 여부를 기록합니다. |
| 피드백의 대상이 스킬인데 예제 수정으로 작업이 빗나감 | 진행 중인 요청 범위에 따라 스킬 개선·figure 수정·리뷰를 구분하도록 진입점에 명시했습니다. |

## 적용 파일

- [스킬 진입점](../skills/paper-figure/SKILL.md)
- [생성 전 관계 설계와 저장 후 검토](../skills/paper-figure/references/relationship-review.md)
- [블라인드 평가 절차와 재사용 프롬프트](../skills/paper-figure/references/blind-review.md)
- [읽기 전용 연결 검사기](../skills/paper-figure/scripts/flow_audit.py)

기존 제작·시각 디자인·편집 검토·평가 지침도 이 절차를 참조하도록 정리했습니다. 특정 과거 실행에서 검증자를 사용할 수 없었다는 문구는 현재 실행의 권한·도구에 따라 판단하도록 바꿨습니다. 프로젝트의 `.agents/skills/paper-figure`가 실제 스킬 폴더에 연결되어 있어 수정 사항이 적용됩니다.

## 확인한 범위

- 스킬 형식 검증 통과. 내부 문서 링크와 배포 ZIP의 파일 일치 확인.
- [전체 테스트 로그](validation/skill-update/tests.log): 기존 28개와 새 연결 진단 7개, 총 35개 통과.
- 기존 두 파일을 읽은 진단: [투명한 연결 대상이 있는 파일](validation/skill-update/old-anchor-audit.json)에서는 6개 연결선이 검토 대상으로 표시됐고, [보이는 특징 평면에 연결한 파일](validation/skill-update/visible-anchor-audit.json)에서는 해당 경고가 없었습니다. 이는 미관에 대한 합격 판정이 아닙니다.
- 검사기의 원본 덮어쓰기 거부와 기존 `output` 내 PPTX·PNG 121개 보존을 확인했습니다. [패키지·보존 확인](validation/skill-update/package-check.json).

새 지침으로 figure를 재생성하거나 블라인드 평가를 다시 수행하지 않았습니다. 따라서 이번 검증은 지침의 형식·연결, 검사기의 동작과 기존 산출물 보존에 한정됩니다. 새 생성물의 품질 향상은 아직 측정하지 않았습니다.

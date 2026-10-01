# 제작 및 검토 기록

공간 spot의 원형 footprint가 세포 mask와 겹친 면적만큼 전체 count vector를 배분하는 예시 그림이다. S2의 벡터는 C1과 C2에 나뉘어 기여하고, S4는 C2 밖의 질량을 유지한다. S5는 두 출력에 모두 기여하지 않는다. 미할당 비중은 A 밖의 정렬 행으로 표시했으며 재정규화하지 않는다.

## 제작 경로

1. 브리프에서 내용 계약과 관계 계획을 먼저 작성했다. 마스크의 인접·비중첩, 다섯 spot의 배치, 2×5 가중치와 두 벡터 합을 명시했다.
2. [CLIP 원본 그림](https://arxiv.org/html/2103.00020v1/main-diagrams.png)을 브라우저에서 직접 시각 검토했다. 입력 identity를 행렬의 행·열에 일치시키는 원칙만 참고했다. 논문의 모듈 구도나 그림을 복사하지 않았다.
3. `blue-apricot` 색상 책을 골라 C1에 파랑, C2에 살구색, spot identity에 중립색 윤곽, 미할당 부분에 중립색 빗금을 배정했다.
4. built-in `image_gen`으로 실제 이미지 초안을 생성했다. 사용한 프롬프트는 `image-prompt.txt`, 선택한 원본 초안은 `image-draft.png`에 저장했다.
5. 초안의 큰 공간 예시 + 오른쪽 행렬 + 아래 출력식 구도를 native PowerPoint 객체로 재구성했다. Artifact Tool과 paper-figure Figure helper로 도형·텍스트·연결을 만들고, 수식 인덱스는 native DrawingML text run의 아래첨자로 정리했다. 전체 그림 raster/SVG, 숨긴 초안, 측정 heatmap을 넣지 않았다.
6. Presentations finalizer에서 package/layout/font 정책과 Artifact Tool 재가져오기를 확인했다. 최종 저장 PPTX를 독립된 profile의 번들 LibreOffice에서 PDF로 렌더링하고 Poppler로 PNG를 만들었다.

## 초안에서 유지·수정한 결정

- 유지: 공간 footprint를 가장 큰 시각 단서로 쓴 구도, 동일한 S1–S5 열 순서, C1/C2의 색상 대응, 외부 footprint 빗금, 하단 두 셀 벡터 식.
- 수정: 초안의 미할당 행은 A의 세 번째 셀 행처럼 읽힐 수 있어 A 경계 밖으로 분리했다. 빗금의 의미를 `Unassigned area` 범례로 정의했다.
- 수정: 두 번 반복되던 하단 벡터 합 표현은 한 번의 큰 식과 공통 count-vector 정의로 합쳤다. α/β는 symbolic이며 F도 미지정임을 명시했다.
- 수정: 첫 PPTX 렌더의 코드식 underscore 표기를 native 아래첨자로 바꾸었다. 공간 집합에서 A로 가는 화살표의 7 px 기울기를 수평으로 정리했다.
- 적응: 초안의 손그림 윤곽은 편집 가능한 단순 polygon으로 바꾸었다. S2의 공통 경계는 직선으로 만들어 두 마스크가 겹치지 않고 S2 disk만 양쪽에 걸쳐 있음을 분명하게 했다. 유기적인 곡선의 부드러움은 줄었지만 관계 의미는 유지했다.

## 최종 저장본 검사

- `pptx.py inspect --contract`: 통과. 필수 텍스트, A의 10개 원소, 5개 미할당 값, 출력 두 식, native 그룹, 방향성 연결을 확인했다.
- `flow_audit.py`: 연결 1개, rendered-review 경고 0개, 미검사 geometry 0개. 연결은 visible spatial frame과 visible matrix frame에 직접 붙는다.
- 최종 파일은 native shape 89개, native connector 1개, native group 7개, picture 0개이다. 행렬은 native table 객체가 아니라 각각 편집 가능한 텍스트·도형·선이다.
- SHA-256: `89ea5647c0406d8d488b9b6d5249b57de90267c515272454a8aad02c0d6f697b`.

## 시각 검토

최종 저장본의 전체 PNG(1344×860, 192 dpi), 게재 폭 대응 PNG(672×430, 96 dpi), 같은 크기의 흑백 PNG를 직접 보았다. 캔버스는 177.8×113.77 mm이다. 화면 픽셀만으로 물리적 출력 크기를 보증하지는 않으며 PDF를 100% 인쇄하면 지정 폭에 대응한다.

- S1/S3의 완전 할당, S2의 양쪽 mask 기여, S4의 외부 부분과 β, S5의 완전 미할당을 공간·행렬·출력식 사이에서 추적했다.
- C1/C2의 색은 흑백에서 비슷해지지만, 공통 경계와 C1/C2 라벨, 행·열 위치가 관계를 유지한다. 미할당 부분은 빗금으로 남는다.
- 최종 렌더에서 텍스트 잘림이나 의도하지 않은 겹침을 발견하지 못했다. A와 outside 행의 분리, 두 출력 벡터의 시각적 구분을 확인했다. 아래첨자는 본문보다 작으므로 전체 게재 폭으로 쓰는 것이 전제다.
- 자동 검사 통과는 구조 확인이며, 이 시각 검토나 미관 평가와 동일하지 않다. 독립 평가자의 미관 점수나 image-first 우월성 비교는 수행하지 않았다.

## 한계

실제 Microsoft PowerPoint 앱에서 클릭·편집·재저장하는 시험은 하지 않았다. 편집 가능성은 native OOXML 구조와 import 검사로 확인했으며, 프리뷰 렌더러는 번들 LibreOffice이다. 수식은 편집 가능한 일반 text run과 Unicode로 만든 것이며 OMML 수식 객체는 아니다. α와 β는 설명용 symbolic weight이고 footprint의 시각적 비율을 실측하거나 수치로 산출했다고 주장하지 않는다.

---
inclusion: always
---

# AI-DLC 실습 규칙

이 워크스페이스의 모든 개발 요청은 아래 절차를 따른다. 절차를 건너뛰고 나온 결과물은 무효로 본다.

## 0. 시작할 때

- 첫 응답에서 **`aidlc_status` 를 부른다.** 지금 어느 단계이고 무엇이 어긋나 있는지 여기서 다 나온다.
  `aidlc-docs/aidlc-state.md` 를 직접 열어 읽지 않는다. 없으면 만들고, 있으면 그 지점부터 이어간다.
- **사람이 말한 요구는 루트의 `spec.md` 에 옮겨 적는다.** 채팅에만 남기고 넘어가지 않는다.
  - **원문 그대로** 옮긴다. 정리 · 요약 · 번호 붙이기를 하지 않는다. 그 일은 STEP 03 의 `requirements.md` 가 한다.
  - 사람이 나중에 요구를 더 말하면 `spec.md` 에 **덧붙인다.** 앞에 적힌 것을 고치거나 지우지 않는다.
  - 요구가 아직 한 줄도 없으면 **거기서 멈추고 무엇을 만들지 묻는다.** 임의로 상상해 채우지 않는다.
- 코드나 문서를 만들거나 고치는 요청일 때, 응답 **첫 줄에 현재 위치**를 표시한다 — 예: `[INCEPTION · STEP 03 요구사항 분석 · 게이트 1 대기]`
- 단순한 질문·설명 요청("이 코드 뭐 하는 거야", "오타 고쳐줘")에는 이 절차를 적용하지 않고 그냥 답한다.
- 문서는 `aidlc-docs/` 아래 **단계별 폴더**에만, 실행 코드는 워크스페이스 루트에만 쓴다. 섞지 않는다.
- 산출물은 아래 위치에 만든다. 폴더가 없으면 만든다. **단계 폴더 밖에 문서를 흘리지 않는다.**

```text
aidlc-docs/
├── inception/
│   ├── requirements/
│   ├── user-stories/
│   ├── plans/
│   └── application-design/
├── construction/
│   ├── {단위이름}/
│   │   ├── functional-design/
│   │   ├── nfr-requirements/
│   │   ├── nfr-design/
│   │   ├── infrastructure-design/
│   │   └── code/
│   ├── plans/
│   └── build-and-test/
├── aidlc-state.md
├── audit.md
└── mistakes.md
```

| 폴더 | 들어가는 것 |
|---|---|
| `inception/requirements/` | `requirement-verification-questions.md` · `requirements.md` |
| `inception/user-stories/` | `stories.md` · `personas.md` |
| `inception/plans/` | 단계별 계획 파일 (`execution-plan.md` 등) |
| `inception/application-design/` | `components.md` · `unit-of-work.md` |
| `construction/{단위이름}/` | 단위 하나의 설계 문서. 단위마다 폴더 하나 |
| `construction/{단위이름}/code/` | 코드 **요약만**. 실제 코드는 루트 `src/` |
| `construction/plans/` | `{단위이름}-{단계}-plan.md` |
| `construction/build-and-test/` | `build-and-test-summary.md` |

  `aidlc-state.md` · `audit.md` · `mistakes.md` 세 개만 `aidlc-docs/` 바로 아래에 둔다.

## 1. INCEPTION — 일곱 단계

계획 파일은 모두 `inception/plans/` 안에, 산출물은 `inception/` 아래 단계 폴더에 둔다.
아래 이름을 그대로 쓴다 — 지어내지 않는다.

| STEP | 단계 | 실행 | 계획 파일 | 남는 것 |
|---|---|---|---|---|
| 01 | 워크스페이스 파악 | 항상 · 게이트 없음 | 없음 | 루트 `spec.md` · `aidlc-state.md` 갱신 |
| 02 | 기존 코드 역분석 | 조건 | 없음 | — (이 실습은 건너뜀) |
| 03 | 요구사항 분석 | 항상 | 없음 — 질문 파일이 대신한다 | `requirements/requirement-verification-questions.md` → `requirements/requirements.md` |
| 04 | 유저 스토리 | 조건 | `story-generation-plan.md` | `user-stories/stories.md` |
| 05 | 실행 계획 수립 | 항상 | `execution-plan.md` | `execution-plan.md` 자체가 산출물 |
| 06 | 애플리케이션 설계 | 조건 | `application-design-plan.md` | `application-design/components.md` |
| 07 | 작업 단위 쪼개기 | 조건 | `unit-of-work-plan.md` | `application-design/unit-of-work.md` |

- 이 실습은 **빈 폴더에서 시작한다.** 읽을 기존 코드가 없으므로 STEP 02는 건너뛴다 — 건너뛴다는 사실만 한 줄로 밝히면 된다.
- 조건 단계를 건너뛸 때는 **왜 건너뛰는지 한 줄로 밝히고 동의를 받는다.** 조용히 건너뛰지 않는다.

### STEP 01 · 02 는 게이트를 돌지 않는다

- STEP 01 은 세 가지까지다 — 폴더 훑기, 사람이 말한 요구를 `spec.md` 에 옮겨 적기, `aidlc-state.md` 채우기.
  승인을 묻지 않고 바로 STEP 03 으로 간다.
- STEP 02 도 건너뛴다는 한 줄만 남기고 지나간다.
- **게이트가 처음 도는 곳은 STEP 03 이다.**

### STEP 03 은 이렇게 한다

- `requirements.md` 는 `.kiro/templates/requirements.md` 의 **섹션 제목과 번호 체계를 그대로** 쓴다. `{ }` 안만 채운다.
- **`spec.md` 를 읽고 시작한다.** 채팅 기억이 아니라 이 파일이 근거다.
- 질문은 **`spec.md` 에 없는 것만** 묻는다. 이미 적힌 것을 다시 묻지 않는다.
- `requirements.md` 는 `spec.md` 를 정리한 결과다. `spec.md` 에 없는 요구를 새로 만들어 넣지 않는다.
- 템플릿의 `Intent Analysis` 표를 먼저 채운다. 여기서 정한 `Complexity` · `Requirements Depth` 가 STEP 05 에서 조건 단계를 판정하는 근거가 된다.

## 2. 단계마다 도는 방식 — 게이트 두 개

`계획 → 질문 → [게이트 1 · 계획 승인] → 생성 → [게이트 2 · 결과 승인]`

- **계획** — 무엇을 할지 체크리스트로 먼저 적고 **파일로 남긴다.**
  파일 이름은 §1 · §3 의 `계획 파일` 칸에 적힌 것을 쓴다. 대화창에만 적고 넘어가지 않는다.
- **질문** — 모호한 곳은 **파일 안에** 묻는다. 채팅으로 묻고 끝내지 않는다.
  - 요구사항 분석은 `inception/requirements/requirement-verification-questions.md` 에, 나머지 단계는 그 단계의 계획 파일 안에 넣는다.
  - **객관식**으로 묻고, **마지막 선택지는 항상 `Other`** 로 둔다.
  - 형식 — `A) …` `B) …` … 마지막 줄 `E) Other (please describe after [Answer]: tag below)`, 그 아래 빈 `[Answer]:`.
  - 한 질문에 하나만 고르게 한다. 서술형으로 묻지 않는다.
  - 답이 "적당히 · 섞어서 · 잘 모르겠다 · 복잡도에 따라" 류면 **되묻는다.**
- **게이트 1** — 계획 파일과 질문 파일을 보여주고 승인을 묻는다. 계획 파일이 없는 단계(STEP 03)는 질문 파일만 보여준다.
- **생성** — 게이트 1 과 2 사이에는 사람에게 되묻지 않고 끝까지 만든다.
- **게이트 2** — 만든 결과를 보여주고 승인을 묻는다. 그 단계에 쌓인 실수 줄 수를 함께 보고한다.

두 게이트 모두 아래를 지킨다.

- 반드시 **두 갈래로만** 묻는다 — `1) 수정 요청   2) 다음 단계로`. 세 번째 선택지를 만들지 않는다.
- 묻기 **직전**에 물음 원문을, 답을 받은 **직후**에 답 원문을 `aidlc-docs/audit.md` 에 덧붙인다.
- **승인 없이 다음 단계로 넘어가지 않는다. 승인 없이 코드를 만들지 않는다.**

게이트 2 직후 `aidlc-docs/aidlc-state.md` 를 갱신한다 — 현재 위치, 그 단계 체크(`[x]`), 남긴 파일 이름.
단계 이름과 순서는 고치지 않는다. 상태 칸만 채운다.

## 3. CONSTRUCTION — 여섯 단계

계획 파일은 `construction/plans/` 에, 산출물은 단위별 폴더 `construction/{단위이름}/` 에 둔다.

| STEP | 단계 | 실행 | 계획 파일 (`plans/`) | 남는 것 (`{단위이름}/`) |
|---|---|---|---|---|
| 01 | 기능 설계 | 조건 | `{단위이름}-functional-design-plan.md` | `functional-design/` — `business-logic-model.md` · `business-rules.md` · `domain-entities.md` · `frontend-components.md` |
| 02 | 비기능 요구 | 조건 | `{단위이름}-nfr-requirements-plan.md` | `nfr-requirements/` — `nfr-requirements.md` · `tech-stack-decisions.md` |
| 03 | 비기능 설계 | 조건 | `{단위이름}-nfr-design-plan.md` | `nfr-design/` — `nfr-design-patterns.md` · `logical-components.md` |
| 04 | 인프라 설계 | 조건 | `{단위이름}-infrastructure-design-plan.md` | `infrastructure-design/` — `infrastructure-design.md` · `deployment-architecture.md` |
| 05 | 코드 생성 | 항상 | `{단위이름}-code-generation-plan.md` | 코드는 루트 `src/` 에, **요약만** `code/` 에 |
| 06 | 빌드와 테스트 | 항상 | `build-and-test-plan.md` (단위 이름 없음) | `construction/build-and-test/build-and-test-summary.md` |

- **STEP 01~05 는 단위마다, STEP 06 은 단위 전부를 합쳐 한 번** 돈다.
- `application-design/unit-of-work.md` 의 단위 **하나를 STEP 05 까지 끝내고** 다음 단위로 간다. 여러 단위를 동시에 벌리지 않는다.
- 각 STEP 은 §2 의 게이트 두 개를 그대로 따른다.
- 조건 단계를 돌릴지는 INCEPTION STEP 05(실행 계획)에서 판정한다. 거기서 정한 대로 하고, 바꾸려면 사유를 밝히고 동의를 받는다.
- **기술 스택은 STEP 02 에서만 고른다.** 언어 · 프레임워크 · 런타임을 정하는 곳은 `nfr-requirements/tech-stack-decisions.md` 한 곳뿐이다.
  - INCEPTION 의 요구사항 · 설계 단계에서는 고르지 않는다. 요구명세가 못 박은 제약만 `requirements.md` §3 에 옮겨 적는다.
  - STEP 01(기능 설계)도 업무 규칙과 데이터 구조까지만 정한다.
  - 요구사항이 다 모인 뒤 **실제로 만들기 직전에** 고르는 것이 이 단계의 목적이다.
- STEP 05 에서 만드는 순서는 **업무 규칙 → API → 저장 → 화면**이고, 층마다 테스트를 같이 만든다.
- 계획 체크리스트는 작업을 끝낸 **그 응답에서 바로** `[x]` 로 바꾼다. 나중에 몰아서 하지 않는다.

## 4. 기록 — `aidlc-docs/audit.md`

- **덧붙이기만** 한다. 파일 전체를 다시 쓰는 도구·명령을 쓰지 않는다.
- 남길 것: 사용자 입력 **원문**, 승인 질문과 답변, 단계 시작·종료.
- 요약하거나 다듬지 않는다. 시각은 `date "+%Y-%m-%d %H:%M"`으로 얻어 적는다.

## 5. 실수 기록 — `aidlc-docs/mistakes.md`

아래 네 경우에는 **묻지 않고 바로** 한 줄 덧붙인다. 덧붙이기만 하고 지우지 않는다.

1. 게이트에서 "수정 요청"이 돌아왔을 때 — 무엇이 어긋났는지
2. 확정된 요구사항·설계와 다르게 만들어 되돌렸을 때
3. 이 문서의 규칙을 어겼을 때 (승인 없이 진행, 산출물 위치 오류, 게이트에 선택지 3개 등)
4. 빌드·테스트 실패의 원인이 앞 단계 누락으로 드러났을 때

형식은 한 줄:

`| 시각 | 단계 | 주체 | 무엇이 잘못됐나 | 왜 | 다음엔 |`

- **주체**는 `AI` 또는 `사람`. 애매하면 `AI`로 적는다. 변명을 쓰지 않는다.
- 사용자가 "이거 틀렸어" 류로 지적한 것도 기록 대상이다.
- 같은 실수가 반복되면 그 줄 끝에 `(반복 N회)`를 붙이고, 이 문서에 규칙을 보완하자고 제안한다.
- **게이트 2에서 그 단계에 쌓인 실수 줄 수를 함께 보고한다.**

## 6. 도구 — 손으로 쓰지 않는다

기록 파일 네 개는 **`aidlc` MCP 도구로만** 건드린다. 편집기로 열어 고치지 않는다.
도구에는 덮어쓰는 기능이 아예 없다. 그래서 §4 · §5 를 어기는 것이 구조적으로 불가능하다.

| 할 일 | 도구 | 언제 |
|---|---|---|
| 지금 어디까지 왔나 보기 | `aidlc_status` | 세션 시작, 게이트 묻기 전, 사람이 물을 때 |
| 규칙 위반만 보기 | `aidlc_check` | 게이트 묻기 직전 |
| 사람이 말한 요구 옮겨 적기 | `aidlc_spec_append` | STEP 01, 그리고 요구가 추가될 때마다 |
| 게이트 질문 남기기 | `aidlc_gate_ask` | 묻기 **직전** |
| 사람 답 남기기 | `aidlc_gate_answer` | 답 받은 **직후** |
| 실수 한 줄 남기기 | `aidlc_mistake` | §5 의 네 경우. 묻지 않고 바로 |
| 상태판 갱신 | `aidlc_state` | 게이트 2 **직후** |
| 단계 커밋 | `aidlc_snapshot` | 상태판 갱신 뒤. 커밋 하나가 단계 하나 |

- `spec.md` · `audit.md` · `mistakes.md` · `aidlc-state.md` 에 **파일 쓰기 도구를 쓰지 않는다.**
- 게이트를 물 때는 `aidlc_check` → `aidlc_gate_ask` 순서다. 위반이 남은 채로 승인을 묻지 않는다.
- `aidlc_gate_answer` 가 "수정 요청이다"라고 알려주면 곧바로 `aidlc_mistake` 를 부른다.
- **도구가 안 보이면 거기서 멈추고 사람에게 알린다.** 손으로 대신 쓰지 않는다.

## 7. 하지 않는 것

- `requirements.md` 확정 전에 코드 파일을 만들거나 고치지 않는다.
- `aidlc-docs/` 안에 실행 코드를 넣지 않는다.
- 산출물을 단계 폴더 밖에 만들지 않는다 — `aidlc-docs/` 바로 아래는 상태판·기록·실수 기록 세 개뿐이다.
- **`spec.md` 를 정리하거나 요약하지 않는다.** 사람이 말한 원문이 남아 있어야 한다.
- **`requirements.md` 나 설계 문서에 언어 · 프레임워크를 못 박지 않는다.** 요구명세가 지정한 것이 아니라면 CONSTRUCTION STEP 02 까지 미룬다.
- 규칙과 숫자를 한 파일에 섞지 않는다 — 규칙 파일에 수치를 박지 않고, 데이터 파일에 규칙을 넣지 않는다.
- `audit.md`와 `mistakes.md`를 덮어쓰지 않는다.
- **기록 파일 네 개를 파일 쓰기 도구로 고치지 않는다.** §6 의 도구만 쓴다.

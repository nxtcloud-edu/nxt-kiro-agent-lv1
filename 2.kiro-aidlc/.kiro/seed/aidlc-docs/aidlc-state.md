# 지금 어디까지 왔나

**상태판이다.** 단계 이름과 순서는 고치지 않는다. 상태·메모·현재 위치만 갱신한다.
갱신 시점은 각 단계의 **게이트 2(결과 승인) 직후**.

## 현재 위치

- 단계 — (아직 시작 안 함)
- 다음에 할 일 — 무엇을 만들지 말한다 (`spec.md` 에 쌓인다)
- 마지막 갱신 — —

## 단계는 이렇게 돈다

`계획 → 질문 → [게이트 1 · 계획 승인] → 생성 → [게이트 2 · 결과 승인]`

승인은 단계마다 두 번. 게이트 1과 2 사이에는 사람이 안 봐도 된다.

**STEP 01·02 는 게이트를 돌지 않는다. 첫 승인은 STEP 03 에서 나온다.**

## INCEPTION — 무엇을 만들지 정한다

| | STEP | 단계 | 상태 | 남은 것 |
|---|---|---|---|---|
| [ ] | 01 | 워크스페이스 파악 | 게이트 없음 | 루트 `spec.md` · `aidlc-state.md` |
| — | 02 | 기존 코드 역분석 | 건너뜀 · 빈 폴더에서 시작 | — |
| [ ] | 03 | 요구사항 분석 |  | `inception/requirements/requirements.md` |
| [ ] | 04 | 유저 스토리 |  | `inception/user-stories/stories.md` |
| [ ] | 05 | 실행 계획 수립 |  | `inception/plans/execution-plan.md` |
| [ ] | 06 | 애플리케이션 설계 |  | `inception/application-design/components.md` |
| [ ] | 07 | 작업 단위 쪼개기 |  | `inception/application-design/unit-of-work.md` |

## CONSTRUCTION — 어떻게 만들지 정한다

STEP 01~05 는 **작업 단위마다**, STEP 06 은 단위 전부를 합쳐 **한 번**.
조건 단계를 돌릴지 말지는 INCEPTION STEP 05(실행 계획)에서 판정한다.

단위별 폴더는 `construction/{단위이름}/`. 아래 경로는 그 폴더 기준.

| STEP | 단계 | 실행 | 남는 것 |
|---|---|---|---|
| 01 | 기능 설계 | 조건 | `functional-design/` — business-logic-model · business-rules · domain-entities · frontend-components |
| 02 | 비기능 요구 | 조건 | `nfr-requirements/` — nfr-requirements · tech-stack-decisions |
| 03 | 비기능 설계 | 조건 | `nfr-design/` — nfr-design-patterns · logical-components |
| 04 | 인프라 설계 | 조건 | `infrastructure-design/` — infrastructure-design · deployment-architecture |
| 05 | 코드 생성 | 항상 | 코드는 루트 `src/` 에, 요약만 `code/` 에 |
| 06 | 빌드와 테스트 | 항상 · 마지막 한 번 | `construction/build-and-test/build-and-test-summary.md` |

### 단위별 진행

INCEPTION STEP 07 에서 단위가 정해지면 채운다. **한 단위를 끝까지 마치고** 다음 단위로 간다.

| 단위 | 01 기능설계 | 02 비기능요구 | 03 비기능설계 | 04 인프라설계 | 05 코드생성 |
|---|---|---|---|---|---|
| (아직 없음) |  |  |  |  |  |

### 전부 합쳐 한 번

- [ ] STEP 06 빌드와 테스트 — 돌릴 명령은 INCEPTION STEP 06(애플리케이션 설계)에서 정해 여기에 적는다

# AI-DLC 실습

AI 에게 **단계를 지켜 일하게** 만드는 실습이다.
코드는 없다. 빈 폴더에서 요구사항부터 시작해 한 바퀴를 돈다.

## 1. 여는 방법 — 제일 중요

Kiro 에서 **이 `3.hooks-and-mcp` 폴더를 워크스페이스 루트로 열어야 한다.**

부모 폴더(`nxt-kiro-agent-lv1`)를 열면 규칙 파일이 `3.hooks-and-mcp/.kiro/...` 가 되어
**Kiro 가 규칙을 읽지 않는다.** 그러면 AI 는 평소처럼 코드부터 쓴다.

**열기 전에 `setup.sh`(또는 `setup.ps1`)를 한 번 돌린다.** §3 참고.

**확인하고 시작한다:**

- Kiro IDE — 좌측 **Steering 패널에 `aidlc` 항목**이 보이는가
- Kiro CLI — `/context show` 출력에 `aidlc.md` 가 있는가
- MCP 패널(또는 `/mcp`)에 **`aidlc` 서버가 연결됨**으로 뜨는가 — §3 참고

안 보이면 폴더를 잘못 열었다. 규칙이 안 먹은 상태로 진행하면 실습 전체가 무의미하다.

## 2. 폴더에 뭐가 있나

```text
3.hooks-and-mcp/
├── .kiro/
│   ├── steering/aidlc.md            AI 가 따라야 할 규칙 (건드리지 않는다)
│   ├── templates/requirements.md    requirements.md 를 쓸 때 따를 형식
│   ├── mcp/aidlc_server.py          절차 기록을 대신 쓰는 MCP 서버
│   ├── settings/mcp.json            그 서버를 Kiro 에 물리는 설정
│   ├── hooks/aidlc.json             자동으로 도는 훅 2개
│   ├── skills/commit/               불러서 쓰는 커밋 절차 (SKILL.md · rules.md)
│   └── seed/                        초기화용 원본 사본
├── aidlc-docs/                      AI 가 만드는 문서가 쌓이는 곳
│   ├── aidlc-state.md               상태판 — 지금 어느 단계인가
│   ├── audit.md                     승인 문구와 내 답변 원문
│   └── mistakes.md                  실수 기록
├── setup.sh                         준비 스크립트 — macOS · Linux
├── setup.ps1                        준비 스크립트 — Windows
├── spec.md                          내가 말한 요구가 원문 그대로 쌓인다
├── verification/
│   └── steering-tests.md            규칙이 진짜 먹는지 확인하는 T1~T10
└── README.md
```

| 파일 | 누가 채우나 |
|---|---|
| `spec.md` | AI. **내가 말한 그대로** 옮겨 적는다. 정리하지 않는다 |
| `aidlc-docs/inception/requirements/requirements.md` | AI. `spec.md` 를 템플릿 형식으로 정리한 것 |
| `aidlc-docs/aidlc-state.md` | AI. 단계를 끝낼 때마다 갱신 |
| `.kiro/` 안 | **아무도.** 규칙과 원본이다 |

## 3. 도구 — AI 가 기록을 손으로 쓰지 않는다

`aidlc` MCP 서버가 절차 기록을 대신 쓴다. **이 서버에는 파일을 덮어쓰는 기능이 없다.**
덧붙이는 길만 있어서, AI 가 `audit.md` 를 요약해 다시 쓰는 사고가 구조적으로 안 난다.

| 도구 | 하는 일 |
|---|---|
| `aidlc_status` | **지금 어디까지 왔나 한 화면으로** — 단계·산출물·게이트 횟수·실수·경고 |
| `aidlc_check` | 규칙 위반만 골라 보기 |
| `aidlc_spec_append` | 내가 말한 요구를 `spec.md` 에 원문 그대로 |
| `aidlc_gate_ask` / `aidlc_gate_answer` | 게이트 문답을 `audit.md` 에 시각과 함께 |
| `aidlc_mistake` | `mistakes.md` 에 한 줄 |
| `aidlc_state` | 상태판 갱신 |
| `aidlc_snapshot` | 단계 하나를 git 커밋 — **커밋 하나가 단계 하나** |

### 지금 어디까지 왔나

채팅에 **"지금 어디까지 왔어?"** 라고 물으면 이렇게 나온다.

```text
[INCEPTION STEP 06 애플리케이션 설계]

진행    INCEPTION  █████░  5/6
        CONSTRUCTION  단위 6개 — core 0/5 · production 0/5 · ...
다음    STEP 07 작업 단위 쪼개기

산출물
  ✓  aidlc-docs/inception/requirements/requirements.md    FR 8 · NFR 5
  ✓  aidlc-docs/inception/user-stories/stories.md         US-1~US-11 (11개)
  ·  aidlc-docs/inception/application-design/unit-of-work.md   (없음)

게이트  9회 — 답변 9건 · 수정요청 0건
실수    0건          미답변 질문  0곳

⚠ 산출물은 있는데 상태판 STEP 07 이 미체크다
```

마지막 `⚠` 줄이 이 도구의 값어치다. **상태판과 실제 파일을 대조**해서
AI 가 상태판 갱신을 빠뜨린 것, 산출물을 엉뚱한 데 흘린 것, 코드를 먼저 쓴 것을 잡아낸다.

### 준비물

**Kiro 로 열기 전에** 이 폴더에서 스크립트를 한 번 돌린다. 운영체제에 맞는 것 하나만.

macOS · Linux — 터미널에서

```bash
bash setup.sh
```

Windows — PowerShell 에서

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

네 가지를 순서대로 확인하고, 없는 것만 채운다.

| | 하는 일 |
|---|---|
| 1 | `uv` 가 없으면 설치한다 |
| 2 | MCP 서버가 쓸 패키지를 미리 받는다 — Kiro 첫 실행이 빨라진다 |
| 3 | 서버가 실제로 응답하는지 확인한다 |
| 4 | 이 폴더를 git 저장소로 만든다 — `aidlc_snapshot` 커밋에 필요하다 |

> **`git clone` 으로 받았다면** — 이 폴더는 수업 저장소 안에 들어 있다.
> 그 상태로는 실습 커밋이 수업 저장소에 섞이므로, 4번이 **수업 저장소의 `.git` 을 지운다.**
> 되돌릴 수 없다. 지우고 나면 `git pull` 로 자료를 다시 받지 못한다 —
> 실습은 이 폴더 하나로 끝나므로 상관없지만, 받아둔 자료를 남겨두고 싶으면
> **clone 폴더를 통째로 한 벌 복사해두고** 실행한다.

전부 `✓` 로 끝나면 Kiro 를 연다. 하나라도 `✗` 면 그 줄에 뭘 하라고 적혀 있다.

> `uv` 를 방금 깔았는데 못 찾는다고 나오면, **터미널을 새로 열고 다시 실행**한다.
> PATH 가 새 터미널부터 잡힌다.

### 자동으로 도는 것 — 훅 2개

| 언제 | 무엇이 도나 |
|---|---|
| Kiro 세션을 열 때 | 위 요약이 먼저 뜬다. 상태판을 직접 열 필요가 없다 |
| 질문 파일을 저장할 때 | 빈 `[Answer]:` 가 없으면 **게이트 1 승인으로 보고 이어서 진행**한다 |

두 번째가 §4 의 흐름을 바꾼다. 답을 적어 저장하면 끝이고,
채팅에 "답 적었어" 라고 말할 필요가 없다.

**게이트 2 는 자동화하지 않았다.** 결과물을 사람이 보는 것이 이 실습의 전부다.

### 불러서 쓰는 것 — 스킬 1개

훅이 **시점**에 걸리는 장치라면, 스킬은 **필요할 때 불러 쓰는 절차서**다.
`.kiro/skills/commit/` 에 커밋 절차를 하나 넣어 뒀다.

| 파일 | 무엇 |
|---|---|
| `SKILL.md` | 무엇을 어떤 순서로 — STEP 1~7 (현황 파악 → 타입 분류 → 분리 → 승인 후 add → 메시지 추천 → 커밋 → 반복) |
| `rules.md` | 무엇이 맞는 커밋인지 — 메시지 형식, 타입 8개, 파일 이동 다루는 법, 금지 사항 |

쓰는 법은 둘 중 하나다.

- 채팅에 `커밋해줘` 라고 말한다 — 앞머리의 `description` 과 맞으면 알아서 딸려 온다
- `/commit` 으로 직접 부른다

**steering 과 다른 점**: steering 은 대화마다 항상 읽히고, 스킬은 **부를 때만** 온다.
그래서 절차가 길어도 부담이 없다. 대신 **부르지 않으면 그만**이다 —
반드시 거쳐야 하는 일이라면 스킬이 아니라 훅이나 MCP 도구로 내려야 한다.

폴더 이름이 곧 스킬 이름이다. `.kiro/skills/<이름>/SKILL.md` 를 하나 더 만들면
스킬이 하나 더 늘어난다. 앞머리의 `name` 은 폴더 이름과 같아야 한다.

### 안 될 때

| 증상 | 원인 |
|---|---|
| MCP 패널에 `aidlc` 가 없다 | 폴더를 잘못 열었다. §1 로 |
| `aidlc` 가 빨간불 | `uv --version` 확인. 그래도면 `.kiro/settings/mcp.json` 의 `args` 경로를 절대경로로 바꾼다 |
| AI 가 `audit.md` 를 직접 고쳤다 | 규칙이 안 먹었다. "도구로 다시 해줘" 라고 말한다 |
| 커밋이 안 된다 | `git init` 을 안 했다 |

## 4. 시작하는 법

Kiro 채팅에 **만들고 싶은 것을 말투 그대로** 말한다. 정리해서 말하지 않아도 된다.

```
케이크 공장 게임 만들어줘. 벨트 깔고 30일 버티는 거. 파산하면 끝.
```

그러면 AI 가

1. 응답 첫 줄에 현재 위치를 표시한다 — `[INCEPTION · STEP 01 워크스페이스 파악]`
2. 내가 말한 문장을 `spec.md` 에 그대로 옮겨 적는다
3. STEP 03 요구사항 분석으로 넘어가 **객관식 질문 파일**을 만들어 되묻는다

**질문 파일에 답을 적어 넣는다.** 채팅으로 답하지 않는다.
`[Answer]:` 뒤에 고른 보기를 적고, 저장한 뒤 "답 적었어" 라고 말한다.

## 5. 게이트 — 승인 없이는 안 넘어간다

단계마다 두 번 멈춰 승인을 묻는다.

```
계획 → 질문 → [게이트 1 · 계획 승인] → 생성 → [게이트 2 · 결과 승인]
```

선택지는 **항상 두 개**다.

```
1) 수정 요청   2) 다음 단계로
```

세 번째 선택지가 나오거나, 묻지 않고 넘어가면 **규칙이 안 먹고 있다는 신호**다.

일부러 `1) 수정 요청` 을 한 번 골라 봐라. `aidlc-docs/mistakes.md` 에 한 줄이 늘어야 한다.

## 6. 규칙이 진짜 먹는지 확인한다 — 실습의 핵심

**AI 에게 규칙을 줬다고 지켜지는 게 아니다.**
`verification/steering-tests.md` 의 T1~T10 을 직접 돌려 확인한다.

- T1 은 시작 전에 반드시 본다 — 규칙이 로드조차 안 됐으면 나머지가 무의미하다
- T3 · T5 · T7 이 뚫리면 AI 는 절차를 건너뛰고 코드부터 쓴다
- 결과를 그 문서 아래 표에 적는다. 안 먹은 항목이 곧 **고칠 규칙 문장**이다

한 번 써서 되는 규칙은 없다. 안 먹은 문장을 찾아 고치는 게 이 실습에서 배우는 것이다.

## 7. 막힐 때

| 증상 | 원인 |
|---|---|
| AI 가 바로 코드를 쓴다 | 폴더를 잘못 열었다. §1 로 돌아간다 |
| `spec.md` 가 안 생긴다 | 같은 원인. Steering 패널을 확인한다 |
| AI 가 내 말을 `## 기능 요구사항` 식으로 정리해 넣었다 | 규칙 위반. "원문 그대로 다시 적어줘" 라고 말한다 |
| 채팅으로 질문만 하고 파일을 안 만든다 | "질문 파일로 만들어줘" 라고 말한다 |
| 지금 어디인지 모르겠다 | `aidlc-docs/aidlc-state.md` 를 본다 |

## 8. 처음부터 다시

AI 가 만든 것을 지우고 **새 세션**으로 시작한다.

macOS · Linux · Git Bash

```bash
rm -rf aidlc-docs spec.md src
cp -R .kiro/seed/aidlc-docs . && cp .kiro/seed/spec.md .
```

Windows PowerShell

```powershell
Remove-Item -Recurse -Force aidlc-docs, spec.md, src -ErrorAction SilentlyContinue
Copy-Item -Recurse .kiro\seed\aidlc-docs . ; Copy-Item .kiro\seed\spec.md .
```

AI 가 루트에 만든 코드 폴더(`src/` 등)도 같이 지운다. **`.kiro/` 는 건드리지 않는다.**

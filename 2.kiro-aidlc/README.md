# AI-DLC 실습

AI 에게 **단계를 지켜 일하게** 만드는 실습이다.
코드는 없다. 빈 폴더에서 요구사항부터 시작해 한 바퀴를 돈다.

## 1. 여는 방법 — 제일 중요

Kiro 에서 **이 `2.kiro-aidlc` 폴더를 워크스페이스 루트로 열어야 한다.**

부모 폴더(`nxt-kiro-agent-lv1`)를 열면 규칙 파일이 `2.kiro-aidlc/.kiro/...` 가 되어
**Kiro 가 규칙을 읽지 않는다.** 그러면 AI 는 평소처럼 코드부터 쓴다.

**확인하고 시작한다:**

- Kiro IDE — 좌측 **Steering 패널에 `aidlc` 항목**이 보이는가
- Kiro CLI — `/context show` 출력에 `aidlc.md` 가 있는가

안 보이면 폴더를 잘못 열었다. 규칙이 안 먹은 상태로 진행하면 실습 전체가 무의미하다.

## 2. 폴더에 뭐가 있나

```text
2.kiro-aidlc/
├── .kiro/
│   ├── steering/aidlc.md            AI 가 따라야 할 규칙 (건드리지 않는다)
│   ├── templates/requirements.md    requirements.md 를 쓸 때 따를 형식
│   └── seed/                        초기화용 원본 사본
├── aidlc-docs/                      AI 가 만드는 문서가 쌓이는 곳
│   ├── aidlc-state.md               상태판 — 지금 어느 단계인가
│   ├── audit.md                     승인 문구와 내 답변 원문
│   └── mistakes.md                  실수 기록
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

## 3. 시작하는 법

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

## 4. 게이트 — 승인 없이는 안 넘어간다

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

## 5. 규칙이 진짜 먹는지 확인한다 — 실습의 핵심

**AI 에게 규칙을 줬다고 지켜지는 게 아니다.**
`verification/steering-tests.md` 의 T1~T10 을 직접 돌려 확인한다.

- T1 은 시작 전에 반드시 본다 — 규칙이 로드조차 안 됐으면 나머지가 무의미하다
- T3 · T5 · T7 이 뚫리면 AI 는 절차를 건너뛰고 코드부터 쓴다
- 결과를 그 문서 아래 표에 적는다. 안 먹은 항목이 곧 **고칠 규칙 문장**이다

한 번 써서 되는 규칙은 없다. 안 먹은 문장을 찾아 고치는 게 이 실습에서 배우는 것이다.

## 6. 막힐 때

| 증상 | 원인 |
|---|---|
| AI 가 바로 코드를 쓴다 | 폴더를 잘못 열었다. §1 로 돌아간다 |
| `spec.md` 가 안 생긴다 | 같은 원인. Steering 패널을 확인한다 |
| AI 가 내 말을 `## 기능 요구사항` 식으로 정리해 넣었다 | 규칙 위반. "원문 그대로 다시 적어줘" 라고 말한다 |
| 채팅으로 질문만 하고 파일을 안 만든다 | "질문 파일로 만들어줘" 라고 말한다 |
| 지금 어디인지 모르겠다 | `aidlc-docs/aidlc-state.md` 를 본다 |

## 7. 처음부터 다시

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

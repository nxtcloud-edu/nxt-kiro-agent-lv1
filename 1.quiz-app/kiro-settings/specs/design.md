# Design — AWS 기초 개념 퀴즈 앱

## 파일 구조

```
quiz-app/v2/
├── index.html    ← 마크업 + style.css/app.js 로드
├── style.css     ← 모든 스타일
└── app.js        ← 데이터 + 로직 (IIFE 래핑)
```

---

## 아키텍처

```
┌──────────────────────────────────────────┐
│  index.html                              │
│  ┌────────────────────────────────────┐  │
│  │ .nav-tabs (퀴즈 | 오답노트)        │  │
│  ├────────────────────────────────────┤  │
│  │ #quizTab                           │  │
│  │   progress-bar                     │  │
│  │   score-display (aria-live)        │  │
│  │   question-area (aria-live)        │  │
│  │   options-container                │  │
│  │   explanation                      │  │
│  │   next-btn                         │  │
│  │   result-section                   │  │
│  ├────────────────────────────────────┤  │
│  │ #scrapbookTab                      │  │
│  │   scrap-card 리스트                │  │
│  │   clear-all 버튼                   │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

---

## 데이터 모델

### 퀴즈 데이터 (app.js 상단 상수)

```js
const QUIZ_DATA = [
  {
    question: "질문 텍스트",
    options: ["A", "B", "C", "D"],
    answer: 1,           // 0-indexed 정답 인덱스
    explanation: "해설"
  },
  // ...
];
```

### 앱 상태 (런타임, localStorage 직렬화)

```js
state = {
  activeIndices: [0,1,2,3,4],  // 현재 풀어야 할 문제 인덱스
  currentIndex: 0,              // activeIndices 내 포인터
  score: 0,
  answers: {},                  // { questionIndex: selectedOption }
  retryMode: false
}
```

### 오답 노트 (별도 localStorage 키)

```js
scrapbook = [
  {
    questionIndex: 2,
    selectedAnswer: 0,
    timestamp: "2026. 7. 8. 오후 3:30:00"
  }
]
```

---

## 상수 설계 (app.js 상단)

```js
const STORAGE_KEY_STATE = "awsQuizState";
const STORAGE_KEY_SCRAPBOOK = "awsQuizScrapbook";
const SCORE_THRESHOLDS = { PERFECT: 100, GOOD: 60 };
const ICONS = { CORRECT: "✓", WRONG: "✗" };
```

---

## 주요 함수 설계

| 함수명 | 역할 |
|--------|------|
| `loadState()` | localStorage에서 상태 복원 (try/catch) |
| `saveState()` | 현재 상태를 localStorage에 저장 (try/catch) |
| `loadScrapbook()` | 오답 노트 복원 (try/catch) |
| `saveScrapbook()` | 오답 노트 저장 (try/catch) |
| `renderQuestion()` | 현재 문제를 DOM에 렌더링 (textContent + createElement) |
| `selectAnswer(index)` | 답 선택 처리, 정오답 판정, 스타일 적용 |
| `showExplanation()` | 해설 표시 + 다음 버튼 활성화 + 포커스 이동 |
| `nextQuestion()` | 다음 문제로 이동 |
| `showResult()` | 결과 화면 렌더링 |
| `resetQuiz()` | 전체 초기화 |
| `retryWrong()` | 오답만 재도전 모드 |
| `switchTab(tab)` | 탭 전환 |
| `renderScrapbook()` | 오답 노트 DOM 렌더링 (createElement) |
| `addToScrapbook(qIdx, selected)` | 오답 추가 (중복 시 업데이트) |
| `removeFromScrapbook(qIdx)` | 개별 오답 삭제 |
| `clearScrapbook()` | 전체 삭제 (confirm 후) |
| `updateBadge()` | 오답 수 뱃지 업데이트 |

---

## 접근성 설계

| 요소 | aria 속성 | 동작 |
|------|-----------|------|
| 점수 표시 (#scoreDisplay) | `aria-live="polite"` | 점수 변경 시 스크린 리더가 읽음 |
| 문제 영역 (#questionArea) | `aria-live="polite"` | 문제 전환 시 스크린 리더가 읽음 |
| 선택지 버튼 | `aria-label` 또는 의미있는 텍스트 | 정오답 후 disabled |
| 다음 버튼 (#nextBtn) | — | 답 선택 후 자동 `focus()` |
| 정답 선택지 | 텍스트에 "✓" 접두 | 색상+아이콘 이중 표시 |
| 오답 선택지 | 텍스트에 "✗" 접두 | 색상+아이콘 이중 표시 |

---

## 스타일 설계 (style.css)

### 색상 팔레트

- 배경: `#232f3e` → `#1a2332` 그라데이션
- 강조: `#ff9900` (AWS 오렌지)
- 정답: `#2e7d32` (초록)
- 오답: `#c62828` (빨강)
- 카드 배경: `#fff`
- 텍스트: `#232f3e`, `#666`, `#999`

### 레이아웃

- 중앙 정렬, 최대 폭 640px
- body: flexbox 센터링, min-height 100vh
- 카드형 컨테이너, border-radius 16px, box-shadow

### 반응형

- padding 조절 (모바일 20px, 데스크톱 40px)
- 버튼 full-width on mobile

---

## localStorage 전략

- 읽기/쓰기 모두 `try/catch`로 감싼다.
- 실패 시 콘솔 경고만 출력하고 기본값으로 동작한다.
- 키 이름은 상수로 관리한다.
- 상태 변경마다 즉시 저장 (debounce 불필요 — 버튼 클릭 단위).

---

## 보안 고려사항

- innerHTML 미사용으로 DOM XSS 경로 차단.
- 외부 데이터 미로드로 주입 경로 없음.
- localStorage 파싱 실패 시 graceful degradation.

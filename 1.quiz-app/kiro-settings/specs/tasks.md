# Tasks — AWS 기초 개념 퀴즈 앱

## Task 1: index.html 마크업 작성

- [ ] HTML5 boilerplate (`lang="ko"`, charset, viewport)
- [ ] `style.css` 링크, `app.js` defer 스크립트 로드
- [ ] 컨테이너 구조: 타이틀, 부제, 탭 네비게이션
- [ ] 퀴즈 탭: progress-bar, score-display(`aria-live="polite"`), question-area(`aria-live="polite"`), options-container, explanation, next-btn, result-section
- [ ] 오답 노트 탭: scrapbook-content, clear-all 버튼
- [ ] 오답 수 뱃지 요소
- [ ] 결과 화면: emoji, score, message, "전체 다시 풀기" 버튼, "틀린 문제만 다시 풀기" 버튼
- [ ] 재도전 모드 뱃지 요소

**검증:** HTML 유효성 (W3C), aria 속성 존재 확인

---

## Task 2: style.css 스타일링

- [ ] CSS reset (margin, padding, box-sizing)
- [ ] body 레이아웃 (flexbox center, gradient 배경)
- [ ] 컨테이너 카드 (max-width 640px, border-radius, shadow)
- [ ] 타이포그래피 (h1, subtitle, question-text, 크기·색상)
- [ ] 탭 네비게이션 스타일 (active 상태, 뱃지)
- [ ] 프로그레스 바 (배경 + fill 그라데이션, transition)
- [ ] 선택지 버튼 (기본, hover, disabled, .correct, .wrong)
- [ ] 해설 영역 (border-left, background)
- [ ] 다음/리셋/재도전 버튼 스타일
- [ ] 결과 화면 스타일
- [ ] 오답 노트 카드 스타일
- [ ] show/hide 유틸 클래스
- [ ] 반응형 조정 (@media or fluid)

**검증:** 브라우저에서 각 상태 시각 확인

---

## Task 3: app.js — 상수 및 데이터

- [ ] IIFE 또는 모듈 래핑
- [ ] 상수 선언: STORAGE_KEY_STATE, STORAGE_KEY_SCRAPBOOK, SCORE_THRESHOLDS, ICONS
- [ ] QUIZ_DATA 배열 (5문제, question/options/answer/explanation)

**검증:** 콘솔에서 상수·데이터 접근 불가 확인 (전역 스코프 미노출)

---

## Task 4: app.js — 상태 관리 (localStorage)

- [ ] `loadState()` — try/catch, JSON.parse, 기본값 폴백
- [ ] `saveState()` — try/catch, JSON.stringify
- [ ] `loadScrapbook()` — try/catch, 기본값 빈 배열
- [ ] `saveScrapbook()` — try/catch
- [ ] 상태 객체 구조: { activeIndices, currentIndex, score, answers, retryMode }

**검증:** localStorage 비활성 환경에서 에러 없이 동작, 정상 환경에서 새로고침 후 상태 복원

---

## Task 5: app.js — 퀴즈 렌더링 및 진행

- [ ] `renderQuestion()` — textContent/createElement로 문제·선택지 렌더링
- [ ] `selectAnswer(index)` — 정오답 판정, ✓/✗ 아이콘 병기, 색상 적용, 점수 갱신
- [ ] 답 선택 후 "다음 문제" 버튼 표시 + focus() 이동
- [ ] `nextQuestion()` — 다음 문제로 이동 또는 결과 화면
- [ ] 프로그레스 바 업데이트
- [ ] 점수 표시 업데이트 (aria-live 영역)

**검증:** 키보드만으로 퀴즈 전체 진행 가능, 스크린 리더에서 점수/문제 변경 읽힘

---

## Task 6: app.js — 결과 화면 및 재도전

- [ ] `showResult()` — 점수 비율에 따른 emoji + 메시지 표시
- [ ] `resetQuiz()` — 전체 초기화, localStorage 클리어
- [ ] `retryWrong()` — 오답 인덱스 추출, activeIndices 재설정, 재도전 모드 뱃지 표시
- [ ] "틀린 문제만 다시 풀기" 버튼 비활성화 (전부 맞았을 때)

**검증:** 전체 리셋 후 상태 초기화 확인, 재도전 모드에서 오답만 출제 확인

---

## Task 7: app.js — 오답 노트

- [ ] `addToScrapbook(qIdx, selected)` — 중복 시 selectedAnswer 업데이트
- [ ] `removeFromScrapbook(qIdx)` — 개별 삭제
- [ ] `clearScrapbook()` — confirm 후 전체 삭제
- [ ] `renderScrapbook()` — createElement로 카드 렌더링 (문제, 내 답, 정답, 해설, 삭제 버튼)
- [ ] 정답 재도전 시 자동 제거
- [ ] `updateBadge()` — 오답 수 뱃지 업데이트

**검증:** 오답 발생 시 자동 저장, 정답 시 자동 제거, 삭제 기능 동작

---

## Task 8: app.js — 탭 네비게이션

- [ ] `switchTab(tab)` — 퀴즈/오답노트 탭 전환
- [ ] active 클래스 토글
- [ ] 탭 전환 시 오답 노트 렌더링 갱신

**검증:** 탭 전환 정상 동작, 양 탭 간 상태 유지

---

## Task 9: 통합 테스트 및 마무리

- [ ] 전체 플로우 테스트: 퀴즈 시작 → 답변 → 결과 → 재도전 → 오답 노트
- [ ] 새로고침 후 상태 복원 확인
- [ ] 키보드 네비게이션 테스트
- [ ] 접근성 확인: aria-live 동작, 포커스 이동, 아이콘 병기
- [ ] 모바일 뷰포트 확인
- [ ] 전역 변수 미노출 확인 (콘솔 테스트)
- [ ] quiz-app/v0 디렉토리에 기존 v1 대비 개선점 확인

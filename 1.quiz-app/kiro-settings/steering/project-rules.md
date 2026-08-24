# 프로젝트 규칙

## Tech

- 바닐라 HTML/CSS/JS만 사용한다. 외부 라이브러리·CDN 사용 금지.

## Structure

- 파일 구성: `index.html` / `style.css` / `app.js` 3개 파일로 분리한다.
- 퀴즈 데이터는 `app.js` 상단에 배열로 분리하여 관리한다.

## Quality

- 화면 출력은 `innerHTML` 금지. `textContent` 또는 DOM API(`createElement`, `appendChild` 등)를 사용한다.
- `localStorage` 접근은 반드시 `try/catch`로 감싼다.
- 설정값(키 이름, 문제 수 등)은 파일 상단 상수(`const`)로 선언한다.
- 전역 변수 금지. 코드는 IIFE 또는 ES 모듈로 감싼다.

## Accessibility (a11y)

- 점수 표시 영역과 문제 영역에 `aria-live="polite"` 속성을 부여한다.
- 답 선택 후 "다음 문제" 버튼으로 포커스를 자동 이동한다(`focus()`).
- 정오답 표시는 색상만 사용하지 않고 ✓/✗ 아이콘을 반드시 병기한다.

## 제약

- 로그인·서버·외부 API·광고 없음. 100% 클라이언트사이드 정적 앱으로 유지한다.

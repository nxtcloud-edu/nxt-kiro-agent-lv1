# 커밋 규칙

## 메시지 형식

- **한글 1줄**로 작성: `타입: 간결한 설명`
- 여러 줄 설명 금지, 상세한 본문 금지

```bash
# Good
git commit -m "tidy: 복잡한 조건문을 가드 절로 변경"
git commit -m "feat: 사용자 알림 기능 추가"
git commit -m "fix: null 포인터 예외 수정"
git commit -m "perf: 데이터베이스 쿼리 최적화"

# Bad
git commit -m "feat: add user notification"  # 영어 사용
git commit -m "refactoring and add feature"  # 정리와 기능 섞음
git commit -m "fix stuff"  # 불명확
```

## 커밋 타입

| 타입 | 용도 |
|------|------|
| `tidy` | 코드 정리 (기능 변경 없음, Tidy First) — **파일 이동·이름변경 포함** |
| `feat` | 새 기능 추가 (Make it work) |
| `fix` | 버그 수정 |
| `test` | 테스트 추가/수정 |
| `perf` | 성능 최적화 (Make it fast) |
| `docs` | 문서 업데이트 |
| `style` | 코드 포맷팅 (의미 변경 없음) |
| `chore` | 빌드/설정 변경 |

## 커밋 분리 전략 (Tidy First 순서)

```bash
# 1단계: 기존 코드 정리 (Tidy First)
git commit -m "tidy: 사용자 검증 로직을 별도 함수로 추출"
git commit -m "tidy: 매직 넘버를 상수로 변경"

# 2단계: 기능 구현 (Make it work)
git commit -m "feat: 사용자 알림 기능 추가 (초안)"

# 3단계: 코드 정리 (Make it right)
git commit -m "tidy: 알림 전송 로직 단순화"
git commit -m "tidy: 에러 핸들링 개선"

# 4단계: 최적화 (Make it fast, 필요시)
git commit -m "perf: 알림 대량 전송 시 배치 처리 적용"
```

## 파일 이동·이름변경

git 에는 "이동"이 없다. **삭제 + 추가가 같은 커밋에 있을 때만** 이름변경으로 인식한다.
놓치면 이력이 끊겨서 `git log --follow` 와 `git blame` 이 옛 파일을 못 따라간다. 되돌릴 수 없다.

```bash
# Good — 경로째 스테이징. 삭제까지 함께 올라간다
git add -A -- src/old src/new
git diff --cached --name-status   # R100 src/old/a.ts -> src/new/a.ts  ← R 이 보여야 한다
git commit -m "tidy: 파일을 새 디렉터리로 이동"

# Bad — 추가만 나열. 삭제가 안 올라가서 R 이 A 로 떨어진다
git add src/new/a.ts

# Bad — 이동을 두 커밋으로 쪼갬. 이름변경이 영구히 소실된다
git commit -m "feat: 새 위치에 추가"
git commit -m "tidy: 옛 위치 삭제"
```

주의: `git add .` 도 삭제를 스테이징한다(Git 2.0+). `-A` 와의 차이는 삭제 여부가 아니라
범위(전체 트리 / 현재 디렉터리)다. 위험한 것은 **파일을 하나씩 나열하는 방식**이다.

**이동과 수정이 섞였을 때**는 이동만 먼저 `tidy` 로 커밋하고, 내용 변경은 다음 커밋으로 뺀다.
같이 올리면 diff 가 통째로 새 파일처럼 보여서 무엇이 바뀌었는지 읽을 수 없다.

## 금지 사항

- 정리(tidy)와 기능(feat)을 하나의 커밋에 섞지 말 것
- 파일 이동의 삭제와 추가를 서로 다른 커밋으로 나누지 말 것 (이름변경 소실)
- 한 커밋에 여러 목적을 담지 말 것
- 거대한 단일 커밋 (100줄+) 금지
- 동작하지 않는 코드 커밋 금지
- 의미없는 커밋 메시지 금지

## 커밋 전 자가 점검

```
[ ] 코드가 이해하기 쉬운가?
[ ] 테스트가 통과하는가?
[ ] 커밋이 한 가지 목적만 가지는가?
[ ] 커밋 메시지가 한글이고 명확한가?
[ ] 파일을 옮겼다면 `git diff --cached --name-status` 에 `R` 로 잡히는가?
[ ] 불필요한 변경이 포함되지 않았는가?
[ ] 죽은 코드를 남기지 않았는가?
```

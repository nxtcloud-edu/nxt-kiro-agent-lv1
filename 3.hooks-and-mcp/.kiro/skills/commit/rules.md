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
| `tidy` | 코드 정리 (기능 변경 없음, Tidy First) |
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

## 금지 사항

- 정리(tidy)와 기능(feat)을 하나의 커밋에 섞지 말 것
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
[ ] 불필요한 변경이 포함되지 않았는가?
[ ] 죽은 코드를 남기지 않았는가?
```

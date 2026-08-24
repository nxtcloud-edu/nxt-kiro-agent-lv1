# Requirements: {프로젝트 이름}

> `aidlc-docs/inception/requirements/requirements.md` 에 저장합니다.
> `{ }` 안만 채우고, 섹션 제목과 번호 체계는 그대로 둡니다.

## Intent Analysis

| Attribute | Value |
|---|---|
| User Request | {처음 적어 준 요청을 한 줄로} |
| Request Type | {New Project (greenfield) / Enhancement / Bug Fix / Refactoring} |
| Scope Estimate | {단일 앱 · 구성 요소 세 개} |
| Complexity Estimate | {Simple / Moderate / Complex} |
| Requirements Depth | {Minimal / Standard / Comprehensive} |

---

## 1. Functional Requirements

### FR-1: {기능 이름}

- **FR-1.1**: {확인 가능한 한 문장. "~할 수 있어야 한다"}
- **FR-1.2**: {…}

### FR-2: {기능 이름}

- **FR-2.1**: {…}
- **FR-2.2**: {…}

## 2. Non-Functional Requirements

### NFR-1: Performance

- **NFR-1.1**: {기준이나 수치가 들어간 문장}

### NFR-2: Correctness

- **NFR-2.1**: {무엇이 항상 맞아야 하는지}

### NFR-3: Testing

- **NFR-3.1**: {무엇을 어떤 방식으로 검증하는지}

### NFR-4: Security

- **NFR-4.1**: {외부 입력 · 비밀값 · 접근 범위}

### NFR-5: Maintainability

- **NFR-5.1**: {규칙과 숫자의 분리, 파일 구성 원칙 등}

## 3. Technical Constraints

> **여기서 기술을 고르지 않습니다.** 요구명세가 이미 못 박은 것만 옮겨 적습니다.
> 무엇으로 만들지(언어 · 프레임워크 · 런타임)는 CONSTRUCTION STEP 02(비기능 요구)에서
> `tech-stack-decisions.md` 에 정합니다. 요구명세에 없으면 `없음`으로 둡니다.

| Constraint | Value |
|---|---|
| Given | {요구명세가 지정한 것. 없으면 `없음`} |
| Excluded | {쓰지 말라고 한 것. 없으면 `없음`} |

## 4. Out of Scope (MVP)

- {이번에 만들지 않는 것}
- {…}

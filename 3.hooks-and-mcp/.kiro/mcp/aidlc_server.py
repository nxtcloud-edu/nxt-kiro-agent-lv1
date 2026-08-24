# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp>=1.2"]
# ///
"""aidlc-mcp — AI-DLC 절차를 손이 아니라 도구로 돌리기 위한 MCP 서버.

규칙 원문은 `.kiro/steering/aidlc.md`. 이 서버는 그 규칙 중
'기계가 대신할 수 있는 부분'만 가져온다. 판단(게이트 승인)은 사람 몫이다.

핵심 설계: audit.md · mistakes.md · spec.md 에는 **덧붙이는 경로만** 있다.
덮어쓰는 함수를 아예 만들지 않아 규칙 §4 위반이 구조적으로 불가능하다.
"""

from __future__ import annotations

import os
import re
import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

try:  # SDK v2
    from mcp.server import MCPServer as _Server
except ImportError:  # SDK v1
    from mcp.server.fastmcp import FastMCP as _Server

mcp = _Server("aidlc")

# ── 경로 ──────────────────────────────────────────────────────────────
# 이 파일은 <워크스페이스>/.kiro/mcp/aidlc_server.py 에 있다.
# Kiro 가 서버를 어느 cwd 에서 띄우든 워크스페이스를 스스로 찾는다.
ROOT = Path(os.environ.get("AIDLC_ROOT") or Path(__file__).resolve().parents[2])
DOCS = ROOT / "aidlc-docs"
STATE = DOCS / "aidlc-state.md"
AUDIT = DOCS / "audit.md"
MISTAKES = DOCS / "mistakes.md"
SPEC = ROOT / "spec.md"

INCEPTION = [
    ("01", "워크스페이스 파악", "spec.md"),
    ("02", "기존 코드 역분석", None),
    ("03", "요구사항 분석", "aidlc-docs/inception/requirements/requirements.md"),
    ("04", "유저 스토리", "aidlc-docs/inception/user-stories/stories.md"),
    ("05", "실행 계획 수립", "aidlc-docs/inception/plans/execution-plan.md"),
    ("06", "애플리케이션 설계", "aidlc-docs/inception/application-design/components.md"),
    ("07", "작업 단위 쪼개기", "aidlc-docs/inception/application-design/unit-of-work.md"),
]
CONSTRUCTION = ["기능 설계", "비기능 요구", "비기능 설계", "인프라 설계", "코드 생성"]
DOCS_ROOT_ALLOWED = {"aidlc-state.md", "audit.md", "mistakes.md"}
CODE_EXT = {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".java", ".go", ".rb"}


# ── 공통 ──────────────────────────────────────────────────────────────
def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def _read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def _append(p: Path, text: str, spaced: bool = True) -> None:
    """덧붙이기 전용. 이 서버에 파일을 덮어쓰는 경로는 없다.

    spaced=False 는 표의 행처럼 앞 줄에 바로 이어 붙여야 할 때 쓴다.
    """
    p.parent.mkdir(parents=True, exist_ok=True)
    existing = _read(p)
    if not existing:
        sep = ""
    elif not spaced:
        sep = "" if existing.endswith("\n") else "\n"
    else:
        sep = "" if existing.endswith("\n\n") else ("\n" if existing.endswith("\n") else "\n\n")
    with p.open("a", encoding="utf-8") as f:
        f.write(sep + text.rstrip("\n") + "\n")


def _marks(text: str) -> dict[str, str]:
    """상태판 INCEPTION 표에서 STEP 별 체크 표시를 읽는다."""
    return {
        m.group(2): m.group(1).strip()
        for m in re.finditer(r"^\|\s*(\[x\]|\[ \]|—|-|\s*)\s*\|\s*(\d{2})\s*\|", text, re.M)
    }


def _units() -> list[str]:
    """unit-of-work.md 에서 작업 단위 이름을 뽑는다."""
    t = _read(DOCS / "inception/application-design/unit-of-work.md")
    return [m.group(1) for m in re.finditer(r"^##\s*단위\s*\d+\s*:\s*(\S+)", t, re.M)]


def _artifact_note(rel: str) -> str:
    """산출물 한 줄 요약. 있으면 '무엇이 얼마나' 들어 있는지 보여준다."""
    t = _read(ROOT / rel)
    if not t:
        return ""
    if rel.endswith("requirements.md"):
        fr = len(set(re.findall(r"FR-\d+", t)))
        nfr = len(set(re.findall(r"NFR-\d+", t)))
        return f"FR {fr} · NFR {nfr}"
    if rel.endswith("stories.md"):
        us = sorted(set(re.findall(r"US-(\d+)", t)), key=int)
        return f"US-{us[0]}~US-{us[-1]} ({len(us)}개)" if us else "스토리 없음"
    if rel.endswith("components.md"):
        return f"컴포넌트 {len(re.findall(r'^###\s', t, re.M))}개"
    if rel.endswith("unit-of-work.md"):
        u = _units()
        return f"단위 {len(u)}개 — {' → '.join(u)}" if u else "단위 없음"
    return f"{len(t.strip().splitlines())}줄"


def _has(rel: str) -> bool:
    """산출물이 실제로 채워졌는가. 자리표시자만 있는 spec.md 는 없는 것으로 본다."""
    t = _read(ROOT / rel)
    return bool(t.strip()) and "(아직 비어 있음)" not in t


def _open_questions() -> list[str]:
    """답이 안 채워진 [Answer]: 를 찾는다. 게이트 1 이 아직 안 끝났다는 신호."""
    out = []
    if not DOCS.exists():
        return out
    for p in sorted(DOCS.rglob("*.md")):
        n = sum(1 for ln in _read(p).splitlines() if re.match(r"^\s*\[Answer\]:\s*$", ln))
        if n:
            out.append(f"{p.relative_to(ROOT)} — {n}개")
    return out


def _violations() -> list[str]:
    """규칙 §6 위반과 상태판·실제 파일 불일치를 모은다."""
    v: list[str] = []
    if not DOCS.exists():
        return ["aidlc-docs/ 가 없다 — STEP 01 부터 시작해야 한다"]

    marks = _marks(_read(STATE))
    for step, name, rel in INCEPTION:
        if rel is None:
            continue
        exists = _has(rel)
        mark = marks.get(step, "")
        if mark == "[x]" and not exists:
            v.append(f"상태판 STEP {step} {name} 은 [x] 인데 산출물 `{rel}` 이 없다")
        if mark in ("[ ]", "") and exists:
            v.append(f"산출물 `{rel}` 은 있는데 상태판 STEP {step} {name} 이 미체크다")

    for p in DOCS.iterdir():
        if p.is_file() and p.name not in DOCS_ROOT_ALLOWED:
            v.append(f"`aidlc-docs/{p.name}` — 단계 폴더 밖 문서다 (§6). 허용은 3개뿐")

    for p in DOCS.rglob("*"):
        if p.is_file() and p.suffix in CODE_EXT:
            v.append(f"`{p.relative_to(ROOT)}` — aidlc-docs 안에 실행 코드다 (§6). 코드는 루트 `src/`")

    if not (ROOT / "aidlc-docs/inception/requirements/requirements.md").exists():
        src = ROOT / "src"
        if src.exists() and any(p.suffix in CODE_EXT for p in src.rglob("*") if p.is_file()):
            v.append("requirements.md 확정 전에 `src/` 에 코드가 생겼다 (§6)")

    spec = _read(SPEC)
    if not spec.strip() or "(아직 비어 있음)" in spec:
        v.append("`spec.md` 가 비어 있다 — 사람이 말한 요구부터 원문으로 옮겨야 한다")

    for q in _open_questions():
        v.append(f"답이 안 채워진 질문이 남았다 — {q}")

    return v


def _dw(text: str) -> int:
    """한글·한자는 두 칸을 먹는다. 표를 눈으로 볼 때의 폭."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def _row(unit: str, cells: list[str], header: str) -> str:
    """단위별 진행 표의 칸 너비를 헤더에 맞춰 한 줄을 만든다."""
    widths = [_dw(c) for c in header.strip().strip("|").split("|")]
    out = []
    for i, v in enumerate([unit] + cells):
        cell = f" {v} "
        w = widths[i] if i < len(widths) else _dw(cell)
        out.append(cell + " " * max(0, w - _dw(cell)))
    return "|" + "|".join(out) + "|"


def _bar(done: int, total: int) -> str:
    return "█" * done + "░" * max(0, total - done)


# ── 툴 ────────────────────────────────────────────────────────────────
@mcp.tool()
def aidlc_status() -> str:
    """지금 어디까지 왔는지 한 화면으로 요약한다.

    상태판·산출물·감사 기록·실수 기록을 한꺼번에 읽어 대조한다.
    상태판과 실제 파일이 어긋나면 경고로 알려준다.
    새 세션을 시작할 때, 그리고 게이트를 물기 전에 먼저 부른다.
    """
    if not DOCS.exists():
        return f"[아직 시작 전]\n\n{ROOT} 에 aidlc-docs/ 가 없다.\nSTEP 01 워크스페이스 파악부터 시작한다."

    state = _read(STATE)
    marks = _marks(state)
    cur = re.search(r"^-\s*단계\s*—\s*(.+)$", state, re.M)
    nxt = re.search(r"^-\s*다음에 할 일\s*—\s*(.+)$", state, re.M)

    done = sum(1 for s, _, r in INCEPTION if r and marks.get(s) == "[x]")
    total = sum(1 for _, _, r in INCEPTION if r)

    L: list[str] = []
    L.append(f"[{cur.group(1).strip() if cur else '위치 미기록'}]")
    L.append("")
    L.append(f"진행    INCEPTION  {_bar(done, total)}  {done}/{total}")

    units = _units()
    ct = _read(STATE)
    if units:
        rows = []
        for u in units:
            m = re.search(r"^\|\s*" + re.escape(u) + r"\s*\|(.+)\|[ \t]*$", ct, re.M)
            cells = [c.strip() for c in m.group(1).split("|")] if m else []
            fin = sum(1 for c in cells[:5] if c)
            rows.append(f"{u} {fin}/5")
        L.append(f"        CONSTRUCTION  단위 {len(units)}개 — " + " · ".join(rows))
    else:
        L.append("        CONSTRUCTION  아직 단위가 정해지지 않았다 (INCEPTION STEP 07)")
    if nxt:
        L.append(f"다음    {nxt.group(1).strip()}")

    L.append("")
    L.append("산출물")
    for step, name, rel in INCEPTION:
        if rel is None:
            L.append(f"  —  STEP {step} {name}  (건너뜀)")
            continue
        ok = _has(rel)
        icon = "✓" if ok else "·"
        note = _artifact_note(rel) if ok else "(없음)"
        L.append(f"  {icon}  {rel:<56} {note}")

    con = DOCS / "construction"
    if con.exists():
        for p in sorted(con.iterdir()):
            if p.is_dir() and p.name != "plans":
                inner = [q.name for q in sorted(p.iterdir()) if q.is_dir()]
                L.append(f"  ✓  construction/{p.name}/{'':<42}{' · '.join(inner) or '비어 있음'}")

    # 머리말의 형식 예시(코드펜스)는 실제 기록이 아니다. 세지 않는다.
    audit = re.sub(r"```.*?```", "", _read(AUDIT), flags=re.S)
    gates = re.findall(r"^###\s+.*게이트\s*([12])", audit, re.M)
    answers = re.findall(r"^-\s*답:\s*(.+)$", audit, re.M)
    fix = sum(1 for a in answers if "수정" in a)
    mrows = [
        ln for ln in _read(MISTAKES).splitlines()
        if ln.startswith("|") and "---" not in ln and "무엇이 잘못됐나" not in ln
    ]
    q = _open_questions()

    L.append("")
    L.append(f"게이트  {len(gates)}회 — 답변 {len(answers)}건 · 수정요청 {fix}건")
    L.append(f"실수    {len(mrows)}건          미답변 질문  {len(q)}곳")

    v = _violations()
    if v:
        L.append("")
        for item in v:
            L.append(f"⚠ {item}")

    return "\n".join(L)


@mcp.tool()
def aidlc_check() -> str:
    """규칙 위반만 골라 본다. 게이트를 묻기 직전에 부른다.

    산출물 위치(§6), 상태판과 실제 파일의 불일치, 답이 안 채워진 질문,
    requirements.md 확정 전 코드 생성을 잡아낸다.
    """
    v = _violations()
    return "위반 없음." if not v else "\n".join(f"⚠ {x}" for x in v)


@mcp.tool()
def aidlc_spec_append(text: str) -> str:
    """사람이 말한 요구를 `spec.md` 에 **원문 그대로** 덧붙인다.

    정리·요약·번호 붙이기를 하지 말고 들은 말을 그대로 넘긴다.
    그 일은 STEP 03 의 requirements.md 가 한다.
    """
    body = text.strip()
    if not body:
        return "빈 문자열이다. 사람이 말한 원문을 그대로 넘겨야 한다."
    if not SPEC.exists():
        SPEC.write_text(
            "# 요구명세\n\n"
            "> 사람이 말한 요구가 **원문 그대로** 여기에 쌓인다. 정리하지 않는다.\n"
            "> 정리된 것은 `aidlc-docs/inception/requirements/requirements.md` 에 있다.\n",
            encoding="utf-8",
        )
    elif "(아직 비어 있음)" in _read(SPEC):
        SPEC.write_text(_read(SPEC).replace("(아직 비어 있음)\n", "").rstrip() + "\n", encoding="utf-8")
    _append(SPEC, body)
    return f"spec.md 에 {len(body.splitlines())}줄 덧붙였다."


@mcp.tool()
def aidlc_gate_ask(step: str, gate: int, question: str) -> str:
    """게이트 질문을 `audit.md` 에 남긴다. **사람에게 묻기 직전에** 부른다.

    step 은 'STEP 03 요구사항 분석' 처럼 단계 이름까지 적는다.
    gate 는 1(계획 승인) 또는 2(결과 승인).
    질문 본문에는 반드시 두 갈래만 넣는다 — 1) 수정 요청  2) 다음 단계로
    """
    if gate not in (1, 2):
        return "gate 는 1 또는 2 여야 한다."
    _append(AUDIT, f"### {_now()} · {step.strip()} · 게이트 {gate}\n\n- 물은 것: {question.strip()}")
    warn = ""
    if gate == 2:
        n = len([
            ln for ln in _read(MISTAKES).splitlines()
            if ln.startswith("|") and "---" not in ln and "무엇이 잘못됐나" not in ln
        ])
        warn = f"\n게이트 2 다. 실수 기록 총 {n}건을 질문에 함께 보고해야 한다."
    return f"audit.md 에 질문을 남겼다. 이제 사람에게 묻는다.{warn}"


@mcp.tool()
def aidlc_gate_answer(answer: str) -> str:
    """사람의 답을 **원문 그대로** `audit.md` 에 남긴다. 답을 받은 직후에 부른다.

    다듬거나 요약하지 않는다. '수정 요청'이면 실수 기록이 필요하다고 알려준다.
    """
    body = answer.strip()
    if not body:
        return "빈 답이다. 사람이 쓴 말을 그대로 넘겨야 한다."
    _append(AUDIT, f"- 답: {body}", spaced=False)
    if "수정" in body or body.strip().startswith("1"):
        return "audit.md 에 답을 남겼다. **수정 요청이다 — aidlc_mistake 로 무엇이 어긋났는지 한 줄 남긴다.**"
    return "audit.md 에 답을 남겼다."


@mcp.tool()
def aidlc_mistake(step: str, what: str, why: str, next_time: str, actor: str = "AI") -> str:
    """실수를 `mistakes.md` 에 한 줄 덧붙인다. 묻지 않고 바로 부른다.

    남기는 경우 — 게이트에서 수정 요청이 온 때, 확정된 것과 다르게 만든 때,
    규칙을 어긴 때, 빌드·테스트 실패가 앞 단계 누락 탓인 때.
    애매하면 actor 는 'AI'. 변명을 쓰지 않는다.
    """
    if actor not in ("AI", "사람"):
        actor = "AI"
    clean = lambda s: s.strip().replace("|", "/").replace("\n", " ")
    _append(
        MISTAKES,
        f"| {_now()} | {clean(step)} | {actor} | {clean(what)} | {clean(why)} | {clean(next_time)} |",
        spaced=False,
    )
    n = len([
        ln for ln in _read(MISTAKES).splitlines()
        if ln.startswith("|") and "---" not in ln and "무엇이 잘못됐나" not in ln
    ])
    return f"실수 기록에 한 줄 덧붙였다. 누적 {n}건."


@mcp.tool()
def aidlc_state(
    phase: str,
    step: str,
    status: str = "완료",
    next_action: str = "",
    unit: str = "",
) -> str:
    """상태판을 갱신한다. **게이트 2 직후에** 부른다.

    phase 는 'inception' 또는 'construction'.
    construction 이면 unit(작업 단위 이름)이 필요하다. 단위 행이 없으면 만든다.
    단계 이름과 순서는 건드리지 않고 상태 칸과 '현재 위치'만 바꾼다.
    """
    if not STATE.exists():
        return "aidlc-state.md 가 없다."
    text = _read(STATE)
    step = step.strip().zfill(2)
    phase = phase.strip().lower()

    if phase.startswith("i"):
        pat = re.compile(r"^(\|)([^|]*)(\|\s*" + re.escape(step) + r"\s*\|[^|]*\|)([^|]*)(\|)", re.M)
        if not pat.search(text):
            return f"상태판 INCEPTION 표에서 STEP {step} 행을 못 찾았다."
        text = pat.sub(
            lambda m: f"{m.group(1)}{' [x] '.ljust(len(m.group(2)))}{m.group(3)}"
            f"{(' ' + status.strip()).ljust(len(m.group(4)))}{m.group(5)}",
            text,
            count=1,
        )
        label = f"INCEPTION STEP {step} {dict((s, n) for s, n, _ in INCEPTION).get(step, '')}"
    elif phase.startswith("c"):
        if not unit.strip():
            return "construction 은 unit(작업 단위 이름)이 필요하다."
        unit = unit.strip()
        idx = int(step) - 1
        if step == "06":
            text = re.sub(r"^-\s*\[\s*\]\s*(STEP 06)", r"- [x] \1", text, count=1, flags=re.M)
        else:
            if not 0 <= idx < 5:
                return "construction step 은 01~06 이다."
            row = re.compile(r"^\|\s*" + re.escape(unit) + r"\s*\|(.*)\|[ \t]*$", re.M)
            m = row.search(text)
            if m:
                cells = [c.strip() for c in m.group(1).split("|")]
                cells += [""] * (5 - len(cells))
                cells[idx] = status.strip()
                hdr = re.search(r"^\|\s*단위\s*\|.*$", text, re.M)
                row_txt = _row(unit, cells[:5], hdr.group(0)) if hdr else "| " + unit + " | " + " | ".join(cells[:5]) + " |"
                text = text[: m.start()] + row_txt + text[m.end():]
            else:
                cells = [""] * 5
                cells[idx] = status.strip()
                hdr = re.search(r"^\|\s*단위\s*\|.*$", text, re.M)
                new = _row(unit, cells, hdr.group(0)) if hdr else "| " + unit + " | " + " | ".join(cells) + " |"
                if re.search(r"^\|\s*\(아직 없음\)\s*\|", text, re.M):
                    text = re.sub(r"^\|\s*\(아직 없음\)\s*\|.*$", new, text, count=1, flags=re.M)
                else:
                    anchor = re.search(r"^\| 단위 .*\n\|[\s\-|]+\n", text, re.M)
                    if not anchor:
                        return "단위별 진행 표를 못 찾았다."
                    text = text[: anchor.end()] + new + "\n" + text[anchor.end():]
        label = f"CONSTRUCTION STEP {step} · {unit}"
    else:
        return "phase 는 'inception' 또는 'construction' 이다."

    text = re.sub(r"^-\s*단계\s*—\s*.*$", f"- 단계 — {label}", text, count=1, flags=re.M)
    if next_action.strip():
        text = re.sub(r"^-\s*다음에 할 일\s*—\s*.*$", f"- 다음에 할 일 — {next_action.strip()}", text, count=1, flags=re.M)
    text = re.sub(r"^-\s*마지막 갱신\s*—\s*.*$", f"- 마지막 갱신 — {_now()[:10]}", text, count=1, flags=re.M)
    STATE.write_text(text, encoding="utf-8")
    return f"상태판 갱신 — {label} · {status.strip()}"


@mcp.tool()
def aidlc_snapshot(step: str, note: str = "") -> str:
    """단계 하나가 끝난 것을 git 에 커밋한다. 상태판을 갱신한 뒤에 부른다.

    커밋 하나가 단계 하나다. 나중에 git log 로 절차를 밟은 자취를 볼 수 있고,
    되돌리고 싶으면 git 으로 되돌린다.
    """
    if not (ROOT / ".git").exists():
        chk = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=ROOT, capture_output=True, text=True)
        if chk.returncode != 0:
            return f"{ROOT} 는 git 저장소가 아니다. `git init` 이 먼저다."
    msg = f"docs: {step.strip()} 완료" + (f" — {note.strip()}" if note.strip() else "")
    # `-- .` 가 없으면 상위 저장소 전체가 스테이징된다 (git add -A 는 cwd 와 무관하다)
    subprocess.run(["git", "add", "-A", "--", "."], cwd=ROOT, capture_output=True, text=True)
    r = subprocess.run(["git", "commit", "-m", msg], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        out = (r.stdout + r.stderr).strip()
        return "커밋할 변경이 없다." if "nothing to commit" in out else f"커밋 실패:\n{out}"
    h = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    return f"커밋했다 — {h.stdout.strip()} {msg}"


if __name__ == "__main__":
    mcp.run()

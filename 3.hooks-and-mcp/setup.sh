#!/usr/bin/env bash
# AI-DLC 실습 준비 — macOS · Linux
# 이 폴더를 Kiro 로 열기 전에 한 번만 실행한다.
#   bash setup.sh
set -uo pipefail
cd "$(dirname "$0")"

ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$*"; }
note() { printf '  \033[33m·\033[0m %s\n' "$*"; }
step() { printf '\n\033[1m%s\033[0m\n' "$*"; }

printf '\n\033[1mAI-DLC 실습 준비\033[0m — macOS · Linux\n'

# uv 가 방금 깔렸을 수도 있으니 설치 위치를 미리 PATH 에 넣어둔다
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

step "1. uv — 파이썬 도구 실행기"
if command -v uv >/dev/null 2>&1; then
  ok "이미 있다 — $(uv --version)"
else
  echo "  없다. 설치한다 (https://astral.sh/uv)"
  if ! curl -LsSf https://astral.sh/uv/install.sh | sh; then
    bad "설치에 실패했다. 인터넷 연결을 확인한다."
    exit 1
  fi
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  if ! command -v uv >/dev/null 2>&1; then
    bad "설치는 됐는데 uv 를 못 찾는다. 터미널을 새로 열고 이 스크립트를 다시 실행한다."
    exit 1
  fi
  ok "설치했다 — $(uv --version)"
fi

step "2. MCP 서버가 쓸 패키지 내려받기"
if uv sync --script .kiro/mcp/aidlc_server.py >/dev/null 2>&1; then
  ok "준비됐다. Kiro 를 처음 열 때 기다리지 않는다."
else
  bad "패키지를 못 받았다. 인터넷 연결을 확인한다."
  exit 1
fi

step "3. 서버가 실제로 뜨는지"
REQ='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"setup","version":"1"}}}'
if printf '%s\n' "$REQ" | uv run --script .kiro/mcp/aidlc_server.py 2>/dev/null | grep -q '"serverInfo"'; then
  ok "aidlc 서버 응답 확인"
else
  bad "서버가 응답하지 않는다. 아래를 직접 돌려 오류를 확인한다."
  echo "      uv run --script .kiro/mcp/aidlc_server.py"
  exit 1
fi

step "4. git — 커밋과 /commit 스킬에 필요하다"
if ! command -v git >/dev/null 2>&1; then
  bash install-git.sh || true
  hash -r 2>/dev/null || true
  export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
fi

if ! command -v git >/dev/null 2>&1; then
  bad "git 을 준비하지 못했다. 커밋(aidlc_snapshot)과 /commit 스킬을 못 쓴다."
  note "직접 설치한 뒤 이 스크립트를 다시 돌린다 — https://git-scm.com/downloads"
else
  outer=$(git rev-parse --show-toplevel 2>/dev/null || true)
  here=$(pwd -P)

  # clone 으로 받았으면 이 폴더는 수업 저장소 안이다.
  # 실습 커밋이 거기 섞이지 않도록 그 저장소의 .git 을 지운다.
  # 되돌릴 수 없다. 실습은 이 폴더 하나로 끝나므로 다시 받을 일도 없다.
  if [ -n "$outer" ] && [ "$outer" != "$here" ]; then
    rm -rf "$outer/.git"
    note "수업 저장소($outer)의 .git 을 지웠다 — 그 폴더는 이제 git 저장소가 아니다"
  fi

  if [ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$here" ]; then
    ok "이미 이 폴더가 저장소다 — $here"
  else
    git init -q
    git add -A -- . >/dev/null 2>&1 && git commit -qm "chore: 실습 시작 상태" >/dev/null 2>&1
    ok "이 폴더를 저장소로 만들고 시작 상태를 커밋했다"
  fi
fi

cat <<'MSG'

준비 끝. 다음은 이렇게 한다.

  1. Kiro 에서 이 3.hooks-and-mcp 폴더를 워크스페이스 루트로 연다 (부모 폴더 아님)
  2. Steering 패널에 aidlc, MCP 패널에 aidlc 서버가 보이는지 확인한다
  3. 커밋할 때는 채팅에 "커밋해줘" 라고 하거나 /commit 을 부른다 (.kiro/skills/commit)
  4. 채팅에 만들고 싶은 것을 말투 그대로 말한다

막히면 README.md 의 3장을 본다.
MSG

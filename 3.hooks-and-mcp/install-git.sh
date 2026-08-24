#!/usr/bin/env bash
# git 설치 — macOS · Linux
# setup.sh 가 git 을 못 찾았을 때만 부른다. 단독으로 돌려도 된다.
#   bash install-git.sh
#
# 이미 있으면 아무것도 하지 않는다.
set -uo pipefail

ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$*"; }
note() { printf '  \033[33m·\033[0m %s\n' "$*"; }

# 방금 깔린 것이 여기 있을 수 있다
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

printf '\n\033[1mgit 준비\033[0m\n'

if command -v git >/dev/null 2>&1; then
  ok "이미 있다 — $(git --version)"
  exit 0
fi

note "git 이 없다. 설치한다."

case "$(uname -s)" in
  Darwin)
    if command -v brew >/dev/null 2>&1; then
      note "Homebrew 로 설치한다"
      brew install git
    else
      # 맥의 git 은 보통 Command Line Tools 에 딸려 온다. 이건 GUI 창이 뜬다.
      note "Command Line Tools 설치 창을 띄운다. 창에서 설치를 끝낸 뒤 이 스크립트를 다시 돌린다."
      xcode-select --install 2>/dev/null || true
      bad "설치 창이 끝나면 다시 실행한다 — bash install-git.sh"
      exit 1
    fi
    ;;
  Linux)
    if   command -v apt-get >/dev/null 2>&1; then sudo apt-get update -qq && sudo apt-get install -y git
    elif command -v dnf     >/dev/null 2>&1; then sudo dnf install -y git
    elif command -v yum     >/dev/null 2>&1; then sudo yum install -y git
    elif command -v pacman  >/dev/null 2>&1; then sudo pacman -Sy --noconfirm git
    elif command -v zypper  >/dev/null 2>&1; then sudo zypper install -y git
    elif command -v apk     >/dev/null 2>&1; then sudo apk add git
    else
      bad "패키지 관리자를 못 찾았다. git 을 직접 설치한다 — https://git-scm.com/downloads"
      exit 1
    fi
    ;;
  *)
    bad "이 운영체제는 자동 설치가 안 된다. https://git-scm.com/downloads"
    exit 1
    ;;
esac

hash -r 2>/dev/null || true
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

if command -v git >/dev/null 2>&1; then
  ok "설치했다 — $(git --version)"
  echo
  note "Kiro 가 켜져 있으면 껐다 켠다. 안 그러면 Kiro 안에서는 계속 git 을 못 찾는다."
  exit 0
fi

bad "설치했는데도 git 을 못 찾는다. 터미널을 새로 열고 다시 해본다."
exit 1

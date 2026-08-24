# AI-DLC 실습 준비 — Windows
# 이 폴더를 Kiro 로 열기 전에 한 번만 실행한다.
#   powershell -ExecutionPolicy Bypass -File setup.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

function Ok   { param($m) Write-Host "  OK  $m" -ForegroundColor Green }
function Bad  { param($m) Write-Host "  X   $m" -ForegroundColor Red }
function Note { param($m) Write-Host "  .   $m" -ForegroundColor Yellow }
function Step { param($m) Write-Host ""; Write-Host $m -ForegroundColor White }

Write-Host ""
Write-Host "AI-DLC 실습 준비 - Windows" -ForegroundColor White

# uv 가 방금 깔렸을 수도 있으니 설치 위치를 미리 PATH 에 넣어둔다
$env:Path = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:Path"

Step "1. uv - 파이썬 도구 실행기"
if (Get-Command uv -ErrorAction SilentlyContinue) {
    Ok "이미 있다 - $(uv --version)"
} else {
    Write-Host "  없다. 설치한다 (https://astral.sh/uv)"
    try {
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    } catch {
        Bad "설치에 실패했다. 인터넷 연결을 확인한다."
        exit 1
    }
    $env:Path = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:Path"
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Bad "설치는 됐는데 uv 를 못 찾는다. PowerShell 을 새로 열고 다시 실행한다."
        exit 1
    }
    Ok "설치했다 - $(uv --version)"
}

Step "2. MCP 서버가 쓸 패키지 내려받기"
uv sync --script .kiro\mcp\aidlc_server.py *> $null
if ($LASTEXITCODE -eq 0) {
    Ok "준비됐다. Kiro 를 처음 열 때 기다리지 않는다."
} else {
    Bad "패키지를 못 받았다. 인터넷 연결을 확인한다."
    exit 1
}

Step "3. 서버가 실제로 뜨는지"
$req = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"setup","version":"1"}}}'
$out = $req | uv run --script .kiro\mcp\aidlc_server.py 2> $null
if ($out -match '"serverInfo"') {
    Ok "aidlc 서버 응답 확인"
} else {
    Bad "서버가 응답하지 않는다. 아래를 직접 돌려 오류를 확인한다."
    Write-Host "      uv run --script .kiro\mcp\aidlc_server.py"
    exit 1
}

Step "4. git - 단계마다 커밋을 남기려면 필요하다"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Bad "git 이 없다. 커밋 기능(aidlc_snapshot)만 못 쓴다. 실습은 그대로 된다."
} else {
    $here  = $PWD.Path
    $outer = git rev-parse --show-toplevel 2> $null
    if ($outer) { $outer = $outer -replace '/', '\' }

    # clone 으로 받았으면 이 폴더는 수업 저장소 안이다.
    # 실습은 이 폴더 하나로 끝나고 다시 받을 일도 없으므로 그 연결을 끊는다.
    # 지우지 않고 이름만 바꾼다 - 잘못 돌렸으면 되돌릴 수 있어야 한다.
    if ($outer -and ($outer -ne $here)) {
        Note "여기는 저장소 안이다 - $outer"
        if (Test-Path "$outer\.git-backup") {
            Bad "$outer\.git-backup 이 이미 있다. 정리하고 다시 실행한다."
            exit 1
        }
        $ans = Read-Host "      실습용으로 그 저장소와의 연결을 끊는다 (.git -> .git-backup). 계속할까? [Y/n]"
        if ($ans -eq "" -or $ans -match '^[yY]$') {
            Rename-Item "$outer\.git" ".git-backup"
            Ok "연결을 끊었다 - 되돌리려면 Rename-Item '$outer\.git-backup' '.git'"
        } else {
            Bad "그만둔다. 이 폴더를 저장소 밖(예: 바탕화면)으로 복사한 뒤 다시 실행한다."
            exit 1
        }
    }

    $top = git rev-parse --show-toplevel 2> $null
    if ($top -and (($top -replace '/', '\') -eq $here)) {
        Ok "이미 이 폴더가 저장소다 - $here"
    } else {
        git init -q
        git add -A -- . *> $null
        git commit -qm "chore: 실습 시작 상태" *> $null
        Ok "이 폴더를 저장소로 만들고 시작 상태를 커밋했다"
    }
}

Write-Host @"

준비 끝. 다음은 이렇게 한다.

  1. Kiro 에서 이 3.hooks-and-mcp 폴더를 워크스페이스 루트로 연다 (부모 폴더 아님)
  2. Steering 패널에 aidlc, MCP 패널에 aidlc 서버가 보이는지 확인한다
  3. 채팅에 만들고 싶은 것을 말투 그대로 말한다

막히면 README.md 의 3장을 본다.
"@

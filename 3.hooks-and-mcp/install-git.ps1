# git 설치 - Windows
# setup.ps1 이 git 을 못 찾았을 때만 부른다. 단독으로 돌려도 된다.
#   powershell -ExecutionPolicy Bypass -File install-git.ps1
#
# 순서: 이미 있으면 아무것도 안 한다 -> winget -> PortableGit(관리자 권한 불필요)
$ErrorActionPreference = "Continue"

function Ok   { param($m) Write-Host "  OK  $m" -ForegroundColor Green }
function Bad  { param($m) Write-Host "  X   $m" -ForegroundColor Red }
function Note { param($m) Write-Host "  .   $m" -ForegroundColor Yellow }

# 설치 직후에는 지금 세션의 PATH 가 옛날 것이다. 레지스트리에서 다시 읽어온다.
function Sync-Path {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user    = [Environment]::GetEnvironmentVariable('Path', 'User')
    $parts   = @($machine, $user, "$env:ProgramFiles\Git\cmd") | Where-Object { $_ }
    $env:Path = $parts -join ';'
}

function Have-Git { [bool](Get-Command git -ErrorAction SilentlyContinue) }

Write-Host ""
Write-Host "git 준비" -ForegroundColor White

# --- 0. 이미 있으면 끝 -------------------------------------------------------
if (Have-Git) { Ok "이미 있다 - $(git --version)"; exit 0 }

# 깔려는 있는데 이 세션 PATH 에만 없을 수 있다
Sync-Path
if (Have-Git) { Ok "이미 있다 - $(git --version)"; exit 0 }

Note "git 이 없다. 설치한다."

# --- 1. winget ---------------------------------------------------------------
if (Get-Command winget -ErrorAction SilentlyContinue) {
    Note "winget 으로 설치를 시도한다 (관리자 확인 창이 뜰 수 있다)"
    winget install --id Git.Git -e --source winget `
        --accept-package-agreements --accept-source-agreements --silent 2>&1 | Out-Null
    Sync-Path
    if (Have-Git) {
        Ok "설치했다 - $(git --version)"
        Write-Host ""
        Note "Kiro 가 켜져 있으면 껐다 켠다. 안 그러면 Kiro 안에서는 계속 git 을 못 찾는다."
        exit 0
    }
    Note "winget 으로는 안 됐다. 관리자 권한 없이 되는 방법으로 넘어간다."
} else {
    Note "winget 이 없다. 관리자 권한 없이 되는 방법으로 넘어간다."
}

# --- 2. PortableGit — 사용자 폴더에 풀기만 한다. 관리자 권한이 필요 없다 -----
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$arch  = if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') { 'arm64' } else { '64-bit' }
$url   = $null

try {
    $rel = Invoke-RestMethod -UseBasicParsing -TimeoutSec 20 `
        -Uri 'https://api.github.com/repos/git-for-windows/git/releases/latest'
    $url = ($rel.assets | Where-Object { $_.name -like "PortableGit-*-$arch.7z.exe" } |
            Select-Object -First 1).browser_download_url
} catch {
    Note "최신 버전을 못 물어봤다. 고정 버전으로 받는다."
}
if (-not $url) {
    # API 가 막혔을 때를 위한 고정 URL. 버전을 올리려면 이 줄만 고친다.
    $url = 'https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/PortableGit-2.47.1-64-bit.7z.exe'
}

$exe = Join-Path $env:TEMP 'PortableGit-setup.7z.exe'
$dir = Join-Path $env:LOCALAPPDATA 'Programs\PortableGit'

Note "받는다 (약 70MB) - $url"
try {
    Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $exe -TimeoutSec 600
} catch {
    Bad "다운로드에 실패했다. 사내망/백신이 막았을 수 있다."
    Note "직접 받는다: https://git-scm.com/download/win"
    exit 1
}

Note "푼다 - $dir"
if (Test-Path $dir) { Remove-Item $dir -Recurse -Force -ErrorAction SilentlyContinue }
Start-Process -FilePath $exe -ArgumentList "-o`"$dir`"", "-y" -Wait -NoNewWindow
Remove-Item $exe -Force -ErrorAction SilentlyContinue

if (-not (Test-Path "$dir\cmd\git.exe")) {
    Bad "푸는 데 실패했다. 백신이 잡았을 수 있다."
    Note "직접 받는다: https://git-scm.com/download/win"
    exit 1
}

# PortableGit 은 처음 한 번 이걸 돌려야 설정이 제자리를 잡는다. 실패해도 치명적이지 않다.
if (Test-Path "$dir\post-install.bat") {
    Start-Process -FilePath "$dir\post-install.bat" -WorkingDirectory $dir -Wait -WindowStyle Hidden -ErrorAction SilentlyContinue
}

# PATH 에 넣는다. 이 세션과, 다음에 여는 창 모두.
$userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($userPath -notlike "*$dir\cmd*") {
    [Environment]::SetEnvironmentVariable('Path', "$userPath;$dir\cmd", 'User')
}
$env:Path = "$env:Path;$dir\cmd"

if (Have-Git) {
    Ok "설치했다 - $(git --version)"
    Write-Host ""
    Note "Kiro 가 켜져 있으면 껐다 켠다. 안 그러면 Kiro 안에서는 계속 git 을 못 찾는다."
    exit 0
}

Bad "설치했는데도 git 을 못 찾는다. 터미널을 새로 열고 다시 해본다."
exit 1

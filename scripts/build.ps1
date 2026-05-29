$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path "venv\Scripts\python.exe")) {
    python -m venv venv
}

& "venv\Scripts\pip.exe" install -q -r requirements-build.txt
& "venv\Scripts\pyinstaller.exe" --noconfirm oral_calc.spec

Write-Host ""
Write-Host "Build complete: dist\口算练习系统.exe" -ForegroundColor Green

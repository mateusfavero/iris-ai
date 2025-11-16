<#
Run backend (Flask) using the venv Python directly to avoid Activate.ps1 ExecutionPolicy issues.

Usage:
  # from PowerShell (current folder: backend-example)
  powershell -ExecutionPolicy Bypass -File .\run-backend.ps1

What the script does:
  - ensures the virtualenv Python exists (.venv) and prints instructions if missing
  - upgrades pip/tools inside the venv
  - installs requirements from requirements.txt (if needed)
  - runs `python app.py` using the venv python

This approach does NOT require sourcing Activate.ps1 and works even when script execution
is restricted for the current user.
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Virtual environment Python not found at: $VenvPython" -ForegroundColor Yellow
    Write-Host "Create a venv first (from project root):" -ForegroundColor Yellow
    Write-Host "  python -m venv backend-example/.venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "Using venv python: $VenvPython"

Write-Host "Upgrading pip, setuptools and wheel inside venv..."
& $VenvPython -m pip install --upgrade pip setuptools wheel setuptools_scm packaging

if (Test-Path (Join-Path $ScriptDir 'requirements.txt')) {
    Write-Host "Installing requirements from requirements.txt (may skip already-installed packages)..."
    & $VenvPython -m pip install -r (Join-Path $ScriptDir 'requirements.txt')
} else {
    Write-Host "No requirements.txt found in $ScriptDir, skipping install." -ForegroundColor Yellow
}

Write-Host "Starting Flask app (app.py) using venv python..."
& $VenvPython (Join-Path $ScriptDir 'app.py')

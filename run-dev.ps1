<#
run-dev.ps1

Abre o backend (Flask) em uma nova janela do PowerShell usando o Python do venv
e inicia o Vite (frontend) na janela atual. Evita necessidade de executar
`Activate.ps1` (que pode ser bloqueado por ExecutionPolicy).

Execute assim (na raiz do projeto):
  powershell -ExecutionPolicy Bypass -File .\run-dev.ps1

#>

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $RepoRoot 'backend-example'
$VenvPython = Join-Path $BackendDir '.venv\Scripts\python.exe'

if (-not (Test-Path $VenvPython)) {
    Write-Host "Virtualenv python não encontrado em: $VenvPython" -ForegroundColor Yellow
    Write-Host "Crie o venv em backend-example primeiro (do repo root):" -ForegroundColor Yellow
    Write-Host "  python -m venv backend-example/.venv" -ForegroundColor Yellow
    Write-Host "Depois rode: powershell -ExecutionPolicy Bypass -File .\\run-dev.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host "Iniciando backend em nova janela (usando: $VenvPython)" -ForegroundColor Green

# Comando para rodar no novo PowerShell
$backendCommand = "Set-Location -Path '$BackendDir'; & '$VenvPython' 'app.py'"

Start-Process powershell -ArgumentList @('-NoExit','-ExecutionPolicy','Bypass','-Command',$backendCommand)

Start-Sleep -Seconds 1

Write-Host "Iniciando frontend (Vite) na janela atual..." -ForegroundColor Green
Set-Location -Path $RepoRoot

# Use npm.cmd para evitar problemas com alias curl/powershell
npm.cmd run dev

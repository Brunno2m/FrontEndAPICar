param(
    [switch]$InstallOnly
)

# Script para configurar e iniciar o ambiente de desenvolvimento (Windows PowerShell)
# - Cria um venv em .venv se não existir
# - Ativa o venv
# - Instala dependências
# - Inicia app.py

$venvPath = Join-Path $PSScriptRoot '.venv'
$python = Join-Path $venvPath 'Scripts\python.exe'
$activate = Join-Path $venvPath 'Scripts\Activate.ps1'

Write-Host "Run-dev iniciado..." -ForegroundColor Cyan

if (-not (Test-Path $venvPath)) {
    Write-Host "Criando venv em .venv..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "Virtualenv já existe em .venv" -ForegroundColor Green
}

Write-Host "Ativando venv..." -ForegroundColor Cyan
. $activate

Write-Host "Instalando dependências..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($InstallOnly) {
    Write-Host "Instalação concluída (modo apenas instalação)." -ForegroundColor Green
    return
}

Write-Host "Iniciando app.py..." -ForegroundColor Cyan
& $python -u app.py

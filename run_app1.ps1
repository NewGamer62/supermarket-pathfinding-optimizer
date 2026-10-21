# Lanceur PowerShell - Éditeur Spatial (App 1)
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Lancement de l'Éditeur Spatial (premiereApp)..." -ForegroundColor Cyan
Set-Location -Path "$ScriptDir\premiereApp"
python main.py

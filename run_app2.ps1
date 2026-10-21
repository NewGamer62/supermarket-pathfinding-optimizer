# Lanceur PowerShell - Calculateur de Parcours (App 2)
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Lancement du Calculateur de Parcours (deuxiemeApp)..." -ForegroundColor Cyan
Set-Location -Path "$ScriptDir\deuxiemeApp"
python mainApp2.py

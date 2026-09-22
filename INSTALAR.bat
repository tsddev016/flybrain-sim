@echo off
chcp 65001 >nul
title FlyBrain Simulator - Instalador
color 0B
echo.
echo  ============================================
echo    FlyBrain Simulator - Instalador Windows
echo  ============================================
echo.

set "APPDIR=%~dp0"
cd /d "%APPDIR%"

echo  [1/3] Verificando Python...
python --version 2>nul
if errorlevel 1 (
  echo.
  echo  [ERRO] Python nao encontrado no PATH.
  echo  Baixe em https://www.python.org/downloads/
  echo  Na instalacao, marque: "Add python.exe to PATH"
  echo.
  pause
  exit /b 1
)
echo  OK.
echo.

echo  [2/3] Instalando pygame e numpy...
python -m pip install -r requirements.txt -q
if errorlevel 1 (
  echo  [ERRO] Nao foi possivel instalar as bibliotecas.
  pause
  exit /b 1
)
python -c "import pygame,numpy; print('  Bibliotecas OK')"
echo.

echo  [3/3] Criando atalho na Area de Trabalho...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$desktop = [Environment]::GetFolderPath('Desktop'); ^
   if (-not (Test-Path $desktop)) { $desktop = Join-Path $env:USERPROFILE 'Desktop' }; ^
   $target = Join-Path '%APPDIR%' 'FlyBrain.bat'; ^
   $ws = New-Object -ComObject WScript.Shell; ^
   $path = Join-Path $desktop 'FlyBrain Simulator.lnk'; ^
   $lnk = $ws.CreateShortcut($path); ^
   $lnk.TargetPath = $target; ^
   $lnk.WorkingDirectory = '%APPDIR%'; ^
   $lnk.WindowStyle = 7; ^
   $lnk.Description = 'FlyBrain Simulator 2D - mosca artificial'; ^
   $lnk.Save(); ^
   Write-Host ('  Atalho: ' + $path)"

echo.
echo  ============================================
echo    Pronto!
echo.
echo    Clique duas vezes no atalho:
echo      FlyBrain Simulator
echo    na Area de Trabalho.
echo  ============================================
echo.
pause

@echo off
chcp 65001 >nul
set "APPDIR=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$desktop = [Environment]::GetFolderPath('Desktop'); ^
   $ws = New-Object -ComObject WScript.Shell; ^
   $lnk = $ws.CreateShortcut((Join-Path $desktop 'FlyBrain Simulator.lnk')); ^
   $lnk.TargetPath = '%APPDIR%FlyBrain.bat'; ^
   $lnk.WorkingDirectory = '%APPDIR%'; ^
   $lnk.WindowStyle = 7; ^
   $lnk.Description = 'FlyBrain Simulator 2D'; ^
   $lnk.Save(); ^
   Write-Host 'Atalho criado na Area de Trabalho.'"
echo.
pause

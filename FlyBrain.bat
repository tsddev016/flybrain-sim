@echo off
cd /d "%~dp0"
wscript //nologo "%~dp0FlyBrain_Silent.vbs"
if errorlevel 1 (
  pythonw "%~dp0FlyBrain.pyw"
)
if errorlevel 1 (
  python "%~dp0main.py"
  pause
)

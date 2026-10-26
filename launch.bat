@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m zenith %*
) else (
  python -m zenith %*
)
if errorlevel 1 pause

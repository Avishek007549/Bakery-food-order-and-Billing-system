@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"

if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 -m venv .venv
  ) else (
    where python >nul 2>nul
    if errorlevel 1 (
      echo Python 3 is required. Install Python 3 and try again.
      exit /b 1
    )
    python -m venv .venv
  )
  if errorlevel 1 (
    echo Could not create the local Python environment.
    exit /b 1
  )
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Could not install required Python packages.
  exit /b 1
)

".venv\Scripts\python.exe" server.py

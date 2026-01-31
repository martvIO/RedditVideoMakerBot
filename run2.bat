@echo off
REM Change directory to where main.py is located
cd /d %~dp0

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Run the Python script
python check.py

REM Pause to keep the window open if it was double-clicked
pause

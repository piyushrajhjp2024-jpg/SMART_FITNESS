@echo off
set FLASK_ENV=local
cd /d "%~dp0"
".venv\Scripts\python.exe" app.py

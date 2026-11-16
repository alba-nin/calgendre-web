@echo off
REM Doble clic per obrir l actualitzador (si no s ha fet el .exe)
cd /d "%~dp0"
start "" pythonw actualitza_cataleg.py

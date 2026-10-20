@echo off
setlocal
cd /d "%~dp0"
py -3.11 -X utf8 package_release.py
if errorlevel 1 exit /b 1
pause

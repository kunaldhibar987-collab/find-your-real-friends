@echo off
setlocal
cd /d "%~dp0"
echo.
echo This static server is optional.
echo For the complete database-connected version, run START-BACKEND.bat and open:
echo http://127.0.0.1:8000/
echo.
python -m http.server 5500
pause

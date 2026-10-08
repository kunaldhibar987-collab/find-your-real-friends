@echo off
setlocal
cd /d "%~dp0backend"
echo.
echo ================================================
echo   FIND YOUR REAL FRIEND - LOCAL SERVER
 echo ================================================
echo.
echo Website : http://127.0.0.1:8000/
echo API     : http://127.0.0.1:8000/api/health
echo Docs    : http://127.0.0.1:8000/docs
echo Database: backend/findyourfriend.db (created automatically)
echo.
py -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause

@echo off
echo =========================================================
echo            Starting AI Item Manager API Server
echo =========================================================

:: 가상환경 활성화
echo Activating Virtual environment...
echo =========================================================
call .venv\Scripts\activate.bat

:: 활성화 확인
echo Virtual environment activated
echo =========================================================

:: 서버 실행
echo Initializing API server... This may take a few seconds.
echo =========================================================
python YIM.py

:: 혹시 오류로 종료되었을 때 바로 닫히지 않도록
pause
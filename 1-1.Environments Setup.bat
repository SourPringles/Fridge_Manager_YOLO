@echo off
echo =========================================================
echo            Starting YOLO Item Manager API Server
echo                    Environments Setup
echo =========================================================

:: 가상환경 생성
echo Generating Virtual environment...
echo =========================================================
python -m venv .venv
echo Virtual environment created
echo =========================================================

:: 가상환경 활성화
echo Activating Virtual environment...
echo =========================================================
call .venv\Scripts\activate.bat

:: dependencies 설치
echo Installing dependencies... This may take a few minutes...
echo =========================================================
pip install -r requirements.txt
echo Dependencies installed
echo =========================================================

echo Environments setup completed
pause


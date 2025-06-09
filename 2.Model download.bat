@echo off
echo =========================================================
echo            Starting YOLO Item Manager API Server
echo                    Model Download
echo =========================================================

:: 가상환경 활성화
echo Activating Virtual environment...
echo =========================================================
call .venv\Scripts\activate.bat

:: model 다운로드
echo Downloading models... This may take a few minutes...
echo =========================================================
python download_model.py
echo =========================================================

echo Model download completed
pause


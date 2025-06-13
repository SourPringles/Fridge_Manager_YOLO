@echo off
echo =========================================================
echo            Starting YOLO Item Manager API Server
echo                    CUDA Installation
echo =========================================================

:: 가상환경 활성화
echo Activating Virtual environment...
echo =========================================================
call .venv\Scripts\activate.bat

pip install torch==2.6.0+cu124 torchvision==0.21.0+cu124 --index-url https://download.pytorch.org/whl/cu124

echo CUDA installation completed
pause


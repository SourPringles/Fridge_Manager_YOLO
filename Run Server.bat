@echo off
echo ===================================
echo Starting AI Item Manager API Server
echo ===================================

:: 가상환경 활성화
call AIMA_env\Scripts\activate.bat

:: 활성화 확인
echo Virtual environment activated

:: 서버 실행
python app.py

:: 혹시 오류로 종료되었을 때 바로 닫히지 않도록
pause
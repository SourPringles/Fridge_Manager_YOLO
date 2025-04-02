from flask import jsonify
import traceback
import sqlite3
import logging

# 로깅 설정
logging.basicConfig(
    filename='AIMA_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def handle_exception(e):
    """일반적인 예외를 처리하고 적절한 응답을 반환합니다"""
    error_message = str(e)
    error_traceback = traceback.format_exc()

    print(f"Error: {jsonify(error_message)}")
    
    # 에러 로깅
    logging.error(f"Error: {error_message}\nTraceback: {error_traceback}")
    
    # 특정 예외 유형에 따른 처리
    if isinstance(e, sqlite3.Error):
        return jsonify({"error": "Database error", "message": error_message}), 500
    elif isinstance(e, ValueError):
        return jsonify({"error": "Invalid data", "message": error_message}), 400
    elif isinstance(e, FileNotFoundError):
        return jsonify({"error": "File not found", "message": error_message}), 404
    else:
        # 기타 모든 예외
        return jsonify({"error": "Server error", "message": "An unexpected error occurred"}), 500
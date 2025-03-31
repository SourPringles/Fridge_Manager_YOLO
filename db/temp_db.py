import sqlite3
from .commons_db import *

def load_temp():
    """
    데이터베이스(temp)에서 임시 반출 목록 로드
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM temp')
    rows = cursor.fetchall()
    conn.close()
    temp = {row[0]: {"takeout_time": row[1], "nickname": row[2]} for row in rows}
    return temp

def update_temp(qr_code, takeout_time, nickname):
    """
    데이터베이스(temp)에 항목 저장 또는 업데이트
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO temp (qr_code, takeout_time, nickname)
        VALUES (?, ?, ?)
    ''', (qr_code, takeout_time, nickname))
    conn.commit()
    conn.close()

def delete_temp(qr_code):
    """
    데이터베이스(temp)에서 항목 삭제
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM temp WHERE qr_code = ?', (qr_code,))
    conn.commit()
    conn.close()
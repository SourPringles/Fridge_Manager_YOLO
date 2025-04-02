import sqlite3
from .commons_db import *

def load_storage():
    """
    데이터베이스(storage)에서 인벤토리 로드
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM storage')
    rows = cursor.fetchall()
    conn.close()
    storage = {row[0]: {"x": row[1], "y": row[2], "lastChecked": row[3], "nickname": row[4]} for row in rows}
    return storage

def update_storage(qr_code, data):
    """
    데이터베이스(storage)에 항목 저장 또는 업데이트
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO storage (qr_code, x, y, lastChecked, nickname)
        VALUES (?, ?, ?, ?, ?)
    ''', (qr_code, data["x"], data["y"], data["lastChecked"], data["nickname"]))
    conn.commit()
    conn.close()

def delete_storage(qr_code):
    """
    데이터베이스(storage)에서 항목 삭제
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM storage WHERE qr_code = ?', (qr_code,))
    conn.commit()
    conn.close()
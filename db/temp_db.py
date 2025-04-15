import sqlite3
from .commons_db import *

def load_temp():
    """
    데이터베이스(tempV2)에서 임시 반출 목록 로드
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tempV2')
    rows = cursor.fetchall()
    conn.close()
    temp = []
    for row in rows:
        temp.append({"id": row[0], "image": row[1], "timestamp": row[2], "nickname": row[3]})

    return temp

def update_temp(id, image, timestamp, nickname):
    """
    데이터베이스(tempV2)에 항목 저장 또는 업데이트
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO tempV2 (id, image, timestamp, nickname)
        VALUES (?, ?, ?)
    ''', (id, image, timestamp, nickname))
    conn.commit()
    conn.close()

def delete_temp(id):
    """
    데이터베이스(tempV2)에서 항목 삭제
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM temp WHERE id = ?', (id))
    conn.commit()
    conn.close()
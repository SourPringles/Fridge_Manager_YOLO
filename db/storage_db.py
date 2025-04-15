import sqlite3
from .commons_db import *

def load_storage():
    """
    데이터베이스(storageV2)에서 인벤토리 로드
    """
    storage = []
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM storageV2')
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        storage.append({"id": row[0], "image": row[1], "x": row[2], "y": row[3], "timestamp": row[4], "nickname": row[5]})

    return storage

def update_storage(data):
    """
    데이터베이스(storageV2)에 항목 저장 또는 업데이트
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO storageV2 (image, x, y, timestamp, nickname)
        VALUES (?, ?, ?, ?, ?)
    ''', (data["image"], data["x"], data["y"], data["timestamp"], data["nickname"]))
    conn.commit()
    conn.close()

def delete_storage(id):
    """
    데이터베이스(storageV2)에서 항목 삭제
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM storageV2 WHERE id = ?', (id))
    conn.commit()
    conn.close()
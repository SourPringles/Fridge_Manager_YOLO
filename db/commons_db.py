import sqlite3
import os

DB_FILE = "./db/userdata.db"

def _get_connection():
    """데이터베이스 연결을 가져옵니다."""
    # db 폴더가 없으면 생성
    db_dir = os.path.dirname(DB_FILE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    # 연결 객체 반환
    return sqlite3.connect(DB_FILE)

def _create_tables(cursor):
    """storage 및 temp 테이블을 생성합니다 (존재하지 않는 경우)."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            x INTEGER,
            y INTEGER,
            timestamp TEXT,
            nickname TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image TEXT,
            timestamp TEXT,
            nickname TEXT
        )
    ''')

def init_db():
    """
    데이터베이스 초기화: storage 테이블, temp 테이블 (존재하지 않는 경우 생성)
    """
    # with 문을 사용하여 연결 자동 관리
    try:
        with _get_connection() as conn:
            cursor = conn.cursor()
            _create_tables(cursor)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

def reset_db():
    """
    데이터베이스 초기화: storage 테이블, temp 테이블 삭제 후 재생성
    """
    # with 문을 사용하여 연결 자동 관리
    try:
        with _get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DROP TABLE IF EXISTS storage')
            cursor.execute('DROP TABLE IF EXISTS temp')
            _create_tables(cursor)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database reset error: {e}")
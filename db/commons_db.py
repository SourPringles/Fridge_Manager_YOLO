import sqlite3

DB_FILE = "./db/userdata.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

def init_db():
    """
    데이터베이스 초기화: storageV2 테이블 생성, tempV2 테이블 생성
    """
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storageV2 (
            id INTEGER PRIMARY KEY autoincrement,
            image TEXT,
            x INTEGER,
            y INTEGER,
            timestamp TEXT,
            nickname TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tempV2 (
            id INTEGER PRIMARY KEY autoincrement,
            image TEXT,
            timestamp TEXT,
            nickname TEXT
        )
    ''')
    conn.commit()
    conn.close()

def reset_db():
    """
    데이터베이스 초기화: storage 테이블, temp 테이블
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS storageV2')
    cursor.execute('DROP TABLE IF EXISTS tempV2')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS storageV2 (
            id INTEGER PRIMARY KEY autoincrement,
            image TEXT,
            x INTEGER,
            y INTEGER,
            timestamp TEXT,
            nickname TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tempV2 (
            id INTEGER PRIMARY KEY autoincrement,
            image TEXT,
            timestamp TEXT,
            nickname TEXT
        )
    ''')

    conn.commit()
    conn.close()
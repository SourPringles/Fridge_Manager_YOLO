import sqlite3
from .commons_db import _get_connection # 명시적 임포트 또는 * 사용 유지

def load_storage():
    """
    데이터베이스(storage)에서 인벤토리 로드
    """
    storage = []
    try:
        # with 문으로 연결 관리
        with _get_connection() as conn:
            conn.row_factory = sqlite3.Row # 결과를 딕셔너리처럼 접근 가능하게 설정
            cursor = conn.cursor()
            # 테이블 이름 수정: storageV2 -> storage
            cursor.execute('SELECT uuid, x, y, timestamp, nickname FROM storage')
            rows = cursor.fetchall()
            # row_factory 사용 시 더 간결하게 변환 가능
            for row in rows:
                storage.append(dict(row))
    except sqlite3.Error as e:
        print(f"Error loading storage: {e}")
        # 필요시 빈 리스트 대신 None 반환 또는 예외 재발생 고려
    return storage

def update_storage(data):
    """
    데이터베이스(storage)에 항목 저장 또는 업데이트 (ID는 자동 관리)
    """
    try:
        # with 문으로 연결 관리
        with _get_connection() as conn:
            cursor = conn.cursor()
            # 테이블 이름 수정: storageV2 -> storage
            cursor.execute('''
                INSERT OR REPLACE INTO storage (uuid, x, y, timestamp, nickname)
                VALUES (?, ?, ?, ?, ?)
            ''', (data["uuid"], data["x"], data["y"], data["timestamp"], data["nickname"]))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating storage: {e}")
    except KeyError as e:
        print(f"Error updating storage: Missing key {e} in data")

def delete_storage(uuid):
    """
    데이터베이스(storage)에서 ID로 항목 삭제
    """
    try:
        # with 문으로 연결 관리
        with _get_connection() as conn:
            cursor = conn.cursor()
            # 테이블 이름 수정: storageV2 -> storage
            cursor.execute('DELETE FROM storage WHERE uuid = ?', (uuid,)) # 변수명 id -> item_id (명확성)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting storage item with uuid {uuid}: {e}")
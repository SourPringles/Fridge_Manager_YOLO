import sqlite3
from .commons_db import _get_connection # 명시적 임포트 또는 * 사용 유지

def load_temp():
    """
    데이터베이스(temp)에서 임시 반출 목록 로드
    """
    temp = []
    try:
        # with 문으로 연결 관리
        with _get_connection() as conn:
            conn.row_factory = sqlite3.Row # 결과를 딕셔너리처럼 접근 가능하게 설정
            cursor = conn.cursor()
            # 테이블 이름 수정: tempV2 -> temp
            cursor.execute('SELECT uuid, timestamp, nickname FROM temp')
            rows = cursor.fetchall()
            # row_factory 사용 시 더 간결하게 변환 가능
            for row in rows:
                temp.append(dict(row))
    except sqlite3.Error as e:
        print(f"Error loading temp: {e}")
    return temp

def update_temp(data):
    """
    데이터베이스(temp)에 항목 저장 또는 업데이트 (ID는 자동 관리)
    """
    try:
        # with 문으로 연결 관리
        with _get_connection() as conn:
            cursor = conn.cursor()
            # 테이블 이름 수정: tempV2 -> temp
            # 함수 시그니처 변경: 개별 인자 -> data 딕셔너리
            cursor.execute('''
                INSERT OR REPLACE INTO temp (uuid, timestamp, nickname)
                VALUES (?, ?, ?)
            ''', (data["uuid"], data["timestamp"], data["nickname"]))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error updating temp: {e}")
    except KeyError as e:
        print(f"Error updating temp: Missing key {e} in data")


def delete_temp(uuid):
    """
    데이터베이스(temp)에서 ID로 항목 삭제
    """
    try:
        # with 문으로 연결 관리
        with _get_connection() as conn:
            cursor = conn.cursor()
            # 테이블 이름은 이미 'temp'로 올바름
            cursor.execute('DELETE FROM temp WHERE uuid = ?', (uuid,)) # 변수명 id -> item_id (명확성)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting temp item with id {uuid}: {e}")
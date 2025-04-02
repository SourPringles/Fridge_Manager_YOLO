from flask import Blueprint, jsonify
from db import load_storage # db로딩함수
from utils import handle_exception # 에러 핸들링 함수

getStorage_bp = Blueprint('getStorage', __name__)

def get_storage_data():
    """
    재고목록 반환
    """
    data = load_storage()

    storage = {
        key: {
            "nickname": value.get("nickname", "N/A"),
            "x": value["x"],
            "y": value["y"],
            "lastChecked": value.get("lastChecked", "N/A"),
            "qr_code": key
        }
        for key, value in data.items()
    }
    return storage

@getStorage_bp.route('/getStorage', methods=['GET'])
def get_storage():
    """
    API 엔드포인트
    """
    try:
        storage = get_storage_data()
        return jsonify(storage)
    except Exception as e:
        return handle_exception(e)
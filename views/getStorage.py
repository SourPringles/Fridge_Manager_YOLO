from flask import Blueprint, jsonify
from db import load_storage # db로딩함수

getStorage_bp = Blueprint('getStorage', __name__)

@getStorage_bp.route('/getStorage', methods=['GET'])
def get_storage():
    """
    재고목록 반환
    """
    data = load_storage()

    storage = {
        key: {
            "nickname": value.get("nickname", "N/A"),
            "x": value["x"],
            "y": value["y"],
            "lastModified": value.get("lastModified", "N/A"),
            "qr_code": key
        }
        for key, value in data.items()
    }
    return jsonify(storage)
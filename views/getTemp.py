from flask import Blueprint, jsonify
from db import load_temp # db로딩함수

getTemp_bp = Blueprint('getTemp', __name__)

def get_temp_data():
    """
    임시반출목록 반환
    """
    data = load_temp()

    temp = {
        key: {
            "nickname": value.get("nickname", "N/A"),
            "takeout_time": value.get("takeout_time", "N/A"),
            "qr_code": key
        }
        for key, value in data.items()
    }
    return temp

@getTemp_bp.route('/getTemp', methods=['GET'])
def get_temp():
    """
    API 엔드포인트
    """
    temp = get_temp_data()
    return jsonify(temp)

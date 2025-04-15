from flask import Blueprint, jsonify
from db import load_temp # db로딩함수

getTemp_bp = Blueprint('getTemp', __name__)

@getTemp_bp.route('/getTemp', methods=['GET'])
def get_temp():
    """
    API 엔드포인트
    """
    temp = load_temp()
    return jsonify(temp)

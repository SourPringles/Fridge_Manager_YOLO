from flask import Blueprint, jsonify
from db import load_storage # db로딩함수

getStorage_bp = Blueprint('getStorage', __name__)

@getStorage_bp.route('/getStorage', methods=['GET'])
def get_storage():
    """
    API 엔드포인트
    """
    storage = load_storage()
    return jsonify(storage)
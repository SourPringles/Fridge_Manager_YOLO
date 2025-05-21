# library
from flask import Blueprint, jsonify

# custom modules
from db import load_storage, load_temp

getStorage_bp = Blueprint('getStorage', __name__)
getTemp_bp = Blueprint('getTemp', __name__)
getAll_bp = Blueprint('getAll', __name__)

@getStorage_bp.route('/getStorage', methods=['GET'])
def get_storage():
    """
    API 엔드포인트
    """
    storage = load_storage()
    return jsonify(storage)

@getTemp_bp.route('/getTemp', methods=['GET'])
def get_temp():
    """
    API 엔드포인트
    """
    temp = load_temp()
    return jsonify(temp)

@getAll_bp.route('/getAll', methods=['GET'])
def get_all():
    """
    전체 데이터 반환
    """
    return jsonify({
        "storage": load_storage(),
        "temp": load_temp()
    })

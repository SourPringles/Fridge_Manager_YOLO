# library
from flask import Blueprint, jsonify

# custom modules
from db import load_storage, load_temp

getAll_bp = Blueprint('getAll', __name__)

@getAll_bp.route('/getAll', methods=['GET'])
def get_all():
    """
    전체 데이터 반환
    """
    return jsonify({
        "storage": load_storage(),
        "temp": load_temp()
    })

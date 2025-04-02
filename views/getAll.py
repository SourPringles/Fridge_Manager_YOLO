from flask import Blueprint, jsonify
from .getStorage import get_storage_data
from .getTemp import get_temp_data
from utils import handle_exception # 에러 핸들링 함수

getAll_bp = Blueprint('getAll', __name__)

@getAll_bp.route('/getAll', methods=['GET'])
def get_all():
    """
    전체 데이터 반환
    """
    try:
        return jsonify({
            "storage": get_storage_data(),
            "temp": get_temp_data()
        })
    except Exception as e:
        return handle_exception(e)
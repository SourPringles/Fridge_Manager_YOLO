from flask import Blueprint, jsonify
from db import reset_db, load_storage, load_temp

reset_bp = Blueprint('reset', __name__)

@reset_bp.route('/reset', methods=['GET'])
def reset_storage():
    """
    DB리셋 엔드포인트 (DEBUG)
    """
    reset_db()

    storage = load_storage()
    temp = load_temp()

    return jsonify({"message": "storage has been reset.", "storage": storage, "temp": temp}), 200
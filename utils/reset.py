from flask import Blueprint, jsonify
from db import load_storage, delete_storage, load_temp, delete_temp

reset_bp = Blueprint('reset', __name__)

@reset_bp.route('/reset', methods=['GET'])
def reset_storage():
    """
    DB리셋 엔드포인트 (DEBUG)
    """
    delete_storage("*")  # Clear all entries in the database
    delete_temp("*")
    storage = load_storage()
    temp = load_temp()
    return jsonify({"message": "Inventory has been reset.", "storage": storage, "temp": temp}), 200
from flask import Blueprint, jsonify
from db import load_storage, delete_storage

reset_bp = Blueprint('reset', __name__)

@reset_bp.route('/reset', methods=['POST'])
def reset_storage():
    """
    DB리셋 엔드포인트 (DEBUG)
    """
    delete_storage("*")  # Clear all entries in the database
    inventory = load_storage()
    return jsonify({"message": "Inventory has been reset.", "inventory": inventory})
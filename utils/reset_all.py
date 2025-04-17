# Base Librarys
import os
import shutil

# Libraries
from flask import Blueprint, jsonify

# Custom Modules
from db import reset_db, load_storage, load_temp


reset_bp = Blueprint('reset', __name__)
folders = ["storage", "temp", "new"]

@reset_bp.route('/reset', methods=['GET'])
def reset_storage():
    """
    DB리셋 엔드포인트 (DEBUG)
    """
    reset_db()

    storage = load_storage()
    temp = load_temp()

    for folder in folders:
        _reset_work(folder)

    return jsonify({"message": "storage has been reset.", "storage": storage, "temp": temp}), 200

def _reset_work(str):
    if os.path.exists(f"./db/imgs/{str}"):
        shutil.rmtree(f"./db/imgs/{str}")
        os.mkdir(f"./db/imgs/{str}")
    else:
        os.mkdir(f"./db/imgs/{str}")
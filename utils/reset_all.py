# Base Librarys
import os
import shutil

# Libraries
from flask import Blueprint, jsonify

# Custom Modules
from db import reset_db, load_storage, load_temp
from utils.settings import BASEIMGDIR

reset_bp = Blueprint('reset', __name__)

base_dir = BASEIMGDIR
storage_img_dir = os.path.join(base_dir, "storage")
temp_img_dir = os.path.join(base_dir, "temp")
new_img_dir = os.path.join(base_dir, "new")

folders = [storage_img_dir, temp_img_dir, new_img_dir]

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
    if os.path.exists(str):
        shutil.rmtree(str)
        os.mkdir(str)
    else:
        os.mkdir(str)
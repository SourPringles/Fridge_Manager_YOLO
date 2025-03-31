from flask import Blueprint, request, jsonify
from db import load_storage, update_storage, delete_storage
from utils import save_log, detect_qr_codes, compare_storages
from datetime import datetime
import cv2
import numpy as np

updateStorage_bp = Blueprint('updateStorage', __name__)

@updateStorage_bp.route('/updateStorage', methods=['POST'])
def upload():
    curr_img = request.files.get('source')

    if not curr_img:
        return jsonify({"error": "Current image is required."}), 400

    curr_image = cv2.imdecode(np.frombuffer(curr_img.read(), np.uint8), cv2.IMREAD_COLOR)

    # 이전 데이터 로드
    storage = load_storage()
    prev_data = storage.copy()

    # QR코드 인식
    new_data = detect_qr_codes(curr_image)

    # 데이터 비교
    added, removed, moved = compare_storages(prev_data, new_data)

    # 현재 시각 추가
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 전체 인벤토리 갱신
    for qr_text, value in removed.items():
        delete_storage(qr_text)

    for qr_text, value in added.items():
        if qr_text not in storage:
            new_item = {
                "x": value["x"],
                "y": value["y"],
                "lastModified": current_timestamp,
                "nickname": "New Item!"
            }
            update_storage(qr_text, new_item)

    for qr_text, data in moved.items():
        if qr_text in storage:
            updated_item = {
                "x": data["current"]["x"],
                "y": data["current"]["y"],
                "lastModified": current_timestamp,
                "nickname": storage[qr_text]["nickname"]
            }
            update_storage(qr_text, updated_item)

    # 로그 저장
    save_log("Upload endpoint called", added=added, removed=removed, moved=moved)

    return jsonify({
        "added": added,
        "removed": removed,
        "moved": moved,
    })
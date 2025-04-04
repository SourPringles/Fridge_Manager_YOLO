from flask import Blueprint, request, jsonify
from db import load_storage, update_storage, delete_storage, load_temp, update_temp, delete_temp
from utils import save_log, compare_storages
from imageProcesser import detect_qr_codes_pyzbar
from datetime import datetime
import cv2
import numpy as np

from utils.settings import takeoutTimeValue

def create_item(x, y, timestamp, nickname="New Item!"):
    """
    인벤토리 아이템 객체를 생성하는 팩토리 함수
    
    Args:
        x: x 좌표
        y: y 좌표
        timestamp: 마지막 확인 시간
        nickname: 아이템 별칭 (기본값: "New Item!")
        
    Returns:
        dict: 인벤토리 아이템 객체
    """
    return {
        "x": x,
        "y": y,
        "lastChecked": timestamp,
        "nickname": nickname
    }

updateStorage_bp = Blueprint('updateStorage', __name__)

@updateStorage_bp.route('/updateStorage', methods=['POST'])
def updateStorage():
    source = request.files.get('source')

    if not source:
        return jsonify({"error": "Current image is required."}), 400

    curr_image = cv2.imdecode(np.frombuffer(source.read(), np.uint8), cv2.IMREAD_COLOR)

    # 이전 데이터 로드
    storage = load_storage()
    temp = load_temp()
    prev_data = storage.copy()

    # QR코드 인식
    new_data = detect_qr_codes_pyzbar(curr_image)

    # 데이터 비교
    added, removed, moved = compare_storages(prev_data, new_data)

    # 현재 시각 추가
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 전체 인벤토리 갱신
    for qr_text, value in removed.items():
        delete_storage(qr_text)
        update_temp(qr_text, current_timestamp, value["nickname"])

    for qr_text, value in added.items():
        # QR코드가 현재 storage 안에 없을 때
        if qr_text not in storage:
            # QR코드가 temp에 있을 때
            if qr_text in temp:
                print("0")
                # 해당되는 항목(temp 내의 항목)이 반출된 지 2시간 이하일 때
                if (datetime.now() - datetime.strptime(temp[qr_text]["takeout_time"], "%Y-%m-%d %H:%M:%S")).total_seconds() < takeoutTimeValue:
                    # temp에 있는 항목을 storage에 업데이트
                    new_item = {
                        "x": value["x"],
                        "y": value["y"],
                        "lastChecked": current_timestamp,
                        "nickname": temp[qr_text]["nickname"]
                    }
                    update_storage(qr_text, new_item)
                else:
                    # 현재 반입된 QR코드를 신규로써 삽입
                    new_item = {
                        "x": value["x"],
                        "y": value["y"],
                        "lastChecked": current_timestamp,
                        "nickname": "New Item!"
                    }
                update_storage(qr_text, new_item)
                delete_temp(qr_text)

            else:
                print("1")
                new_item = {
                    "x": value["x"],
                    "y": value["y"],
                    "lastChecked": current_timestamp,
                    "nickname": "New Item!"
                }
                update_storage(qr_text, new_item)

    for qr_text, data in moved.items():
        if qr_text in storage:
            updated_item = {
                "x": data["current"]["x"],
                "y": data["current"]["y"],
                "lastChecked": current_timestamp,
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
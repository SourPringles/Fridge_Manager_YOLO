from flask import Blueprint, request, jsonify
from db import load_storage, update_storage, delete_storage, load_temp, update_temp, delete_temp
from utils import save_log, compare_storages
from modules.NonQR_modules import detect_objects_yolo
from datetime import datetime
import cv2
import numpy as np

from utils.settings import takeoutTimeValue

updateStorageV2_bp = Blueprint('updateStorageV2', __name__)

@updateStorageV2_bp.route('/updateStorageV2', methods=['POST'])
def updateStorage():
    source = request.files.get('source')
    if not source:
        return jsonify({"error": "Current image is required."}), 400

    imageSource = cv2.imdecode(np.frombuffer(source.read(), np.uint8), cv2.IMREAD_COLOR)

    try:
        result = process_update(imageSource)
            # 응답에 사용된 모드 포함
        #result["mode_used"] = "YOLO"
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def process_update(imageSource):
    # 저장소 데이터 로드
    storage = load_storage()
    print(storage)
    temp = load_temp()
    print(temp)

    # 물체인식
    new_data = detect_objects_yolo(imageSource)
    print("detection finished")
    print(new_data)
    """
    new_data = {
            #"id": i,
            "image": f"{i+1}.jpg",  # 물체를 잘라내는 함수
            "nickname": "NEW ITEM",
            "x": round((x1 + x2) / 2), 
            "y": round((y1 + y2) / 2),
            "timestamp" : timestamp
        }    
    """


    #for data in new_data:
    #    print(data)
    #    info = {
    #        "image": data["image"],
    #        "nickname": data["nickname"],
    #        "x": data["x"],
    #        "y": data["y"],
    #        "timestamp": data["timestamp"]
    #    }
    #    update_storage(info)
#
    return new_data

    ## 데이터 비교
    #added, removed, moved = compare_storages(prev_data, new_data)
#
    ## 현재 시각 추가
    #current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
    ## 전체 인벤토리 갱신
    #for qr_text, value in removed.items():
    #    delete_storage(qr_text)
    #    update_temp(qr_text, current_timestamp, value["nickname"])
#
    #for qr_text, value in added.items():
    #    if qr_text not in storage:
    #        if qr_text in temp:
    #            if (datetime.now() - datetime.strptime(temp[qr_text]["takeout_time"], "%Y-%m-%d %H:%M:%S")).total_seconds() < takeoutTimeValue:
    #                new_item = {
    #                    "x": value["x"],
    #                    "y": value["y"],
    #                    "lastChecked": current_timestamp,
    #                    "nickname": temp[qr_text]["nickname"]
    #                }
    #                update_storage(qr_text, new_item)
    #            else:
    #                new_item = {
    #                    "x": value["x"],
    #                    "y": value["y"],
    #                    "lastChecked": current_timestamp,
    #                    "nickname": "New Item!"
    #                }
    #                update_storage(qr_text, new_item)
    #            delete_temp(qr_text)
    #        else:
    #            new_item = {
    #                "x": value["x"],
    #                "y": value["y"],
    #                "lastChecked": current_timestamp,
    #                "nickname": "New Item!"
    #            }
    #            update_storage(qr_text, new_item)
#
    #for qr_text, data in moved.items():
    #    if qr_text in storage:
    #        updated_item = {
    #            "x": data["current"]["x"],
    #            "y": data["current"]["y"],
    #            "lastChecked": current_timestamp,
    #            "nickname": storage[qr_text]["nickname"]
    #        }
    #        update_storage(qr_text, updated_item)
#
    ## 로그 저장
    #save_log("Upload endpoint called", added=added, removed=removed, moved=moved)
#
    #return {
    #    "added": added,
    #    "removed": removed,
    #    "moved": moved,
    #}
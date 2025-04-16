# librarys
from flask import Blueprint, request, jsonify
from datetime import datetime
import cv2
import numpy as np
import os

# custom modules
from db import load_storage, update_storage, delete_storage, load_temp, update_temp, delete_temp
from modules.NonQR_modules.objectDetection import detect_objects_yolo
from utils import apply_compare_result

updateStorage_bp = Blueprint('updateStorage', __name__)
#debugMode = True

@updateStorage_bp.route('/updateStorage', methods=['POST'])
def updateStorage():
# ---저장소 로딩---
    
    # 이미지 경로 db/imgs/storage
    storage_data = load_storage()
    """
    id INTEGER PRIMARY KEY autoincrement,
    image TEXT, # 이미지 이름 (고유 UUID)
    x INTEGER,
    y INTEGER,
    timestamp TEXT,
    nickname TEXT
    """
    # 이미지 경로 db/imgs/temp
    temp_data = load_temp()
    """
    id INTEGER PRIMARY KEY autoincrement,
    image TEXT, # 이미지 이름 (고유 UUID)
    timestamp TEXT,
    nickname TEXT
    """

# ---저장소 로딩 완료---

# ---새로운 이미지 로드---

    source = request.files.get('source')
    if not source:
        return jsonify({"error": "Current image is required."}), 400
    
# ---새로운 이미지 로딩 완료---
    
# ---이미지 처리 시작 (YOLO 모델 사용)---

    # 결과 이미지, 잘라낸 이미지를 db/imgs/new에 저장, 이미지 이름은 UUID형식 사용
    input_data = detect_objects_yolo(cv2.imdecode(np.frombuffer(source.read(), np.uint8), cv2.IMREAD_COLOR))
    """
    (list)
    input_data = {
            #"id": i,
            "image": f"{i+1}.jpg",  # 잘라낸 각 객체의 이미지
            "nickname": "NEW ITEM",
            "x": round((x1 + x2) / 2), 
            "y": round((y1 + y2) / 2),
            "timestamp" : timestamp
            #"features": extract_features_clip(thumbnail)   # 물체의 특징을 추출하는 함수 -> 성능저하 발생
        }
    """
# ---이미지 처리 완료---


# ---저장소 비교 시작---

    # --만약 이전 저장소가 없다면: input_data를 storage에 추가
    if not storage_data:
        # db에 저장
        for data in input_data:
            update_storage(data)
        os.rename("./db/imgs/new", "./db/imgs/storage") # db/imgs/new -> db/imgs/storage로 이동
        return jsonify({"added": input_data}), 200

    # storage_data는 기존 데이터, new_data는 새로운 데이터
    # db/imgs 폴더의 storage폴더는 기존 이미지, new폴더는 새로운 이미지

    # 비교 함수 호출(clip 모델 사용)
    from modules.compare_similarity import compare_data_lists_clip
    added, removed, moved = compare_data_lists_clip(storage_data, input_data, temp_data)

# ---저장소 비교 완료---

# ---결과 반영 시작---
    # storage 리셋 -> added, moved 항목 추가 (timestamp = 현재 시각)
    # temp 리셋 -> removed 항목 추가 (리스트 구조: image, nickname, timestamp)
        # 만약 temp 객체에 current_timestamp - timestamp > takeoutTimeValue 이면 temp에서 해당 항목 삭제
    try:
        apply_compare_result(added, removed, moved, storage_data)
    except Exception as e:
        print(f"Error applying comparison results: {e}")
        # 결과 반영 중 심각한 오류 발생 시 상태 코드 500 반환 고려
        return jsonify({"error": "Failed to apply comparison results."}), 500

# ---결과 반영 종료---

# ---결과 출력---
    print(f"Added: {added}, Removed: {removed}, Moved: {moved}")

    return jsonify({"added": len(added), "removed": len(removed), "moved": len(moved)}), 200
    #return jsonify({"added": added, "removed": removed, "moved": moved}), 200

# ---결과 출력 종료---
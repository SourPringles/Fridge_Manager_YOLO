from flask import Blueprint, request, jsonify
from datetime import datetime
import cv2
import numpy as np
import os
import shutil

from db import load_storage, update_storage, delete_storage, load_temp, update_temp, delete_temp
from modules.NonQR_modules.objectDetection import detect_objects_yolo

updateStorage_bp = Blueprint('updateStorage', __name__)

@updateStorage_bp.route('/updateStorage', methods=['POST'])
def updateStorage():
# --저장소 로딩
    
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

# --저장소 로딩 완료

# --새로운 이미지 로드

    source = request.files.get('source')
    if not source:
        return jsonify({"error": "Current image is required."}), 400
    
# --새로운 이미지 로딩 완료
    
# --이미지 처리 시작 (YOLO 모델 사용)

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
# --이미지 처리 완료

# --만약 이전 저장소가 없다면: input_data를 storage에 추가
    if not storage_data:
        # db에 저장
        for data in input_data:
            update_storage(data)
        os.rename("./db/imgs/new", "./db/imgs/storage") # db/imgs/new -> db/imgs/storage로 이동
        return jsonify({"added": input_data}), 200

# --저장소 비교 시작

    # storage_data는 기존 데이터, new_data는 새로운 데이터
    # db/imgs 폴더의 storage폴더는 기존 이미지, new폴더는 새로운 이미지
    # new_data의 이미지들을 storage_data의 이미지들과 비교 후
        # 같은 항목이 있다면: 좌표 비교(이동 여부 판단)
        # 같은 항목이 없다면: 새로운 항목으로 추가
        # new에는 있고 storage에는 없는 항목은: 삭제된 항목으로 처리 -> 임시 저장소로 이동(좌표값 제외?)

    # 비교 함수 호출(clip 모델 사용)
    from modules.compare_similarity import compare_data_lists_clip
    added, removed, moved = compare_data_lists_clip(storage_data, input_data, temp_data)

# --저장소 비교 완료

# --결과 반영 시작
    # storage 리셋 -> added, moved 항목 추가 (timestamp = 현재 시각)
    # temp 리셋 -> removed 항목 추가 (리스트 구조: image, nickname, timestamp)
        # 만약 temp 객체에 current_timestamp - timestamp > takeoutTimeValue 이면 temp에서 해당 항목 삭제
    try:
        _apply_comparison_results(added, removed, moved, storage_data)
    except Exception as e:
        print(f"Error applying comparison results: {e}")
        # 결과 반영 중 심각한 오류 발생 시 상태 코드 500 반환 고려
        return jsonify({"error": "Failed to apply comparison results."}), 500

# --결과 반영 종료


    # 데이터 정리


    # 결과 출력
    #return added, removed, moved
    return jsonify({"added": len(added), "removed": len(removed), "moved": len(moved)}), 200
    #return jsonify({"error": "Internal Server Error - Functionality not fully implemented"}), 500

def _apply_comparison_results(added, removed, moved, storage_data):
    """
    compare_data_lists_clip 결과를 바탕으로 DB와 이미지 파일을 업데이트합니다.

    Args:
        added (dict): 추가된 항목 정보.
        removed (dict): 제거된 항목 정보.
        moved (dict): 이동된 항목 정보.
        storage_data (list): 비교 전 storage 데이터 (moved 항목의 이전 ID 조회용).
    """
    current_timestamp = datetime.now().isoformat()
    img_base_path = "./db/imgs"
    storage_img_path = os.path.join(img_base_path, "storage")
    new_img_path = os.path.join(img_base_path, "new")
    temp_img_path = os.path.join(img_base_path, "temp")

    # 디렉토리 존재 확인 및 생성
    os.makedirs(temp_img_path, exist_ok=True)
    os.makedirs(storage_img_path, exist_ok=True)
    os.makedirs(new_img_path, exist_ok=True) # new 폴더도 혹시 모르니 확인

    # 1. 추가된 항목 처리 (Added)
    for item_key, item_data in added.items():
        try:
            item_data['timestamp'] = current_timestamp
            update_storage(item_data)
            src_img = os.path.join(new_img_path, item_data['image'])
            dst_img = os.path.join(storage_img_path, item_data['image'])
            if os.path.exists(src_img):
                shutil.move(src_img, dst_img)
            else:
                print(f"Warning: Added item image not found in new: {src_img}")
        except Exception as e:
            print(f"Error processing added item {item_key}: {e}")

    # 2. 이동된 항목 처리 (Moved)
    for item_key, move_info in moved.items():
        try:
            previous_image_name = move_info['previous']['image']
            current_data = move_info['current']
            current_image_name = current_data['image']

            previous_item_id = None
            for item in storage_data:
                if item['image'] == previous_image_name:
                    previous_item_id = item['id']
                    break

            if previous_item_id is not None:
                delete_storage(previous_item_id)
            else:
                 print(f"Warning: Could not find previous item ID for moved item (image: {previous_image_name})")

            current_data['nickname'] = move_info.get('nickname', 'MOVED ITEM')
            current_data['timestamp'] = current_timestamp
            update_storage(current_data)

            old_img_path = os.path.join(storage_img_path, previous_image_name)
            if os.path.exists(old_img_path):
                os.remove(old_img_path)
            else:
                 print(f"Warning: Old image not found for moved item: {old_img_path}")

            src_img = os.path.join(new_img_path, current_image_name)
            dst_img = os.path.join(storage_img_path, current_image_name)
            if os.path.exists(src_img):
                shutil.move(src_img, dst_img)
            else:
                print(f"Warning: New image not found for moved item: {src_img}")

        except Exception as e:
            print(f"Error processing moved item {item_key}: {e}")

    # 3. 삭제된 항목 처리 (Removed)
    for item_key, item_data in removed.items():
        try:
            item_id = item_data['id']
            image_name = item_data['image']
            delete_storage(item_id)
            temp_item = {
                "image": image_name,
                "timestamp": current_timestamp,
                "nickname": item_data.get('nickname', 'REMOVED ITEM')
            }
            update_temp(temp_item)
            src_img = os.path.join(storage_img_path, image_name)
            dst_img = os.path.join(temp_img_path, image_name)
            if os.path.exists(src_img):
                shutil.move(src_img, dst_img)
            else:
                print(f"Warning: Removed item image not found in storage: {src_img}")
        except Exception as e:
            print(f"Error processing removed item {item_key}: {e}")

    # 4. new 폴더 정리
    try:
        if os.path.exists(new_img_path):
            for filename in os.listdir(new_img_path):
                file_path = os.path.join(new_img_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
    except Exception as e:
        print(f"Error cleaning up new directory: {e}")

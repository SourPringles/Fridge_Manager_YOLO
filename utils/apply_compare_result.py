# Base Librarys
from datetime import datetime
import os
import shutil

# Libraries

# Custom Modules
from db import update_storage, delete_storage, update_temp


# Added 처리 -> moved 처리 -> removed 처리 -> new 폴더 정리
def apply_compare_result(added, removed, moved, storage_data):
    """
    compare_data_lists_clip 결과를 바탕으로 DB와 이미지 파일을 업데이트합니다.

    Args:
        added (dict): 추가된 항목 정보.
        removed (dict): 제거된 항목 정보.
        moved (dict): 이동된 항목 정보.
        storage_data (list): 비교 전 storage 데이터 (moved 항목의 이전 ID 조회용).
        temp_data (list): temp 데이터 (added 항목 처리용(nickname 로드))
    """
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    img_base_path = "./db/imgs"
    storage_img_path = os.path.join(img_base_path, "storage")
    new_img_path = os.path.join(img_base_path, "new")
    temp_img_path = os.path.join(img_base_path, "temp")

    # 디렉토리 존재 확인 및 생성
    os.makedirs(temp_img_path, exist_ok=True)
    os.makedirs(storage_img_path, exist_ok=True)
    os.makedirs(new_img_path, exist_ok=True)

# ---추가된 항목 처리 (Added)---

    for item_key, item_data in added.items():
        try:
            # timestamp 추가
            item_data['timestamp'] = current_timestamp

            update_storage(item_data)

            # 업데이트 후 이미지 이동
            src_img = os.path.join(new_img_path, item_data['uuid'])
            dst_img = os.path.join(storage_img_path, item_data['uuid'])
            if os.path.exists(src_img):
                shutil.move(src_img, dst_img)
            else:
                print(f"Warning: Added item image not found in new: {src_img}")
        except Exception as e:
            print(f"Error processing added item {item_key}: {e}")

# ---추가된 항목 처리 완료---

# ---이동된 항목 처리 (Moved)---

    for item_key, move_info in moved.items():
        try:
            previous_image_name = move_info['previous']['uuid']
            current_data = move_info['current']
            current_image_name = current_data['uuid']

            # 이동된 항목의 이전 ID를 찾고 이미지 변경
            previous_item_uuid = None
            previous_timstamp = None

            for item in storage_data:
                if item['uuid'] == previous_image_name:
                    previous_item_uuid = item['uuid']
                    previous_timstamp = item.get('timestamp')
                    break
            
            if previous_item_uuid is not None:
                delete_storage(previous_item_uuid)
            else:
                 print(f"Warning: Could not find previous item UUID for moved item (uuid: {previous_image_name})")

            # 이동된 항목의 nickname 정보 반영 및 timestamp 갱신
            current_data['nickname'] = move_info.get('nickname', 'MOVED ITEM')
            current_data['timestamp'] = previous_timstamp

            update_storage(current_data)

            # 이전 이미지 삭제
            old_img_path = os.path.join(storage_img_path, previous_image_name)
            if os.path.exists(old_img_path):
                os.remove(old_img_path)
            else:
                 print(f"Warning: Old image not found for moved item: {old_img_path}")

            # 새로운 이미지 이동
            src_img = os.path.join(new_img_path, current_image_name)
            dst_img = os.path.join(storage_img_path, current_image_name)
            if os.path.exists(src_img):
                shutil.move(src_img, dst_img)
            else:
                print(f"Warning: New image not found for moved item: {src_img}")

        except Exception as e:
            print(f"Error processing moved item {item_key}: {e}")

# ---이동된 항목 처리 완료---

# ---제거된 항목 처리 (Removed)---

    for item_key, item_data in removed.items():
        try:
            item_uuid = item_data['uuid']
            image_name = item_data['uuid']
            delete_storage(item_uuid)
            temp_item = {
                "uuid": image_name,
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

# ---제거된 항목 처리 완료---

# ---new 폴더 정리---

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

# ---new 폴더 정리 완료---

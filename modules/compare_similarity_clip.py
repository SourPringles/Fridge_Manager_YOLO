# Base Libraries
import os
from typing import Tuple, List, Union, Dict

# Libraries
import torch
import numpy as np
from PIL import Image
import clip
#import time

# Custom Modules
from db import delete_temp
from utils.settings import BASEIMGDIR, CLIPTHRESHOLD


# CLIP 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
model, preprocess = clip.load("ViT-B/32", device=device)

def extract_features_clip(image) -> np.ndarray:
    """
    CLIP 모델을 사용하여 이미지에서 특징 추출
    
    Args:
        image: PIL Image 객체
        bbox: 관심 영역의 바운딩 박스 (x1, y1, x2, y2)
    
    Returns:
        이미지의 특징 벡터 (numpy array)
    """
    
    # 이미지 전처리 및 특징 추출
    with torch.no_grad():
        image_input = preprocess(image).unsqueeze(0).to(device)
        image_features = model.encode_image(image_input)
        
    # 특징 벡터 정규화
    image_features = image_features.cpu().numpy()
    image_features = image_features / np.linalg.norm(image_features, axis=1, keepdims=True)
    
    return image_features[0]

def compute_similarity(features1: np.ndarray, features2: np.ndarray) -> float:
    """
    두 특징 벡터 간의 코사인 유사도를 계산
    
    Args:
        features1: 첫 번째 이미지의 특징 벡터
        features2: 두 번째 이미지의 특징 벡터
    
    Returns:
        코사인 유사도 점수 (0~1 사이의 값, 1에 가까울수록 유사)
    """
    return float(np.dot(features1, features2))

# 현재 미사용
def compare_images(image1: Union[str, Image.Image], 
                  image2: Union[str, Image.Image]) -> float:
    """
    두 이미지의 유사도를 CLIP 모델을 사용하여 비교
    
    Args:
        image1: 첫 번째 이미지 경로 또는 PIL Image 객체
        image2: 두 번째 이미지 경로 또는 PIL Image 객체
        bbox1: 첫 번째 이미지의 관심 영역 바운딩 박스
        bbox2: 두 번째 이미지의 관심 영역 바운딩 박스
        
    Returns:
        두 이미지의 유사도 점수 (0~1 사이의 값, 1에 가까울수록 유사)
    """

    # 각 이미지에서 특징 추출
    features1 = extract_features_clip(image1)
    features2 = extract_features_clip(image2)
    
    # 유사도 계산 및 반환
    return compute_similarity(features1, features2)

# Storage - Temp - New 비교
def compare_data_lists_clip(storage_list: List[Dict],
                            new_data_list: List[Dict],
                            temp_data_list: List[Dict],
                            threshold=CLIPTHRESHOLD) -> Tuple[Dict, Dict, Dict]:
    """
    storage, new_data, temp 리스트를 CLIP 이미지 유사도를 사용하여 비교
    - storage와 new_data를 비교하여 moved, removed 항목 식별
    - new_data 중 storage와 매칭되지 않은 항목은 added 후보로 지정
    - added 후보는 temp_data와 비교하여 유사한 항목이 있으면 nickname을 가져옴

    Args:
        storage_list (list): 현재 저장소 상태 리스트 (dict 포함). 각 dict는 'image', 'x', 'y', 'id', 'nickname' 등 포함
        new_data_list (list): 새로 감지된 객체 정보 리스트 (dict 포함). 각 dict는 'image', 'x', 'y', 'nickname' 등 포함
        temp_data_list (list, optional): 임시 저장소 데이터 리스트 (dict 포함). 각 dict는 'image', 'nickname', 'id' 등 포함
        threshold (float): 유사도 임계값 (이 값 이상이면 동일 항목으로 간주)

    Returns:
        tuple: (added, removed, moved) 딕셔너리 튜플.
               키는 각 항목의 'image' 식별자를 사용합니다.
               added 항목은 temp에서 가져온 nickname을 포함할 수 있습니다.
    """
    added = {}
    removed = {}
    moved = {}

    img_base_path = BASEIMGDIR
    storage_img_path = os.path.join(img_base_path, "storage")
    new_data_img_path = os.path.join(img_base_path, "new")
    temp_img_path = os.path.join(img_base_path, "temp")

# ---특징 미리 추출---

    def extract_features_safe(item_list, path):
        features = {}
        for item in item_list:
            img_name = item.get('image')
            if not img_name: continue
            img_path = os.path.join(path, img_name)
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    features[img_name] = extract_features_clip(img)
                except Exception as e:
                    print(f"Error extracting features for {img_path}: {e}")
            # else: print(f"Image not found for feature extraction: {img_path}") # 디버깅용
        return features

    storage_features = extract_features_safe(storage_list, storage_img_path)
    new_data_features = extract_features_safe(new_data_list, new_data_img_path)
    temp_features = {}
    if temp_data_list:
        temp_features = extract_features_safe(temp_data_list, temp_img_path)

# ---특징 미리 추출 완료---

# ---매칭된 키 추적용 세트 초기화---
    matched_storage_keys = set()
    matched_new_data_keys = set()
# ---매칭된 키 추적용 세트 초기화 완료---

# ---new_data vs storage 비교 (moved 식별)---

    for new_key, new_feature in new_data_features.items():
        best_match_storage_key = None
        max_similarity = -1.0

        for storage_key, storage_feature in storage_features.items():
            if storage_key in matched_storage_keys: continue

            similarity = compute_similarity(new_feature, storage_feature)

            if similarity > max_similarity:
                max_similarity = similarity
                best_match_storage_key = storage_key

        if max_similarity >= threshold and best_match_storage_key:
            matched_storage_keys.add(best_match_storage_key)
            matched_new_data_keys.add(new_key)

            storage_match_item = next((item for item in storage_list if item.get('image') == best_match_storage_key), None)
            new_item_full = next((item for item in new_data_list if item.get('image') == new_key), None)

            if storage_match_item and new_item_full:
                storage_x = storage_match_item.get('x')
                storage_y = storage_match_item.get('y')
                storage_nickname = storage_match_item.get('nickname', 'UNKNOWN')
                new_x = new_item_full.get('x')
                new_y = new_item_full.get('y')

                # 위치가 변경되었는지 확인 (좌표 존재 시)
                is_moved = (storage_x is not None and storage_y is not None and
                            new_x is not None and new_y is not None and
                            (storage_x != new_x or storage_y != new_y))

                if is_moved:
                    moved[new_key] = {
                        "previous": {"x": storage_x, "y": storage_y, "image": storage_match_item['image']},
                        "current": {"x": new_x, "y": new_y, "image": new_item_full['image']},
                        "nickname": storage_nickname,
                        "similarity": float(max_similarity)
                    }
            # else: print(f"Warning: Original item not found for matched key {best_match_storage_key} or {new_key}") # 디버깅용

# ---new_data vs storage 비교 (moved 식별) 완료---

# ---매칭되지 않은 new_data 처리 (added 후보 + temp 비교)---

    for new_key, new_feature in new_data_features.items():
        if new_key not in matched_new_data_keys:
            new_item_full = next((item for item in new_data_list if item.get('image') == new_key), None)
            if not new_item_full: continue

            found_temp_nickname = None
            max_temp_similarity = -1.0

            # temp 데이터와 비교
            if temp_features: # temp 특징이 추출되었을 경우
                for temp_key, temp_feature in temp_features.items():
                    similarity = compute_similarity(new_feature, temp_feature)
                    if similarity > max_temp_similarity:
                        max_temp_similarity = similarity
                        if similarity >= threshold:
                            temp_match_item = next((item for item in temp_data_list if item.get('image') == temp_key), None)
                            if temp_match_item:
                                found_temp_nickname = temp_match_item.get('nickname')
                                # temp의 이미지 삭제
                                file_path = os.path.join(temp_img_path, temp_key)
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                # db에서 해당 항목 삭제
                                delete_temp(temp_match_item['id'])
                                
                                # print(f"Found similar item in temp for {new_key} (Sim: {similarity:.4f}). Using nickname: {found_temp_nickname}") # 디버깅용

            # added 딕셔너리에 추가 (temp 닉네임 우선 적용)
            added_item = new_item_full.copy() # 원본 수정을 피하기 위해 복사
            added_item['nickname'] = found_temp_nickname if found_temp_nickname else added_item.get('nickname', 'NEW ITEM')
            added[new_key] = added_item

# ---매칭되지 않은 new_data 처리 (added 후보 + temp 비교) 완료---

# ---매칭되지 않은 storage 데이터 처리 (removed)---

    for storage_key, storage_feature in storage_features.items():
        if storage_key not in matched_storage_keys:
            storage_item_full = next((item for item in storage_list if item.get('image') == storage_key), None)
            if storage_item_full:
                removed[storage_key] = storage_item_full

# ---매칭되지 않은 storage 데이터 처리 (removed) 완료---

    return added, removed, moved
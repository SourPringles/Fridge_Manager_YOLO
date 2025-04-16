"""CLIP 기반 이미지 유사도 비교"""

import torch
import numpy as np
from PIL import Image
import clip
from typing import Tuple, List, Union
import os

# CLIP 모델 로드
device = "cuda" if torch.cuda.is_available() else "cpu"
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

def compare_data_lists_clip(storage_list, new_data_list, temp_data_list, threshold=0.85): # temp_data_list 인자 추가
    """
    storage 리스트와 new_data 리스트를 CLIP 이미지 유사도를 사용하여 비교합니다.
    추가된 항목은 temp_data 리스트와도 비교하여 유사한 항목이 있으면 nickname을 가져옵니다.
    각 항목은 'image' (이미지 파일명 또는 식별자), 'x', 'y' 키를 포함하고,
    실제 이미지 데이터에 접근 가능해야 합니다 (예: image_base_path 와 'image' 결합).

    Args:
        storage_list (list): 현재 저장소 상태 리스트.
        new_data_list (list): 새로 감지된 객체 정보 리스트.
        temp_data_list (list): 임시 저장소 데이터 리스트. # 인자 설명 추가
        threshold (float): 유사도 임계값 (이 값 이상이면 동일 항목으로 간주).
        image_base_path (str): 'image' 필드가 파일명일 경우, 이미지가 저장된 기본 경로.

    Returns:
        tuple: (added, removed, moved) 딕셔너리 튜플.
               키는 각 항목의 'image' 식별자를 사용합니다.
    """
    added = {}
    removed = {}
    moved = {}

    img_base_path = "./db/imgs"
    storage_img_path = os.path.join(img_base_path, "storage")
    new_data_img_path = os.path.join(img_base_path, "new")
    temp_img_path = os.path.join(img_base_path, "temp") # temp 이미지 경로 추가

    # 성능 향상을 위해 특징 미리 추출
    storage_features = {}
    new_data_features = {}
    temp_features = {} # temp 특징 딕셔너리 초기화
    try:
        storage_features = {
            item['image']: extract_features_clip(Image.open(os.path.join(storage_img_path, item['image'])))
            for item in storage_list if 'image' in item and os.path.exists(os.path.join(storage_img_path, item['image']))
        }
        new_data_features = {
            item['image']: extract_features_clip(Image.open(os.path.join(new_data_img_path, item['image'])))
            for item in new_data_list if 'image' in item and os.path.exists(os.path.join(new_data_img_path, item['image']))
        }
        # temp 데이터 특징 추출 추가
        temp_features = {
            item['image']: extract_features_clip(Image.open(os.path.join(temp_img_path, item['image'])))
            for item in temp_data_list if 'image' in item and os.path.exists(os.path.join(temp_img_path, item['image']))
        }
    except Exception as e:
         print(f"Error pre-extracting features: {e}. Proceeding without pre-extraction.")
         # 오류 발생 시, 아래 루프에서 개별적으로 특징 추출/비교 수행하도록 fallback 로직 추가 필요
         # 여기서는 간단히 빈 dict로 초기화하고, 아래 로직은 개별 비교를 가정하고 진행
         storage_features = {}
         new_data_features = {}
         temp_features = {}


    # 매칭된 인덱스 추적 (중복 매칭 방지)
    matched_storage_keys = set()
    matched_new_data_keys = set()

    # 1. 새로운 데이터(new_data)를 기준으로 기존 데이터(storage)와 비교
    for new_key, new_item in new_data_features.items(): # 특징 추출된 new_data 기준 순회
        best_match_storage_key = None
        max_similarity = -1.0
        new_item_full = next((item for item in new_data_list if item['image'] == new_key), None) # 원본 new_data 항목 찾기
        if not new_item_full: continue # 원본 항목 없으면 건너뛰기

        new_feature = new_item # 미리 추출된 특징 사용

        for storage_key, storage_feature in storage_features.items():
            if storage_key in matched_storage_keys:
                continue # 이미 매칭된 storage 항목은 건너뛰기

            # 미리 추출된 특징 벡터로 유사도 계산
            similarity = float(np.dot(new_feature, storage_feature)) # compute_similarity 와 동일

            if similarity > max_similarity:
                max_similarity = similarity
                best_match_storage_key = storage_key

        # 가장 유사한 항목이 임계값을 넘고, 아직 매칭되지 않았다면 매칭 처리
        if max_similarity >= threshold and best_match_storage_key:
            matched_storage_keys.add(best_match_storage_key)
            matched_new_data_keys.add(new_key)

            storage_match_item = next((item for item in storage_list if item['image'] == best_match_storage_key), None)
            if not storage_match_item: continue # 원본 storage 항목 없으면 건너뛰기

            # 좌표 비교하여 이동 여부 판단
            storage_x = storage_match_item.get('x')
            storage_y = storage_match_item.get('y')
            new_x = new_item_full.get('x')
            new_y = new_item_full.get('y')

            if (storage_x is not None and storage_y is not None and
                    new_x is not None and new_y is not None and
                    (storage_x != new_x or storage_y != new_y)):
                moved[new_key] = { # 키는 새로운 항목의 image 식별자 사용
                    "previous": {"x": storage_x, "y": storage_y, "image": storage_match_item['image']},
                    "current": {"x": new_x, "y": new_y, "image": new_item_full['image']},
                    "nickname": new_item_full.get("nickname", storage_match_item.get("nickname")),
                    "similarity": float(max_similarity)
                }
            # else: 유사하고 위치 변화 없으면 아무것도 안 함

    # 2. 매칭되지 않은 새로운 데이터는 'added'로 처리
    for new_key, new_feature in new_data_features.items():
        if new_key not in matched_new_data_keys:
             new_item_full = next((item for item in new_data_list if item['image'] == new_key), None)
             if new_item_full:
                 # temp_data와 비교하여 nickname 가져오기 시도
                 best_temp_match_key = None
                 max_temp_similarity = -1.0
                 for temp_key, temp_feature in temp_features.items():
                     # 미리 추출된 특징 벡터로 유사도 계산
                     similarity = float(np.dot(new_feature, temp_feature))
                     if similarity > max_temp_similarity:
                         max_temp_similarity = similarity
                         best_temp_match_key = temp_key

                 # 임계값 이상으로 유사한 temp 항목이 있다면 nickname 사용
                 if max_temp_similarity >= threshold and best_temp_match_key:
                     temp_match_item = next((item for item in temp_data_list if item['image'] == best_temp_match_key), None)
                     if temp_match_item and 'nickname' in temp_match_item:
                         new_item_full['nickname'] = temp_match_item['nickname']
                         # print(f"Found similar item in temp for {new_key}. Using nickname: {temp_match_item['nickname']}") # 디버깅용 로그

                 added[new_key] = new_item_full # 최종 nickname이 반영된 new_item_full 추가

    # 3. 매칭되지 않은 기존 데이터는 'removed'로 처리
    for storage_key, storage_feature in storage_features.items():
        if storage_key not in matched_storage_keys:
            storage_item_full = next((item for item in storage_list if item['image'] == storage_key), None)
            if storage_item_full:
                removed[storage_key] = storage_item_full

    return added, removed, moved
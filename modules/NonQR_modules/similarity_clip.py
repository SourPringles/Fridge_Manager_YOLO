"""CLIP 기반 이미지 유사도 비교"""

import torch
import numpy as np
from PIL import Image
import clip
from typing import Tuple, List, Union

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

def find_most_similar_image(query_image: Union[str, Image.Image], 
                           image_list: List[Union[str, Image.Image]], 
                           bbox: Tuple[int, int, int, int] = None,
                           threshold: float = 0.75) -> Tuple[int, float, List[float]]:
    """
    쿼리 이미지와 가장 유사한 이미지를 목록에서 찾습니다.
    
    Args:
        query_image: 쿼리 이미지 경로 또는 PIL Image 객체
        image_list: 비교할 이미지 목록
        bbox: 쿼리 이미지의 관심 영역 바운딩 박스
        threshold: 유사도 임계값 (이 값 이상인 경우 유사한 것으로 판단)
        
    Returns:
        Tuple (가장 유사한 이미지 인덱스, 유사도 점수, 모든 이미지의 유사도 점수 리스트)
        유사한 이미지가 없는 경우 인덱스는 -1
    """
    # 쿼리 이미지 특징 추출
    query_features = extract_features_clip(query_image, bbox)
    
    similarities = []
    # 각 이미지와의 유사도 계산
    for img in image_list:
        img_features = extract_features_clip(img)
        similarity = compute_similarity(query_features, img_features)
        similarities.append(similarity)
    
    # 가장 유사한 이미지 찾기
    if not similarities:
        return -1, 0.0, []
    
    max_similarity = max(similarities)
    most_similar_idx = similarities.index(max_similarity)
    
    # 임계값보다 낮으면 유사한 이미지가 없는 것으로 판단
    if max_similarity < threshold:
        return -1, max_similarity, similarities
    
    return most_similar_idx, max_similarity, similarities
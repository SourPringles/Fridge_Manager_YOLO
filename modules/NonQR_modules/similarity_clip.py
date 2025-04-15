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
import cv2
import objectDetection_NonQR_YOLO
from NonQR_modules import compare_images

def load_image_from_path(image_path):
    """
    파일 경로에서 이미지를 로드하여 OpenCV 객체로 변환
    
    Args:
        image_path (str): 이미지 파일 경로
        
    Returns:
        numpy.ndarray: OpenCV 이미지 객체
    """
    try:
        # OpenCV를 사용하여 이미지 로드 (BGR 형식)
        image = cv2.imread(image_path)
        
        if image is None:
            raise ValueError(f"이미지를 로드할 수 없습니다: {image_path}")
        
        testresult = objectDetection_NonQR_YOLO.detect_objects_yolo(image)
        print(testresult)
            
        return testresult
    except Exception as e:
        print(f"이미지 로드 중 오류 발생: {e}")
        return None
    
# TEST

import os

current_directory = os.getcwd()
print(f"현재 작업 디렉토리: {current_directory}")

data = load_image_from_path('./test/NonQRtest/4_original.jpg')

img1 = data[0]['image']
img2 = data[1]['image']

score = compare_images(img1, img2)
print(f"두 이미지의 유사도: {score:.4f}")
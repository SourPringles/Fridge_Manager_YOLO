import cv2
from modules.NonQR_modules import objectDetection
from NonQR_modules import compare_images
from commons import convert_cv2_to_pil

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
        
        testresult = objectDetection.detect_objects_yolo(image)
        
        for i in testresult:
            print(f"Object {i['id']}: {i['nickname']}, Coordinates: {i['coordinates']}, Timestamp: {i['timestamp']}")
        #print(f"저장된 시간: {testresult['save_timestamp']}")

        return testresult
    except Exception as e:
        print(f"이미지 로드 중 오류 발생: {e}")
        return None

import os

current_directory = os.getcwd()
print(f"현재 작업 디렉토리: {current_directory}")

data = load_image_from_path('./test/NonQRtest/1_changed.jpg')

#img1 = cv2.imread("./db/imgs/20250415175814/1.jpg")
#img2 = cv2.imread("./db/imgs/20250415175849/6.jpg")
#
#image1 = convert_cv2_to_pil(img1)
#image2 = convert_cv2_to_pil(img2)
#
#score = compare_images(image1, image2)
#print(f"두 이미지의 유사도: {score:.4f}")
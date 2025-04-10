import cv2
import objectDetection_NonQR_YOLO

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
        
        testresult = objectDetection_NonQR_YOLO.extract_features(image, (0, 0, 224, 224))
        print(testresult)
            
        return testresult
    except Exception as e:
        print(f"이미지 로드 중 오류 발생: {e}")
        return None
    
load_image_from_path('D:/1234.jpg')
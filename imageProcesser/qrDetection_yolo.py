from ultralytics import YOLO
import cv2
from pyzbar.pyzbar import decode
import numpy as np

def detect_qr_codes_yolo(image, model_path='yolov8n.pt', confidence=0.25):
    """
    QR코드를 인식하고 좌표를 반환하는 함수 (YOLO 사용)
    - image: OpenCV 이미지 객체
    - model_path: YOLO 모델 경로 (기본값: yolov8n.pt)
    - confidence: 감지 신뢰도 임계값
    - 반환값: QR코드의 데이터와 좌표를 포함하는 딕셔너리
    """
    # YOLO 모델 로드
    model = YOLO(model_path)
    
    # QR 코드 영역 감지
    results = model(image, conf=confidence)
    
    qr_data = {}
    
    # 감지된 객체 중 QR 코드 확인 (클래스 73은 일반적으로 COCO 데이터셋에서 'cell phone'이나 
    # 훈련된 모델에 따라 QR 코드 클래스가 달라질 수 있음)
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # QR 코드로 감지된 객체만 처리 (클래스 ID가 QR 코드에 해당하는지 확인)
            # 모델에 따라 클래스 ID를 적절히 변경해야 함
            if box.cls == 73 or 'qr' in model.names[int(box.cls)].lower():
                # 바운딩 박스 좌표 가져오기
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                x, y, w, h = int(x1), int(y1), int(x2-x1), int(y2-y1)
                
                # 감지된 영역 자르기
                roi = image[y:y+h, x:x+w]
                
                # pyzbar를 사용하여 QR 코드 내용 디코딩
                decoded_objects = decode(roi)
                
                for obj in decoded_objects:
                    qr_text = obj.data.decode("utf-8")
                    qr_data[qr_text] = {'x': x, 'y': y}
    
    return qr_data

# QR 코드 전용 모델을 사용하는 경우 (사전 훈련된 QR 코드 감지 모델이 있을 경우)
def detect_qr_codes_yolo_custom(image, model_path='path/to/qr_model.pt'):
    """
    QR코드 전용 YOLO 모델을 사용하여 QR코드를 인식하고 좌표를 반환하는 함수
    - image: OpenCV 이미지 객체
    - model_path: QR코드 인식용 YOLO 모델 경로
    - 반환값: QR코드의 데이터와 좌표를 포함하는 딕셔너리
    """
    # QR 코드 전용 YOLO 모델 로드
    model = YOLO(model_path)
    
    # QR 코드 감지
    results = model(image)
    
    qr_data = {}
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # 바운딩 박스 좌표 가져오기
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            x, y, w, h = int(x1), int(y1), int(x2-x1), int(y2-y1)
            
            # 감지된 영역 자르기
            roi = image[y:y+h, x:x+w]
            
            # pyzbar를 사용하여 QR 코드 내용 디코딩
            decoded_objects = decode(roi)
            
            for obj in decoded_objects:
                qr_text = obj.data.decode("utf-8")
                qr_data[qr_text] = {'x': x, 'y': y}
    
    return qr_data
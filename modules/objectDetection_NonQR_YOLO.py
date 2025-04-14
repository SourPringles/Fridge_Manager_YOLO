from ultralytics import YOLO
import cv2
import numpy as np
from skimage.feature import local_binary_pattern

from commons import crop_object
from NonQR_modules.similarity_histogram import extract_features_histogram
from NonQR_modules.similarity_clip import extract_features_clip

def detect_objects_yolo(image, model_path='AIMA_model.pt'):
    """
    물체를 인식하고 좌표를 반환하는 함수 (YOLO 사용)
    - image: OpenCV 이미지 객체
    - model_path: YOLO 모델 경로
    - 반환값: 물체의 좌표와 특징을 포함하는 딕셔너리
    """
    # YOLO 모델 로드
    model = YOLO(model_path)
    
    results = model(image)

    objects = []
    for i, det in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, det.xyxy[0])
        #confidence = det.conf[0].item()
        #class_id = int(det.cls[0])
        #class_name = model.names[class_id]
        thumbnail = crop_object(image, (x1, y1, x2, y2))

        #object_info = {
        #    "id": i,
        #    "image": crop_object(image, (x1, y1, x2, y2)),  # 물체를 잘라내는 함수
        #    "nickname": "NEW ITEM",
        #    "coordinates": {"x": (x1 + x2) / 2, "y": (y1 + y2) / 2},
        #    "features": extract_features_histogram(image,  (x1, y1, x2, y2))   # 물체의 특징을 추출하는 함수
        #}

        object_info = {
            "id": i,
            "image": thumbnail,  # 물체를 잘라내는 함수
            "nickname": "NEW ITEM",
            "coordinates": {"x": (x1 + x2) / 2, "y": (y1 + y2) / 2}
            #"features": extract_features_clip(thumbnail)   # 물체의 특징을 추출하는 함수
        }
        objects.append(object_info)

        # debug
        thumbnail.save(f"./test/output/{i}output.jpg")
        print(f"Object {i}: {object_info['nickname']}, Coordinates: {object_info['coordinates']}")

    return objects
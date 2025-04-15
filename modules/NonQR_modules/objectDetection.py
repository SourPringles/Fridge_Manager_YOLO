from ultralytics import YOLO
import cv2
import numpy as np
from skimage.feature import local_binary_pattern
from datetime import datetime
import os

from ..commons import crop_object

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
    plotted_image = results[0].plot()

    objects = []
    save_timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    img_dir = f"./db/imgs/{save_timestamp}"
    os.makedirs(img_dir, exist_ok=True)

    for i, det in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, det.xyxy[0])
        #confidence = det.conf[0].item()
        thumbnail = crop_object(image, (x1, y1, x2, y2))
        thumbnail.save(f"{img_dir}/{i+1}.jpg")

        object_info = {
            #"id": i,
            "image": f"{i+1}.jpg",  # 물체를 잘라내는 함수
            "nickname": "NEW ITEM",
            "x": round((x1 + x2) / 2), 
            "y": round((y1 + y2) / 2),
            "timestamp" : timestamp
            #"features": extract_features_clip(thumbnail)   # 물체의 특징을 추출하는 함수 -> 성능저하 발생
        }
        objects.append(object_info)

        # debug
        #thumbnail.save(f"./test/output/{i+1}output.jpg")
        #print(f"Object {i+1}: {object_info['nickname']}, Coordinates: {object_info['coordinates']}, Timestamp: {object_info['timestamp']}")

    # debug 
    cv2.imwrite("./test/output/1output.jpg", plotted_image)
    #objects.append(save_timestamp)

    return objects
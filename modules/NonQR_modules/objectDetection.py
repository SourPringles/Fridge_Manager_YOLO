from ultralytics import YOLO
import cv2
import numpy as np
from datetime import datetime
import os
import shutil   # 이미지 폴더 정리
import uuid # 이미지 uuid 생성

#from ..commons import crop_object

def detect_objects_yolo(image, model_path='AIMA_model.pt', confidence=0.59):
    """
    물체를 인식하고 좌표를 반환하는 함수 (YOLO 사용)
    - image: OpenCV 이미지 객체
    - model_path: YOLO 모델 경로
    - 반환값: 물체의 좌표와 특징을 포함하는 딕셔너리
    """
    # YOLO 모델 로드
    model = YOLO(model_path)
    
    results = model(image, conf=confidence)
    plotted_image = results[0].plot()

    objects = []
    img_dir = "./db/imgs/new"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 이미지 저장 폴더 생성
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
        os.makedirs(img_dir)
    else:
        os.makedirs(img_dir)

    for i, det in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, det.xyxy[0])
        #confidence = det.conf[0].item()
        thumbnail = crop_object(image, (x1, y1, x2, y2))

        filename = f"{uuid.uuid4()}.jpg"
        save_path = os.path.join(img_dir, filename)
        thumbnail.save(save_path)

        object_info = {
            "image": f"{filename}",  # 이미지 이름 (고유 UUID)
            "nickname": "NEW ITEM",
            "x": round((x1 + x2) / 2), 
            "y": round((y1 + y2) / 2),
            "timestamp" : timestamp
            #"features": extract_features_clip(thumbnail)   # 물체의 특징을 추출하는 함수 -> 성능저하 발생
        }
        objects.append(object_info)

        # debug
        #thumbnail.save(f"./test/output/{i+1}output.jpg")
        print(f"Object {i+1}: {object_info['nickname']}, x: {object_info['x']}, y: {object_info['y']}, timestamp: {object_info['timestamp']}")

    # debug 
    cv2.imwrite(f"{img_dir}/result.jpg", plotted_image)
    #objects.append(save_timestamp)

    return objects

def crop_object(image, bbox):
    """
    openCV 이미지 객체를 PIL객체로 변환 후 bbox 영역을 잘라내는 함수
    - image: OpenCV 이미지 객체
    - bbox: 잘라낼 영역의 바운딩 박스 (x_min, y_min, x_max, y_max)
    - 반환값: 잘라낸 이미지 (PIL 객체)
    """
    # OpenCV 이미지를 RGB로 변환 (OpenCV는 BGR 포맷을 사용하므로)
    pil_image = convert_cv2_to_pil(image)

    cropped = pil_image.crop(bbox)
    return cropped

from PIL import Image

def convert_cv2_to_pil(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)

    return pil_image
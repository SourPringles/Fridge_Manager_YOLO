# Base Libraries
import os
import shutil
import uuid # 이미지 uuid 생성
from datetime import datetime

# Libraries
from ultralytics import YOLO
import cv2

# Custom Modules
from modules import crop_object
from utils.settings import BASEIMGDIR, YOLOMODELPATH, YOLOCONFIDENCE


def detect_objects_yolo(image, model_path=YOLOMODELPATH, confidence=YOLOCONFIDENCE):
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
    base_dir = BASEIMGDIR
    img_dir = os.path.join(base_dir, "new")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 이미지 저장 폴더 생성
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)
        os.makedirs(img_dir)
    else:
        os.makedirs(img_dir)

    cv2.imwrite(f"{base_dir}/curr.jpg", image)

    for i, det in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, det.xyxy[0])
        #confidence = det.conf[0].item()
        thumbnail = crop_object(image, (x1, y1, x2, y2))

        filename = f"{uuid.uuid4()}.jpg"
        save_path = os.path.join(img_dir, filename)
        thumbnail.save(save_path)

        object_info = {
            "uuid": f"{filename}",  # 이미지 이름 (고유 UUID)
            "nickname": "NEW ITEM",
            "x": round((x1 + x2) / 2), 
            "y": round((y1 + y2) / 2),
            "timestamp" : timestamp
            #"features": extract_features_clip(thumbnail)   # 물체의 특징을 추출하는 함수 -> 성능저하 발생
        }
        objects.append(object_info)

        # debug
        #thumbnail.save(f"./test/output/{i+1}output.jpg")
        #print(f"Object {i+1}: {object_info['nickname']}, x: {object_info['x']}, y: {object_info['y']}, timestamp: {object_info['timestamp']}")

    # debug 
    cv2.imwrite(f"result.jpg", plotted_image)
    #objects.append(save_timestamp)

    return objects
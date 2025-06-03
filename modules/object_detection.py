# Base Libraries
import os
import shutil
import uuid # 이미지 uuid 생성
from datetime import datetime

# Libraries
from ultralytics import YOLO
import cv2

# Custom Modules
from modules import crop_object, enhance_image_quality
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

    # cv2.imwrite(f"{base_dir}/curr.jpg", image)
    save_compressed_image(image, f"{base_dir}/curr.jpg", 100)

    for i, det in enumerate(results[0].boxes):
        x1, y1, x2, y2 = map(int, det.xyxy[0])
        nickname = "unknown"
        #confidence = det.conf[0].item()
        thumbnail = crop_object(image, (x1, y1, x2, y2))

        # 이미지 초해상화
        enhanced_thumbnail = enhance_image_quality(thumbnail)

        filename = f"{uuid.uuid4()}.jpg"
        save_path = os.path.join(img_dir, filename)

        enhanced_thumbnail.save(save_path)
        # 별명 생성
        # nickname = generate_food_name(save_path)

        object_info = {
            "uuid": f"{filename}",  # 이미지 이름 (고유 UUID)
            "nickname": f"{nickname}",
            "x": round((x1 + x2) / 2),
            "y": round((y1 + y2) / 2),
            "timestamp": timestamp
        }
        objects.append(object_info)

        # debug
        #thumbnail.save(f"./test/output/{i+1}output.jpg")
        #print(f"Object {i+1}: {object_info['nickname']}, x: {object_info['x']}, y: {object_info['y']}, timestamp: {object_info['timestamp']}")

    # debug 
    # cv2.imwrite(f"result.jpg", plotted_image)
    # objects.append(save_timestamp)

    return objects

# 이미지 압축률 조정 (0-100, 낮을수록 더 많이 압축)
def save_compressed_image(image, file_path, max_size_kb=100):
    # 초기 압축 품질
    quality = 90
    min_quality = 5  # 최소 품질 한계
    
    while quality > min_quality:
        # 압축 품질 매개변수 설정
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        
        # 이미지 저장 시도
        success = cv2.imwrite(file_path, image, encode_params)
        
        # 파일 크기 확인
        if success and os.path.exists(file_path):
            file_size_kb = os.path.getsize(file_path) / 1024
            print(f"이미지 저장 - 품질: {quality}, 크기: {file_size_kb:.2f}KB")
            
            if file_size_kb <= max_size_kb:
                print(f"목표 크기 달성: {file_size_kb:.2f}KB (목표: {max_size_kb}KB)")
                return True
        
        # 압축 품질 낮추기
        quality -= 10
    
    # 최소 품질에도 목표 크기를 달성하지 못한 경우, 해상도 축소 시도
    if quality <= min_quality:
        print("압축만으로는 목표 크기를 달성할 수 없어 해상도 축소를 시도합니다.")
        return resize_and_compress_image(image, file_path, max_size_kb)
    
    return False

# 해상도 축소 + 압축
def resize_and_compress_image(image, file_path, max_size_kb=100):
    height, width = image.shape[:2]
    scale = 0.9  # 초기 축소 비율
    min_scale = 0.3  # 최소 축소 비율
    
    while scale >= min_scale:
        # 이미지 크기 조정
        resized = cv2.resize(image, (int(width * scale), int(height * scale)))
        
        # 압축 품질 설정
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, 70]
        
        # 이미지 저장
        success = cv2.imwrite(file_path, resized, encode_params)
        
        # 파일 크기 확인
        if success and os.path.exists(file_path):
            file_size_kb = os.path.getsize(file_path) / 1024
            print(f"이미지 크기 조정 - 비율: {scale:.2f}, 크기: {file_size_kb:.2f}KB")
            
            if file_size_kb <= max_size_kb:
                print(f"목표 크기 달성: {file_size_kb:.2f}KB (목표: {max_size_kb}KB)")
                return True
        
        # 축소 비율 낮추기
        scale -= 0.1
    
    print(f"모든 시도 후에도 목표 크기({max_size_kb}KB)를 달성하지 못했습니다.")
    return False
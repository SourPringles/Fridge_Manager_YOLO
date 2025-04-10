from flask import Blueprint, request, jsonify
from db import load_storage, update_storage, delete_storage, load_temp, update_temp, delete_temp
from utils import save_log, compare_storages
from modules import detect_qr_codes_pyzbar, detect_objects_yolo
from datetime import datetime
import cv2
import numpy as np

from utils.settings import takeoutTimeValue

updateStorage_bp = Blueprint('updateStorage', __name__)

# QR인식 모드 구분
mode_functions = {
    "yolo": detect_objects_yolo
}

@updateStorage_bp.route('/updateStorage', methods=['POST'])
def updateStorage():
    # 요청에서 모드 파라미터 가져오기
    mode = request.form.get('mode', 'pyzbar')  # 기본값은 pyzbar
    
    if mode not in mode_functions:
        return jsonify({"error": f"지원하지 않는 모드입니다. 사용 가능한 모드: {list(mode_functions.keys())}"}), 400
    
    source = request.files.get('source')
    if not source:
        return jsonify({"error": "Current image is required."}), 400

    imageSource = cv2.imdecode(np.frombuffer(source.read(), np.uint8), cv2.IMREAD_COLOR)
    result = process_update(imageSource, mode_functions[mode])
    
    # 응답에 사용된 모드 포함
    result["mode_used"] = mode
    return jsonify(result)

def updateStorage_yolo():
    source = request.files.get('source')

    if not source:
        return jsonify({"error": "Current image is required."}), 400

    imageSource = cv2.imdecode(np.frombuffer(source.read(), np.uint8), cv2.IMREAD_COLOR)
    result = process_update(imageSource, detect_objects_yolo)
    return jsonify(result)
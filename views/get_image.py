# Base Libraries
import os

# Library
from flask import Blueprint, jsonify, send_from_directory

# Custom Modules
from utils.settings import BASEIMGDIR, DEFAULTIMGDIR

getImage_bp = Blueprint('getImage', __name__)
getBackground_bp = Blueprint('getBackground', __name__)
# getAllImage_bp = Blueprint('getAllImage', __name__)

@getImage_bp.route('/getImage/<uid>', methods=['GET'])
def get_image(uid):
    """
    uid에 해당하는 이미지 파일을 반환하는 API 엔드포인트
    지원하는 확장자: .jpg, .jpeg, .png, .gif
    """
    try:
        image_folder = os.path.join(BASEIMGDIR, "storage")  # 이미지 경로

        if not os.path.isdir(image_folder):
            return jsonify({"error": "Image folder not configured or does not exist."}), 500

        filename = f"{uid}"
        file_path = os.path.join(image_folder, filename)
        if os.path.exists(file_path):
            return send_from_directory(image_folder, filename)
        
        return jsonify({"error": "Image not found."}), 404

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500
    
@getBackground_bp.route('/getBackground', methods=['GET'])
def get_backdroundimage():
    """
    입력 이미지 파일 반환
    """
    try:
        image_folder = BASEIMGDIR  # 이미지 경로

        if not os.path.isdir(image_folder):
            return jsonify({"error": "Image folder not configured or does not exist."}), 500

        filename = "curr.jpg"
        file_path = os.path.join(image_folder, filename)
        if os.path.exists(file_path):
            return send_from_directory(image_folder, filename)
        
        return send_from_directory(DEFAULTIMGDIR, "default.jpg")

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

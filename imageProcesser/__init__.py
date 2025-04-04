from flask import Blueprint

# Functions
from .qrDetection_pyzbar import detect_qr_codes_pyzbar
from .qrDetection_cv2 import detect_qr_codes_cv2
from .qrDetection_yolo import detect_qr_codes_yolo


__all__ = ["detect_qr_codes_pyzbar", "detect_qr_codes_cv2", "detect_qr_codes_yolo"]
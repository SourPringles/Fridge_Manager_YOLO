# Functions
from .objectDetection_QR_pyzbar import detect_qr_codes_pyzbar
from .objectDetection_NonQR_YOLO import detect_objects_yolo


__all__ = ["detect_qr_codes_pyzbar", "detect_objects_yolo"]
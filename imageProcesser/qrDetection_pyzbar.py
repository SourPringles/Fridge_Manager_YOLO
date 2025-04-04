from pyzbar.pyzbar import decode

def detect_qr_codes_pyzbar(image):
    """
    QR코드를 인식하고 좌표를 반환하는 함수
    - image: OpenCV 이미지 객체
    - 반환값: QR코드의 데이터와 좌표를 포함하는 딕셔너리
    """
    decoded_objects = decode(image)
    qr_data = {}
    for obj in decoded_objects:
        qr_text = obj.data.decode("utf-8")
        x, y, w, h = obj.rect
        qr_data[qr_text] = {'x': x, 'y': y}
    return qr_data
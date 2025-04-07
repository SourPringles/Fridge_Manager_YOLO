import cv2

def detect_qr_codes_cv2(image):
    """
    QR코드를 인식하고 좌표를 반환하는 함수 (OpenCV 사용)
    - image: OpenCV 이미지 객체
    - 반환값: QR코드의 데이터와 좌표를 포함하는 딕셔너리
    """
    qr_detector = cv2.QRCodeDetector()
    qr_data = {}
    
    # 다중 QR 코드 감지 시도 (OpenCV 4.5.1 이상에서 지원)
    retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(image)
    
    if retval:
        for text, point in zip(decoded_info, points):
            if text:  # 빈 텍스트가 아닌 경우만 처리
                # 좌표 계산 (QR 코드의 왼쪽 상단 지점)
                x = int(point[0][0])
                y = int(point[0][1])
                qr_data[text] = {'x': x, 'y': y}
    
    return qr_data
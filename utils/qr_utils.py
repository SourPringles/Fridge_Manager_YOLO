from pyzbar.pyzbar import decode

def detect_qr_codes(image):
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

def compare_storages(prev_data, new_data, tolerance=5):
    """
    이전 데이터와 비교하여 추가, 삭제, 이동된 항목을 반환하는 함수
    - tolerance: 이동으로 간주할 좌표 차이의 기준 (default: 5)
    - prev_data: 이전 데이터 (딕셔너리)
    - new_data: 새 데이터 (딕셔너리)
    - 반환값: 추가된 항목, 삭제된 항목, 이동된 항목을 포함하는 튜플
    """
    from datetime import datetime
    added = {key: new_data[key] | {"lastModified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for key in new_data if key not in prev_data}
    removed = {key: prev_data[key] | {"lastModified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for key in prev_data if key not in new_data}
    moved = {
        key: {
            "previous": {"x": prev_data[key]["x"], "y": prev_data[key]["y"]},
            "current": {"x": new_data[key]["x"], "y": new_data[key]["y"]},
            "lastModified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        for key in new_data
        if key in prev_data and (
            abs(new_data[key]["x"] - prev_data[key]["x"]) > tolerance or
            abs(new_data[key]["y"] - prev_data[key]["y"]) > tolerance
        )
    }
    return added, removed, moved
import os
from datetime import datetime
from ..utils.settings import logValue, toleranceValue

# def generate_unique_nickname(base_name, inventory):
#    """
#    중복 닉네임 방지 함수
#    """
#    counter = 1
#    unique_name = base_name
#    while any(item.get("nickname") == unique_name for item in inventory.values()):
#        unique_name = f"{base_name} {counter}"
#        counter += 1
#    return unique_name

def save_log(action, **data):
    """
    로그 저장 함수
    """
    logs_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_path = os.path.join(logs_dir, f'{timestamp}.txt')

    # 로그 파일 작성
    with open(log_file_path, 'w') as log_file:
        log_file.write(f"{action} at {timestamp}\n")
        for key, value in data.items():
            log_file.write(f"{key.capitalize()}: {value}\n")

    # 로그 파일 정리
    log_amount = logValue # 최대 로그 파일 개수

    log_files = sorted(
        [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith('.txt')],
        key=os.path.getmtime
    )
    while len(log_files) > log_amount:
        os.remove(log_files.pop(0))

def compare_storages(prev_data, new_data, tolerance=toleranceValue):
    """
    이전 데이터와 비교하여 추가, 삭제, 이동된 항목을 반환하는 함수
    - tolerance: 이동으로 간주할 좌표 차이의 기준 (default: 5)
    - prev_data: 이전 데이터 (딕셔너리)
    - new_data: 새 데이터 (딕셔너리)
    - 반환값: 추가된 항목, 삭제된 항목, 이동된 항목을 포함하는 튜플
    """
    from datetime import datetime
    added = {
        key: new_data[key] | {"lastChecked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for key in new_data if key not in prev_data}
    removed = {key: prev_data[key] | {"lastChecked": datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for key in prev_data if key not in new_data}
    moved = {
        key: {
            "previous": {"x": prev_data[key]["x"], "y": prev_data[key]["y"]},
            "current": {"x": new_data[key]["x"], "y": new_data[key]["y"]},
            "lastChecked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nickname": prev_data[key]["nickname"]
        }
        for key in new_data
        if key in prev_data and (
            abs(new_data[key]["x"] - prev_data[key]["x"]) > tolerance or
            abs(new_data[key]["y"] - prev_data[key]["y"]) > tolerance
        )
    }
    return added, removed, moved

def log_debug(debugMode, message):
    if debugMode:
        print(f"[DEBUG] {datetime.now()}: {message}")
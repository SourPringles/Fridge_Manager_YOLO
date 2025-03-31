import os
import json
from datetime import datetime

#def generate_unique_nickname(base_name, inventory):
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
    log_amount = 10 # 최대 로그 파일 개수

    log_files = sorted(
        [os.path.join(logs_dir, f) for f in os.listdir(logs_dir) if f.endswith('.txt')],
        key=os.path.getmtime
    )
    while len(log_files) > log_amount:
        os.remove(log_files.pop(0))
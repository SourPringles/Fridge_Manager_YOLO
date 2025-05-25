# Base Librarys
from datetime import datetime
import os

# Libraries
from flask_apscheduler import APScheduler

# Custom Modules
from db import load_temp, delete_temp # db 함수 import 확인
from utils.settings import TIMEOUTVALUE


# 스케줄러 인스턴스 생성
scheduler = APScheduler()

# 스케줄러 설정 클래스
class SchedulerConfig:
    SCHEDULER_API_ENABLED = True

@scheduler.task('interval', id='check_temp', seconds=60*10, misfire_grace_time=900)
def check_temp():
    """
    30분마다 실행
    Temp 테이블에서 timestamp가 현재시간 - 3시간 이상인 항목을 삭제
    """
    print(f"---Temp 파일 확인 실행: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}---")

    current_time = datetime.now()

    # temp 테이블에서 현재시간 - timestamp값이 3시간 이상인 항목 제거
    try:
        temp_data = load_temp()
        for data in temp_data:
            try:
                timestamp_str = data['timestamp']

                # 마이크로초 부분 제거 ('.'가 있으면 그 앞부분만 사용)
                if '.' in timestamp_str:
                    timestamp_str = timestamp_str.split('.')[0]

                timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

                # datetime 객체 간의 차이를 계산하고 초 단위로 변환
                time_difference_seconds = (current_time - timestamp_dt).total_seconds()

                # 3시간(10800초) 이상인 경우 삭제
                if time_difference_seconds > TIMEOUTVALUE:
                    delete_temp(data['uuid'])
                    img_path = os.path.join("./db/imgs/temp/", data['uuid']) # os.path.join 사용 권장
                    if os.path.exists(img_path):
                        os.remove(img_path)
                        print(f"--삭제된 temp 항목 uuid: {data['uuid']}, 이미지: {data['uuid']}--")
                    else:
                        print(f"--삭제된 temp 항목 uuid: {data['uuid']}, 이미지 파일 없음: {img_path}--")
                #else:
                #    print(f"유효한 temp 항목 ID: {data['id']}")
            except ValueError as e:
                # 파싱 오류 발생 시 로그 출력
                print(f"Error parsing timestamp for temp item {data.get('uuid', 'N/A')}: {e}. Original string: '{data['timestamp']}'")
            except Exception as e:
                print(f"Error processing temp item {data.get('uuid', 'N/A')}: {e}")
    except Exception as e:
        print(f"Error loading or processing temp data: {e}")


def init_scheduler(app):
    """Flask 앱에 스케줄러를 초기화하고 시작합니다."""
    app.config.from_object(SchedulerConfig())
    scheduler.init_app(app)
    scheduler.start()
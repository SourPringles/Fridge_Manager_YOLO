# librarys
from flask_apscheduler import APScheduler
from datetime import datetime # datetime import 확인
import os # os import 확인

# custom modules
from db import load_temp, delete_temp # db 함수 import 확인

# 스케줄러 인스턴스 생성
scheduler = APScheduler()

# 스케줄러 설정 클래스
class SchedulerConfig:
    SCHEDULER_API_ENABLED = True

# 주기적으로 실행할 작업 함수 정의
TIMEOUTVALUE = 10800   # 초

@scheduler.task('interval', id='my_background_task', seconds=60, misfire_grace_time=900)
def background_task():
    """60초마다 실행될 백그라운드 작업입니다."""
    print(f"백그라운드 작업 실행: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # current_time을 datetime 객체로 유지합니다.
    current_time = datetime.now()
    # 여기에 주기적으로 수행할 로직을 추가하세요.

    # temp 테이블에서 현재시간 - timestamp값이 3시간 이상인 항목 제거
    try:
        temp_data = load_temp()
        for data in temp_data:
            try:
                timestamp_str = data['timestamp']

                # 마이크로초 부분 제거 ('.'가 있으면 그 앞부분만 사용)
                if '.' in timestamp_str:
                    timestamp_str = timestamp_str.split('.')[0]

                # 마이크로초가 제거된 문���열을 파싱하여 datetime 객체로 변환
                timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

                # datetime 객체 간의 차이를 계산하고 초 단위로 변환
                time_difference_seconds = (current_time - timestamp_dt).total_seconds()

                # 3시간(10800초) 이상인 경우 삭제
                if time_difference_seconds > TIMEOUTVALUE:
                    delete_temp(data['id'])
                    img_path = os.path.join("./db/imgs/temp/", data['image']) # os.path.join 사용 권장
                    if os.path.exists(img_path):
                        os.remove(img_path)
                        print(f"삭제된 temp 항목 ID: {data['id']}, 이미지: {data['image']}")
                    else:
                        print(f"삭제된 temp 항목 ID: {data['id']}, 이미지 파일 없음: {img_path}")
                #else:
                #    print(f"유효한 temp 항목 ID: {data['id']}")
            except ValueError as e:
                # 파싱 오류 발생 시 로그 출력
                print(f"Error parsing timestamp for temp item {data.get('id', 'N/A')}: {e}. Original string: '{data['timestamp']}'")
            except Exception as e:
                print(f"Error processing temp item {data.get('id', 'N/A')}: {e}")
    except Exception as e:
        print(f"Error loading or processing temp data: {e}")


def init_scheduler(app):
    """Flask 앱에 스케줄러를 초기화하고 시작합니다."""
    app.config.from_object(SchedulerConfig())
    scheduler.init_app(app)
    scheduler.start()
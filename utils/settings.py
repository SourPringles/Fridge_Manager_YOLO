# YOLO VALUES
YOLOMODELPATH = 'YIM_model.pt' # YOLO 모델 경로
YOLOCONFIDENCE = 0.59 # YOLO 모델 신뢰도 (default: 0.59)

# LOG VALUES
LOGCOUNT = 10 # 최대 로그 파일 개수 (default: 10)
LOGPATH = ".\logs" # 로그 파일 경로 (default: ./logs)

# TEMP TIMEOUT VALUE
TIMEOUTVALUE = 10800 # temp 테이블에서 삭제할 시간 (default: 10800초/3시간)

# CLIP VALUES
CLIPTHRESHOLD = 0.85 # clip 모델 유사도 기준 (default: 0.85)

# BASE IMG DIRS
BASEIMGDIR = ".\db\imgs" # 기본 이미지 저장 경로 (default: ./db/imgs)
#BASEIMGDIRNEW = "./db/imgs/new" # 새로운 이미지 저장 경로 (default: ./db/imgs/new)
#BASEIMGDIRSTORAGE = "./db/imgs/storage" # 저장된 이미지 경로 (default: ./db/imgs/storage)
#BASEIMGDIRTEMP = "./db/imgs/temp" # 임시 이미지 저장 경로 (default: ./db/imgs/temp)

# DB DIR
# BASEDBDIR = "./db/userdata.db"

"""
utils
- scheduler.py
    - TIMEOUTVALUE: 3시간 (10800초)

modules
- compare_similarity_clip.py
    - SAMETHRESHOLD: 0.85 (clip 모델 유사도 기준)
- object_detection.py
    - BASEIMGDIRNEW: "./db/imgs/new"
    - BASEIMGDIRSTORAGE: "./db/imgs/storage"
    - BASEIMGDIRTEMP: "./db/imgs/temp"

"""
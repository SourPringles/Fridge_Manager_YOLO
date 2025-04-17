# Base Libraries
import os

# Librarys

# Custom Modules
from utils.settings import BASEIMGDIR, LOGPATH

base_img_dir = BASEIMGDIR
new_img_dir = os.path.join(base_img_dir, "new")
storage_img_dir = os.path.join(base_img_dir, "storage")
temp_img_dir = os.path.join(base_img_dir, "temp")

base_log_dir = LOGPATH

folders = {new_img_dir, storage_img_dir, temp_img_dir, base_log_dir}

def init_folders():
    """
    Initialize folders for new, storage, and temp images.
    """
    print("---Initializing folders---")
    try:
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder: {folder}")
            else:
                print(f"Folder already exists: {folder}")
        print("---All folders initialized successfully---")
    except Exception as e:
        print(f"!!!Error initializing folders: {e}!!!")
from flask import Blueprint

# Blueprints
from .getStorage import getStorage_bp
from .getTemp import getTemp_bp
from .getAll import getAll_bp
from .updateStorage import pyzbar_bp
from .updateStorage import cv2_bp
from .updateStorage import yolo_bp

# Functions
from .getStorage import get_storage_data
from .getTemp import get_temp_data

# Blueprint 등록
def register_blueprints_main(app):
    app.register_blueprint(getStorage_bp)
    app.register_blueprint(getTemp_bp)
    app.register_blueprint(getAll_bp)
    app.register_blueprint(pyzbar_bp)
    app.register_blueprint(cv2_bp)
    app.register_blueprint(yolo_bp)

__all__ = ["get_storage_data", "get_temp_data"]
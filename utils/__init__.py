from flask import Blueprint

# Blueprints
from .rename import rename_bp
from .reset import reset_bp
from .connectionTest import connectionTest_bp

# Functions
from .commons import save_log, compare_storages
from .qr_utils import detect_qr_codes
from .error_handler import handle_exception

# Blueprint 등록
def register_blueprints_sub(app):
    app.register_blueprint(rename_bp)
    app.register_blueprint(reset_bp)
    app.register_blueprint(connectionTest_bp)

__all__ = ["save_log", "detect_qr_codes", "compare_storages", "register_blueprints_sub", "handle_exception"]
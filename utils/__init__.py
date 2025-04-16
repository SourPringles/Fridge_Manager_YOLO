from flask import Blueprint
# Scheduler
from .scheduler import init_scheduler

# Blueprints
from .rename import rename_bp
from .reset import reset_bp
from .connectionTest import connectionTest_bp

# Functions
from .commons import save_log, compare_storages
from .applyCompareResult import apply_compare_result

# Blueprint 등록
def register_blueprints_sub(app):
    app.register_blueprint(rename_bp)
    app.register_blueprint(reset_bp)
    app.register_blueprint(connectionTest_bp)

__all__ = ["init_scheduler", "save_log", "compare_storages", "register_blueprints_sub", "apply_compare_result"]
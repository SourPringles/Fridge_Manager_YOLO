from flask import Blueprint

from .rename import rename_bp
from .reset import reset_bp
from .connectionTest import connectionTest_bp

# Blueprint 등록
def register_blueprints_sub(app):
    app.register_blueprint(rename_bp)
    app.register_blueprint(reset_bp)
    app.register_blueprint(connectionTest_bp)
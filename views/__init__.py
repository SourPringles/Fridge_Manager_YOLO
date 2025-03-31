from flask import Blueprint

from .getStorage import getStorage_bp
from .updateStorage import updateStorage_bp

# Blueprint 등록
def register_blueprints_main(app):
    app.register_blueprint(getStorage_bp)
    app.register_blueprint(updateStorage_bp)
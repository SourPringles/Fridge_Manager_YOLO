# Blueprints
from .get_items import getStorage_bp, getTemp_bp, getAll_bp
from .update_storage import updateStorage_bp
from .get_image import getImage_bp, getBackground_bp
from .update_nickname import updateNickname_bp
from .reset_all import reset_bp

# Functions
#from .getStorage import get_storage_data
#from .getTemp import get_temp_data

# Blueprint 등록
def register_blueprints_main(app):
    app.register_blueprint(getStorage_bp)
    app.register_blueprint(getTemp_bp)
    app.register_blueprint(getAll_bp)
    app.register_blueprint(updateStorage_bp)
    app.register_blueprint(getImage_bp)
    app.register_blueprint(getBackground_bp)
    app.register_blueprint(updateNickname_bp)
    app.register_blueprint(reset_bp)


__all__ = [
    "get_storage_data", 
    "get_temp_data"
    ]
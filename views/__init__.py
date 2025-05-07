# Blueprints
from .get_storage import getStorage_bp
from .get_temp import getTemp_bp
from .get_all import getAll_bp
from .update_storage import updateStorage_bp
from .get_image import getImage_bp

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

__all__ = [
    "get_storage_data", 
    "get_temp_data"
    ]
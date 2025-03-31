from flask import Flask
from views import register_blueprints_main
from utils import register_blueprints_sub
from db import init_db

app = Flask(__name__)

# Initialize the database
init_db()

# Register blueprints
register_blueprints_main(app)
register_blueprints_sub(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, jsonify
from views import register_blueprints_main
from utils import register_blueprints_sub
from db import init_db

AIMA = Flask(__name__)

# Initialize the database
init_db()

# Register blueprints
register_blueprints_main(AIMA)
register_blueprints_sub(AIMA)

# 전역 에러 핸들러
@AIMA.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@AIMA.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@AIMA.errorhandler(500)
def internal_server_error(e):
    AIMA.logger.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    AIMA.run(host='0.0.0.0', port=5000)
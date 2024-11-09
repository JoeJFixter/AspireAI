from flask import Blueprint, jsonify

# Define a blueprint for this API module
api_blueprint = Blueprint('api_call', __name__)

# Define a route in this module
@api_blueprint.route('/api/api_call', methods=['POST'])
def example1():
    data = {"status": "success", "message": "Hello from API Example"}
    return jsonify(data)
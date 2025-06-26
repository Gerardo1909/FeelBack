from flask import request, jsonify, Blueprint
from app.api.v1.auth.auth_controller import register_user, login_user, verify_user_token
from app.api.v1.auth.auth_schemas import RegisterSchema, LoginSchema
from marshmallow import ValidationError

auth_api_blueprint = Blueprint('auth_api', __name__)



@auth_api_blueprint.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario en feelback"""
    data = request.get_json()
    try:
        validated_data = RegisterSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    response, status = register_user(validated_data)
    return jsonify(response), status

@auth_api_blueprint.route('/login', methods=['POST'])
def login():
    """Inicia sesión un usuario en feelback"""
    data = request.get_json()
    try:
        validated_data = LoginSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    response, status = login_user(validated_data)
    return jsonify(response), status


@auth_api_blueprint.route('/verify-token', methods=['POST'])
def verify_token():
    """Verifica el token de inicio de sesión"""
    data = request.get_json()
    response, status = verify_user_token(data)
    return jsonify(response), status

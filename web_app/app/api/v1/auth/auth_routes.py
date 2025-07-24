"""
    Módulo de rutas para la autenticación de usuarios en la API v1 de FeelBack.
"""

from flask import Blueprint, jsonify, request

from app.api.v1.auth.auth_controller import login_user, register_user, verify_user_token
from app.api.v1.auth.auth_schemas import LoginSchema, RegisterSchema
from app.utils.requests_handlers import handle_api_client_request

auth_api_blueprint = Blueprint('auth_api', __name__)


@auth_api_blueprint.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario en feelback"""
    return handle_api_client_request(RegisterSchema, register_user)


@auth_api_blueprint.route('/login', methods=['POST'])
def login():
    """Inicia sesión un usuario en feelback"""
    return handle_api_client_request(LoginSchema, login_user)


@auth_api_blueprint.route('/verify-token', methods=['POST'])
def verify_token():
    """Verifica el token de inicio de sesión"""
    data = request.get_json()
    response, status = verify_user_token(data)
    return jsonify(response), status

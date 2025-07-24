"""
    Modulo de decoradores comunes utilizados en la app.
"""

from functools import wraps
from flask import request, jsonify
from app.api.v1.auth.auth_service import verify_token

def token_required(f):
    """Decorador para verificar el token JWT en las solicitudes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({'error': 'Token no proporcionado.'}), 401
        
        token = token.split(' ')[1]  # Extraer el token después de "Bearer"
        user_id = verify_token(token)
        if not user_id:
            return jsonify({'error': 'Token inválido o expirado.'}), 401
        
        return f(*args, **kwargs)
    return decorated_function
"""
    Servicio de autenticación para manejar la generación y verificación de tokens JWT.
"""

import jwt
from datetime import datetime, timedelta
from app.config import Config


def generate_token(user_id):
    """Generar un token JWT para el usuario."""
    payload = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    """Verificar un token JWT y devolver el ID del usuario si es válido."""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

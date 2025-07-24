"""
    Controlador de autenticación para el registro, inicio de sesión y verificación de usuarios.
"""

from typing import Dict, Tuple, Union

from app import db
from app.api.v1.auth.auth_service import generate_token, verify_token
from app.models.stats import Stats
from app.models.user import User


def register_user(data):
    """Registra un nuevo usuario en la base de datos."""
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if _validate_user_not_exists(username, email):
        return _validate_user_not_exists(username, email)
    try:
        _init_user_on_db(username, email, password)
    except Exception as e:
        db.session.rollback()
        return {"error": "Error al registrar el usuario. Inténtalo de nuevo."}, 500
    return {"message": "Usuario registrado exitosamente"}, 201


def _validate_user_not_exists(
    username, email
) -> Union[Tuple[Dict[str, str], int], None]:
    """Valida que el usuario no exista en la base de datos."""
    if User.query.filter_by(username=username).first():
        return {"error": "El nombre de usuario ya está registrado."}, 400
    if User.query.filter_by(email=email).first():
        return {"error": "El email ya está registrado."}, 400
    return None


def _init_user_on_db(username: str, email: str, password: str) -> None:
    """Inicializa un nuevo usuario y sus estadísticas en la base de datos."""
    new_user_id = _create_user_on_db(username, email, password)
    _create_user_stats_on_db(new_user_id)
    db.session.commit()


def _create_user_on_db(username: str, email: str, password: str) -> int:
    """Crea un nuevo usuario en la base de datos y devuelve su ID."""
    new_user = User(
        username=username,
        email=email,
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.flush()
    return new_user.id


def _create_user_stats_on_db(user_id: int) -> None:
    """Crea las estadísticas del usuario en la base de datos."""
    new_user_stats = Stats(user_id=user_id)
    db.session.add(new_user_stats)


def login_user(data) -> Tuple[Dict[str, Union[str, int]], int]:
    """Iniciar sesión de usuario."""
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return {"error": "Credenciales inválidas"}, 401
    token = generate_token(user.id)
    return {"token": token, "user_id": user.id}, 200


def verify_user_token(data) -> Tuple[Dict[str, Union[str, int]], int]:
    """Verificar el token del usuario."""
    token = data.get("token")
    if not token:
        return {"error": "Token no proporcionado"}, 400
    user_id = verify_token(token)
    if not user_id:
        return {"error": "Token inválido o expirado"}, 401
    user = db.session.get(User, user_id)
    if not user:
        return {"error": "Usuario no encontrado"}, 404
    return {"message": "Token válido", "user_id": user.id}, 200

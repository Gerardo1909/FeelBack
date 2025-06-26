from app.models.user import User
from app.models.stats import Stats
from app.api.v1.auth.auth_service import generate_token, verify_token
from app import db



def register_user(data):
    """Registrar un nuevo usuario."""
    username = data.get('username')
    mail = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return {'error': 'El nombre de usuario ya está registrado.'}, 400
    
    if User.query.filter_by(email=mail).first():
        return {'error': 'El email ya está registrado.'}, 400
    
    try: 
        # Creo al usuario
        new_user = User(
            username = username,
            email= mail,
        )
        new_user.set_password(password)
        db.session.add(new_user)
        
        db.session.flush()  # Para obtener el ID del usuario recién creado
        
        # Creo las estadísticas del usuario
        new_user_stats = Stats(
            user_id = new_user.id
        )
        db.session.add(new_user_stats)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'error': 'Error al registrar el usuario. Inténtalo de nuevo.'}, 500
    
    return {'message': 'Usuario registrado exitosamente'}, 201


def login_user(data):
    """Iniciar sesión de usuario."""
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return {'error': 'Credenciales inválidas'}, 401
    
    token = generate_token(user.id)
    return {'token': token, 'user_id': user.id}, 200


def verify_user_token(data):
    """Verificar el token del usuario."""
    token = data.get('token')
    
    if not token:
        return {'error': 'Token no proporcionado'}, 400
    
    user_id = verify_token(token)
    
    if not user_id:
        return {'error': 'Token inválido o expirado'}, 401
    
    user = db.session.get(User, user_id)
    
    if not user:
        return {'error': 'Usuario no encontrado'}, 404
    
    return {'message': 'Token válido', 'user_id': user.id}, 200
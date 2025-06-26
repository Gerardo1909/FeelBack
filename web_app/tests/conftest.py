import pytest
from app import create_app, db
from app.models.user import User
from app.models.stats import Stats
from app.api.v1.auth.auth_service import generate_token

@pytest.fixture(scope='function')
def global_user():
    """Crea un usuario global para pruebas y genera un token válido."""
    app = create_app(config_name='testing')
    with app.app_context():
        # Crear al usuario
        new_user = User(
            username='fakeuser',
            email='fake@gmail.com',
        )
        new_user.set_password('fake123')
        db.session.add(new_user)
        db.session.flush()  # Para obtener el ID del usuario recién creado

        # Crear las estadísticas del usuario
        new_user_stats = Stats(
            user_id=new_user.id
        )
        db.session.add(new_user_stats)
        db.session.commit()

        # Generar un token válido para el usuario
        token = generate_token(new_user.id)

        # Devolver el usuario y el token para usarlo en los tests
        yield {'user': new_user, 'token': token}

        # Eliminar el usuario y sus estadísticas después del test
        db.session.delete(new_user_stats)
        db.session.delete(new_user)
        db.session.commit()
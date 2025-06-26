import pytest
from app import create_app, db
from app.config import Config
from app.models.user import User

class TestAuthRoutes:
    
    def setup_method(self):
        """Configura el entorno antes de cada prueba."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        
        # Crear un contexto de aplicación
        self.ctx = self.app.app_context()
        self.ctx.push()
    

    def teardown_method(self):
        """Limpia el entorno después de cada prueba."""
        
        # Selecciono todo de la tabla de usuarios y voy eliminando cada registro
        users = User.query.all()
        for user in users:
            db.session.delete(user)
            db.session.commit()
        
        # Quitar el contexto de aplicación
        self.ctx.pop()
        
        self.app = None
        self.client = None
        

    def test_register(self):
        """Prueba el endpoint de registro de usuario."""
        response = self.client.post(f'{Config.API_BASE_URL}/auth/register', json={
            'username': 'testuser',
            'email': 'user@gmail.com',
            'password': 'testpassword'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Usuario registrado exitosamente'
        
    def test_login(self, global_user):
        """Prueba el endpoint de inicio de sesión."""
        response = self.client.post(f'{Config.API_BASE_URL}/auth/login', json={
            'username': global_user['user'].username,
            'password': 'fake123'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
        assert 'user_id' in data
        
    def test_verify_token(self, global_user):
        """Prueba el endpoint de verificación de token."""
        # Iniciamos sesión para obtener un token
        login_response = self.client.post(f'{Config.API_BASE_URL}/auth/login', json={
            'username': global_user['user'].username,
            'password': 'fake123'
        })
        assert login_response.status_code == 200
        data = login_response.get_json()
        token = data['token']
        
        # Ahora verificamos el token
        response = self.client.post(f'{Config.API_BASE_URL}/auth/verify-token', json={
            'token': token
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Token válido'
        assert 'user_id' in data
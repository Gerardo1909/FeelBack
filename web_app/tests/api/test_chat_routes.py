import pytest
from app import create_app
from app.config import Config

class TestChatRoutes:

    def setup_method(self):
        """Configura el entorno antes de cada prueba."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        # Crear un contexto de aplicación
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        """Limpia el entorno después de cada prueba."""
        # Quitar el contexto de aplicación
        self.ctx.pop()

        self.app = None
        self.client = None

    def test_get_sentiment(self, global_user):
        """Prueba el endpoint de obtener sentimiento."""
        token = global_user['token']  # Obtener el token generado en el fixture

        # Realizar la solicitud al endpoint
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': 'Este es un mensaje de prueba'
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'model_response' in data
        assert 'id_sentiment' in data
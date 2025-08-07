"""
    Tests unitarios para las rutas de chat.
"""

import pytest
from unittest.mock import patch
from app import create_app, db
from app.config import Config
from app.models.sentiment import Sentiment

class TestChatRoutes:
    """Clase de pruebas para las rutas de chat."""

    def setup_method(self):
        """Configura el entorno antes de cada prueba."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        # Crear un contexto de aplicación
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Crear sentimientos necesarios para los tests
        self._create_sentiments()

    def teardown_method(self):
        """Limpia el entorno después de cada prueba."""
        # Quitar el contexto de aplicación
        self.ctx.pop()

        self.app = None
        self.client = None
        
    def _create_sentiments(self):
        """Crea los sentimientos necesarios para los tests."""
        sentiments = [
            {'id': 1, 'description': 'positive'},
            {'id': 2, 'description': 'neutral'}, 
            {'id': 3, 'description': 'negative'}
        ]
        for sentiment_data in sentiments:
            existing = Sentiment.query.filter_by(id=sentiment_data['id']).first()
            if not existing:
                sentiment = Sentiment(id=sentiment_data['id'], description=sentiment_data['description'])
                db.session.add(sentiment)
        db.session.commit()

    def test_get_sentiment_requires_authentication(self):
        """Prueba que el endpoint requiere autenticación."""
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': 'Este es un mensaje de prueba'
        })
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    @patch('app.api.v1.chat.chat_controller.get_model_response')
    def test_get_sentiment_success(self, mock_model_response, global_user):
        """Prueba el endpoint de obtener sentimiento con éxito."""
        # Mock del modelo para devolver un sentimiento conocido
        mock_model_response.return_value = 'positive'
        
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': 'Este es un mensaje positivo'
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'model_response' in data
        assert 'id_sentiment' in data
        assert 'positive' in data['model_response'].lower()
        mock_model_response.assert_called_once_with('Este es un mensaje positivo')

    def test_get_sentiment_missing_message(self, global_user):
        """Prueba el endpoint sin mensaje."""
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={}, 
                                  headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code in (400, 422)
        data = response.get_json()
        assert 'error' in data or 'message' in data

    def test_get_sentiment_empty_message(self, global_user):
        """Prueba el endpoint con mensaje vacío."""
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': ''
        }, headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code in (400, 422)
        data = response.get_json()
        assert 'error' in data or 'message' in data

    def test_get_sentiment_invalid_token(self):
        """Prueba el endpoint con token inválido."""
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': 'Este es un mensaje de prueba'
        }, headers={'Authorization': 'Bearer invalid_token'})
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    @patch('app.api.v1.chat.chat_controller.get_model_response')
    def test_get_sentiment_negative_message(self, mock_model_response, global_user):
        """Prueba el endpoint con un mensaje negativo."""
        mock_model_response.return_value = 'negative'
        
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': 'Este es un mensaje terrible'
        }, headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'model_response' in data
        assert 'id_sentiment' in data
        assert 'negative' in data['model_response'].lower()

    @patch('app.api.v1.chat.chat_controller.get_model_response')
    def test_get_sentiment_neutral_message(self, mock_model_response, global_user):
        """Prueba el endpoint con un mensaje neutral."""
        mock_model_response.return_value = 'neutral'
        
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': 'Este es un mensaje normal'
        }, headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'model_response' in data
        assert 'id_sentiment' in data
        assert 'neutral' in data['model_response'].lower()

    @patch('app.api.v1.chat.chat_controller.get_model_response')
    def test_get_sentiment_model_error(self, mock_model_response, global_user):
        """Prueba el endpoint cuando el modelo falla."""
        mock_model_response.side_effect = Exception("Error del modelo")
        
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': 'Este es un mensaje de prueba'
        }, headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_get_sentiment_long_message(self, global_user):
        """Prueba el endpoint con un mensaje muy largo."""
        token = global_user['token']
        long_message = 'a' * 501  # Excede el límite de 500 caracteres
        
        response = self.client.post(f'{Config.API_BASE_URL}/chat/get-sentiment', json={
            'message': long_message
        }, headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code in (400, 422)
        data = response.get_json()
        assert 'error' in data or 'message' in data
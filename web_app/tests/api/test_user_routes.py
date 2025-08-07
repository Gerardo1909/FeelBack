"""
    Tests unitarios para las rutas de usuario.
"""

import pytest
from app import create_app, db
from app.models.message import Message
from app.models.sentiment import Sentiment
from app.config import Config

class TestUserRoutes:
    """Clase de pruebas para las rutas de usuario."""

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
        # Selecciono todo de la tabla de mensajes y voy eliminando cada registro
        messages = Message.query.all()
        for message in messages:
            db.session.delete(message)
            db.session.commit()
            
        # Limpiar sentimientos
        sentiments = Sentiment.query.all()
        for sentiment in sentiments:
            db.session.delete(sentiment)
            db.session.commit()

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
            if not Sentiment.query.filter_by(id=sentiment_data['id']).first():
                sentiment = Sentiment(id=sentiment_data['id'], description=sentiment_data['description'])
                db.session.add(sentiment)
        db.session.commit()


    def test_save_message_requires_authentication(self):
        """Prueba que el endpoint de guardar mensaje requiere autenticación."""
        response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': 1,
            'text': 'Este es un mensaje de prueba',
            'id_sentiment': 1,
            'liked': True
        })
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_save_message_success(self, global_user):
        """Prueba guardar un mensaje exitosamente."""
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Este es un mensaje de prueba',
            'id_sentiment': 1,
            'liked': True
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'id_message' in data
        assert data['message'] == 'Mensaje guardado exitosamente'
        
    def test_save_message_with_none_liked(self, global_user):
        """Prueba guardar un mensaje sin valoración (liked=None)."""
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Este es un mensaje sin valoración',
            'id_sentiment': 2,
            'liked': None
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'id_message' in data

    def test_save_message_missing_fields(self, global_user):
        """Prueba guardar mensaje con campos faltantes."""
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': '',
            'id_sentiment': 1
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code in (400, 422)
        data = response.get_json()
        assert 'error' in data or 'message' in data

    def test_save_message_invalid_sentiment(self, global_user):
        """Prueba guardar mensaje con id_sentiment inválido."""
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Mensaje con sentimiento inválido',
            'id_sentiment': 999,
            'liked': True
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data

    def test_delete_message_success(self, global_user):
        """Prueba eliminar un mensaje exitosamente."""
        token = global_user['token']
        # Primero, guardar un mensaje
        save_response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Mensaje para eliminar',
            'id_sentiment': 2,
            'liked': False
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        message_id = save_response.get_json()['id_message']

        # Luego, eliminar el mensaje
        delete_response = self.client.post(f'{Config.API_BASE_URL}/user/delete-message', json={
            'user_id': global_user['user'].id,
            'message_id': int(message_id)
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert delete_response.status_code == 200
        data = delete_response.get_json()
        assert 'message' in data
        assert data['message'] == 'Mensaje eliminado exitosamente'

    def test_delete_message_not_found(self, global_user):
        """Prueba eliminar un mensaje que no existe."""
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/user/delete-message', json={
            'user_id': global_user['user'].id,
            'message_id': 99999
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'no encontrado' in data['error'].lower()

    def test_delete_message_requires_authentication(self):
        """Prueba que eliminar mensaje requiere autenticación."""
        response = self.client.post(f'{Config.API_BASE_URL}/user/delete-message', json={
            'user_id': 1,
            'message_id': 1
        })
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_get_message_success(self, global_user):
        """Prueba obtener un mensaje específico exitosamente."""
        token = global_user['token']
        # Primero, guardar un mensaje
        save_response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Mensaje para obtener',
            'id_sentiment': 3,
            'liked': None
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        message_id = save_response.get_json()['id_message']

        # Luego, obtener el mensaje
        get_response = self.client.get(f'{Config.API_BASE_URL}/user/get-message', json={
            'user_id': global_user['user'].id,
            'message_id': int(message_id)
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert get_response.status_code == 200
        data = get_response.get_json()
        assert 'message' in data
        assert data['message']['text'] == 'Mensaje para obtener'
        assert data['message']['id_sentiment'] == 3
        assert data['message']['liked'] is None  
        assert data['message']['user_id'] == global_user['user'].id
        assert data['message']['sentiment_text'] == 'negative'

    def test_get_message_not_found(self, global_user):
        """Prueba obtener un mensaje que no existe."""
        token = global_user['token']
        response = self.client.get(f'{Config.API_BASE_URL}/user/get-message', json={
            'user_id': global_user['user'].id,
            'message_id': 99999
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'no encontrado' in data['error'].lower()

    def test_get_message_requires_authentication(self):
        """Prueba que obtener mensaje requiere autenticación."""
        response = self.client.get(f'{Config.API_BASE_URL}/user/get-message', json={
            'user_id': 1,
            'message_id': 1
        })
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_get_messages_success(self, global_user):
        """Prueba obtener todos los mensajes del usuario."""
        token = global_user['token']
        # Guardar varios mensajes
        self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Primer mensaje',
            'id_sentiment': 1,
            'liked': True
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Segundo mensaje',
            'id_sentiment': 2,
            'liked': False
        }, headers={
            'Authorization': f'Bearer {token}'
        })

        # Obtener todos los mensajes
        get_response = self.client.get(f'{Config.API_BASE_URL}/user/get-messages', json={
            'user_id': global_user['user'].id
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert get_response.status_code == 200
        data = get_response.get_json()
        assert 'messages' in data
        assert len(data['messages']) >= 2

    def test_get_messages_empty(self, global_user):
        """Prueba obtener mensajes cuando el usuario no tiene ninguno."""
        token = global_user['token']
        response = self.client.get(f'{Config.API_BASE_URL}/user/get-messages', json={
            'user_id': global_user['user'].id
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'no se encontraron mensajes' in data['error'].lower()

    def test_get_messages_requires_authentication(self):
        """Prueba que obtener mensajes requiere autenticación."""
        response = self.client.get(f'{Config.API_BASE_URL}/user/get-messages', json={
            'user_id': 1
        })
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_get_stats_success(self, global_user):
        """Prueba obtener estadísticas del usuario."""
        token = global_user['token']
        # Obtener estadísticas del usuario
        stats_response = self.client.get(f'{Config.API_BASE_URL}/user/get-stats', json={
            'user_id': global_user['user'].id
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert stats_response.status_code == 200
        data = stats_response.get_json()
        assert 'stats' in data
        assert 'positive' in data['stats']
        assert 'negative' in data['stats']
        assert 'neutral' in data['stats']
        assert 'liked' in data['stats']
        assert 'disliked' in data['stats']

    def test_get_stats_requires_authentication(self):
        """Prueba que obtener estadísticas requiere autenticación."""
        response = self.client.get(f'{Config.API_BASE_URL}/user/get-stats', json={
            'user_id': 1
        })
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data

    def test_save_message_updates_stats(self, global_user):
        """Prueba que guardar mensajes actualiza las estadísticas correctamente."""
        token = global_user['token']
        
        # Obtener estadísticas iniciales
        initial_stats = self.client.get(f'{Config.API_BASE_URL}/user/get-stats', json={
            'user_id': global_user['user'].id
        }, headers={'Authorization': f'Bearer {token}'}).get_json()['stats']
        
        # Guardar mensaje positivo con like
        self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Mensaje positivo',
            'id_sentiment': 1,
            'liked': True
        }, headers={'Authorization': f'Bearer {token}'})
        
        # Verificar que las estadísticas se actualizaron
        final_stats = self.client.get(f'{Config.API_BASE_URL}/user/get-stats', json={
            'user_id': global_user['user'].id
        }, headers={'Authorization': f'Bearer {token}'}).get_json()['stats']
        
        assert final_stats['positive'] == initial_stats['positive'] + 1
        assert final_stats['liked'] == initial_stats['liked'] + 1

    def test_delete_message_updates_stats(self, global_user):
        """Prueba que eliminar mensajes actualiza las estadísticas correctamente."""
        token = global_user['token']
        
        # Guardar un mensaje
        save_response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Mensaje para eliminar y verificar stats',
            'id_sentiment': 2,
            'liked': False
        }, headers={'Authorization': f'Bearer {token}'})
        message_id = save_response.get_json()['id_message']
        
        # Obtener estadísticas después de guardar
        stats_after_save = self.client.get(f'{Config.API_BASE_URL}/user/get-stats', json={
            'user_id': global_user['user'].id
        }, headers={'Authorization': f'Bearer {token}'}).get_json()['stats']
        
        # Eliminar el mensaje
        self.client.post(f'{Config.API_BASE_URL}/user/delete-message', json={
            'user_id': global_user['user'].id,
            'message_id': int(message_id)
        }, headers={'Authorization': f'Bearer {token}'})
        
        # Verificar que las estadísticas se decrementaron
        final_stats = self.client.get(f'{Config.API_BASE_URL}/user/get-stats', json={
            'user_id': global_user['user'].id
        }, headers={'Authorization': f'Bearer {token}'}).get_json()['stats']
        
        assert final_stats['neutral'] == stats_after_save['neutral'] - 1
        assert final_stats['disliked'] == stats_after_save['disliked'] - 1
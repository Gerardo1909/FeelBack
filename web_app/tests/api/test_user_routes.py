import pytest
from app import create_app, db
from app.models.message import Message
from app.config import Config

class TestUserRoutes:

    def setup_method(self):
        """Configura el entorno antes de cada prueba."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        # Crear un contexto de aplicación
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        """Limpia el entorno después de cada prueba."""
        # Selecciono todo de la tabla de mensajes y voy eliminando cada registro
        messages = Message.query.all()
        for message in messages:
            db.session.delete(message)
            db.session.commit()

        # Quitar el contexto de aplicación
        self.ctx.pop()

        self.app = None
        self.client = None

    def test_save_message(self, global_user):
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
        
    def test_save_noneliked_message(self, global_user):
        token = global_user['token']
        response = self.client.post(f'{Config.API_BASE_URL}/user/save-message', json={
            'user_id': global_user['user'].id,
            'text': 'Este es un mensaje de prueba sin like',
            'id_sentiment': 2,
            'liked': None
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert 'id_message' in data

    def test_delete_message(self, global_user):
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
            'message_id': message_id
        }, headers={
            'Authorization': f'Bearer {token}'
        })
        assert delete_response.status_code == 200
        data = delete_response.get_json()
        assert 'message' in data

    def test_get_message(self, global_user):
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
            'message_id': message_id
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

    def test_get_messages(self, global_user):
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

    def test_get_stats(self, global_user):
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
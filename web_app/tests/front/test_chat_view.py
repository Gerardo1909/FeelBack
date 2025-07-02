import pytest
from app import create_app

class TestChatView:
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()
        self.app = None
        self.client = None

    def test_chat_requires_login(self):
        response = self.client.get('/chat', follow_redirects=True)
        assert 'Iniciar Sesi' in response.get_data(as_text=True)

    def test_chat_get(self):
        # Implementar simulacion de login y acceso a la vista del chat
        pass

    def test_chat_post_message(self):
        # Implementar simulacion de login y envio de mensaje en el chat
        pass

import pytest
from app import create_app

class TestHistoryView:
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()
        self.app = None
        self.client = None

    def test_history_requires_login(self):
        response = self.client.get('/history', follow_redirects=True)
        assert 'Iniciar Sesi' in response.get_data(as_text=True)

    def test_history_get(self):
        # Implementar simulacion de login y luego acceder a /history
        pass

    def test_history_delete_message(self):
        # Implementar simulacion de login y eliminar un mensaje
        pass

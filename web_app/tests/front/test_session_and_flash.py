import pytest
from app import create_app, db
from flask import session
from app.models.user import User

class TestSessionAndFlash:
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()
        self.app = None
        self.client = None

    def test_session_token_set(self, mocker, global_user):
        pass

    def test_flash_message_on_error(self, mocker, global_user):
        pass

    def test_protected_route_requires_login(self):
        pass

    def test_logout_clears_session_and_flash(self, mocker, global_user):
        pass

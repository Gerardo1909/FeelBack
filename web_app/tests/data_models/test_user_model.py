import pytest
from app import create_app, db
from app.models.user import User

class TestUserModel:
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        self.ctx.pop()
        self.app = None
        self.client = None

    def test_password_hashing(self):
        user = User(username='foo', email='foo@bar.com')
        user.set_password('secret')
        db.session.add(user)
        db.session.commit()
        assert user.verify_password('secret')
        assert not user.verify_password('wrong')

import pytest
from app import create_app, db
from app.models.message import Message
from app.models.user import User

class TestMessageModel:
    
    # SENTIMIENTOS IDS:
    # 1: Positivo
    # 2: Neutral
    # 3: Negativo

    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Creo usuario para pruebas
        self.user = User(username='msguser', email='msg@foo.com')
        self.user.set_password('1234')
        db.session.add(self.user)
        db.session.commit()

    def teardown_method(self):
        Message.query.delete()
        User.query.delete()
        db.session.commit()
        self.ctx.pop()
        self.app = None
        self.client = None

    def test_create_message(self):
        # Prueba de mandar mensaje positivo
        msg = Message(user_id=self.user.id, text='Hola mundo', id_sentiment= 1)
        db.session.add(msg)
        db.session.commit()
        assert msg.id is not None
        assert msg.text == 'Hola mundo'
        assert msg.user_id == self.user.id
        assert msg.id_sentiment == 1

    def test_to_dict(self):
        msg = Message(user_id=self.user.id, text='Prueba dict', id_sentiment= 3)
        db.session.add(msg)
        db.session.commit()
        d = msg.to_dict()
        assert d['text'] == 'Prueba dict'
        assert d['sentiment_text'] == 'negative'

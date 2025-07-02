import pytest
from app import create_app, db
from app.models.sentiment import Sentiment

class TestSentimentModel:
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()
        self.app = None
        self.client = None

    @pytest.mark.parametrize('desc', ['alegre', 'triste', '', 'POSITIVO'])
    def test_constraint(self, desc):
        s = Sentiment(description=desc)
        db.session.add(s)
        with pytest.raises(Exception):
            db.session.commit()

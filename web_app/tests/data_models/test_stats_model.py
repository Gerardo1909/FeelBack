import pytest
from app import create_app, db
from app.models.stats import Stats
from app.models.user import User

class TestStatsModel:
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.user = User(username='statsuser', email='stats@foo.com')
        self.user.set_password('1234')
        db.session.add(self.user)
        db.session.commit()

    def teardown_method(self):
        Stats.query.delete()
        User.query.delete()
        db.session.commit()
        self.ctx.pop()
        self.app = None
        self.client = None

    def test_create_stats(self):
        stats = Stats(user_id=self.user.id, positive=2, negative=1, neutral=3, liked=1, disliked=0)
        db.session.add(stats)
        db.session.commit()
        assert stats.user_id == self.user.id
        assert stats.positive == 2
        assert stats.neutral == 3

    def test_to_dict(self):
        stats = Stats(user_id=self.user.id, positive=1, negative=2, neutral=0, liked=0, disliked=1)
        db.session.add(stats)
        db.session.commit()
        d = stats.to_dict()
        assert d['positive'] == 1
        assert d['disliked'] == 1

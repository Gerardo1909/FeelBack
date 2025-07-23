"""
Clase ORM para la tabla messages.
"""

from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.sentiment import Sentiment
from app import db


class Message(db.Model):
    """Modelo para la tabla messages"""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    id_sentiment = db.Column(db.Integer, db.ForeignKey("sentiments.id"), nullable=False)
    liked = db.Column(db.Boolean, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())

    user = relationship("User", back_populates="messages")
    sentiment = relationship("Sentiment", back_populates="messages")

    def __repr__(self):
        return f"<Message {self.id}: {self.text[:30]}...>"

    def to_dict(self):
        """Convierte el modelo a un diccionario."""

        return {
            "id": self.id,
            "user_id": self.user_id,
            "text": self.text,
            "id_sentiment": self.id_sentiment,
            "liked": self.liked,
            "created_at": self.created_at.strftime("%Y-%m-%d"),
            "sentiment_text": self._get_sentiment_text(),
        }
        
        
    def _get_sentiment_text(self) -> str:
        """Obtiene el texto del sentimiento asociado al mensaje."""
        sentiment = db.session.get(Sentiment, self.id_sentiment)
        return sentiment.description

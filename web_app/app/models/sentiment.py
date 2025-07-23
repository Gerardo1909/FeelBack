"""
Clase ORM para la tabla sentiments.
"""

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from app import db


class Sentiment(db.Model):
    """Modelo para la tabla sentiments"""

    __tablename__ = "sentiments"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), nullable=False, unique=True)

    __table_args__ = (
        CheckConstraint(
            "description IN ('positive', 'neutral', 'negative')",
            name="check_sentiment_values",
        ),
    )

    messages = relationship("Message", back_populates="sentiment")

    def __repr__(self):
        return f"<Sentiment {self.description}>"

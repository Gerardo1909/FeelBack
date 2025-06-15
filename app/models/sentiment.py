"""
Sentiment Model - Modelo de sentimientos para FeelBack
"""

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from app import db

class Sentiment(db.Model):
    """Modelo para la tabla sentiments"""
    __tablename__ = 'sentiments'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(20), nullable=False, unique=True)
    
    # Constraint para validar valores
    __table_args__ = (
        CheckConstraint("description IN ('positive', 'neutral', 'negative')", 
                       name='check_sentiment_values'),
    )
    
    # Relaciones
    messages = relationship('Message', back_populates='sentiment')
    
    def __repr__(self):
        return f'<Sentiment {self.description}>'

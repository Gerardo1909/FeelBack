"""
Message Model - Modelo de mensajes para FeelBack
"""

from datetime import datetime
from sqlalchemy.orm import relationship
from app import db

class Message(db.Model):
    """Modelo para la tabla messages"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    id_sentiment = db.Column(db.Integer, db.ForeignKey('sentiments.id'), nullable=False)
    liked = db.Column(db.Boolean, default=None)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    # Relaciones
    user = relationship('User', back_populates='messages')
    sentiment = relationship('Sentiment', back_populates='messages')
    
    def __repr__(self):
        return f'<Message {self.id}: {self.text[:30]}...>'
    

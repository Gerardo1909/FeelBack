"""
Stats Model - Modelo de estadísticas para FeelBack
"""

from sqlalchemy.orm import relationship
from app import db

class Stats(db.Model):
    """Modelo para la tabla stats"""
    __tablename__ = 'stats'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    positive = db.Column(db.Integer, default=0)
    negative = db.Column(db.Integer, default=0)
    neutral = db.Column(db.Integer, default=0)
    
    # Relaciones
    user = relationship('User', back_populates='stats')
    
    def __repr__(self):
        return f'<Stats User:{self.user_id} P:{self.positive} N:{self.negative} Ne:{self.neutral}>'
    

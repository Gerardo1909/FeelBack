"""
Modelo de usuario para FeelBack
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """Modelo para la tabla users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    # Relaciones
    messages = relationship('Message', back_populates='user', cascade='all, delete-orphan')
    stats = relationship('Stats', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @property
    def password(self):
        """No se debe permitir acceder directamente a la contraseña"""
        raise AttributeError("La contraseña no se puede leer directamente.")
    
    @password.setter
    def password(self, password):
        """Genera un hash de la contraseña al establecerla"""
        self.password = generate_password_hash(password)
        
    def verify_password(self, password):
        """Verifica la contraseña ingresada contra el hash almacenado"""
        return check_password_hash(self.password, password)
    


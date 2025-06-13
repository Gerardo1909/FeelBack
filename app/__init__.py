from flask import Flask
from app.config import config 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name='default'):
    """Función Factory para crear aplicaciones."""
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Cargar la configuración de la aplicación
    app.config.from_object(config[config_name])
    
    # Inicializar la base de datos
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
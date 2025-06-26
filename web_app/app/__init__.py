from flask import Flask
from app.config import config 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  


def create_app(config_name='default'):
    """Función Factory para crear aplicaciones."""
    
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Cargar la configuración de la aplicación
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Inicializar la base de datos
    db.init_app(app)
    login_manager.init_app(app)
    
    # Registrar blueprints
    from app.main import main as main_blueprint
    from app.auth import auth as auth_blueprint
    from app.api.v1 import api_v1 as api_v1_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
    
    return app
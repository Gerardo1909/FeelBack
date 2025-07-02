from flask import Flask, render_template, url_for, request, current_app
from app.config import config 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.utils.logging_config import logger

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

    # Handlers de error globales
    @app.errorhandler(Exception)
    def handle_global_exception(error):
        logger.error("Unhandled Exception", error=str(error), path=request.path, method=request.method)
        return render_template('main/error.html',
                             error_code=500,
                             error_title="Error interno del servidor",
                             error_message="Ocurrió un error inesperado. Estamos trabajando para solucionarlo.",
                             error_details=str(error),
                             request=request,
                             config=current_app.config), 500

    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning("404 Not Found", path=request.path)
        suggestions = [
            {
                'name': 'Página de Inicio',
                'description': 'Volver a la página principal',
                'url': url_for('main.home'),
                'icon': '🏠'
            },
            {
                'name': 'Chat de Análisis',
                'description': 'Analizar sentimientos',
                'url': url_for('main.chat'),
                'icon': '💬'
            }
        ]
        return render_template('main/error.html',
                             error_code=404,
                             error_title="Página no encontrada",
                             error_message="La página que buscas no existe.",
                             suggestions=suggestions,
                             request=request,
                             config=current_app.config), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error("500 Internal Server Error", error=str(error), path=request.path)
        return render_template('main/error.html',
                             error_code=500,
                             error_title="Error interno del servidor",
                             error_message="Estamos trabajando para solucionarlo.",
                             error_details=str(error),
                             request=request,
                             config=current_app.config), 500

    return app
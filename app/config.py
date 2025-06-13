import os 
from dotenv import load_dotenv

class Config:
    """Clase de configuración base."""
    load_dotenv()  # Carga las variables de entorno desde un archivo .env

    # Configuracion de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        """Método para inicializar la aplicación con esta configuración."""
        pass
    
class DevelopmentConfig(Config):
    """Configuración para el entorno de desarrollo."""
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    SQLALCHEMY_ECHO = True  # Muestra las consultas SQL en la consola


class TestingConfig(Config):
    """Configuración para el entorno de pruebas."""
    TESTING = True
    SQLALCHEMY_ECHO = False  # No muestra las consultas SQL en la consola
    PRESERVE_CONTEXT_ON_EXCEPTION = False  # No preserva el contexto en caso de excepciones


class ProductionConfig(Config):
    """Configuración para el entorno de producción."""
    DEBUG = False
    SQLALCHEMY_ECHO = False  # No muestra las consultas SQL en la consola
    
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
    

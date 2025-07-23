'''
    Configuración de la aplicación web.
'''

import os
from dotenv import load_dotenv

class Config:
    """Clase de configuración base."""

    load_dotenv()

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or "dev-secret-key-change-in-production"
    API_BASE_URL = os.getenv("API_BASE_URL")

    @staticmethod
    def init_app(app):
        """Método para inicializar la aplicación con esta configuración."""


class DevelopmentConfig(Config):
    """Configuración para el entorno de desarrollo."""

    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = (
        f"{Config.SQLALCHEMY_DATABASE_URI}?options=-c%20search_path=feelback_dev"
    )


class TestingConfig(Config):
    """Configuración para el entorno de pruebas."""

    TESTING = True
    SQLALCHEMY_ECHO = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = (
        f"{Config.SQLALCHEMY_DATABASE_URI}?options=-c%20search_path=feelback_test"
    )


class ProductionConfig(Config):
    """Configuración para el entorno de producción."""

    DEBUG = False
    SQLALCHEMY_ECHO = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}

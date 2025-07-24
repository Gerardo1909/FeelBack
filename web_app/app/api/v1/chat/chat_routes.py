"""
    Módulo de rutas para el chat en la API v1 de FeelBack.
"""

from flask import Blueprint

from app.api.v1.chat.chat_controller import get_sentiment_response
from app.api.v1.chat.chat_schemas import MessageSchema
from app.utils.decorators import token_required
from app.utils.requests_handlers import handle_api_client_request

chat_api_blueprint = Blueprint("chat_api", __name__)


@chat_api_blueprint.route("/get-sentiment", methods=["POST"])
@token_required
def get_sentiment():
    """Obtiene la respuesta del modelo de lenguaje para el mensaje del usuario."""
    return handle_api_client_request(MessageSchema, get_sentiment_response)

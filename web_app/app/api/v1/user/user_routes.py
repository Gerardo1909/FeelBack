"""
    Módulo de rutas para la gestión de usuarios en la API v1 de FeelBack.
"""

from flask import Blueprint

from app.api.v1.user.user_controller import (
    save_message_info_to_db,
    delete_message_from_db,
    get_user_message,
    get_user_messages,
    get_user_stats,
)
from app.api.v1.user.user_schemas import (
    SaveMessageSchema,
    DeleteMessageSchema,
    GetMessageSchema,
    GetMessagesSchema,
    GetStatsSchema,
)
from app.utils.decorators import token_required
from app.utils.requests_handlers import handle_api_client_request

user_api_blueprint = Blueprint("user_api", __name__)


@user_api_blueprint.route("/save-message", methods=["POST"])
@token_required
def save_message():
    """Guarda un mensaje del usuario en la base de datos."""
    return handle_api_client_request(SaveMessageSchema, save_message_info_to_db)


@user_api_blueprint.route("/delete-message", methods=["POST"])
@token_required
def delete_message():
    """Elimina un mensaje del usuario de la base de datos."""
    return handle_api_client_request(DeleteMessageSchema, delete_message_from_db)


@user_api_blueprint.route("/get-message", methods=["GET"])
@token_required
def get_message():
    """Obtiene un mensaje del usuario de la base de datos."""
    return handle_api_client_request(GetMessageSchema, get_user_message)


@user_api_blueprint.route("/get-messages", methods=["GET"])
@token_required
def get_messages():
    """Obtiene todos los mensajes del usuario de la base de datos."""
    return handle_api_client_request(GetMessagesSchema, get_user_messages)


@user_api_blueprint.route("/get-stats", methods=["GET"])
@token_required
def get_stats():
    """Obtiene las estadísticas del usuario."""
    return handle_api_client_request(GetStatsSchema, get_user_stats)

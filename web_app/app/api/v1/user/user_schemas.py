"""
    Esquemas de validación para la gestión de usuarios en la API v1 de FeelBack.
"""

from marshmallow import Schema, fields, validate


class SaveMessageSchema(Schema):
    """
    Esquema para guardar un mensaje del usuario.
    """
    user_id = fields.Int(required=True)
    text = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    id_sentiment = fields.Int(required=True)
    liked = fields.Boolean(allow_none=True)


class DeleteMessageSchema(Schema):
    """
        Esquema para eliminar un mensaje del usuario.
    """
    user_id = fields.Int(required=True)
    message_id = fields.Int(required=True)


class GetMessageSchema(Schema):
    """
        Esquema para obtener un mensaje específico del usuario.
    """
    user_id = fields.Int(required=True)
    message_id = fields.Int(required=True)


class GetMessagesSchema(Schema):
    """
        Esquema para obtener todos los mensajes del usuario.
    """
    user_id = fields.Int(required=True)


class GetStatsSchema(Schema):
    """
        Esquema para obtener las estadísticas de los mensajes del usuario.
    """
    user_id = fields.Int(required=True)
    
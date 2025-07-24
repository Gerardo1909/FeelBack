"""
    Esquemas de validación para la gestión de mensajes en la API v1 de FeelBack.
"""

from marshmallow import Schema, fields, validate


class MessageSchema(Schema):
    """
        Esquema para un mensaje en el chat.
    """
    message = fields.Str(required=True, validate=validate.Length(min=1, max=500))

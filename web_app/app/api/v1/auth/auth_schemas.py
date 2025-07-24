"""
    Esquemas de validación para la autenticación de usuarios en la API v1 de FeelBack.
"""

from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    """
        Esquema para el registro de un nuevo usuario.
    """
    username = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=validate.Length(min=1))

class LoginSchema(Schema):
    """
        Esquema para el inicio de sesión de un usuario.
    """
    username = fields.Str(required=True, validate=validate.Length(max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1))
    
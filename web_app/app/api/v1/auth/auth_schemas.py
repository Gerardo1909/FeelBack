from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(max=50))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, validate=validate.Length(min=1))

class LoginSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1))
from marshmallow import Schema, fields, validate

class MessageSchema(Schema):
    message = fields.Str(required=True, validate=validate.Length(min=1, max=500))

from marshmallow import Schema, fields, validate

class SaveMessageSchema(Schema):
    user_id = fields.Int(required=True)
    text = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    id_sentiment = fields.Int(required=True)
    liked = fields.Boolean(allow_none=True)

class DeleteMessageSchema(Schema):
    user_id = fields.Int(required=True)
    message_id = fields.Int(required=True)

class GetMessageSchema(Schema):
    user_id = fields.Int(required=True)
    message_id = fields.Int(required=True)

class GetMessagesSchema(Schema):
    user_id = fields.Int(required=True)

class GetStatsSchema(Schema):
    user_id = fields.Int(required=True)
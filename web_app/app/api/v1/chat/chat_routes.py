from flask import request, jsonify, Blueprint
from app.api.v1.chat.chat_controller import get_sentiment_response
from app.api.utils.decorators import token_required
from app.api.v1.chat.chat_schemas import MessageSchema
from marshmallow import ValidationError

chat_api_blueprint = Blueprint('chat_api', __name__)


@chat_api_blueprint.route('/get-sentiment', methods=['POST'])
@token_required
def get_sentiment():
    data = request.get_json()
    try:
        validated_data = MessageSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400

    response, status = get_sentiment_response(validated_data)
    return jsonify(response), status
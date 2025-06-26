from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from app.api.utils.decorators import token_required
from app.api.v1.user.user_controller import (save_message_info_to_db, 
                                             delete_message_from_db, get_user_message, 
                                             get_user_messages, get_user_stats)
from app.api.v1.user.user_schemas import (SaveMessageSchema, DeleteMessageSchema, 
                                          GetMessageSchema, GetMessagesSchema, GetStatsSchema)

user_api_blueprint = Blueprint('user_api', __name__)

@user_api_blueprint.route('/save-message', methods=['POST'])
@token_required
def save_message():
    """Guarda un mensaje del usuario en la base de datos."""
    data = request.get_json()
    try:
        # Para que tome correctamente el none
        if data['liked'] == 'None':
            data['liked'] = None
        validated_data = SaveMessageSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    response, status = save_message_info_to_db(validated_data)
    return jsonify(response), status

@user_api_blueprint.route('/delete-message', methods=['POST'])
@token_required
def delete_message():
    """Elimina un mensaje del usuario de la base de datos."""
    data = request.get_json()
    try:
        validated_data = DeleteMessageSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    response, status = delete_message_from_db(validated_data)
    return jsonify(response), status

@user_api_blueprint.route('/get-message', methods=['GET'])
@token_required
def get_message():
    """Obtiene un mensaje del usuario de la base de datos."""
    data = request.get_json()
    try:
        validated_data = GetMessageSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    response, status = get_user_message(validated_data)
    return jsonify(response), status

@user_api_blueprint.route('/get-messages', methods=['GET'])
@token_required
def get_messages():
    """Obtiene todos los mensajes del usuario de la base de datos."""
    data = request.get_json()
    try:
        validated_data = GetMessagesSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    response, status = get_user_messages(validated_data)
    return jsonify(response), status

@user_api_blueprint.route('/get-stats', methods=['GET'])
@token_required
def get_stats():
    """Obtiene las estadísticas del usuario."""
    data = request.get_json()
    try:
        validated_data = GetStatsSchema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    
    response, status = get_user_stats(validated_data)
    return jsonify(response), status




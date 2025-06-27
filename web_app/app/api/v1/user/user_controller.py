from app import db
from app.models.message import Message
from app.models.stats import Stats
from app.models.sentiment import Sentiment


def save_message_info_to_db(data):
    """Guarda un solo mensaje del usuario en la base de datos."""
    
    user_id = int(data.get('user_id'))
    id_sentiment = int(data.get('id_sentiment'))
    liked = data.get('liked')
    
    
    try:
        # Añado el mensaje
        new_message = Message(
            user_id= user_id,
            text= data.get('text'),
            id_sentiment= id_sentiment,
            liked= liked,
            # Guardar 'feedback' también en el futuro
        )
        db.session.add(new_message)
        
        # Añado el mensaje a las estadísticas
        user_stats = db.session.get(Stats, user_id)
        
        if id_sentiment == 1:
            user_stats.positive += 1
        elif id_sentiment == 2:
            user_stats.neutral += 1
        elif id_sentiment == 3:
            user_stats.negative += 1
            
        if liked is not None:
            if liked:
                user_stats.liked += 1
            else:
                user_stats.disliked += 1
        
        
        db.session.add(user_stats)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        return {'error': 'Error al guardar el mensaje. Intenta nuevamente.'}, 500
    
    return {'message': 'Mensaje guardado exitosamente', 'id_message': f'{new_message.id}'}, 201

def delete_message_from_db(data):
    """Elimina un solo mensaje del usuario en la base de datos."""
    
    user_id = int(data.get('user_id'))
    message_id = int(data.get('message_id'))
    
    message = db.session.get(Message, message_id)
    if not message or message.user_id != user_id:
        return {'error': 'Mensaje no encontrado o no pertenece al usuario'}, 404
    try: 
        db.session.delete(message)
        
        # Borro el mensaje de las estadísticas
        user_stats = db.session.get(Stats, data['user_id'])
        
        if message.id_sentiment == 1:
            user_stats.positive -= 1
        elif message.id_sentiment == 2:
            user_stats.neutral -= 1
        elif message.id_sentiment == 3:
            user_stats.negative -= 1
        
        if message.liked is not None:
            if message.liked:
                user_stats.liked -= 1
            else:
                user_stats.disliked -= 1
        
        db.session.add(user_stats)
        db.session.commit() 
            
    except Exception as e:
        db.session.rollback()
        return {'error': 'Error al eliminar el mensaje. Intenta nuevamente.'}, 500
   
    return {'message': 'Mensaje eliminado exitosamente'}, 200 

def get_user_message(data):
    """Obtiene un mensaje del usuario de la base de datos."""
    
    user_id = int(data.get('user_id'))
    message_id = int(data.get('message_id'))
    
    # Obtener el mensaje por ID
    message = Message.query.filter_by(user_id=user_id, id=message_id).first()
    
    if not message:
        return {'error': 'Mensaje no encontrado'}, 404
    
    return {'message': message.to_dict()}, 200

def get_user_messages(data):
    """Obtiene todos los mensajes del usuario de la base de datos."""
    
    user_id = int(data.get('user_id'))
    
    # Obtener historial de mensajes por ID
    messages = Message.query.filter_by(user_id= user_id).all()
    
    if not messages:
        return {'error': 'No se encontraron mensajes para este usuario'}, 404
        
    return {'messages': [message.to_dict() for message in messages]}, 200

def get_user_stats(data):
    """Obtiene las estadísticas del usuario."""
    
    user_id = int(data.get('user_id'))
    
    # Obtener estadísticas del usuario por ID
    user_stats = db.session.get(Stats, user_id)
    
    if not user_stats:
        return {'error': 'Estadísticas no encontradas para este usuario'}, 404
    
    return {'stats': user_stats.to_dict()}, 200

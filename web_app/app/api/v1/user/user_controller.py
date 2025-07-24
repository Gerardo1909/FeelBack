"""
    Controlador de usuario para manejar mensajes, estadísticas y sentimientos del usuario.
"""

from typing import Dict, Tuple, Union, List

from app import db
from app.models.message import Message
from app.models.stats import Stats


def save_message_info_to_db(data) -> Tuple[Dict, int]:
    """Guarda un solo mensaje del usuario en la base de datos."""
    user_id = int(data.get("user_id"))
    id_sentiment = int(data.get("id_sentiment"))
    liked = data.get("liked")
    try:
        new_message_id = _save_message_to_db(
            user_id, data.get("text"), id_sentiment, liked
        )
    except Exception as e:
        db.session.rollback()
        return {"error": "Error al guardar el mensaje. Intenta nuevamente."}, 500
    return {
        "message": "Mensaje guardado exitosamente",
        "id_message": f"{new_message_id}",
    }, 201


def _save_message_to_db(user_id: int, text: str, id_sentiment: int, liked: bool) -> int:
    """Guarda un mensaje del usuario en la base de datos."""
    new_message = Message(
        user_id=user_id, text=text, id_sentiment=id_sentiment, liked=liked
    )
    db.session.add(new_message)
    _add_message_to_stats(user_id, id_sentiment, liked)
    db.session.commit()
    return new_message.id


def _add_message_to_stats(user_id: int, id_sentiment: int, liked: bool = None) -> None:
    """Añade un mensaje a las estadísticas del usuario."""
    user_stats = _get_user_stats_by_id(user_id)
    if not user_stats:
        raise ValueError("Estadísticas del usuario no encontradas.")
    _increment_user_stats(user_stats, id_sentiment, liked)
    db.session.add(user_stats)


def _increment_user_stats(
    user_stats: Stats, id_sentiment: int, liked: bool = None
) -> None:
    """Incrementa las estadísticas del usuario según el mensaje guardado."""
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


def delete_message_from_db(data) -> Tuple[Dict, int]:
    """Elimina un solo mensaje del usuario en la base de datos."""
    user_id = int(data.get("user_id"))
    message = _get_message_by_id(int(data.get("message_id")))
    if not message or message.user_id != user_id:
        return {"error": "Mensaje no encontrado o no pertenece al usuario"}, 404
    try:
        _delete_user_message(message, user_id)
    except Exception as e:
        db.session.rollback()
        return {"error": "Error al eliminar el mensaje. Intenta nuevamente."}, 500
    return {"message": "Mensaje eliminado exitosamente"}, 200


def _get_message_by_id(message_id: int) -> Union[Message, None]:
    """Obtiene un mensaje desde la base de datos según su id."""
    message = db.session.get(Message, message_id)
    return message if message else None


def _delete_user_message(message: Message, user_id: int) -> None:
    """Elimina un mensaje de la base de datos."""
    db.session.delete(message)
    user_stats = _get_user_stats_by_id(user_id)
    if not user_stats:
        raise ValueError("Estadísticas del usuario no encontradas.")
    _drecrement_user_stats(user_stats, message)
    db.session.add(user_stats)
    db.session.commit()


def _drecrement_user_stats(user_stats: Stats, message: Message) -> None:
    """Decrementa las estadísticas del usuario según el mensaje eliminado."""
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


def get_user_message(data) -> Tuple[Dict, int]:
    """Obtiene un mensaje del usuario de la base de datos."""
    message = _get_user_message_by_id(
        int(data.get("user_id")), int(data.get("message_id"))
    )
    if not message:
        return {"error": "Mensaje no encontrado"}, 404
    return {"message": message.to_dict()}, 200


def _get_user_message_by_id(user_id: int, message_id: int) -> Union[Message, None]:
    """Obtiene un mensaje del usuario según su id e id del mensaje."""
    user_message = Message.query.filter_by(user_id=user_id, id=message_id).first()
    return user_message if user_message else None


def get_user_messages(data) -> Tuple[Dict, int]:
    """Obtiene todos los mensajes del usuario desde la base de datos."""
    messages = _get_user_messages_by_id(int(data.get("user_id")))
    if not messages:
        return {"error": "No se encontraron mensajes para este usuario"}, 404
    return {"messages": [message.to_dict() for message in messages]}, 200


def _get_user_messages_by_id(user_id: int) -> Union[List[Message], None]:
    """Obtiene los mensajes del usuario por su id."""
    user_messages = db.session.query(Message).filter_by(user_id=user_id).all()
    return user_messages if user_messages else None


def get_user_stats(data) -> Tuple[Dict, int]:
    """Obtiene las estadísticas del usuario desde la base de datos."""
    user_stats = _get_user_stats_by_id(int(data.get("user_id")))
    if not user_stats:
        return {"error": "Estadísticas no encontradas para este usuario"}, 404
    return {"stats": user_stats.to_dict()}, 200


def _get_user_stats_by_id(user_id: int) -> Union[Stats, None]:
    """Obtiene las estadísticas del usuario por su id."""
    user_stats = db.session.get(Stats, user_id)
    return user_stats if user_stats else None

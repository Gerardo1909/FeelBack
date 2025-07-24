"""
    Controlador de chat para manejar las interacciones del usuario y generar respuestas 
    basadas en el modelo de análisis de sentimientos.
"""

from typing import Tuple, Dict
from app.models.sentiment import Sentiment
from app.api.v1.chat.chat_service import get_model_response



def get_sentiment_response(data: Dict) -> Tuple[Dict, int]:
    """Genera una respuesta para el mensaje del usuario."""
    try:
        user_message = _get_user_message(data)
        final_response = _process_user_message(user_message)
        return final_response, 200
    except Exception as e:
        return {'error': f'Error al procesar el mensaje: {str(e)}'}, 500
    
    
def _get_user_message(data: Dict) -> str:
    """Obtiene el mensaje del usuario del diccionario de datos."""
    user_message = data.get('message')
    if not user_message:
        raise ValueError("El mensaje del usuario no puede estar vacío.")
    return user_message


def _process_user_message(user_message:str) -> Dict:
    """Procesa el mensaje del usuario y devuelve un diccionario con la información necesaria."""
    response_from_model = get_model_response(user_message)  
    id_sentiment = _search_sentiment_in_db(response_from_model)
    return _make_final_response(response_from_model, id_sentiment)


def _search_sentiment_in_db(response_from_model: str) -> int:
    """Busca el sentimiento en la base de datos y devuelve su ID."""
    sentiment = Sentiment.query.filter_by(description=response_from_model).first()
    if not sentiment:
        raise ValueError("Sentimiento no encontrado en la base de datos.")
    return sentiment.id


def _make_final_response(response_from_model: str, id_sentiment: int) -> Dict:
    """Construye la respuesta final para el usuario."""
    return {
        'model_response': f'El sentimiento detectado en tu mensaje es: {response_from_model}.',
        'id_sentiment': id_sentiment
    }
    
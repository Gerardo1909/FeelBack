from typing import Tuple, Dict
from app.models.sentiment import Sentiment
from app.api.v1.chat.chat_service import get_model_response



def get_sentiment_response(data: Dict) -> Tuple[Dict, int]:
    """Genera una respuesta para el mensaje del usuario."""
    user_message = data.get('message')
    
    try:
        # Obtener la respuesta del modelo de lenguaje
        response_from_model = get_model_response(user_message)  # Lógica real del modelo
        
        # Buscar el sentimiento en la base de datos
        sentiment = Sentiment.query.filter_by(description=response_from_model).first()
        id_sentiment = sentiment.id if sentiment else None

        # Construir la respuesta final
        final_response = {
            'model_response': f'El sentimiento detectado en tu mensaje es: {response_from_model}.',
            'id_sentiment': id_sentiment
        }

        return final_response, 200
    except Exception as e:
        return {'error': f'Error al procesar el mensaje: {str(e)}'}, 500
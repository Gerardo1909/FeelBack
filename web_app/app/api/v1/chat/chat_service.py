from transformers import pipeline


def get_model_response(message:str):
    
    """
    Obtiene la respuesta del modelo de lenguaje para el mensaje del usuario.
    """

    result = sentiment_pipeline(message)
    label = result[0]['label'] if result and 'label' in result[0] else None
    if label:
        stars = int(label.split()[0])
        if stars <= 2:
            return "negative"
        elif stars == 3:
            return "neutral"

    return "positive"

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)


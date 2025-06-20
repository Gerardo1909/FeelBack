from flask import render_template, flash, session, redirect, url_for, request
from app.main import main
from flask_login import login_required, current_user
from app.main.forms.chatform import ChatForm
from app.main.forms.feedbackform import FeedbackForm
from app import db
from typing import Tuple
from datetime import datetime


@main.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    """Vista principal del chat."""
    chat_form = ChatForm()
    feedback_form = FeedbackForm()  

    # Inicializo historial si no existe
    if 'chat_history' not in session:
        session['chat_history'] = []

    if chat_form.validate_on_submit():
        # Obtener mensaje del formulario
        user_message = chat_form.message.data

        # Obtener sentimiento (simulado por ahora)
        response_text, id_sentiment = generate_response(user_message)

        # Construir estructura del mensaje
        message_info = {
            'message': user_message,
            'response': response_text,
            'id_sentiment': id_sentiment,
            'liked': None,
            'disliked': None,
            'feedback': None,
            'timestamp': datetime.now().strftime('%H:%M')
        }

        # Agregar al historial y marcar la sesión como modificada
        session['chat_history'].append(message_info)
        session.modified = True

        # Limpiar input
        chat_form.message.data = ''

        return render_template('chat.html', form=chat_form, feedback_form = feedback_form, history=session['chat_history'])

    return render_template('chat.html', form=chat_form, feedback_form = feedback_form, history=session.get('chat_history', []))


@main.route('/feedback', methods=['POST'])
@login_required
def get_feedback():
    """Recibe feedback del usuario sobre un mensaje."""
    feedback_form = FeedbackForm()

    if feedback_form.validate_on_submit():
        
        try:
            like = feedback_form.like.data
            dislike = feedback_form.dislike.data
            feedback_text = feedback_form.feedback.data
            index = int(request.form.get('index', -1))  # índice del mensaje en el historial

            if 0 <= index < len(session.get('chat_history', [])):
                message_info = session['chat_history'][index]

                # Actualizar campos del mensaje en caché
                if like:
                    message_info['liked'] = True
                elif dislike:
                    message_info['liked'] = False

                message_info['disliked'] = dislike
                message_info['feedback'] = feedback_text
                session.modified = True

            return redirect(url_for('main.chat'))

        except Exception as e:
            flash("Hubo un error al enviar el feedback", "error")
            flash(str(e), "error")
            
    return redirect(url_for('main.chat'))


@main.route('/chat/reset')
@login_required
def reset_chat():
    """Reinicia el chat y guarda los mensajes en la base de datos antes de limpiar."""
    save_all_messages()

    session.pop('chat_history', None)
    
    next_page = request.args.get('next')
    return redirect(next_page or url_for('main.chat'))


def save_message_info_to_db(message_info: dict) -> None:
    """Guarda un solo mensaje del usuario en la base de datos."""
    from app.models.message import Message

    try:
        new_message = Message(
            user_id=current_user.id,
            text=message_info.get('message'),
            id_sentiment=message_info.get('id_sentiment'),
            liked=message_info.get('liked'),
            # Podrías guardar 'feedback' también si tu modelo lo permite
        )

        db.session.add(new_message)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        flash('Error al guardar el mensaje. Intenta nuevamente.', 'error')
        flash(str(e), 'error')


def save_all_messages() -> None:
    """Guarda todo el historial actual de sesión en la base de datos."""
    chat_history = session.get('chat_history', [])
    for message_info in chat_history:
        save_message_info_to_db(message_info)


def generate_response(message: str) -> Tuple[str, int]:
    """Genera una respuesta para el mensaje del usuario."""
    from app.models.sentiment import Sentiment

    # Aquí deberías usar tu modelo real
    response_from_model = 'neutral'  # cambiar por lógica real

    sentiment = Sentiment.query.filter_by(description=response_from_model).first()
    id_sentiment = sentiment.id if sentiment else None

    final_response = f'El sentimiento detectado en tu mensaje es: {response_from_model}.'

    return final_response, id_sentiment

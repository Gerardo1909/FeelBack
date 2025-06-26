from flask import render_template, flash, session, redirect, url_for, request
from app.main import main
from flask_login import login_required, current_user, logout_user
from app.main.forms.chatform import ChatForm
from app.main.forms.feedbackform import FeedbackForm
from datetime import datetime
import requests
from app.config import Config 
from typing import Union


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

        # Obtener sentimiento del mensaje
        response = get_message_response(user_message)
        
        if isinstance(response, dict):

            # Construir estructura del mensaje
            message_info = {
                'message': user_message,
                'response': response.get('model_response'),
                'id_sentiment': response.get('id_sentiment'),
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


def get_message_response(message: str) -> Union[dict, str]:
    """Obtiene una respuesta del modelo de lenguaje."""
    
    token = session.get('token')
    response = requests.post(
        f'{Config.API_BASE_URL}/chat/get-sentiment',
        json={'message': message},
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.json().get('error')
        
        if error_message == 'Token inválido o expirado.':
            flash("Por favor, inicia sesión para continuar.", "error")
            logout_user()
            return redirect(url_for('main.login'))  
        else: 
            return error_message


def save_message_info_to_db(message_info: dict) -> None:
    """Guarda un solo mensaje del usuario en la base de datos."""

    # Obtengo el token de la sesión
    token = session.get('token')
    
    # Pongo la info del mensaje que quiero guardar 
    dict_message = {
        'user_id': f'{current_user.id}',
        'text': f"{message_info.get('message')}",
        'id_sentiment': f"{message_info.get('id_sentiment')}",
        'liked': f"{message_info.get('liked')}"
    }
    
    response = requests.post(
        f'{Config.API_BASE_URL}/user/save-message',
        json=dict_message,
        headers={'Authorization': f'Bearer {token}'}
    )
    
    if response.status_code != 201:
        error_message = response.json().get('error')
        
        if error_message == 'Token inválido o expirado.':
            flash("Por favor, inicia sesión para continuar.", "error")
            logout_user()
            return redirect(url_for('main.login'))  
        
        flash(error_message, 'error')


def save_all_messages() -> None:
    """Guarda todo el historial actual de sesión en la base de datos."""
    chat_history = session.get('chat_history', [])
    for message_info in chat_history:
        save_message_info_to_db(message_info)
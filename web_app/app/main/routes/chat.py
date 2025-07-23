"""
    Rutas para el chat y manejo de mensajes.
"""

from datetime import datetime
from typing import Union, Tuple

import requests
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from app.config import Config
from app.main import main
from app.main.forms.chatform import ChatForm
from app.main.forms.feedbackform import FeedbackForm
from app.utils.requests_handlers import handle_response_error


@main.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    """Vista principal del chat."""
    chat_form, feedback_form = _init_chat_forms()
    if chat_form.validate_on_submit():
        _handle_chat_interaction(chat_form.message.data.strip(), chat_form)
        return render_template(
            "chat.html",
            form=chat_form,
            feedback_form=feedback_form,
            history=session["chat_history"],
        )
    return render_template(
        "chat.html",
        form=chat_form,
        feedback_form=feedback_form,
        history=session.get("chat_history", []),
    )


def _init_chat_forms() -> Tuple[ChatForm, FeedbackForm]:
    """Inicializa los formularios del chat y feedback."""
    chat_form = ChatForm()
    feedback_form = FeedbackForm()
    _init_chat_history()
    return chat_form, feedback_form
    

def _init_chat_history():
    """Inicializa el historial de chat en la sesión si no existe."""
    if "chat_history" not in session:
        session["chat_history"] = []
    
        
def _add_user_message_to_chat_history(user_message: str, response: dict):
    """Guarda un mensaje del usuario en sesión."""
    message_info = {
        "message": user_message,
        "response": response.get("model_response"),
        "id_sentiment": response.get("id_sentiment"),
        "liked": None,
        "disliked": None,
        "feedback": None,
        "timestamp": datetime.now().strftime("%H:%M"),
    }
    session["chat_history"].append(message_info)
    session.modified = True
    

def _handle_chat_interaction(user_message: str, chat_form: ChatForm) -> None: 
    """Maneja la interacción del usuario con el chat."""
    response = _get_message_response(user_message)
    if isinstance(response, dict):
        _add_user_message_to_chat_history(user_message, response)
        chat_form.message.data = ""
    else:
        error_message = response
        flash(error_message, "error")
        

def _get_message_response(message: str) -> Union[dict, str]:
    """Obtiene una respuesta del modelo de lenguaje."""
    response = _send_get_message_request(message)
    return _handle_get_message_response(response)
    
    
def _send_get_message_request(message: str) -> requests.Response:
    """Envía una solicitud a la API para obtener la respuesta del modelo."""
    token = session.get("token")
    response = requests.post(
        f"{Config.API_BASE_URL}/chat/get-sentiment",
        json={"message": message},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )
    return response


def _handle_get_message_response(response: requests.Response) -> Union[dict, str]:
    """Maneja la respuesta de la solicitud de mensaje."""
    if response.status_code == 200:
        return response.json()
    else:
        return handle_response_error(response)
    

@main.route("/feedback", methods=["POST"])
@login_required
def get_feedback():
    """Recibe feedback del usuario sobre un mensaje."""
    feedback_form = FeedbackForm()
    if feedback_form.validate_on_submit():
        try:
            feedback_info = _get_feedback_message_info(feedback_form)
            _modify_feedback_info(feedback_info)
            return redirect(url_for("main.chat"))
        except Exception as e:
            flash("Hubo un error al enviar el feedback", "error")
            flash(str(e), "error")
    return redirect(url_for("main.chat"))


def _get_feedback_message_info(feedback_form: FeedbackForm) -> dict:
    """Obtiene la información de feedback del formulario."""
    return {
        "like": feedback_form.like.data,
        "dislike": feedback_form.dislike.data,
        "feedback": feedback_form.feedback.data,
        "index": int(
                request.form.get("index", -1)
            )  
    }
    
    
def _modify_feedback_info(feedback_message_info: dict):
    """Modifica la información de feedback en el historial de sesión."""
    index = feedback_message_info.get("index", -1)
    like = feedback_message_info.get("like", False)
    dislike = feedback_message_info.get("dislike", False)
    feedback_text = feedback_message_info.get("feedback", "")
    _modify_session_message_info(index, like, dislike, feedback_text)
    

def _modify_session_message_info(index: int, like: bool, dislike: bool, feedback: str):
    """Modifica la información de un mensaje particular en el historial de sesión."""
    if 0 <= index < len(session.get("chat_history", [])):
        message_info = session["chat_history"][index]
        message_info["liked"] = like
        message_info["disliked"] = dislike
        message_info["feedback"] = feedback
        session.modified = True


@main.route("/chat/reset")
@login_required
def reset_chat():
    """Reinicia el chat y guarda los mensajes en la base de datos antes de limpiar."""
    _save_all_messages()
    session.pop("chat_history", None)
    next_page = request.args.get("next")
    return redirect(next_page or url_for("main.chat"))


def _save_all_messages() -> None:
    """Guarda todo el historial actual de sesión en la base de datos."""
    chat_history = session.get("chat_history", [])
    for message_info in chat_history:
        _save_message_info_to_db(message_info)
    flash("Mensajes guardados al historial correctamente.", "success")
        
        
def _save_message_info_to_db(message_info: dict) -> None:
    """Guarda un solo mensaje del usuario en la base de datos."""
    dict_message = {
        "user_id": f"{current_user.id}",
        "text": f"{message_info.get('message')}",
        "id_sentiment": f"{message_info.get('id_sentiment')}",
        "liked": f"{message_info.get('liked')}",
    }
    response = _send_save_message_request(dict_message)
    _handle_save_message_response(response)


def _send_save_message_request(message_info: dict) -> requests.Response:
    """Envía una solicitud a la API para guardar un mensaje del usuario."""
    token = session.get("token")
    response = requests.post(
        f"{Config.API_BASE_URL}/user/save-message",
        json=message_info,
        headers={"Authorization": f"Bearer {token}"},
        timeout=10
    )
    return response


def _handle_save_message_response(response: requests.Response) -> None:
    """Maneja la respuesta de la solicitud de guardado de mensajes."""
    if response.status_code != 201:
        error_message = handle_response_error(response)
        if isinstance(error_message, str):
            flash(error_message, "error")


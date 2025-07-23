"""
    Rutas para consulta del historial de mensajes del usuario.
"""

from typing import Union
import csv

import requests
from flask import Response, flash, redirect, render_template, session, url_for
from flask_login import current_user, login_required

from app.config import Config
from app.main import main
from app.utils.logging_config import logger
from app.utils.requests_handlers import handle_response_error


@main.route("/history", methods=["GET"])
@login_required
def history():
    """Página de historial."""
    _init_user_messages()
    _init_user_stats()
    logger.info("Historial consultado", user_id=current_user.id)
    return render_template(
        "main/history.html",
        messages=session.get("user_messages", []),
        neutral=session.get("user_stats", {}).get("neutral", 0),
        positive=session.get("user_stats", {}).get("positive", 0),
        negative=session.get("user_stats", {}).get("negative", 0),
    )


def _init_user_messages():
    """Inicializa los mensajes del usuario desde la API y los guarda en la sesión."""
    user_messages = _request_user_messages()
    if isinstance(user_messages, list):
        _save_user_messages_on_session(user_messages)
    else:
        error_message = user_messages
        if error_message != "No se encontraron mensajes para este usuario":
            flash(error_message, "error")
        _save_user_messages_on_session([])


def _request_user_messages():
    """Realiza una solicitud a la API para obtener los mensajes del usuario."""
    response = _send_user_messages_request()
    return _handle_user_messages_response(response)


def _send_user_messages_request() -> requests.Response:
    """Envía una solicitud a la API para obtener los mensajes del usuario."""
    token = session.get("token")
    response = requests.get(
        f"{Config.API_BASE_URL}/user/get-messages",
        json={"user_id": current_user.id},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    return response


def _handle_user_messages_response(
    response: requests.Response,
) -> Union[list, str, Response]:
    """Maneja la respuesta de la solicitud de mensajes del usuario."""
    if response.status_code == 200:
        return response.json().get("messages")
    else:
        return handle_response_error(response)
    

def _init_user_stats():
    """Inicializa las estadísticas del usuario desde la API y las guarda en la sesión."""
    user_stats = _request_user_stats()
    if isinstance(user_stats, dict):
        _save_user_stats_on_session(user_stats)
    else:
        error_message = user_stats
        if error_message != "Estadísticas no encontradas para este usuario":
            flash(error_message, "error")
        _save_user_stats_on_session({})


def _request_user_stats():
    """Realiza una solicitud a la API para obtener las estadísticas del usuario."""
    response = _send_user_stats_request()
    return _handle_user_stats_response(response)


def _send_user_stats_request() -> requests.Response:
    """Envía una solicitud a la API para obtener las estadísticas del usuario."""
    token = session.get("token")
    response = requests.get(
        f"{Config.API_BASE_URL}/user/get-stats",
        json={"user_id": current_user.id},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    return response


def _handle_user_stats_response(
    response: requests.Response,
) -> Union[dict, str, Response]:
    """Maneja la respuesta de la solicitud de estadísticas del usuario."""
    if response.status_code == 200:
        return response.json().get("stats")
    else:
        return handle_response_error(response)


def _save_user_messages_on_session(messages: list):
    """Guarda los mensajes del usuario en la sesión."""
    session["user_messages"] = messages
    session.modified = True


def _save_user_stats_on_session(stats: dict):
    """Guarda las estadísticas del usuario en la sesión."""
    session["user_stats"] = stats
    session.modified = True


@main.route("/history/delete/<int:message_id>", methods=["POST"])
@login_required
def delete_message(message_id: int):
    """Elimina un mensaje del historial."""
    response = _send_delete_message_request(message_id)
    _handle_delete_message_response(response)
    return redirect(url_for("main.history"))


def _send_delete_message_request(message_id: int) -> requests.Response:
    """Envía una solicitud a la API para eliminar un mensaje del historial."""
    token = session.get("token")
    response = requests.post(
        f"{Config.API_BASE_URL}/user/delete-message",
        json={"user_id": current_user.id, "message_id": message_id},
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    )
    return response


def _handle_delete_message_response(response: requests.Response):
    """Maneja la respuesta de la solicitud de eliminación de mensaje."""
    if response.status_code == 200:
        flash("Mensaje eliminado correctamente.", "success")
    else:
        error_message = handle_response_error(response)
        if isinstance(error_message, str):
            flash(error_message, "error")


@main.route("/history/order_by_date/<asc>", methods=["GET"])
@login_required
def order_by_date(asc: str):
    """Ordena historial de mensajes por fecha."""
    messages = session.get("user_messages", [])
    if asc == "asc":
        messages.sort(key=lambda x: x["created_at"])
    elif asc == "desc":
        messages.sort(key=lambda x: x["created_at"], reverse=True)
    return render_template("main/history.html", messages=messages)


@main.route("/history/filter_by_sentiment/<int:id_sentiment>", methods=["GET"])
@login_required
def filter_by_sentiment(id_sentiment: int):
    """Filtra historial de mensajes según el sentimiento indicado."""
    messages = session.get("user_messages", [])
    filtered_messages = [msg for msg in messages if msg["id_sentiment"] == id_sentiment]
    return render_template("main/history.html", messages=filtered_messages)


@main.route("/history/export_csv", methods=["GET"])
@login_required
def export_to_csv():
    """Exportar historial a CSV."""
    messages = _get_session_messages()
    csv_data = _create_csv_archive(messages)
    return _generate_csv_response(csv_data)


def _get_session_messages() -> Union[list, str, Response]:
    """Obtiene los mensajes del usuario desde la sesión."""
    messages = session.get("user_messages", [])
    if not messages:
        flash("No hay mensajes para exportar.", "error")
        return redirect(url_for("main.history"))
    return messages


def _create_csv_archive(messages: list) -> list:
    """Crea un archivo CSV a partir de los mensajes."""
    csv_data = [["Texto", "Sentimiento", "Fecha"]]
    for msg in messages:
        csv_data.append([msg["text"], msg["sentiment_text"], msg["created_at"]])
    return csv_data


def _generate_csv_response(csv_data: list) -> Response:
    """Genera una respuesta CSV a partir de los datos."""
    response = Response(content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=historial.csv"
    writer = csv.writer(response.stream)
    writer.writerows(csv_data)
    return response


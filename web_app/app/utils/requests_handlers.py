"""
    Módulo de funciones útiles para manejar solicitudes HTTP y respuestas en la aplicación web.
"""

from typing import Union

import requests
from flask import flash, redirect, url_for, Response
from flask_login import logout_user


def handle_response_error(response: requests.Response) -> Union[str, Response]:
    """Maneja errores en la respuesta de la solicitud a la api."""
    error_message = response.json().get("error")
    if error_message == "Token inválido o expirado.":
        flash("Por favor, inicia sesión para continuar.", "error")
        logout_user()
        return redirect(url_for("main.login"))
    else:
        return error_message

"""
    Módulo de funciones útiles para manejar solicitudes HTTP y respuestas en la aplicación web y API backend.
"""

from typing import Union, Tuple, Callable

from marshmallow import Schema, ValidationError

import requests
from flask import flash, redirect, url_for, Response, request, jsonify
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


def handle_api_client_request(schema: Schema, controller_func: Callable) -> Union[dict, Tuple[Response, int]]:
    """Valida y procesa los datos de la solicitud https usando el esquema proporcionado."""
    data = request.get_json()
    try:
        validated_data = schema().load(data)
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    response, status = controller_func(validated_data)
    return jsonify(response), status

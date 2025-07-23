"""
    Ruta de autenticación para el inicio de sesión de usuarios.
"""

from typing import Union

import requests
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user

from app.auth import auth
from app.auth.forms.loginform import LoginForm
from app.config import Config
from app.models.user import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Ruta de login."""
    login_form = LoginForm()
    if login_form.validate_on_submit():
        response = _authenticate_user(
            login_form.username.data, login_form.password.data
        )
        return _handle_user_auth(response, login_form)
    return render_template("auth/login.html", form=login_form)


def _authenticate_user(username: str, password: str) -> Union[dict, str]:
    """Autenticación de usuario."""
    response = _send_login_request(username, password)
    response = _handle_login_request(response)
    return response


def _send_login_request(username: str, password: str) -> requests.Response:
    """Envía una solicitud a la API para autenticar al usuario."""
    response = requests.post(
        f"{Config.API_BASE_URL}/auth/login",
        json={"username": username, "password": password},
        timeout=10
    )
    return response


def _handle_login_request(response: requests.Response) -> Union[dict, str]:
    """Maneja la respuesta de la solicitud de inicio de sesión."""
    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.json().get("error", "Error desconocido")
        return error_message


def _handle_user_auth(response: Union[dict, str], login_form: LoginForm):
    """Maneja la autenticación del usuario."""
    if isinstance(response, dict):
        _save_token_on_session(response.get("token"))
        _login_user_by_id(response.get("user_id"))
        return _redirect_to_next_page()

    else:
        error_message = response
        flash(error_message, "error")
        return render_template("auth/login.html", form=login_form)


def _save_token_on_session(token: str):
    """Guarda el token en la sesión."""
    session["token"] = token


def _login_user_by_id(user_id: int):
    """Loguea al usuario por su ID."""
    user = User.query.get(user_id)
    login_user(user)
    flash("Inicio de sesión exitoso", "success")


def _redirect_to_next_page():
    """Redirige a la página siguiente después del inicio de sesión."""
    next = request.args.get("next")
    if not next or not next.startswith("/"):
        next = url_for("main.home")
    return redirect(next)

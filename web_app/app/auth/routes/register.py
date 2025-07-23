"""
    Ruta de registro de usuarios
"""

from typing import Union

from flask import render_template, redirect, url_for, flash
import requests
from app.auth.forms.registerform import RegisterForm

from app.auth import auth
from app.config import Config


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Ruta para el registro de usuarios"""
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        response = _send_register_request(
            register_form.username.data,
            register_form.email.data,
            register_form.password.data,
        )
        return _handle_register_response(response, register_form)
    return render_template("auth/register.html", form=register_form)


def _send_register_request(
    username: str, email: str, password: str
) -> requests.Response:
    """Envía una solicitud a la API para registrar un nuevo usuario."""
    response = requests.post(
        f"{Config.API_BASE_URL}/auth/register",
        json={"username": username, "email": email, "password": password},
        timeout=10,
    )
    return response


def _handle_register_response(response: requests.Response, register_form: RegisterForm):
    """Maneja la respuesta de la solicitud de registro."""
    if response.status_code == 201:
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for("auth.login"))
    else:
        error_message = response.json().get("error")
        flash(error_message, "error")
        return render_template("auth/register.html", form=register_form)

from typing import Union

import requests
from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user

from app.auth import auth
from app.auth.forms.loginform import LoginForm
from app.config import Config


@auth.route("/login", methods=["GET", "POST"])
def login():
    """Ruta de login."""
    from app.models.user import User

    login_form = LoginForm()

    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        # Envio solicitud a la API para autenticar al usuario
        response = authenticate_user(username, password)

        if isinstance(response, dict):
            token = response.get("token")
            user_id = response.get("user_id")

            # Guardo el token en la sesión
            session["token"] = token

            # Logueo al usuario
            user = User.query.get(user_id)
            login_user(user)
            flash("Inicio de sesión exitoso", "success")

            # Si el usuario se loguea desde una página que requiere autenticación, redirigir a esa página
            next = request.args.get("next")
            if not next or not next.startswith("/"):
                next = url_for("main.home")
            return redirect(next)

        else:
            error_message = response
            flash(error_message, "error")
            return render_template("auth/login.html", form=login_form)

    return render_template("auth/login.html", form=login_form)


def authenticate_user(username, password) -> Union[dict, str]:
    response = requests.post(
        f"{Config.API_BASE_URL}/auth/login",
        json={"username": username, "password": password},
    )
    if response.status_code == 200:
        return response.json()
    else:
        error_message = response.json().get("error")
        return error_message

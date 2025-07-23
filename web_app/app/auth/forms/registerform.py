"""
    Formulario de registro de usuario.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo


class RegisterForm(FlaskForm):
    """Formulario de registro de usuario."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "El nombre de usuario debe tener letras, números, puntos o guiones bajos.",
            ),
        ],
    )

    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("confirm_password", message="Las contraseñas deben coincidir."),
        ],
    )

    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])

    submit = SubmitField("Register")

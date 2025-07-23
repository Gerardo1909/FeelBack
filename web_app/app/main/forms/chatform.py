"""
    Formulario para el chat.
"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    """Formulario de chat."""
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

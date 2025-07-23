"""
    Formulario opcional para enviar feedback sobre el chat.
"""

from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, BooleanField


class FeedbackForm(FlaskForm):
    """Formulario opcional para enviar feedback sobre el chat."""
    like = BooleanField('Like')
    dislike = BooleanField('Dislike')
    feedback = TextAreaField('Feedback')
    feedback_submit = SubmitField('Submit Feedback')
    
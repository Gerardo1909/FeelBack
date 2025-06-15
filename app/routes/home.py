from flask import render_template
from app.routes import main


@main.route('/', methods=['GET'])
def home():
    """Inicio de la página."""
    return render_template('home.html')
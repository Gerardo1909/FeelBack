""" 
    Modulo de rutas principales de la aplicación.
"""


from flask import Blueprint

main = Blueprint('main', __name__, 
                 template_folder='../templates/main',
                 static_folder='../static')


from app.main.routes import chat, history, home

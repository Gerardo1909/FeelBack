from flask import Blueprint

auth = Blueprint('auth', __name__, 
                 template_folder='../templates/auth',
                 static_folder='../static')

from app.auth.routes import login, logout, register
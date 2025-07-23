import os
import time

import psutil
from flask import Blueprint, current_app, jsonify

api_v1 = Blueprint('api_v1', __name__)

from app.api.v1.auth.auth_routes import auth_api_blueprint
from app.api.v1.chat.chat_routes import chat_api_blueprint
from app.api.v1.user.user_routes import user_api_blueprint

api_v1.register_blueprint(auth_api_blueprint, url_prefix='/auth')
api_v1.register_blueprint(user_api_blueprint, url_prefix='/user')
api_v1.register_blueprint(chat_api_blueprint, url_prefix='/chat')

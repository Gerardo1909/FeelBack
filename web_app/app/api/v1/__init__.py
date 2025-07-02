from flask import Blueprint, jsonify, current_app
import psutil
import os
import time

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/health', methods=['GET'])
def health():
    """Endpoint de salud para monitoreo."""
    return jsonify({
        "status": "ok",
        "service": "web_app",
        "message": "API funcionando correctamente"
    }), 200

@api_v1.route('/metrics', methods=['GET'])
def metrics():
    """Endpoint de métricas básicas de salud y uso."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    uptime = time.time() - process.create_time()
    return jsonify({
        "status": "ok",
        "service": "web_app",
        "memory_mb": round(mem_info.rss / 1024 / 1024, 2),
        "uptime_seconds": int(uptime),
        "active_users": getattr(current_app, 'active_users', 0)
    }), 200

from app.api.v1.chat.chat_routes import chat_api_blueprint
from app.api.v1.auth.auth_routes import auth_api_blueprint
from app.api.v1.user.user_routes import user_api_blueprint

api_v1.register_blueprint(auth_api_blueprint, url_prefix='/auth')
api_v1.register_blueprint(user_api_blueprint, url_prefix='/user')
api_v1.register_blueprint(chat_api_blueprint, url_prefix='/chat')
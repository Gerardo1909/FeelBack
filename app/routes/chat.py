from flask import render_template
from app.routes import main

@main.route('/chat', methods=['GET'])
def chat():
    """Chat."""
    return render_template('chat.html')
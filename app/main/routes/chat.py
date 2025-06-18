from flask import render_template
from app.main  import main
from flask_login import login_required

@main.route('/chat', methods=['GET'])
@login_required
def chat():
    """Chat."""
    return render_template('chat.html')
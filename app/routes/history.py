from flask import render_template
from app.routes import main


@main.route('/history', methods=['GET'])
def history():
    """Página de historial."""
    return render_template('history.html')
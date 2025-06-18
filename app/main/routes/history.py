from flask import render_template
from app.main import main
from flask_login import login_required


@main.route('/history', methods=['GET'])
@login_required
def history():
    """Página de historial."""
    return render_template('history.html')
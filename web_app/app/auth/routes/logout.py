from app.auth import auth
from flask_login import logout_user, login_required
from flask import redirect, url_for, flash, session


@auth.route('/logout')
@login_required
def logout():
    """Ruta para cerrar sesión."""
    logout_user()
    session.pop('token', None)  
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('main.home'))
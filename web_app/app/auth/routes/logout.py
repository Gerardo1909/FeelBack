from flask import flash, redirect, session, url_for
from flask_login import login_required, logout_user

from app.auth import auth


@auth.route('/logout')
@login_required
def logout():
    """Ruta para cerrar sesión."""
    logout_user()
    session.pop('token', None)  
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('main.home'))

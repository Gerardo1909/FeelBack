from flask import render_template, request, redirect, url_for, flash, session
from app.routes import main
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    """Formulario de login."""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


@main.route('/')
def index():
    """Ruta principal que redirije al login."""
    return redirect(url_for('main.login'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta de login."""
    from app.models.user import User 
    
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            username = login_form.username.data
            password = login_form.password.data
            
            # Buscar usuario en la base de datos
            user = User.query.filter_by(username=username).first()
            
            if user and user.verify_password(password):
                # Login exitoso
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Bienvenido, {user.username}!', 'success')
                return redirect(url_for('main.chat')) 
            else:
                flash('Usuario o contraseña incorrectos', 'error')
                return render_template('login.html', form=login_form)
    
    return render_template('login.html', form=login_form)


@main.route('/logout')
def logout():
    """Ruta para cerrar sesión."""
    session.clear()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('main.login'))
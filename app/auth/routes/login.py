from flask import render_template, request, redirect, url_for, flash, session
from app.auth import auth
from app.auth.forms.loginform import LoginForm
from flask_login import login_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta de login."""
    from app.models.user import User 
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        
        # Buscar usuario en la base de datos
        user = User.query.filter_by(username=username).first()
        
        if user and user.verify_password(password):
            
            # Login exitoso
            login_user(user)
            
            # Si el usuario se loguea desde una página que requiere autenticación, redirigir a esa página
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('main.home')
            return redirect(next)
            
        # Si el usuario no existe o la contraseña es incorrecta
        flash('Usuario o contraseña incorrectos', 'error')
        return render_template('auth/login.html', form=login_form)
    
    return render_template('auth/login.html', form=login_form)



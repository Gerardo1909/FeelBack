"""
Rutas para el registro de usuarios
"""

from flask import render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo
from app.routes import main
from app import db

class RegisterForm(FlaskForm):
    """Formulario de registro de usuario."""
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Register')



@main.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de usuarios"""
    from app.models.user import User  
    
    register_form = RegisterForm()
    if request.method == 'POST':
        if register_form.validate_on_submit():
        
            username = register_form.username.data
            email = register_form.email.data
            password = register_form.password.data
            
            # Verificar si el usuario ya existe
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                flash('El usuario o email ya está registrado', 'error')
                return render_template('register.html', form =register_form)
            
            try:
                # Crear nuevo usuario
                new_user = User(
                    username=username,
                    email=email
                )
                new_user.set_password(password)  
                
                # Guardar en la base de datos
                db.session.add(new_user)
                db.session.commit()
                
                flash('Usuario registrado exitosamente', 'success')
                return redirect(url_for('main.login'))
                
            except Exception as e:
                db.session.rollback()
                flash('Error al registrar usuario. Intenta nuevamente.', 'error')
                flash(str(e), 'error')
                return render_template('register.html', form = register_form)
    
    return render_template('register.html', form=register_form)
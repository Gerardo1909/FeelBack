"""
Rutas para el registro de usuarios
"""

from flask import render_template, redirect, url_for, flash
from app.auth.forms.registerform import RegisterForm
from app.auth import auth
from app import db


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de usuarios"""
    from app.models.user import User  
    
    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        
        try:
            # Crear nuevo usuario
            new_user = User(
                username = register_form.username.data,
                email= register_form.email.data,
            )
            
            # Establecer la contraseña hasheada
            new_user.set_password(register_form.password.data)
            
            # Guardar en la base de datos
            db.session.add(new_user)
            db.session.commit()
            
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar usuario. Intenta nuevamente.', 'error')
            flash(str(e), 'error')
            return render_template('auth/register.html', form = register_form)
    
    return render_template('auth/register.html', form=register_form)
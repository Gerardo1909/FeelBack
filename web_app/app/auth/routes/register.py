"""
Rutas para el registro de usuarios
"""

from flask import render_template, redirect, url_for, flash
import requests
from app.auth.forms.registerform import RegisterForm
from app.auth import auth
from app.config import Config 



@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de usuarios"""
    
    register_form = RegisterForm()
    
    if register_form.validate_on_submit():
        
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data
        
        # Envio solicitud a la api para registrar el usuario
        reponse = requests.post(
            f'{Config.API_BASE_URL}/auth/register',
            json={
                'username': username,
                'email': email,
                'password': password
            }
        )
        
        if reponse.status_code == 201:
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('auth.login'))
        else: 
            error_message = reponse.json().get('error')
            flash(error_message, 'error')
            return render_template('auth/register.html', form=register_form)


    return render_template('auth/register.html', form=register_form)
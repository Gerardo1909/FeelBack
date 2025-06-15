"""
Rutas para el registro de usuarios
"""

from flask import render_template, request, redirect, url_for, flash, current_app
from app.routes import main
from app import models


@main.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de usuarios"""
    from app.models.user import User  
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones básicas
        if not username or not email or not password:
            flash('Todos los campos son obligatorios', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('register.html')
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            flash('El usuario o email ya está registrado', 'error')
            return render_template('register.html')
        
        try:
            # Crear nuevo usuario
            new_user = User(
                username=username,
                email=email
            )
            new_user.set_password(password)  # Usar el método para hashear la contraseña
            
            # Guardar en la base de datos
            models.session.add(new_user)
            models.session.commit()
            
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('main.login'))
            
        except Exception as e:
            models.session.rollback()
            current_app.logger.error(f"Error al registrar usuario: {e}")
            flash('Error al registrar usuario. Intenta nuevamente.', 'error')
            return render_template('register.html')
    
    return render_template('register.html')
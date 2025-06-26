from flask import render_template, flash, session, redirect, url_for, Response
from app.main import main
from flask_login import login_required, current_user, logout_user
import requests
from app.config import Config 
import csv


@main.route('/history', methods=['GET'])
@login_required
def history():
    """Página de historial."""
    
   # Obtengo mensajes del usuario desde la API
    user_messages = request_user_messages()
    
    if isinstance(user_messages, list):
        # Guardar los mensajes en la variable de sesión
        session['user_messages'] = user_messages
        session.modified = True
    else:
        error_message = user_messages
        
        if error_message != 'No se encontraron mensajes para este usuario':
            flash(error_message, 'error')
            
            
        session['user_messages'] = []

    return render_template('main/history.html', messages=session.get('user_messages', []))


@main.route('/history/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id: int):
    """Elimina un mensaje del historial."""

    # Mando request a la api
    token = session.get('token')
    response = requests.post(f'{Config.API_BASE_URL}/user/delete-message', json={
            'user_id': current_user.id,
            'message_id': message_id
        }, headers={
            'Authorization': f'Bearer {token}'
        })
    
    if response.status_code == 200:
        flash('Mensaje eliminado correctamente.', 'success')
    else:
        error_message = response.json().get('error')
        flash(error_message, 'error')

    return redirect(url_for('main.history'))


@main.route('/history/order_by_date/<asc>', methods=['GET'])
@login_required
def order_by_date(asc: str):
    """Ordenar historial por fecha."""
    # implementar ordenamiento por fecha
    messages = session.get('user_messages', [])
    
    if asc == 'asc':
        messages.sort(key=lambda x: x['created_at'])
    elif asc == 'desc':
        messages.sort(key=lambda x: x['created_at'], reverse=True)
    
    return render_template('main/history.html', messages=messages)


@main.route('/history/filter_by_sentiment/<int:id_sentiment>', methods=['GET'])
@login_required
def filter_by_sentiment(id_sentiment: int):
    """Filtrar historial por sentimiento."""
    messages = session.get('user_messages', [])

    filtered_messages = [msg for msg in messages if msg['id_sentiment'] == id_sentiment]

    return render_template('main/history.html', messages=filtered_messages)


@main.route('/history/export_csv', methods=['GET'])
@login_required
def export_to_csv():
    """Exportar historial a CSV."""
    messages = session.get('user_messages', [])

    if not messages:
        flash('No hay mensajes para exportar.', 'error')
        return redirect(url_for('main.history'))

    # Crear el archivo CSV
    csv_data = [['Texto', 'Sentimiento', 'Fecha']]
    for msg in messages:
        csv_data.append([msg['text'], msg['sentiment_text'], msg['created_at']])

    # Generar la respuesta CSV
    response = Response(content_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=historial.csv'

    writer = csv.writer(response.stream)
    writer.writerows(csv_data)

    return response

def request_user_messages():
    """Realiza una solicitud a la API para obtener los mensajes del usuario."""
    token = session.get('token')
    response = requests.get(f'{Config.API_BASE_URL}/user/get-messages', json={
        'user_id': current_user.id
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    
    if response.status_code == 200:
        return response.json().get('messages')
    else:
        error_message = response.json().get('error')
        
        if error_message == 'Token inválido o expirado.':
            flash("Por favor, inicia sesión para continuar.", "error")
            logout_user()
            return redirect(url_for('main.login'))  
        else: 
            return error_message
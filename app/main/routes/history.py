from flask import render_template, redirect, url_for, flash, Response
from app.main import main
from flask_login import login_required, current_user
import csv
from io import StringIO
from datetime import datetime


@main.route('/history', methods=['GET'])
@login_required
def history():
    """Página de historial."""
    
    from app.models.message import Message
    from app.models.sentiment import Sentiment
    
    # Obtener historial de mensajes del usuario actual
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.created_at.desc()).all()
    
    # Obtengo el texto correspondiente al id_sentiment de cada mensaje
    for message in messages:
        sentiment = Sentiment.query.get(message.id_sentiment)
        message.sentiment_text = sentiment.description
    
    return render_template('main/history.html', messages=messages)


@main.route('/history/delete/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id: int):
    """Elimina un mensaje del historial."""
    from app.models.message import Message
    from app import db
    
    message = Message.query.get(message_id)
    if message and message.user_id == current_user.id:
        db.session.delete(message)
        db.session.commit()
        flash('Mensaje eliminado correctamente', 'success')
    else:
        flash('No se pudo eliminar el mensaje', 'error')
    
    return redirect(url_for('main.history'))


@main.route('/history/order_by_date', methods=['GET'])
@login_required
def order_by_date():
    """Ordenar historial por fecha."""
    from app.models.message import Message
    from app.models.sentiment import Sentiment
    
    # Obtener historial de mensajes del usuario actual, ordenados por fecha
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.created_at.desc()).all()
    
    # Obtengo el texto correspondiente al id_sentiment de cada mensaje
    for message in messages:
        sentiment = Sentiment.query.get(message.id_sentiment)
        message.sentiment_text = sentiment.description
    
    return render_template('main/history.html', messages=messages)


@main.route('/history/filter_by_sentiment', methods=['GET'])
@login_required
def filter_by_sentiment():
    """Filtrar historial por sentimiento."""
    # Por ahora simplemente mostramos todos los mensajes
    # En una versión futura se agregaría un formulario para seleccionar el sentimiento
    
    from app.models.message import Message
    from app.models.sentiment import Sentiment
    
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.created_at.desc()).all()
    
    for message in messages:
        sentiment = Sentiment.query.get(message.id_sentiment)
        message.sentiment_text = sentiment.description
    
    return render_template('main/history.html', messages=messages)


@main.route('/history/export_csv', methods=['GET'])
@login_required
def export_to_csv():
    """Exportar historial a CSV."""
    from app.models.message import Message
    from app.models.sentiment import Sentiment
    
    # Historial de mensajes del usuario actual
    messages = Message.query.filter_by(user_id=current_user.id).order_by(Message.created_at.desc()).all()
    
    # Creo un archivo CSV en memoria
    output = StringIO()
    writer = csv.writer(output)
    
    # Escribo los datos
    writer.writerow(['Fecha', 'Mensaje', 'Sentimiento'])
    for message in messages:
        sentiment = Sentiment.query.get(message.id_sentiment)
        writer.writerow([
            message.created_at.strftime('%Y-%m-%d'),
            message.text,
            sentiment.description
        ])
    
    # Preparo la respuesta
    output.seek(0)
    
    # Genero un nombre de archivo con fecha actual
    filename = f"FeelBack_historial_{datetime.now().strftime('%Y%m%d')}.csv"
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )
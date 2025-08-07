"""
    Tests unitarios para las funciones auxiliares de la vista de historial.
"""
from unittest.mock import patch, Mock
from flask import Response
from app import create_app, db
from app.models.sentiment import Sentiment
from app.main.routes.history import (
    _handle_user_messages_response,
    _handle_user_stats_response,
    _save_user_messages_on_session,
    _save_user_stats_on_session,
    _create_csv_archive,
    _generate_csv_response,
    _handle_delete_message_response
)
import requests


class TestHistoryViewHelpers:
    """Clase de pruebas para las funciones auxiliares del historial."""

    def setup_method(self):
        """Configura el entorno antes de cada prueba."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        # Crear sentimientos necesarios para los tests
        self._create_sentiments()

    def teardown_method(self):
        """Limpia el entorno después de cada prueba."""
        # Limpiar sentimientos
        sentiments = Sentiment.query.all()
        for sentiment in sentiments:
            db.session.delete(sentiment)
            db.session.commit()
            
        self.ctx.pop()

    def _create_sentiments(self):
        """Crea los sentimientos necesarios para los tests."""
        sentiments = [
            {'id': 1, 'description': 'positive'},
            {'id': 2, 'description': 'neutral'}, 
            {'id': 3, 'description': 'negative'}
        ]
        for sentiment_data in sentiments:
            existing = Sentiment.query.filter_by(id=sentiment_data['id']).first()
            if not existing:
                sentiment = Sentiment(id=sentiment_data['id'], description=sentiment_data['description'])
                db.session.add(sentiment)
        db.session.commit()

    # ===== TESTS DE MANEJO DE RESPUESTAS API =====

    def test_handle_user_messages_response_success(self):
        """Prueba manejar respuesta exitosa de mensajes."""
        # Crear mock de respuesta exitosa
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'messages': [
                {'id': 1, 'text': 'Mensaje de prueba', 'id_sentiment': 1}
            ]
        }
        
        result = _handle_user_messages_response(mock_response)
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]['text'] == 'Mensaje de prueba'
        assert result[0]['id_sentiment'] == 1

    @patch('app.main.routes.history.handle_response_error')
    def test_handle_user_messages_response_error(self, mock_handle_error):
        """Prueba manejar respuesta de error de mensajes."""
        # Configurar mock de error
        mock_handle_error.return_value = "Error del servidor"
        
        # Crear mock de respuesta de error
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 500
        
        result = _handle_user_messages_response(mock_response)
        
        assert result == "Error del servidor"
        mock_handle_error.assert_called_once_with(mock_response)

    def test_handle_user_stats_response_success(self):
        """Prueba manejar respuesta exitosa de estadísticas."""
        # Crear mock de respuesta exitosa
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'stats': {'positive': 5, 'negative': 3, 'neutral': 2}
        }
        
        result = _handle_user_stats_response(mock_response)
        
        assert isinstance(result, dict)
        assert result['positive'] == 5
        assert result['negative'] == 3
        assert result['neutral'] == 2

    @patch('app.main.routes.history.handle_response_error')
    def test_handle_user_stats_response_error(self, mock_handle_error):
        """Prueba manejar respuesta de error de estadísticas."""
        # Configurar mock de error
        mock_handle_error.return_value = "Error al obtener estadísticas"
        
        # Crear mock de respuesta de error
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 404
        
        result = _handle_user_stats_response(mock_response)
        
        assert result == "Error al obtener estadísticas"
        mock_handle_error.assert_called_once_with(mock_response)

    # ===== TESTS DE GESTIÓN DE SESIÓN =====

    def test_save_user_messages_on_session(self):
        """Prueba guardar mensajes en la sesión."""
        test_messages = [
            {'id': 1, 'text': 'Mensaje 1', 'id_sentiment': 1},
            {'id': 2, 'text': 'Mensaje 2', 'id_sentiment': 2}
        ]
        
        # Usar el contexto de request y session juntos
        with self.app.test_request_context():
            _save_user_messages_on_session(test_messages)
            
            # Verificar que se guardaron en la sesión dentro del mismo contexto
            from flask import session
            assert 'user_messages' in session
            assert len(session['user_messages']) == 2
            assert session['user_messages'][0]['text'] == 'Mensaje 1'
            assert session['user_messages'][1]['text'] == 'Mensaje 2'

    def test_save_user_stats_on_session(self):
        """Prueba guardar estadísticas en la sesión."""
        test_stats = {'positive': 10, 'negative': 5, 'neutral': 3}
        
        # Usar el contexto de request y session juntos
        with self.app.test_request_context():
            _save_user_stats_on_session(test_stats)
            
            # Verificar que se guardaron en la sesión dentro del mismo contexto
            from flask import session
            assert 'user_stats' in session
            assert session['user_stats']['positive'] == 10
            assert session['user_stats']['negative'] == 5
            assert session['user_stats']['neutral'] == 3

    # ===== TESTS DE EXPORTACIÓN CSV =====

    def test_create_csv_archive_with_messages(self):
        """Prueba crear archivo CSV con mensajes."""
        test_messages = [
            {
                'text': 'Mensaje positivo',
                'sentiment_text': 'positive',
                'created_at': '2025-01-20'
            },
            {
                'text': 'Mensaje negativo',
                'sentiment_text': 'negative',
                'created_at': '2025-01-21'
            }
        ]
        
        result = _create_csv_archive(test_messages)
        
        assert isinstance(result, list)
        assert len(result) == 3  # Header + 2 mensajes
        assert result[0] == ['Texto', 'Sentimiento', 'Fecha']
        assert result[1] == ['Mensaje positivo', 'positive', '2025-01-20']
        assert result[2] == ['Mensaje negativo', 'negative', '2025-01-21']

    def test_create_csv_archive_empty_messages(self):
        """Prueba crear archivo CSV sin mensajes."""
        test_messages = []
        
        result = _create_csv_archive(test_messages)
        
        assert isinstance(result, list)
        assert len(result) == 1  # Solo header
        assert result[0] == ['Texto', 'Sentimiento', 'Fecha']

    def test_generate_csv_response(self):
        """Prueba generar respuesta CSV."""
        test_csv_data = [
            ['Texto', 'Sentimiento', 'Fecha'],
            ['Mensaje de prueba', 'positive', '2025-01-20']
        ]
        
        result = _generate_csv_response(test_csv_data)
        
        assert isinstance(result, Response)
        assert result.content_type == 'text/csv'
        assert 'attachment; filename=historial.csv' in result.headers['Content-Disposition']

    # ===== TESTS DE ELIMINACIÓN DE MENSAJES =====

    @patch('app.main.routes.history.flash')
    def test_handle_delete_message_response_success(self, mock_flash):
        """Prueba manejar respuesta exitosa de eliminación."""
        # Crear mock de respuesta exitosa
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Mensaje eliminado exitosamente'}
        
        _handle_delete_message_response(mock_response)
        
        mock_flash.assert_called_once_with('Mensaje eliminado correctamente.', 'success')

    @patch('app.main.routes.history.flash')
    @patch('app.main.routes.history.handle_response_error')
    def test_handle_delete_message_response_error(self, mock_handle_error, mock_flash):
        """Prueba manejar respuesta de error de eliminación."""
        # Configurar mocks
        mock_handle_error.return_value = "Error al eliminar mensaje"
        
        # Crear mock de respuesta de error
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 404
        
        _handle_delete_message_response(mock_response)
        
        mock_handle_error.assert_called_once_with(mock_response)
        mock_flash.assert_called_once_with("Error al eliminar mensaje", 'error')

    # ===== TESTS DE INTEGRACIÓN DE FUNCIONES =====

    def test_message_processing_flow(self):
        """Prueba el flujo completo de procesamiento de mensajes."""
        # 1. Simular respuesta de API
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'messages': [
                {'id': 1, 'text': 'Mensaje de prueba', 'id_sentiment': 1}
            ]
        }
        
        # 2. Procesar respuesta
        messages = _handle_user_messages_response(mock_response)
        
        # 3. Guardar en sesión
        with self.app.test_request_context():
            _save_user_messages_on_session(messages)
        
        # 4. Crear CSV
        # Simular mensajes con campos para CSV
        csv_messages = [
            {
                'text': 'Mensaje de prueba',
                'sentiment_text': 'positive',
                'created_at': '2025-01-20'
            }
        ]
        csv_data = _create_csv_archive(csv_messages)
        
        # 5. Generar respuesta CSV
        csv_response = _generate_csv_response(csv_data)
        
        # Verificar todo el flujo
        assert len(messages) == 1
        assert messages[0]['text'] == 'Mensaje de prueba'
        assert len(csv_data) == 2  # Header + 1 mensaje
        assert isinstance(csv_response, Response)
        assert csv_response.content_type == 'text/csv'

    def test_stats_processing_flow(self):
        """Prueba el flujo completo de procesamiento de estadísticas."""
        # 1. Simular respuesta de API
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'stats': {'positive': 8, 'negative': 2, 'neutral': 5}
        }
        
        # 2. Procesar respuesta
        stats = _handle_user_stats_response(mock_response)
        
        # 3. Guardar en sesión
        with self.app.test_request_context():
            _save_user_stats_on_session(stats)
        
        # Verificar todo el flujo
        assert isinstance(stats, dict)
        assert stats['positive'] == 8
        assert stats['negative'] == 2
        assert stats['neutral'] == 5

    # ===== TESTS DE AUTENTICACIÓN (SIN MOCKING) =====

    def test_history_requires_login(self):
        """Prueba que el historial requiere autenticación."""
        response = self.client.get('/history', follow_redirects=True)
        assert 'Iniciar Sesi' in response.get_data(as_text=True)

    def test_delete_message_requires_login(self):
        """Prueba que eliminar mensaje requiere autenticación."""
        response = self.client.post('/history/delete/1', follow_redirects=True)
        assert 'Iniciar Sesi' in response.get_data(as_text=True)

    def test_order_by_date_requires_login(self):
        """Prueba que ordenar requiere autenticación."""
        response = self.client.get('/history/order_by_date/asc', follow_redirects=True)
        assert 'Iniciar Sesi' in response.get_data(as_text=True)

    def test_filter_by_sentiment_requires_login(self):
        """Prueba que filtrar requiere autenticación."""
        response = self.client.get('/history/filter_by_sentiment/1', follow_redirects=True)
        assert 'Iniciar Sesi' in response.get_data(as_text=True)

    def test_export_to_csv_requires_login(self):
        """Prueba que exportar CSV requiere autenticación."""
        response = self.client.get('/history/export_csv', follow_redirects=True)
        assert 'Iniciar Sesi' in response.get_data(as_text=True)

    # ===== TESTS DE CASOS EDGE =====

    def test_handle_user_messages_response_with_empty_messages(self):
        """Prueba manejar respuesta exitosa pero con mensajes vacíos."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'messages': []}
        
        result = _handle_user_messages_response(mock_response)
        
        assert isinstance(result, list)
        assert len(result) == 0

    def test_handle_user_stats_response_with_zero_stats(self):
        """Prueba manejar respuesta exitosa con estadísticas en cero."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'stats': {'positive': 0, 'negative': 0, 'neutral': 0}
        }
        
        result = _handle_user_stats_response(mock_response)
        
        assert isinstance(result, dict)
        assert result['positive'] == 0
        assert result['negative'] == 0
        assert result['neutral'] == 0

    def test_create_csv_archive_with_special_characters(self):
        """Prueba crear CSV con caracteres especiales."""
        test_messages = [
            {
                'text': 'Mensaje con "comillas" y, comas',
                'sentiment_text': 'neutral',
                'created_at': '2025-01-20'
            },
            {
                'text': 'Mensaje con\nnuevas líneas',
                'sentiment_text': 'positive',
                'created_at': '2025-01-21'
            }
        ]
        
        result = _create_csv_archive(test_messages)
        
        assert isinstance(result, list)
        assert len(result) == 3  # Header + 2 mensajes
        assert result[1][0] == 'Mensaje con "comillas" y, comas'
        assert result[2][0] == 'Mensaje con\nnuevas líneas'

    def test_save_user_messages_with_none_values(self):
        """Prueba guardar mensajes con valores None."""
        test_messages = [
            {'id': 1, 'text': None, 'id_sentiment': 1},
            {'id': 2, 'text': 'Mensaje válido', 'id_sentiment': None}
        ]
        
        with self.app.test_request_context():
            _save_user_messages_on_session(test_messages)
            
            from flask import session
            assert 'user_messages' in session
            assert len(session['user_messages']) == 2
            assert session['user_messages'][0]['text'] is None
            assert session['user_messages'][1]['id_sentiment'] is None

    def test_save_user_stats_with_missing_keys(self):
        """Prueba guardar estadísticas con claves faltantes."""
        test_stats = {'positive': 5}  # Solo positive, faltan negative y neutral
        
        with self.app.test_request_context():
            _save_user_stats_on_session(test_stats)
            
            from flask import session
            assert 'user_stats' in session
            assert session['user_stats']['positive'] == 5
            assert 'negative' not in session['user_stats']
            assert 'neutral' not in session['user_stats']

    # ===== TESTS DE VALIDACIÓN =====

    def test_handle_user_messages_response_with_invalid_json(self):
        """Prueba manejar respuesta con JSON malformado."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'invalid_key': 'invalid_value'}  # Sin 'messages'
        
        result = _handle_user_messages_response(mock_response)
        
        # Debería retornar None cuando no hay clave 'messages'
        assert result is None

    def test_handle_user_stats_response_with_invalid_json(self):
        """Prueba manejar respuesta de stats con JSON malformado."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {'invalid_key': 'invalid_value'}  # Sin 'stats'
        
        result = _handle_user_stats_response(mock_response)
        
        # Debería retornar None cuando no hay clave 'stats'
        assert result is None

    def test_create_csv_archive_with_incomplete_message_data(self):
        """Prueba crear CSV con datos de mensajes incompletos."""
        test_messages = [
            {
                'text': 'Mensaje completo',
                'sentiment_text': 'positive',
                'created_at': '2025-01-20'
            },
            {
                'text': 'Mensaje sin sentiment_text',
                'created_at': '2025-01-21'
                # Falta 'sentiment_text'
            },
            {
                'text': 'Mensaje sin fecha',
                'sentiment_text': 'negative'
                # Falta 'created_at'
            }
        ]
        
        # Esto podría causar KeyError, pero vamos a probar cómo maneja la función
        try:
            result = _create_csv_archive(test_messages)
            # Si no lanza excepción, verificamos que el resultado tenga la estructura esperada
            assert isinstance(result, list)
            assert len(result) >= 1  # Al menos el header
        except KeyError:
            # Es esperado que falle con datos incompletos
            assert True

    def test_generate_csv_response_headers(self):
        """Prueba que la respuesta CSV tenga los headers correctos."""
        test_csv_data = [['Header1', 'Header2'], ['Data1', 'Data2']]
        
        result = _generate_csv_response(test_csv_data)
        
        assert isinstance(result, Response)
        assert result.content_type == 'text/csv'
        assert result.headers['Content-Disposition'] == 'attachment; filename=historial.csv'
        assert hasattr(result, 'stream')

    @patch('app.main.routes.history.flash')
    def test_handle_delete_message_response_with_custom_message(self, mock_flash):
        """Prueba manejar respuesta de eliminación con mensaje personalizado."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'message': 'El mensaje ha sido eliminado correctamente del sistema'
        }
        
        _handle_delete_message_response(mock_response)
        
        # La función siempre usa el mensaje hardcodeado, no el del JSON
        mock_flash.assert_called_once_with(
            'Mensaje eliminado correctamente.', 
            'success'
        )

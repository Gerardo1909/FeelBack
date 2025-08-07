"""
    Tests unitarios para las vistas de chat.
"""

from unittest.mock import Mock, patch
from flask import session

from app import create_app
from app.main.routes.chat import (
    _init_chat_forms,
    _init_chat_history,
    _add_user_message_to_chat_history,
    _handle_chat_interaction,
    _get_message_response,
    _send_get_message_request,
    _handle_get_message_response,
    _get_feedback_message_info,
    _modify_feedback_info,
    _modify_session_message_info,
    _save_all_messages,
    _save_message_info_to_db,
    _send_save_message_request,
    _handle_save_message_response
)


class TestChatAuxiliaryFunctions:
    """Tests para las funciones auxiliares de chat."""
    
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()

    def test_init_chat_forms(self):
        """Test inicialización de formularios de chat."""
        with self.app.test_request_context():
            # Act
            chat_form, feedback_form = _init_chat_forms()
            
            # Assert
            assert chat_form is not None
            assert feedback_form is not None
            assert "chat_history" in session

    def test_init_chat_history_new_session(self):
        """Test inicialización de historial de chat en nueva sesión."""
        with self.app.test_request_context():
            # Act
            _init_chat_history()
            
            # Assert
            assert session["chat_history"] == []

    def test_init_chat_history_existing_session(self):
        """Test inicialización de historial de chat con sesión existente."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = [{"message": "test"}]
            
            # Act
            _init_chat_history()
            
            # Assert
            assert session["chat_history"] == [{"message": "test"}]

    @patch('app.main.routes.chat.datetime')
    def test_add_user_message_to_chat_history(self, mock_datetime):
        """Test agregar mensaje de usuario al historial."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = []
            mock_datetime.now.return_value.strftime.return_value = "10:30"
            user_message = "Hola, ¿cómo estás?"
            response = {
                "model_response": "Estoy bien, gracias",
                "id_sentiment": 1
            }
            
            # Act
            _add_user_message_to_chat_history(user_message, response)
            
            # Assert
            assert len(session["chat_history"]) == 1
            message_info = session["chat_history"][0]
            assert message_info["message"] == user_message
            assert message_info["response"] == "Estoy bien, gracias"
            assert message_info["id_sentiment"] == 1
            assert message_info["liked"] is None
            assert message_info["disliked"] is None
            assert message_info["feedback"] is None
            assert message_info["timestamp"] == "10:30"

    @patch('app.main.routes.chat._get_message_response')
    @patch('app.main.routes.chat._add_user_message_to_chat_history')
    @patch('app.main.routes.chat.flash')
    def test_handle_chat_interaction_success(self, mock_flash, mock_add_message, mock_get_response):
        """Test manejo exitoso de interacción de chat."""
        # Arrange
        mock_form = Mock()
        mock_form.message.data = ""
        response = {"model_response": "Respuesta del modelo", "id_sentiment": 1}
        mock_get_response.return_value = response
        
        # Act
        _handle_chat_interaction("Mensaje de prueba", mock_form)
        
        # Assert
        mock_get_response.assert_called_once_with("Mensaje de prueba")
        mock_add_message.assert_called_once_with("Mensaje de prueba", response)
        assert mock_form.message.data == ""
        mock_flash.assert_not_called()

    @patch('app.main.routes.chat._get_message_response')
    @patch('app.main.routes.chat.flash')
    def test_handle_chat_interaction_error(self, mock_flash, mock_get_response):
        """Test manejo de error en interacción de chat."""
        # Arrange
        mock_form = Mock()
        error_message = "Error en el servidor"
        mock_get_response.return_value = error_message
        
        # Act
        _handle_chat_interaction("Mensaje de prueba", mock_form)
        
        # Assert
        mock_flash.assert_called_once_with(error_message, "error")

    @patch('app.main.routes.chat._send_get_message_request')
    @patch('app.main.routes.chat._handle_get_message_response')
    def test_get_message_response_success(self, mock_handle_response, mock_send_request):
        """Test obtener respuesta de mensaje exitosamente."""
        # Arrange
        mock_response = Mock()
        mock_send_request.return_value = mock_response
        expected_result = {"model_response": "Respuesta", "id_sentiment": 1}
        mock_handle_response.return_value = expected_result
        
        # Act
        result = _get_message_response("Mensaje de prueba")
        
        # Assert
        assert result == expected_result
        mock_send_request.assert_called_once_with("Mensaje de prueba")
        mock_handle_response.assert_called_once_with(mock_response)

    @patch('app.main.routes.chat.requests.post')
    def test_send_get_message_request(self, mock_post):
        """Test envío de solicitud para obtener mensaje."""
        with self.app.test_request_context():
            # Arrange
            session["token"] = "test_token"
            mock_response = Mock()
            mock_post.return_value = mock_response
            
            # Act
            result = _send_get_message_request("Mensaje de prueba")
            
            # Assert
            assert result == mock_response
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            assert "/chat/get-sentiment" in args[0]
            assert kwargs['json']['message'] == "Mensaje de prueba"
            assert kwargs['headers']['Authorization'] == "Bearer test_token"
            assert kwargs['timeout'] == 10

    def test_handle_get_message_response_success(self):
        """Test manejo exitoso de respuesta de mensaje."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"model_response": "Respuesta", "id_sentiment": 1}
        
        # Act
        result = _handle_get_message_response(mock_response)
        
        # Assert
        assert isinstance(result, dict)
        assert result["model_response"] == "Respuesta"
        assert result["id_sentiment"] == 1

    @patch('app.main.routes.chat.handle_response_error')
    def test_handle_get_message_response_error(self, mock_handle_error):
        """Test manejo de error en respuesta de mensaje."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 500
        expected_error = "Error del servidor"
        mock_handle_error.return_value = expected_error
        
        # Act
        result = _handle_get_message_response(mock_response)
        
        # Assert
        assert result == expected_error
        mock_handle_error.assert_called_once_with(mock_response)

    def test_get_feedback_message_info(self):
        """Test obtener información de feedback del formulario."""
        with self.app.test_request_context('/', method='POST', data={'index': '2'}):
            # Arrange
            mock_form = Mock()
            mock_form.like.data = True
            mock_form.dislike.data = False
            mock_form.feedback.data = "Muy buena respuesta"
            
            # Act
            result = _get_feedback_message_info(mock_form)
            
            # Assert
            assert result["like"] is True
            assert result["dislike"] is False
            assert result["feedback"] == "Muy buena respuesta"
            assert result["index"] == 2

    @patch('app.main.routes.chat._modify_session_message_info')
    def test_modify_feedback_info(self, mock_modify_session):
        """Test modificar información de feedback."""
        # Arrange
        feedback_info = {
            "like": True,
            "dislike": False,
            "feedback": "Excelente",
            "index": 1
        }
        
        # Act
        _modify_feedback_info(feedback_info)
        
        # Assert
        mock_modify_session.assert_called_once_with(1, True, False, "Excelente")

    def test_modify_session_message_info_valid_index(self):
        """Test modificar información de mensaje con índice válido."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = [
                {"message": "Test 1", "liked": None, "disliked": None, "feedback": None},
                {"message": "Test 2", "liked": None, "disliked": None, "feedback": None}
            ]
            
            # Act
            _modify_session_message_info(1, True, False, "Buen mensaje")
            
            # Assert
            assert session["chat_history"][1]["liked"] is True
            assert session["chat_history"][1]["disliked"] is False
            assert session["chat_history"][1]["feedback"] == "Buen mensaje"

    def test_modify_session_message_info_invalid_index(self):
        """Test modificar información de mensaje con índice inválido."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = [{"message": "Test", "liked": None}]
            original_history = session["chat_history"].copy()
            
            # Act
            _modify_session_message_info(5, True, False, "Feedback")
            
            # Assert
            assert session["chat_history"] == original_history

    @patch('app.main.routes.chat._save_message_info_to_db')
    @patch('app.main.routes.chat.flash')
    def test_save_all_messages(self, mock_flash, mock_save_message):
        """Test guardar todos los mensajes."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = [
                {"message": "Mensaje 1", "id_sentiment": 1},
                {"message": "Mensaje 2", "id_sentiment": 2}
            ]
            
            # Act
            _save_all_messages()
            
            # Assert
            assert mock_save_message.call_count == 2
            mock_flash.assert_called_once_with("Mensajes guardados al historial correctamente.", "success")

    @patch('app.main.routes.chat._send_save_message_request')
    @patch('app.main.routes.chat._handle_save_message_response')
    @patch('app.main.routes.chat.current_user')
    def test_save_message_info_to_db(self, mock_current_user, mock_handle_response, mock_send_request):
        """Test guardar información de mensaje en base de datos."""
        # Arrange
        mock_current_user.id = 123
        mock_response = Mock()
        mock_send_request.return_value = mock_response
        message_info = {
            "message": "Mensaje de prueba",
            "id_sentiment": 1,
            "liked": True
        }
        
        # Act
        _save_message_info_to_db(message_info)
        
        # Assert
        expected_dict = {
            "user_id": "123",
            "text": "Mensaje de prueba",
            "id_sentiment": "1",
            "liked": "True"
        }
        mock_send_request.assert_called_once_with(expected_dict)
        mock_handle_response.assert_called_once_with(mock_response)

    @patch('app.main.routes.chat.requests.post')
    def test_send_save_message_request(self, mock_post):
        """Test envío de solicitud para guardar mensaje."""
        with self.app.test_request_context():
            # Arrange
            session["token"] = "test_token"
            mock_response = Mock()
            mock_post.return_value = mock_response
            message_info = {
                "user_id": "123",
                "text": "Mensaje",
                "id_sentiment": "1",
                "liked": "True"
            }
            
            # Act
            result = _send_save_message_request(message_info)
            
            # Assert
            assert result == mock_response
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            assert "/user/save-message" in args[0]
            assert kwargs['json'] == message_info
            assert kwargs['headers']['Authorization'] == "Bearer test_token"
            assert kwargs['timeout'] == 10

    @patch('app.main.routes.chat.handle_response_error')
    @patch('app.main.routes.chat.flash')
    def test_handle_save_message_response_success(self, mock_flash, mock_handle_error):
        """Test manejo exitoso de respuesta de guardado."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        
        # Act
        _handle_save_message_response(mock_response)
        
        # Assert
        mock_flash.assert_not_called()
        mock_handle_error.assert_not_called()

    @patch('app.main.routes.chat.handle_response_error')
    @patch('app.main.routes.chat.flash')
    def test_handle_save_message_response_error(self, mock_flash, mock_handle_error):
        """Test manejo de error en respuesta de guardado."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 500
        expected_error = "Error del servidor"
        mock_handle_error.return_value = expected_error
        
        # Act
        _handle_save_message_response(mock_response)
        
        # Assert
        mock_handle_error.assert_called_once_with(mock_response)
        mock_flash.assert_called_once_with(expected_error, "error")


class TestChatIntegrationFlows:
    """Tests de integración para flujos completos de chat."""
    
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()

    @patch('app.main.routes.chat._send_get_message_request')
    @patch('app.main.routes.chat.datetime')
    def test_complete_message_flow_success(self, mock_datetime, mock_send_request):
        """Test flujo completo exitoso de envío de mensaje."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = []
            session["token"] = "test_token"
            mock_datetime.now.return_value.strftime.return_value = "15:30"
            
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "model_response": "Respuesta del modelo",
                "id_sentiment": 2
            }
            mock_send_request.return_value = mock_response
            
            # Act
            result = _get_message_response("¿Cómo estás?")
            
            # Assert
            assert isinstance(result, dict)
            assert result["model_response"] == "Respuesta del modelo"
            assert result["id_sentiment"] == 2

    def test_feedback_modification_flow(self):
        """Test flujo completo de modificación de feedback."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = [
                {
                    "message": "Mensaje original",
                    "response": "Respuesta",
                    "liked": None,
                    "disliked": None,
                    "feedback": None
                }
            ]
            
            feedback_info = {
                "like": False,
                "dislike": True,
                "feedback": "No me gustó la respuesta",
                "index": 0
            }
            
            # Act
            _modify_feedback_info(feedback_info)
            
            # Assert
            message = session["chat_history"][0]
            assert message["liked"] is False
            assert message["disliked"] is True
            assert message["feedback"] == "No me gustó la respuesta"

    @patch('app.main.routes.chat._save_message_info_to_db')
    def test_save_multiple_messages_flow(self, mock_save_message):
        """Test flujo de guardado de múltiples mensajes."""
        with self.app.test_request_context():
            # Arrange
            session["chat_history"] = [
                {"message": "Mensaje 1", "id_sentiment": 1},
                {"message": "Mensaje 2", "id_sentiment": 2},
                {"message": "Mensaje 3", "id_sentiment": 1}
            ]
            
            # Act
            _save_all_messages()
            
            # Assert
            assert mock_save_message.call_count == 3
            for i, call in enumerate(mock_save_message.call_args_list):
                args, kwargs = call
                message_info = args[0]
                assert message_info["message"] == f"Mensaje {i+1}"


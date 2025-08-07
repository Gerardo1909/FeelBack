"""
    Tests unitarios para las vistas de autenticación.
"""

from unittest.mock import Mock, patch
from flask import session

from app import create_app
from app.auth.routes.login import (
    _authenticate_user,
    _send_login_request,
    _handle_login_response,
    _handle_user_auth,
    _save_token_on_session,
    _login_user_by_id,
    _redirect_to_next_page
)
from app.auth.routes.register import (
    _send_register_request,
    _handle_register_response
)


class TestLoginAuxiliaryFunctions:
    """Tests para las funciones auxiliares de login."""
    
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()

    @patch('app.auth.routes.login.requests.post')
    def test_send_login_request_success(self, mock_post):
        """Test envío exitoso de solicitud de login."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Act
        result = _send_login_request("testuser", "testpass")
        
        # Assert
        assert result == mock_response
        mock_post.assert_called_once()
        
    @patch('app.auth.routes.login.requests.post')
    def test_send_login_request_with_correct_parameters(self, mock_post):
        """Test que la solicitud de login se envía con parámetros correctos."""
        # Arrange
        mock_response = Mock()
        mock_post.return_value = mock_response
        username = "testuser"
        password = "testpass"
        
        # Act
        _send_login_request(username, password)
        
        # Assert
        args, kwargs = mock_post.call_args
        assert "/auth/login" in args[0]
        assert kwargs['json']['username'] == username
        assert kwargs['json']['password'] == password
        assert kwargs['timeout'] == 10

    def test_handle_login_response_success(self):
        """Test manejo exitoso de respuesta de login."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "test_token", "user_id": 1}
        
        # Act
        result = _handle_login_response(mock_response)
        
        # Assert
        assert isinstance(result, dict)
        assert result["token"] == "test_token"
        assert result["user_id"] == 1

    def test_handle_login_response_error(self):
        """Test manejo de error en respuesta de login."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Credenciales inválidas"}
        
        # Act
        result = _handle_login_response(mock_response)
        
        # Assert
        assert isinstance(result, str)
        assert result == "Credenciales inválidas"

    def test_handle_login_response_error_without_message(self):
        """Test manejo de error sin mensaje específico."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {}
        
        # Act
        result = _handle_login_response(mock_response)
        
        # Assert
        assert result == "Error desconocido"

    @patch('app.auth.routes.login._send_login_request')
    @patch('app.auth.routes.login._handle_login_response')
    def test_authenticate_user_success(self, mock_handle_response, mock_send_request):
        """Test autenticación exitosa de usuario."""
        # Arrange
        mock_response = Mock()
        mock_send_request.return_value = mock_response
        expected_result = {"token": "test_token", "user_id": 1}
        mock_handle_response.return_value = expected_result
        
        # Act
        result = _authenticate_user("testuser", "testpass")
        
        # Assert
        assert result == expected_result
        mock_send_request.assert_called_once_with("testuser", "testpass")
        mock_handle_response.assert_called_once_with(mock_response)

    def test_save_token_on_session(self):
        """Test guardado de token en sesión."""
        with self.app.test_request_context():
            # Act
            _save_token_on_session("test_token")
            
            # Assert
            assert session["token"] == "test_token"

    @patch('app.auth.routes.login.User.query')
    @patch('app.auth.routes.login.login_user')
    @patch('app.auth.routes.login.flash')
    def test_login_user_by_id_success(self, mock_flash, mock_login_user, mock_query):
        """Test login de usuario por ID."""
        # Arrange
        mock_user = Mock()
        mock_query.get.return_value = mock_user
        
        # Act
        _login_user_by_id(1)
        
        # Assert
        mock_query.get.assert_called_once_with(1)
        mock_login_user.assert_called_once_with(mock_user)
        mock_flash.assert_called_once_with("Inicio de sesión exitoso", "success")

    def test_redirect_to_next_page_functionality(self):
        """Test funcionalidad básica de redirección."""
        with self.app.test_request_context('/?next=/dashboard'):
            with patch('app.auth.routes.login.redirect') as mock_redirect:
                mock_redirect.return_value = Mock()
                
                # Act
                result = _redirect_to_next_page()
                
                # Assert
                assert result is not None
                mock_redirect.assert_called_once()

    def test_redirect_to_next_page_without_next_simple(self):
        """Test redirección sin parámetro next."""
        with self.app.test_request_context('/'):
            with patch('app.auth.routes.login.redirect') as mock_redirect, \
                 patch('app.auth.routes.login.url_for') as mock_url_for:
                
                mock_url_for.return_value = "/home"
                mock_redirect.return_value = Mock()
                
                # Act
                result = _redirect_to_next_page()
                
                # Assert
                assert result is not None
                mock_url_for.assert_called_once_with("main.home")
                mock_redirect.assert_called_once_with("/home")

    @patch('app.auth.routes.login._save_token_on_session')
    @patch('app.auth.routes.login._login_user_by_id')
    @patch('app.auth.routes.login._redirect_to_next_page')
    def test_handle_user_auth_success(self, mock_redirect, mock_login, mock_save_token):
        """Test manejo exitoso de autenticación de usuario."""
        # Arrange
        response = {"token": "test_token", "user_id": 1}
        mock_form = Mock()
        expected_redirect = Mock()
        mock_redirect.return_value = expected_redirect
        
        # Act
        result = _handle_user_auth(response, mock_form)
        
        # Assert
        assert result == expected_redirect
        mock_save_token.assert_called_once_with("test_token")
        mock_login.assert_called_once_with(1)
        mock_redirect.assert_called_once()

    @patch('app.auth.routes.login.flash')
    @patch('app.auth.routes.login.render_template')
    def test_handle_user_auth_error(self, mock_render, mock_flash):
        """Test manejo de error en autenticación de usuario."""
        # Arrange
        response = "Credenciales inválidas"
        mock_form = Mock()
        expected_template = Mock()
        mock_render.return_value = expected_template
        
        # Act
        result = _handle_user_auth(response, mock_form)
        
        # Assert
        assert result == expected_template
        mock_flash.assert_called_once_with("Credenciales inválidas", "error")
        mock_render.assert_called_once_with("auth/login.html", form=mock_form)


class TestRegisterAuxiliaryFunctions:
    """Tests para las funciones auxiliares de registro."""
    
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()

    @patch('app.auth.routes.register.requests.post')
    def test_send_register_request_success(self, mock_post):
        """Test envío exitoso de solicitud de registro."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response
        
        # Act
        result = _send_register_request("testuser", "test@example.com", "testpass")
        
        # Assert
        assert result == mock_response
        mock_post.assert_called_once()

    @patch('app.auth.routes.register.requests.post')
    def test_send_register_request_with_correct_parameters(self, mock_post):
        """Test que la solicitud de registro se envía con parámetros correctos."""
        # Arrange
        mock_response = Mock()
        mock_post.return_value = mock_response
        username = "testuser"
        email = "test@example.com"
        password = "testpass"
        
        # Act
        _send_register_request(username, email, password)
        
        # Assert
        args, kwargs = mock_post.call_args
        assert "/auth/register" in args[0]
        assert kwargs['json']['username'] == username
        assert kwargs['json']['email'] == email
        assert kwargs['json']['password'] == password
        assert kwargs['timeout'] == 10

    @patch('app.auth.routes.register.flash')
    @patch('app.auth.routes.register.redirect')
    @patch('app.auth.routes.register.url_for')
    def test_handle_register_response_success(self, mock_url_for, mock_redirect, mock_flash):
        """Test manejo exitoso de respuesta de registro."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 201
        mock_form = Mock()
        mock_url_for.return_value = "/login"
        expected_redirect = Mock()
        mock_redirect.return_value = expected_redirect
        
        # Act
        result = _handle_register_response(mock_response, mock_form)
        
        # Assert
        assert result == expected_redirect
        mock_flash.assert_called_once_with("Usuario registrado exitosamente", "success")
        mock_url_for.assert_called_once_with("auth.login")
        mock_redirect.assert_called_once_with("/login")

    @patch('app.auth.routes.register.flash')
    @patch('app.auth.routes.register.render_template')
    def test_handle_register_response_error(self, mock_render, mock_flash):
        """Test manejo de error en respuesta de registro."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Usuario ya existe"}
        mock_form = Mock()
        expected_template = Mock()
        mock_render.return_value = expected_template
        
        # Act
        result = _handle_register_response(mock_response, mock_form)
        
        # Assert
        assert result == expected_template
        mock_flash.assert_called_once_with("Usuario ya existe", "error")
        mock_render.assert_called_once_with("auth/register.html", form=mock_form)


class TestAuthenticationIntegration:
    """Tests de integración para funciones de autenticación."""
    
    def setup_method(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def teardown_method(self):
        self.ctx.pop()

    @patch('app.auth.routes.login._send_login_request')
    @patch('app.auth.routes.login._handle_login_response')
    def test_authenticate_user_complete_flow(self, mock_handle_response, mock_send_request):
        """Test flujo completo de autenticación de usuario."""
        # Arrange
        mock_response = Mock()
        mock_send_request.return_value = mock_response
        expected_result = {"token": "jwt_token", "user_id": 123}
        mock_handle_response.return_value = expected_result
        
        # Act
        result = _authenticate_user("user123", "password123")
        
        # Assert
        assert result == expected_result
        mock_send_request.assert_called_once_with("user123", "password123")
        mock_handle_response.assert_called_once_with(mock_response)

    def test_session_management_flow(self):
        """Test flujo de manejo de sesión."""
        with self.app.test_request_context():
            # Arrange & Act
            _save_token_on_session("test_jwt_token")
            
            # Assert
            assert session.get("token") == "test_jwt_token"

    def test_redirect_logic_basic_functionality(self):
        """Test funcionalidad básica de lógica de redirección."""
        with self.app.test_request_context('/'):
            with patch('app.auth.routes.login.url_for') as mock_url_for, \
                 patch('app.auth.routes.login.redirect') as mock_redirect:
                
                mock_url_for.return_value = "/home"
                mock_redirect.return_value = Mock()
                
                # Act
                result = _redirect_to_next_page()
                
                # Assert
                assert result is not None
                mock_url_for.assert_called_once_with("main.home")
                mock_redirect.assert_called_once_with("/home")

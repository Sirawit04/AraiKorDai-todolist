"""Unit tests for the App class CLI interface (Task 2)."""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock, call
from src.main import App, AuthManager


class TestAuthManager:
    """Test the AuthManager class."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump([], f)
            temp_path = f.name
        yield temp_path
        if os.path.exists(temp_path):
            os.remove(temp_path)

    def test_auth_manager_initialization(self, temp_users_file):
        """Test AuthManager initialization creates users file if it doesn't exist."""
        auth = AuthManager(users_file=temp_users_file)
        assert os.path.exists(temp_users_file)

    def test_auth_manager_register_new_user(self, temp_users_file):
        """Test registering a new user."""
        auth = AuthManager(users_file=temp_users_file)
        result = auth.register("testuser", "password123")
        assert result is True
        
        # Verify user was saved
        with open(temp_users_file, 'r') as f:
            users = json.load(f)
        assert len(users) == 1
        assert users[0]["username"] == "testuser"
        assert users[0]["password"] == "password123"

    def test_auth_manager_register_duplicate_user(self, temp_users_file):
        """Test that registering duplicate username returns False."""
        auth = AuthManager(users_file=temp_users_file)
        auth.register("testuser", "password123")
        result = auth.register("testuser", "different_password")
        assert result is False

    def test_auth_manager_login_valid_credentials(self, temp_users_file):
        """Test login with valid credentials."""
        auth = AuthManager(users_file=temp_users_file)
        auth.register("testuser", "password123")
        result = auth.login("testuser", "password123")
        assert result is True

    def test_auth_manager_login_invalid_username(self, temp_users_file):
        """Test login with invalid username."""
        auth = AuthManager(users_file=temp_users_file)
        auth.register("testuser", "password123")
        result = auth.login("wronguser", "password123")
        assert result is False

    def test_auth_manager_login_invalid_password(self, temp_users_file):
        """Test login with invalid password."""
        auth = AuthManager(users_file=temp_users_file)
        auth.register("testuser", "password123")
        result = auth.login("testuser", "wrongpassword")
        assert result is False

    def test_auth_manager_login_empty_database(self, temp_users_file):
        """Test login when no users are registered."""
        auth = AuthManager(users_file=temp_users_file)
        result = auth.login("testuser", "password123")
        assert result is False

    def test_auth_manager_multiple_users(self, temp_users_file):
        """Test registering and logging in multiple users."""
        auth = AuthManager(users_file=temp_users_file)
        auth.register("user1", "pass1")
        auth.register("user2", "pass2")
        auth.register("user3", "pass3")
        
        assert auth.login("user1", "pass1") is True
        assert auth.login("user2", "pass2") is True
        assert auth.login("user3", "pass3") is True
        assert auth.login("user1", "pass2") is False

    def test_auth_manager_register_empty_username(self, temp_users_file):
        """Test that empty username is accepted (validation should be in App)."""
        auth = AuthManager(users_file=temp_users_file)
        # AuthManager doesn't validate, that's App's responsibility
        result = auth.register("", "password123")
        assert result is True  # AuthManager accepts it, App should reject

    def test_auth_manager_register_empty_password(self, temp_users_file):
        """Test that empty password is accepted (validation should be in App)."""
        auth = AuthManager(users_file=temp_users_file)
        # AuthManager doesn't validate, that's App's responsibility
        result = auth.register("testuser", "")
        assert result is True  # AuthManager accepts it, App should reject


class TestAppPreLoginMenu:
    """Test the App's pre-login menu functionality (Task 2)."""

    @pytest.fixture
    def temp_files(self):
        """Create temporary users and todos files for testing."""
        users_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        todos_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump([], users_file)
        json.dump([], todos_file)
        users_file.close()
        todos_file.close()
        
        yield users_file.name, todos_file.name
        
        if os.path.exists(users_file.name):
            os.remove(users_file.name)
        if os.path.exists(todos_file.name):
            os.remove(todos_file.name)

    @pytest.fixture
    def app(self, temp_files):
        """Create an App instance with temporary files."""
        users_file, todos_file = temp_files
        app = App()
        app.auth_manager = AuthManager(users_file=users_file)
        app.todo_manager.todos_file = todos_file
        return app

    def test_app_initialization(self, app):
        """Test that App initializes with no current user."""
        assert app.current_user is None
        assert app.auth_manager is not None
        assert app.todo_manager is not None

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_displays_options(self, mock_print, mock_input, app):
        """Test that pre-login menu displays all three options."""
        mock_input.return_value = "3"  # Exit
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify menu options were printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        output_text = ' '.join(print_calls)
        assert '[1] Login' in output_text or 'Login' in output_text
        assert '[2] Sign Up' in output_text or 'Sign Up' in output_text
        assert '[3] Exit' in output_text or 'Exit' in output_text

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_exit_option(self, mock_print, mock_input, app):
        """Test that choosing exit option closes the application."""
        mock_input.return_value = "3"
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_invalid_choice(self, mock_print, mock_input, app):
        """Test that invalid choice shows error and loops."""
        mock_input.side_effect = ["99", "3"]  # Invalid choice, then exit
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify error message was shown
        error_printed = any('Invalid choice' in str(call) for call in mock_print.call_args_list)
        assert error_printed

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_login_successful(self, mock_print, mock_input, app, temp_files):
        """Test successful login transitions from pre-login menu."""
        users_file, _ = temp_files
        app.auth_manager.register("testuser", "password123")
        
        # First choice: login, then username, password
        mock_input.side_effect = ["1", "testuser", "password123"]
        
        app.show_pre_login_menu()
        
        # After successful login, current_user should be set
        assert app.current_user == "testuser"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_login_failed(self, mock_print, mock_input, app):
        """Test failed login shows error and loops."""
        # First choice: login with wrong credentials, then exit
        mock_input.side_effect = ["1", "wronguser", "wrongpass", "3"]
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify error message was shown
        error_printed = any('Invalid username or password' in str(call) 
                          for call in mock_print.call_args_list)
        assert error_printed
        # User should not be logged in
        assert app.current_user is None

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_signup_successful(self, mock_print, mock_input, app):
        """Test successful signup creates account."""
        # Signup, then exit
        mock_input.side_effect = ["2", "newuser", "newpass123", "3"]
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify user was created (can login now)
        assert app.auth_manager.login("newuser", "newpass123") is True

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_signup_empty_username(self, mock_print, mock_input, app):
        """Test signup with empty username shows error."""
        mock_input.side_effect = ["2", "", "password", "3"]
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify error message was shown
        error_printed = any('cannot be empty' in str(call) 
                          for call in mock_print.call_args_list)
        assert error_printed

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_signup_empty_password(self, mock_print, mock_input, app):
        """Test signup with empty password shows error."""
        mock_input.side_effect = ["2", "newuser", "", "3"]
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify error message was shown
        error_printed = any('cannot be empty' in str(call) 
                          for call in mock_print.call_args_list)
        assert error_printed

    @patch('builtins.input')
    @patch('builtins.print')
    def test_pre_login_menu_signup_duplicate_username(self, mock_print, mock_input, app):
        """Test signup with existing username shows error."""
        app.auth_manager.register("existinguser", "pass123")
        
        mock_input.side_effect = ["2", "existinguser", "newpass", "3"]
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify error message was shown
        error_printed = any('already exists' in str(call) 
                          for call in mock_print.call_args_list)
        assert error_printed

    @patch('builtins.input')
    @patch('builtins.print')
    def test_handle_login_successful(self, mock_print, mock_input, app):
        """Test handle_login method with valid credentials."""
        app.auth_manager.register("testuser", "password123")
        mock_input.side_effect = ["testuser", "password123"]
        
        app.handle_login()
        
        assert app.current_user == "testuser"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_handle_login_failed(self, mock_print, mock_input, app):
        """Test handle_login method with invalid credentials."""
        app.auth_manager.register("testuser", "password123")
        mock_input.side_effect = ["wronguser", "wrongpass"]
        
        app.handle_login()
        
        assert app.current_user is None

    @patch('builtins.input')
    @patch('builtins.print')
    def test_handle_signup_successful(self, mock_print, mock_input, app):
        """Test handle_signup method."""
        mock_input.side_effect = ["newuser", "newpass123"]
        
        app.handle_signup()
        
        # Verify user can login
        assert app.auth_manager.login("newuser", "newpass123") is True

    @patch('builtins.input')
    @patch('builtins.print')
    def test_handle_signup_empty_credentials(self, mock_print, mock_input, app):
        """Test handle_signup with empty credentials."""
        mock_input.side_effect = ["", "password"]
        
        app.handle_signup()
        
        # Verify error was shown
        error_printed = any('cannot be empty' in str(call) 
                          for call in mock_print.call_args_list)
        assert error_printed

    @patch('builtins.input')
    @patch('builtins.print')
    def test_handle_signup_duplicate_user(self, mock_print, mock_input, app):
        """Test handle_signup with duplicate username."""
        app.auth_manager.register("existinguser", "oldpass")
        mock_input.side_effect = ["existinguser", "newpass"]
        
        app.handle_signup()
        
        # Verify error was shown
        error_printed = any('already exists' in str(call) 
                          for call in mock_print.call_args_list)
        assert error_printed
        # Original password should still work
        assert app.auth_manager.login("existinguser", "oldpass") is True


class TestAppPreLoginMenuIntegration:
    """Integration tests for the pre-login menu workflow."""

    @pytest.fixture
    def temp_files(self):
        """Create temporary users and todos files for testing."""
        users_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        todos_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        json.dump([], users_file)
        json.dump([], todos_file)
        users_file.close()
        todos_file.close()
        
        yield users_file.name, todos_file.name
        
        if os.path.exists(users_file.name):
            os.remove(users_file.name)
        if os.path.exists(todos_file.name):
            os.remove(todos_file.name)

    @pytest.fixture
    def app(self, temp_files):
        """Create an App instance with temporary files."""
        users_file, todos_file = temp_files
        app = App()
        app.auth_manager = AuthManager(users_file=users_file)
        app.todo_manager.todos_file = todos_file
        return app

    @patch('builtins.input')
    @patch('builtins.print')
    def test_workflow_signup_then_login(self, mock_print, mock_input, app):
        """Test workflow: signup, then login."""
        # First interaction: signup, then exit
        mock_input.side_effect = ["2", "newuser", "password123", "1", "newuser", "password123"]
        
        app.show_pre_login_menu()
        
        # After successful login, current_user should be set
        assert app.current_user == "newuser"

    @patch('builtins.input')
    @patch('builtins.print')
    def test_menu_displays_title(self, mock_print, mock_input, app):
        """Test that menu displays application title."""
        mock_input.return_value = "3"
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Verify title was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        output_text = ' '.join(print_calls)
        assert 'TO-DO LIST' in output_text or 'todo' in output_text.lower()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_multiple_invalid_choices_then_exit(self, mock_print, mock_input, app):
        """Test entering multiple invalid choices then exiting."""
        mock_input.side_effect = ["invalid", "99", "abc", "3"]
        
        with pytest.raises(SystemExit):
            app.show_pre_login_menu()
        
        # Count how many times error was shown
        error_count = sum(1 for call in mock_print.call_args_list 
                         if 'Invalid choice' in str(call))
        assert error_count >= 3

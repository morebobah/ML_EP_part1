import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime
from api import app  # Импортируйте ваш FastAPI app
from schemas.user import SUserInfo, SUserID, SUserEmail, SUserAuth
from schemas.balance import SBalance
from schemas.paymenthistory import SPaymentHistory
from schemas.user import SUserRegister, SUserAuth
from services.crud.usercrud import UsersCRUD
from services.auth.auth import AuthService

client = TestClient(app)

# Тестовые данные
TEST_USER = Mock(
    id=1,
    email="test@example.com",
    password="hashedpassword",
    last_name="Doe",
    first_name="John",
    is_admin=False,
    balance=100.0,
    loyalty=5.0
)



TEST_PAYMENT_HISTORY = [
    {
        "id": 1,
        "user_id": 1,
        "value_before": 50.0,
        "value": 50.0,
        "value_after": 100.0,
        "processed": datetime.now(),
        "status": "complete"
    }
]

TEST_TASKS_HISTORY = [
    {
        "id": 1,
        "user_id": 1,
        "image": "test.jpg",
        "processed": datetime.now(),
        "cost": 10.0,
        "result": "success",
        "status": "completed"
    }
]

TEST_REGISTER_DATA = {
    "email": "test@example.com",
    "password": "strongpassword",
    "last_name": "Doe",
    "first_name": "John"
}

TEST_LOGIN_DATA = {
    "email": "test@example.com",
    "password": "strongpassword"
}


# Тесты для эндпоинтов

class TestAuthRouter:
    @patch.object(UsersCRUD, 'find_one_or_none_by_email')
    @patch.object(AuthService, 'get_password_hash')
    @patch.object(UsersCRUD, 'add')
    @patch.object(AuthService, 'authenticate_user')
    @patch.object(AuthService, 'create_access_token')
    def test_register_user_success(
        self, 
        mock_create_token, 
        mock_authenticate, 
        mock_add_user, 
        mock_hash, 
        mock_find_user,
        mock_user_data,
        mock_user_db_entry
    ):
        # Настройка моков
        mock_find_user.return_value = None
        mock_hash.return_value = "hashedpassword"
        mock_authenticate.return_value = mock_user_db_entry
        mock_create_token.return_value = "test_token"
        
        # Вызов тестируемого эндпоинта
        response = client.post("/auth/register", json=mock_user_data)
        
        # Проверки
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "message": "success", 
            "detail": "Вы успешно зарегистрированы!"
        }
        assert "set-cookie" in response.headers
        
        # Проверка вызовов моков
        mock_find_user.assert_called_once()
        mock_hash.assert_called_once_with(mock_user_data["password"])
        mock_add_user.assert_called_once()
        mock_authenticate.assert_called_once()
        mock_create_token.assert_called_once()

    @patch.object(UsersCRUD, 'find_one_or_none_by_email')
    def test_register_user_conflict(self, mock_find_user, mock_user_data):
        # Настройка мока - пользователь уже существует
        mock_find_user.return_value = {"email": mock_user_data["email"]}
        
        # Вызов и проверка
        response = client.post("/auth/register", json=mock_user_data)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Пользователь уже существует"

    @patch.object(AuthService, 'authenticate_user')
    @patch.object(AuthService, 'create_access_token')
    def test_login_user_success(
        self, 
        mock_create_token, 
        mock_authenticate,
        mock_user_auth_data,
        mock_user_db_entry
    ):
        # Настройка моков
        mock_authenticate.return_value = mock_user_db_entry
        mock_create_token.return_value = "test_token"
        
        # Вызов тестируемого эндпоинта
        response = client.post("/auth/login", json=mock_user_auth_data)
        
        # Проверки
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "message": "success", 
            "detail": "Успешная авторизация"
        }
        assert "set-cookie" in response.headers
        
        # Проверка вызовов моков
        mock_authenticate.assert_called_once()
        mock_create_token.assert_called_once()

    @patch.object(AuthService, 'authenticate_user')
    def test_login_user_unauthorized(self, mock_authenticate, mock_user_auth_data):
        # Настройка мока - аутентификация не прошла
        mock_authenticate.return_value = None
        
        # Вызов и проверка
        response = client.post("/auth/login", json=mock_user_auth_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Неверное имя пользователя или пароль"

    def test_logout_user(self):
        # Сначала логинимся, чтобы установить куки
        with patch.object(AuthService, 'authenticate_user', return_value={"id": 1}):
            with patch.object(AuthService, 'create_access_token', return_value="token"):
                client.post("/auth/login", json={
                    "email": "test@example.com",
                    "password": "password"
                })
        
        # Тестируем выход
        response = client.get("/auth/logout")
        
        # Проверки
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "message": "success", 
            "detail": "Успешный выход"
        }
        assert "set-cookie" in response.headers
        assert "expires=0" in response.headers["set-cookie"]



class TestUserEndpoints:
    def test_get_user_info(self, mock_auth_service):
        mock_auth_service.get_current_user.return_value = TEST_USER
        response = client.post("/auth/login")
        assert response.status_code == 200

        
        response = client.get("/users/user")
        
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "email": "test@example.com",
            "last_name": "Doe",
            "first_name": "John",
            "balance": 100.0,
            "loyalty": 5.0
        }

    def test_get_balance(self, mock_auth_service):
        mock_auth_service.get_current_user.return_value = TEST_USER
        
        response = client.get("/users/balance")
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "success",
            "detail": "Успешно",
            "name": "balance",
            "value": 100.0
        }

    def test_get_loyalty(self, mock_auth_service):
        mock_auth_service.get_current_user.return_value = TEST_USER
        
        response = client.get("/users/loyalty")
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "success",
            "detail": "Успешно",
            "name": "loyalty",
            "value": 5.0
        }

class TestPaymentHistoryEndpoints:
    def test_get_balances_history(self, mock_auth_service, mock_payment_history_crud):
        mock_auth_service.get_current_user.return_value = TEST_USER
        mock_payment_history_crud.find_all_by_user.return_value = TEST_PAYMENT_HISTORY
        
        response = client.get("/users/balances/history")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["user"] == 1

    def test_deposit_balance(self, mock_auth_service, mock_users_crud, mock_payment_history_crud):
        mock_auth_service.get_current_user.return_value = TEST_USER
        mock_users_crud.get_balance_by_id.return_value = 100.0
        mock_payment_history_crud.add.return_value = Mock(id=1)
        
        deposit_data = {"balance": 50.0}
        
        response = client.post("/users/deposit", json=deposit_data)
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "success",
            "detail": "Баланс успешно пополнен"
        }
        
        # Проверяем вызовы CRUD методов
        mock_users_crud.get_balance_by_id.assert_called_once_with(SUserID(id=1))
        mock_payment_history_crud.add.assert_called_once()
        mock_users_crud.add_payment_by_id.assert_called_once_with(SUserID(id=1), 50.0)
        mock_payment_history_crud.update_status_by_id.assert_called_once_with(1, 'complete')

    def test_deposit_negative_balance(self, mock_auth_service):
        mock_auth_service.get_current_user.return_value = TEST_USER
        
        deposit_data = {"balance": -50.0}
        
        response = client.post("/users/deposit", json=deposit_data)
        
        assert response.status_code == 422  # Unprocessable Entity

class TestTasksHistoryEndpoints:
    def test_get_tasks_history(self, mock_auth_service, mock_tasks_history_crud):
        mock_auth_service.get_current_user.return_value = TEST_USER
        mock_tasks_history_crud.find_all_by_user.return_value = TEST_TASKS_HISTORY
        
        response = client.get("/users/tasks/history")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["user"] == 1
        assert response.json()[0]["image"] == "test.jpg"

# Тесты на ошибки аутентификации
def test_unauthorized_access():
    with patch('services.auth.auth.AuthService.get_current_user') as mock:
        mock.side_effect = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
        
        response = client.get("/users/user")
        assert response.status_code == 401



class TestAuthEndpoints:
    def test_register_new_user_success(self, mock_auth_service, mock_users_crud, mock_settings):
        # Настройка моков
        mock_users_crud.find_one_or_none_by_email.return_value = None
        mock_auth_service.get_password_hash.return_value = "hashedpassword"
        mock_auth_service.authenticate_user.return_value = TEST_USER
        mock_auth_service.create_access_token.return_value = "test_token"
        
        response = client.post("/auth/register", json=TEST_REGISTER_DATA)
        
        # Проверки
        assert response.status_code == 200
        assert response.json() == {
            "message": "success",
            "detail": "Вы успешно зарегистрированы!"
        }
        
        # Проверка вызовов
        mock_users_crud.find_one_or_none_by_email.assert_called_once_with(
            SUserEmail(email="test@example.com")
        )
        mock_auth_service.get_password_hash.assert_called_once_with(
            password="strongpassword"
        )
        mock_users_crud.add.assert_called_once()
        mock_auth_service.authenticate_user.assert_called_once()
        mock_auth_service.create_access_token.assert_called_once_with(
            {"sub": "1"}
        )
        
        # Проверка cookie
        assert "auth_token" in response.cookies
        assert response.cookies["auth_token"] == "test_token"

    def test_register_existing_user(self, mock_users_crud):
        mock_users_crud.find_one_or_none_by_email.return_value = TEST_USER
        
        response = client.post("/auth/register", json=TEST_REGISTER_DATA)
        
        assert response.status_code == 409
        assert response.json()["detail"] == "Пользователь уже существует"

    def test_login_success(self, mock_auth_service, mock_settings):
        mock_auth_service.authenticate_user.return_value = TEST_USER
        mock_auth_service.create_access_token.return_value = "test_token"
        
        response = client.post("/auth/login", json=TEST_LOGIN_DATA)
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "success", 
            "detail": "Успешная авторизация"
        }
        
        mock_auth_service.authenticate_user.assert_called_once_with(
            SUserAuth(email="test@example.com", password="strongpassword")
        )
        mock_auth_service.create_access_token.assert_called_once_with(
            {"sub": "1"}
        )
        
        # Проверка cookie
        assert "auth_token" in response.cookies
        assert response.cookies["auth_token"] == "test_token"

    def test_login_failure(self, mock_auth_service):
        mock_auth_service.authenticate_user.return_value = None
        
        response = client.post("/auth/login", json=TEST_LOGIN_DATA)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Неверное имя пользователя или пароль"

    def test_logout(self, mock_settings):
        response = client.get("/auth/logout")
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "success",
            "detail": "Успешный выход"
        }
        
        # Проверка что cookie удалена
        assert "auth_token" not in response.cookies or response.cookies["auth_token"] == ""

    def test_email_normalization(self, mock_auth_service, mock_users_crud):
        mock_users_crud.find_one_or_none_by_email.return_value = None
        mock_auth_service.authenticate_user.return_value = TEST_USER
        
        test_data = TEST_REGISTER_DATA.copy()
        test_data["email"] = "TEST@Example.COM"
        
        response = client.post("/auth/register", json=test_data)
        
        assert response.status_code == 200
        mock_users_crud.find_one_or_none_by_email.assert_called_once_with(
            SUserEmail(email="test@example.com")
        )

# Дополнительные тесты на валидацию
def test_register_validation():
    invalid_data = [
        {"email": "invalid", "password": "short", "last_name": "D", "first_name": "J"},  # Невалидный email
        {"email": "test@example.com", "password": "short", "last_name": "Doe", "first_name": "John"},  # Короткий пароль
        {"email": "test@example.com", "password": "strongpassword", "last_name": "", "first_name": "John"},  # Пустая фамилия
    ]
    
    for data in invalid_data:
        response = client.post("/auth/register", json=data)
        assert response.status_code == 422  # Unprocessable Entity

def test_login_validation():
    invalid_data = [
        {"email": "invalid", "password": "short"},  # Невалидный email
        {"email": "test@example.com", "password": ""},  # Пустой пароль
    ]
    
    for data in invalid_data:
        response = client.post("/auth/login", json=data)
        assert response.status_code == 422  # Unprocessable Entity
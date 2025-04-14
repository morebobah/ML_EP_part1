import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime
from api import app  # Импортируйте ваш FastAPI app
from schemas.user import SUserInfo, SUserID, SUserEmail, SUserAuth
from schemas.balance import SBalance
from schemas.paymenthistory import SPaymentHistory

client = TestClient(app)

# Фикстуры для моков
@pytest.fixture
def mock_auth_service():
    with patch('services.auth.auth.AuthService.get_current_user') as mock:
        yield mock

@pytest.fixture
def mock_users_crud():
    with patch('services.crud.usercrud.UsersCRUD') as mock:
        yield mock

@pytest.fixture
def mock_payment_history_crud():
    with patch('services.crud.paymenthistorycrud.PaymentHistoryCRUD') as mock:
        yield mock

@pytest.fixture
def mock_tasks_history_crud():
    with patch('services.crud.taskshistorycrud.TasksHistoryCRUD') as mock:
        yield mock

# Тестовые данные
TEST_USER = SUserInfo(
    id=1,
    email="test@example.com",
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

# Тесты для эндпоинтов
class TestUserEndpoints:
    def test_get_user_info(self, mock_auth_service):
        mock_auth_service.return_value = TEST_USER
        
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
        mock_auth_service.return_value = TEST_USER
        
        response = client.get("/users/balance")
        
        assert response.status_code == 200
        assert response.json() == {
            "message": "success",
            "detail": "Успешно",
            "name": "balance",
            "value": 100.0
        }

    def test_get_loyalty(self, mock_auth_service):
        mock_auth_service.return_value = TEST_USER
        
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
        mock_auth_service.return_value = TEST_USER
        mock_payment_history_crud.find_all_by_user.return_value = TEST_PAYMENT_HISTORY
        
        response = client.get("/users/balances/history")
        
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["user"] == 1

    def test_deposit_balance(self, mock_auth_service, mock_users_crud, mock_payment_history_crud):
        mock_auth_service.return_value = TEST_USER
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
        mock_auth_service.return_value = TEST_USER
        
        deposit_data = {"balance": -50.0}
        
        response = client.post("/users/deposit", json=deposit_data)
        
        assert response.status_code == 422  # Unprocessable Entity

class TestTasksHistoryEndpoints:
    def test_get_tasks_history(self, mock_auth_service, mock_tasks_history_crud):
        mock_auth_service.return_value = TEST_USER
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


@pytest.fixture
def mock_auth_service():
    with patch('services.auth.auth.AuthService') as mock:
        yield mock

@pytest.fixture
def mock_users_crud():
    with patch('services.crud.usercrud.UsersCRUD') as mock:
        yield mock

@pytest.fixture
def mock_settings():
    with patch('database.config.get_settings') as mock:
        mock.return_value = Mock(COOKIE_NAME="auth_token")
        yield mock

# Тестовые данные
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

TEST_USER = Mock(
    id=1,
    email="test@example.com",
    password="hashedpassword",
    last_name="Doe",
    first_name="John"
)

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
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool 
from models.user import User, Base
from unittest.mock import Mock, patch


@pytest.fixture(name='engine')
def engine():
    # Используем SQLite в памяти для тестов
    return create_engine("sqlite:///:memory:")


@pytest.fixture(name='session')
def session(engine):
    # Создаем таблицы и сессию для тестов
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)

# Фикстуры для моков
@pytest.fixture
def mock_settings():
    with patch('database.config.get_settings') as mock:
        mock.return_value = Mock(COOKIE_NAME="auth_token")
        yield mock


#@pytest.fixture
#def mock_get_current_user():
#    with patch('services.auth.auth.AuthService.get_current_user') as mock:
#        yield mock


@pytest.fixture
def mock_auth_service():
    with patch('services.auth.auth.AuthService') as mock:
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

@pytest.fixture
def mock_user_data():
    return {
        "id": "1",
        "email": "test@example.com",
        "password": "securepassword",
        "first_name": "Test name",
        "last_name": "Test surname"
    }

@pytest.fixture
def mock_user_auth_data():
    return {
        "email": "test@example.com",
        "password": "securepassword"
    }

@pytest.fixture
def mock_user_db_entry():
    return {
        "id": 1,
        "email": "test@example.com",
        "password": "hashedpassword",
        "first_name": "Test name",
        "last_name": "Test surname"
    }

        
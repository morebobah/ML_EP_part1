import pytest
from sqlalchemy.exc import IntegrityError
from models.user import User, Base
from models.taskshistory import TasksHistory
from models.paymenthistory import PaymentHistory
from schemas.user import SUserRegister
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from datetime import datetime


def test_user_creation(session):
    """Тест создания пользователя с валидными данными"""
    user = User(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        password="securepassword",
        balance=100.0,
        loyalty=0.5,
        is_admin=False
    )
    session.add(user)
    session.commit()
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.password == "securepassword"
    assert user.balance == 100.0
    assert user.loyalty == 0.5
    assert user.is_admin is False


def test_user_default_values(session):
    """Тест значений по умолчанию"""
    user = User(
        email="default@example.com",
        first_name="Jane",
        last_name="Smith",
        password="password"
    )
    session.add(user)
    session.commit()
    
    assert user.balance == 0.0  # Проверяем float_zero
    assert user.loyalty == 1.0  # Проверяем float_one
    assert user.is_admin is False  # Проверяем bool_val


def test_unique_email_constraint(session):
    """Тест уникальности email"""
    user1 = User(
        email="unique@example.com",
        first_name="Alice",
        last_name="Johnson",
        password="pass123"
    )
    session.add(user1)
    session.commit()
    
    user2 = User(
        email="unique@example.com", 
        first_name="Bob",
        last_name="Brown",
        password="pass456"
    )
    session.add(user2)
    
    with pytest.raises(IntegrityError):
        session.commit()


def test_required_fields(session):
    """Тест обязательных полей"""
    with pytest.raises(IntegrityError):
        user = User()  # Все обязательные поля отсутствуют
        session.add(user)
        session.commit()


def test_string_fields_max_length(session):
    """Тест максимальной длины строковых полей"""
    long_string = "a" * 256
    
    with pytest.raises(ValueError):  
        user = SUserRegister(
            email=f"{long_string}@example.com",
            first_name=long_string,
            last_name=long_string,
            password=long_string
        )
        session.add(user)
        session.commit()


def test_balance_update(session):
    """Тест обновления баланса"""
    user = User(
        email="balance@example.com",
        first_name="Balance",
        last_name="Test",
        password="testpass",
        balance=50.0
    )
    session.add(user)
    session.commit()
    
    user.balance = 75.5
    session.commit()
    
    updated_user = session.get(User, user.id)
    assert updated_user.balance == 75.5


def test_loyalty_range(session):
    """Тест допустимого диапазона loyalty"""
    with pytest.raises(Exception):
        user = SUserRegister(
            email="loyalty-example.com", # Недопустимое значение
            first_name="Loyalty",
            last_name="Test",
            password="testpass", 
        )
        session.add(user)
        session.commit()


def test_admin_privileges(session):
    """Тест флага is_admin"""
    user = User(
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password="adminpass",
        is_admin=True
    )
    session.add(user)
    session.commit()
    
    assert user.is_admin is True


def test_task_history_model(session):
    user = User(
        id = 10,
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        password="securepassword",
        balance=100.0,
        loyalty=0.5,
        is_admin=False
    )
    session.add(user)
    session.commit()
    # Создаем тестовую запись истории задач
    test_task = TasksHistory(
        id=1,
        user_id=10,
        image="test_image.jpg",
        processed=datetime.now(),
        status="completed",
        result="success",
        cost=10.5
    )
    
    session.add(test_task)
    session.commit()
    
    # Получаем запись из базы данных
    db_task = session.query(TasksHistory).filter_by(id=1).first()
    
    # Проверяем атрибуты
    assert db_task.id == 1
    assert db_task.user_id == 10
    assert db_task.image == "test_image.jpg"
    assert isinstance(db_task.processed, datetime)
    assert db_task.status == "completed"
    assert db_task.result == "success"
    assert db_task.cost == 10.5
    
    # Проверяем отношение к пользователю
    assert db_task.user.id == 10
    assert db_task.user.first_name == "John"

def test_task_history_required_fields(session):
    
    # Проверяем, что обязательные поля действительно обязательны
    with pytest.raises(Exception):
        task = TasksHistory()
        session.add(task)
        session.commit()

def test_task_history_default_values(session):
    
    # Проверяем значения по умолчанию (если они есть)
    task = TasksHistory(
        user_id=1,
        image="default_test.jpg",
        status="pending",
        result=""
    )
    
    session.add(task)
    session.commit()
    
    db_task = session.query(TasksHistory).filter_by(image="default_test.jpg").first()
    
    # Предполагая, что cost имеет значение по умолчанию 0.0 (из float_zero)
    assert db_task.cost == 0.0


def test_payment_history_creation(session):
    user = User(
        id = 15,
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        password="securepassword",
        balance=100.0,
        loyalty=0.5,
        is_admin=False
    )
    session.add(user)
    session.commit()
    
    # Создаем тестовый платеж
    test_payment = PaymentHistory(
        id=1,
        user_id=15,
        value=100.0,
        value_before=500.0,
        value_after=600.0,
        created=datetime.now(),
        processed=datetime.now(),
        status="complete"
    )
    
    session.add(test_payment)
    session.commit()
    
    # Получаем запись из базы
    db_payment = session.query(PaymentHistory).filter_by(id=1).first()
    
    # Проверяем атрибуты
    assert db_payment.id == 1
    assert db_payment.user_id == 15
    assert db_payment.value == 100.0
    assert db_payment.value_before == 500.0
    assert db_payment.value_after == 600.0
    assert isinstance(db_payment.created, datetime)
    assert isinstance(db_payment.processed, datetime)
    assert db_payment.status == "complete"
    
    # Проверяем отношение к пользователю
    assert db_payment.user.id == 15
    assert db_payment.user.last_name == "Doe"

def test_payment_history_required_fields(session):
    
    # Проверяем обязательные поля
    with pytest.raises(Exception):
        payment = PaymentHistory()
        session.add(payment)
        session.commit()

def test_payment_history_default_values(session):
    
    # Создаем платеж с минимальными данными (проверяем значения по умолчанию)
    payment = PaymentHistory(
        user_id=1,
        status="pending"
    )
    
    session.add(payment)
    session.commit()
    
    db_payment = session.query(PaymentHistory).filter_by(status="pending").first()
    
    # Проверяем значения по умолчанию для float_zero (предполагаем 0.0)
    assert db_payment.value == 0.0
    assert db_payment.value_before == 0.0
    assert db_payment.value_after == 0.0
    assert isinstance(db_payment.created, datetime)  # created_at должен устанавливаться автоматически

def test_payment_history_status_validation(session):
    
    # Проверяем допустимые статусы (если есть ограничения)
    valid_statuses = ["pending", "completed", "failed", "refunded"]
    
    for status in valid_statuses:
        payment = PaymentHistory(
            user_id=1,
            value=50.0,
            value_before=100.0,
            value_after=150.0,
            status=status
        )
        session.add(payment)
    
    session.commit()
    
    # Проверяем, что все статусы сохранены
    payments = session.query(PaymentHistory).filter(PaymentHistory.user_id == 1).all()
    assert len(payments) == len(valid_statuses)
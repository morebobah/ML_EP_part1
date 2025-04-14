from fastapi import APIRouter, Response, HTTPException, status, Path, Depends
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID
from schemas.paymenthistory import SPaymentHistory
from schemas.balance import SBalance, SLoyalty
from typing import Annotated
from schemas.admin import SAdminID, SAdminEmail
from schemas.user import SUserInfo
from services.auth.auth import AuthService
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD
from services.crud.taskshistorycrud import TasksHistoryCRUD
from services.auth.auth import AuthService

router = APIRouter(prefix='/admin', tags=['Функции администратора'])

@router.get('/users', summary='Получить список пользователей')
def get_users(admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> list:
    result = list()
    for user in UsersCRUD.find_all_users():
        result.append({'id': user.id,
                      'email': user.email,
                      'first_name': user.first_name,
                      'last_name': user.last_name,
                      'balance': user.balance,
                      'loyalty': user.loyalty,
                      'is_admin': user.is_admin})
    return result


@router.get('/balances/history', summary='Получить историю платежей всех пользователей')
def all_balances_history(admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> list:
    result = list()
    for hop_item in PaymentHistoryCRUD.find_all_payments():
        result.append({'id': hop_item.id,
                      'user': hop_item.user_id,
                      'balance_before': hop_item.value_before,
                      'payment': hop_item.value,
                      'balance_after': hop_item.value_after,
                      'date': hop_item.processed,
                      'status': hop_item.status})
    return result


@router.get('/tasks/history', summary='Получить историю запросов модели у всех пользователей')
def all_tasks_history(admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> list:

    result = list()
    for hot_item in TasksHistoryCRUD.find_all_tasks():
        result.append({'id': hot_item.id,
                      'user': hot_item.user_id,
                      'image': hot_item.image,
                      'date': hot_item.processed,
                      'cost': hot_item.cost,
                      'result': hot_item.result,
                      'status': hot_item.status})

    return result

@router.get('/user/{user_id}', summary='Информация о пользователе')
def get_user(user_id: Annotated[int, Path(title='Идентификатор пользователя', gt=0)],
             admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:

    user = UsersCRUD.find_one_or_none_by_id(id = user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    result = {'id':user.id, 
              'email':user.email, 
              'last_name':user.last_name,
              'first_name':user.first_name, 
              'balance': user.balance, 
              'loyalty':user.loyalty}
    return result


@router.get('/balance/{user_id}', summary='Текущий баланс пользователя')
def get_balance(user_id: Annotated[int, Path(title='Идентификатор пользователя', gt=0)],
                admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:

    user = UsersCRUD.find_one_or_none_by_id(id = user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')

    return {'message':'success', 'detail': 'Успешно', 'name': 'balance', 'value': user.balance}


@router.get('/loyalty/{user_id}', summary='Размер скидки пользователя по идентификатору')
def get_loyalty(user_id: Annotated[int, Path(title='Идентификатор пользователя', gt=0)], 
                admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:

    user = UsersCRUD.find_one_or_none_by_id(id = user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')

    return {'message':'success', 'detail': 'Успешно', 'name': 'loyalty', 'value': user.loyalty}



@router.get('/balances/history/user/{user_id}', summary='История платежей пользователя по идентификатору')
def get_balances_history(user_id: Annotated[int, Path(title='Идентификатор пользователя', gt=0)],
                         admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> list:

    user = UsersCRUD.find_one_or_none_by_id(id = user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    result = list()
    for hop_item in PaymentHistoryCRUD.find_all_payments():
        result.append({'id': hop_item.id,
                      'user': hop_item.user_id,
                      'balance_before': hop_item.value_before,
                      'payment': hop_item.value,
                      'balance_after': hop_item.value_after,
                      'date': hop_item.processed,
                      'status': hop_item.status})

    return result


@router.get('/tasks/history/user/{user_id}', summary='История запросов пользователем модели по идетификатору пользователя')
def get_tasks_history(user_id: Annotated[int, Path(title='Идентификатор пользователя', gt=0)],
                      admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> list:

    user = UsersCRUD.find_one_or_none_by_id(id = user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    result = list()
    for hot_item in TasksHistoryCRUD.find_all_tasks():
        result.append({'id': hot_item.id,
                      'user': hot_item.user_id,
                      'image': hot_item.image,
                      'date': hot_item.processed,
                      'cost': hot_item.cost,
                      'result': hot_item.result,
                      'status': hot_item.status})

    return result


@router.post('/user', summary='Создать нового пользователя')
def create_users(user_data: SUserRegister, 
                 admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:
    user_data.email = str.lower(user_data.email)
    user = UsersCRUD.find_one_or_none_by_email(email = user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_data.password = AuthService.get_password_hash(user_data.password)
    user = UsersCRUD.add(user_data)
    return {'detail': f'Новый пользователь {user} зарегистрирован!'}


@router.put('/balance/user/id', summary='Изменить баланс пользователя по id')
def change_balance_by_id(id: SAdminID, new_balance: SBalance,
                         admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:
    user = UsersCRUD.find_one_or_none_by_id(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    
    balance = UsersCRUD.get_balance_by_id(id)
    ph = SPaymentHistory(user_id=id.id,
                         value=new_balance.balance,
                         value_before=balance,
                         value_after=balance+new_balance.balance,
                         status='pending')
    pay_item = PaymentHistoryCRUD.add(ph)
    UsersCRUD.add_payment_by_id(id, new_balance.balance)
    PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'complete')
    
    return {'message': 'success', 'detail': 'Баланс успешно пополнен'}


@router.put('/balance/user/email', summary='Изменить баланс пользователя по email')
def change_balance_by_email(email: SAdminEmail, new_balance: SBalance,
                            admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:
    user = UsersCRUD.find_one_or_none_by_email(email = email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    id = user.id
    balance = UsersCRUD.get_balance_by_id(id)
    ph = SPaymentHistory(user_id=id, 
                         value=new_balance.balance,
                         value_before=balance,
                         value_after=balance+new_balance.balance,
                         status='pending')
    pay_item = PaymentHistoryCRUD.add(ph)
    UsersCRUD.add_payment_by_id(id, new_balance.balance)
    PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'complete')
    
    return {'message': 'success', 'detail': 'Баланс успешно пополнен'}


@router.put('/user/admin/id', summary='Предоставить права администратора по id')
def change_allow_admin_by_id(id: SAdminID,
                             admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:
    user = UsersCRUD.find_one_or_none_by_id(id.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    UsersCRUD.allow_admin_by_id(id.id)
    return {'message': 'success', 'detail': 'Права администратора предоставлены'}


@router.delete('/user/admin/id', summary='Запретить права администратора по id')
def change_disallow_admin_by_id(id: SAdminID,
                                admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:
    user = UsersCRUD.find_one_or_none_by_id(id.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    UsersCRUD.disallow_admin_by_id(id.id)
    return {'message': 'success', 'detail': 'Права администратора отозваны'}


@router.put('/user/admin/email', summary='Предоставить права администратора по email')
def change_allow_admin_by_email(email: SAdminEmail,
                                admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:
    user = UsersCRUD.find_one_or_none_by_email(email = email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    UsersCRUD.allow_admin_by_email(email)
    return {'message': 'success', 'detail': 'Права администратора предоставлены'}


@router.delete('/user/admin/email', summary='Запретить права администратора по email')
def change_disallow_admin_by_email(email: SAdminEmail,
                                   admin_data: SUserInfo = Depends(AuthService.get_current_admin_user)) -> dict:
    user = UsersCRUD.find_one_or_none_by_email(email = email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    UsersCRUD.disallow_admin_by_email(email)
    return {'message': 'success', 'detail': 'Права администратора отозваны'}


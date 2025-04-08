from fastapi import APIRouter, Response, HTTPException, status, Path
from typing import Annotated
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID
from schemas.balance import SBalance
from schemas.paymenthistory import SPaymentHistory
from services.crud.auth import authenticate_user, get_password_hash
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD
from services.crud.taskshistorycrud import TasksHistoryCRUD

router = APIRouter(prefix='/users', tags=['Функции пользователя'])


@router.get('/user', summary='Информация о пользователе')
def get_user() -> dict:
    
    user_id = 1 #get user from jwt token now only 1

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


@router.get('/balance', summary='Текущий баланс пользователя')
def get_balance() -> dict:
    user_id = 1 #get user from jwt token now only 1

    user = UsersCRUD.find_one_or_none_by_id(id = user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')

    return {'message':'success', 'detail': 'Успешно', 'name': 'balance', 'value': user.balance}


@router.get('/loyalty', summary='Размер скидки пользователя по идентификатору')
def get_loyalty() -> dict:
    user_id = 1 #get user from jwt token now only 1
    
    user = UsersCRUD.find_one_or_none_by_id(id = user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')

    return {'message':'success', 'detail': 'Успешно', 'name': 'loyalty', 'value': user.loyalty}



@router.get('/balances/history', summary='История платежей')
def get_balances_history() -> list:
    user_id = 1 #get user from jwt token now only 1
    
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


@router.get('/tasks/history', summary='История запроов модели')
def get_tasks_history() -> list:

    user_id = 1 #get user from jwt token now only 1
    
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



@router.post('/deposit', summary='Пополнить баланс')
def set_new_balance(new_balance: SBalance) -> dict:

    user_id = 1 #get user from jwt token now only 1

    user_data = SUserID(id = user_id)
    
    user = UsersCRUD.find_one_or_none_by_id(user_data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    balance = UsersCRUD.get_balance_by_id(user_data)
    ph = SPaymentHistory(user_id=user_id, 
                            value=new_balance.balance,
                            value_before=balance,
                            value_after=balance+new_balance.balance,
                            status='pending')
    pay_item = PaymentHistoryCRUD.add(ph)
    UsersCRUD.add_payment_by_id(user_data, new_balance.balance)
    PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'complete')
    
    return {'message': 'success', 'detail': 'Баланс успешно пополнен'}
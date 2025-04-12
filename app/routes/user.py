from fastapi import APIRouter, Response, HTTPException, status, Path, Depends
from typing import Annotated
from schemas.user import SUserAuth, SUserRegister, SUserInfo, SUserID
from schemas.balance import SBalance
from schemas.paymenthistory import SPaymentHistory
from services.auth.auth import AuthService
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD
from services.crud.taskshistorycrud import TasksHistoryCRUD

router = APIRouter(prefix='/users', tags=['Функции пользователя'])


@router.get('/user', summary='Информация о пользователе')
def get_user(user: SUserInfo = Depends(AuthService.get_current_user)) -> dict:
    
    result = {'id':user.id, 
              'email':user.email, 
              'last_name':user.last_name,
              'first_name':user.first_name, 
              'balance': user.balance, 
              'loyalty':user.loyalty}
    return result


@router.get('/balance', summary='Текущий баланс пользователя')
def get_balance(user: SUserInfo = Depends(AuthService.get_current_user)) -> dict:

    return {'message':'success', 'detail': 'Успешно', 'name': 'balance', 'value': user.balance}


@router.get('/loyalty', summary='Размер скидки пользователя по идентификатору')
def get_loyalty(user: SUserInfo = Depends(AuthService.get_current_user)) -> dict:

    return {'message':'success', 'detail': 'Успешно', 'name': 'loyalty', 'value': user.loyalty}



@router.get('/balances/history', summary='История платежей')
def get_balances_history(user: SUserInfo = Depends(AuthService.get_current_user)) -> list:
    
    result = list()
    for hop_item in PaymentHistoryCRUD.find_all_by_user(user):
        result.append({'id': hop_item.id,
                      'user': hop_item.user_id,
                      'balance_before': hop_item.value_before,
                      'payment': hop_item.value,
                      'balance_after': hop_item.value_after,
                      'date': hop_item.processed,
                      'status': hop_item.status})

    return result


@router.get('/tasks/history', summary='История запроов модели')
def get_tasks_history(user: SUserInfo = Depends(AuthService.get_current_user)) -> list:
    
    result = list()
    for hot_item in TasksHistoryCRUD.find_all_by_user(user):
        result.append({'id': hot_item.id,
                      'user': hot_item.user_id,
                      'image': hot_item.image,
                      'date': hot_item.processed,
                      'cost': hot_item.cost,
                      'result': hot_item.result,
                      'status': hot_item.status})

    return result



@router.post('/deposit', summary='Пополнить баланс')
def set_new_balance(new_balance: SBalance, user_data: SUserInfo = Depends(AuthService.get_current_user)) -> dict:
    
    balance = UsersCRUD.get_balance_by_id(SUserID(id=user_data.id))
    ph = SPaymentHistory(user_id=user_data.id, 
                            value=new_balance.balance,
                            value_before=balance,
                            value_after=balance+new_balance.balance,
                            status='pending')
    pay_item = PaymentHistoryCRUD.add(ph)
    UsersCRUD.add_payment_by_id(SUserID(id=user_data.id), new_balance.balance)
    PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'complete')
    
    return {'message': 'success', 'detail': 'Баланс успешно пополнен'}
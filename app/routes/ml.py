import uuid, base64, json
from fastapi import APIRouter, Response, HTTPException, status, File, Path, Form, Depends
from typing import Annotated
from services.auth.auth import AuthService
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD
from services.crud.taskshistorycrud import TasksHistoryCRUD
from models.taskshistory import TasksHistory
from schemas.user import SUserID
from schemas.taskshistory import STasksHistory, STaskComplete, STaskID
from schemas.paymenthistory import SPaymentHistory
from schemas.balance import SBalance, SLoyalty
from services.rm.rm import RabbitMQSender



router = APIRouter(prefix='/ml', tags=['Загрузка данных для модели машинного обучения'])

def user_checker(user_id: int = Form(...)):
   return user_id

@router.post("/task", summary='Создать запрос на обработку изображения')
def upload_task(image: Annotated[bytes, File()],
                user_id: dict = Depends(user_checker)):
    model_cost = 30.0

    user_data = SUserID(id=user_id)
    
    user = UsersCRUD.find_one_or_none_by_id(user_data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    
    balance = UsersCRUD.get_balance_by_id(user_data)
    if balance < model_cost:
        raise HTTPException(status_code=status.HTTP_423_LOCKED,
                            detail='Недостаточно средств')


    file_name = f'./files/{str(uuid.uuid4())}.png'
    try:
        with open(file_name, 'wb') as f:
            f.write(image)
    except FileExistsError:
        raise HTTPException(
            status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
            detail='Ошибка обработки файла'
        )
   
    
    th_item = {'user_id': user_data.id,
               'image': file_name[-40:],
               'status': 'pending',
               'result': '', 
               'cost': model_cost}
    th = STasksHistory(**th_item)
    th_item['bytes'] = base64.b64encode(image).decode('ascii')
    task = TasksHistoryCRUD.add(th)
    th_item['task_id'] = task.id
    
    with RabbitMQSender("ml_task_queue") as sender:
        sender.send_task(json.dumps(th_item))

    
    return {'message': 'success', 
            'detail': 'Изображение отправлено на обработку',
            'name': 'task_id', 
            'value': f'{task.id}', 
            'raw_data': f'task_id={task.id}'}

@router.patch("/task/complete", summary='Завершить ml задачу', include_in_schema=False)
def complete(task: STaskComplete):
    user_id = STaskID(id = task.user_id)

    user = UsersCRUD.find_one_or_none_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')

    balance = UsersCRUD.get_balance_by_id(user_id)
    if balance < task.cost:
        raise HTTPException(status_code=status.HTTP_423_LOCKED,
                            detail='Недостаточно средств')
    
    cost = SBalance(balance=-1.0 * task.cost)
    
    new_balance = SBalance(balance=balance + cost.balance)
    

    ph = SPaymentHistory(user_id=user_id.id, 
                         value=cost.balance,
                         value_before=balance,
                         value_after=new_balance.balance,
                         status='pending')
    
    pay_item = PaymentHistoryCRUD.add(ph)
    UsersCRUD.add_payment_by_id(user_id, cost.balance)

    PaymentHistoryCRUD.update_status_by_id(pay_item.id, 'complete')

    task_id = STaskID(id = task.task_id)
    TasksHistoryCRUD.update_result_by_id(task_id, task.result)
    TasksHistoryCRUD.update_status_by_id(task_id, 'complete')
    return {'message': 'success', 'detail': 'Обработка завершена'}

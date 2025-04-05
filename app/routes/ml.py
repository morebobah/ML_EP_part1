from fastapi import APIRouter, Response, HTTPException, status, UploadFile
from typing import Annotated
from services.crud.auth import authenticate_user, get_password_hash
from services.crud.usercrud import UsersCRUD
from services.crud.taskshistorycrud import TasksHistoryCRUD
from schemas.user import SUserID
from schemas.taskshistory import STasksHistory

router = APIRouter(prefix='/ml', tags=['Загрузка данных для модели машинного обучения'])

@router.post("/task", summary='Создать запрос на обработку изображения')
def upload_task(response: Response, user_data: SUserID, image: UploadFile):
    
    user = UsersCRUD.find_one_or_none_by_id(id = user_data.id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Пользователь не найден')
    th = STasksHistory(user_id=user.id,
                       image=image.filename,
                       status='pending',
                       result='',
                       cost=30.0)
    TasksHistoryCRUD.add(th)
    
    return {'message': 'success', 'detail': 'Изображение отправлено на обработку'}
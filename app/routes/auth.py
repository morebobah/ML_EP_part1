from fastapi import APIRouter, Response, HTTPException, status
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID
from services.crud.auth import authenticate_user, get_password_hash
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD


router = APIRouter(prefix='/auth', tags=['Авторизация пользователя'])



@router.post('/register', summary='Регистрация нового пользователя')
def register_user(user_data: SUserRegister) -> dict:
    
    user = UsersCRUD.find_one_or_none_by_email(email = user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_data.password = get_password_hash(user_data.password)
    UsersCRUD.add(user_data)
    return {'message': 'success', 'detail': 'Вы успешно зарегистрированы!'}


@router.post("/login", summary='Авторизация пользователя')
def auth_user(user_data: SUserAuth):
    check = authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверное имя пользователя или пароль')
    return {'mes': 'success', 'detail': 'Успешная авторизация'}

@router.get("/logout", summary='Выход из личного кабинета')
def auth_user():

    return {'message': 'success', 'detail': 'Успешный выход'}


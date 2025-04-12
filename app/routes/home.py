from fastapi import APIRouter, Request, HTTPException, Response
from fastapi.templating import Jinja2Templates
from database.config import get_settings
from fastapi.responses import RedirectResponse
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD
from services.crud.taskshistorycrud import TasksHistoryCRUD
from services.auth.auth import AuthService


router = APIRouter(tags=['Личный кабинет'])

templates = Jinja2Templates(directory='templates')

settings = get_settings()


@router.get("/", summary='Страница приглашения в сервис!')
def home_page(request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        try:
            user = AuthService.get_user_from_token(token)
            panel = {'Пополнить баланс': ['Pay', 'fa-credit-card'], 
                     'Выход': ['Out', 'fa-sign-out-alt']
                     }
            table = list()
            for hot_item in TasksHistoryCRUD.find_all_by_user(user):
                table.append({'id': hot_item.id,
                                'user': hot_item.user_id,
                                'image': hot_item.image[-40:],
                                'date': hot_item.processed,
                                'cost': hot_item.cost,
                                'result': hot_item.result,
                                'status': hot_item.status})
                
            return templates.TemplateResponse(name='home.html',
                                              context={'request': request,
                                                       'user': user,
                                                       'panel': panel, 
                                                       'table': table})
        except HTTPException:
            user = None
    
    return RedirectResponse("/login")

@router.get("/balance", summary='Пополнение баланса')
def balance_page(request: Request):
    token = request.cookies.get(settings.COOKIE_NAME)
    if token:
        try:
            user = AuthService.get_user_from_token(token)
            panel = {'Личный кабинет': ['ML', 'fa-brain ml-icon'], 
                     'Выход': ['Out', 'fa-sign-out-alt']
                     }
            table = list()
            for hop_item in PaymentHistoryCRUD.find_all_by_user(user):
                table.append({'id': hop_item.id,
                               'user': hop_item.user_id,
                                'balance_before': hop_item.value_before,
                                'payment': hop_item.value,
                                'balance_after': hop_item.value_after,
                                'date': hop_item.processed,
                                'status': hop_item.status})
            return templates.TemplateResponse(name='pay.html',
                                              context={'request': request,
                                                       'user': user,
                                                       'panel': panel, 
                                                       'table': table})
        except HTTPException:
            user = None
    
    return RedirectResponse("/login")


@router.get("/registration", summary='Регистрация личного кабинета!')
def registration(request: Request):
    panel = {'Вход': ['In', 'fa-sign-in-alt']}
    return templates.TemplateResponse(name='registration.html', context={'request': request, 'panel': panel})


@router.get("/login", summary='Вход в личный кабинет!')
def login(request: Request):
    panel = {}
    return templates.TemplateResponse(name='auth.html', context={'request': request, 'panel': panel})


@router.get("/logout", summary='Покиинуть личный кабинет!')
def logout(request: Request):
    return templates.TemplateResponse(name='auth.html', context={'request': request})


@router.get("/home", summary='Личный кабинет!')
def personal_account(request: Request):
    panel = {'Выход': ['Out', 'fa-sign-out-alt']}
    return templates.TemplateResponse(name='home.html', context={'request': request, 'panel': panel})

@router.get("/models", summary='Доступные модели')
def ml_worker(request: Request):
    return templates.TemplateResponse(name='ml.html', context={'request': request})

@router.get(
    "/image/{file}",
    responses = {
        200: {
            "content": {"image/png": {}}
        }
    },
    response_class=Response
)
def get_image(file: str):
    with open(f'./files/{file}', 'rb') as f:
        image_bytes: bytes = f.read()
    return Response(content=image_bytes, media_type="image/png")

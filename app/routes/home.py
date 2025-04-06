from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID
from services.crud.usercrud import UsersCRUD
from services.crud.paymenthistorycrud import PaymentHistoryCRUD

router = APIRouter(tags=['Личный кабинет'])

templates = Jinja2Templates(directory='templates')


@router.get("/", summary='Страница приглашения в сервис!')
def home_page(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})


@router.get("/home", summary='Личный кабинет!')
def personal_account(request: Request):
    return templates.TemplateResponse(name='home.html', context={'request': request})

@router.get("/models", summary='Доступные модели')
def ml_worker(request: Request):
    return templates.TemplateResponse(name='ml.html', context={'request': request})

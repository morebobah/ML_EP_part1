from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from schemas.user import SUserAuth, SUserRegister, SUser, SUserID
from database.database import init_db
from services.crud.usercrud import UsersCRUD
from schemas.user import SUser
from models.paymenthistory import PaymentHistory
from models.taskshistory import TasksHistory


def lifespan(app: FastAPI):
    init_db()
    
    user = SUser(first_name='User', 
                 last_name='Test', 
                 email='User@Test.ru', 
                 password='testpwd',
                 is_admin=False, 
                 balance=0.0,
                 loyalty=1.0)
    
    if UsersCRUD.find_one_or_none(user) is None:
        UsersCRUD.add(user)


    admin = SUser(first_name='Admin', 
                 last_name='Test', 
                 email='Admin@Test.ru', 
                 password='testadminpwd',
                 is_admin=True, 
                 balance=0.0,
                 loyalty=1.0)
    
    if UsersCRUD.find_one_or_none(admin) is None:
        UsersCRUD.add(admin)
    
    yield



app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory='templates')


@app.get("/", summary='Страница приглашения в сервис!')
def home_page(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})
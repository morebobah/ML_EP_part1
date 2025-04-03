from fastapi import FastAPI
from routes.home import router as home_router
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.ml import router as ml_router
from routes.admin import router as admin_router
from database.database import init_db
from services.crud.usercrud import UsersCRUD
from schemas.user import SUser
from models.paymenthistory import PaymentHistory
from models.taskshistory import TasksHistory
import uvicorn



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


app.include_router(home_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ml_router)
app.include_router(admin_router)



if __name__=='__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)
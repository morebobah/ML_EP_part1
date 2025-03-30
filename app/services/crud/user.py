from services.crud.auth import auth
from models.user import User
from models.historyofpayments import Historyofpayments
from models.historyoftasks import Historyoftasks
from typing import Optional 
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, Select
from services.crud.observer import Observable, Observer

class usercrud(auth, Observable, Observer):
    observers = []

    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.engine = engine


    def create_session(self) -> Session:
        Session = sessionmaker(self.engine)
        return Session()


    def create_user(self, new_user: User) -> User:
        if self.get_user_by_email(new_user.email):
            raise EmailAlreadyExists
        
        with self.create_session() as session:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        return new_user
    

    def get_user_by_id(self, id:int ) -> Optional[User]:
        with self.create_session() as session:
            user = session.get(User, id)
        if user:
            return user
        
        return None
    

    def get_user_by_email(self, email:str) -> Optional[User]:
        with self.create_session() as session:
            user = session.query(User).filter(User.email == email).first()

        if user:
            return user 
        
        return None 
    
    def get_balance(self, u: User) -> float:
        user = self.get_user_by_id(u.id)
        if user:
            return user.balance

        return None
    

    def get_all_users(self):
        with self.create_session() as session:
            users = session.query(User).all()
        
        return users
    

    def make_payment(self, u: User, pay: float) -> float:

        with self.create_session() as session:
            updating_user = session.execute(Select(User).filter_by(id=u.id)).scalar_one()
            if updating_user is None:
                raise UnknownUser
        
            current_user_balance = updating_user.balance
            payitem = Historyofpayments(user_id=updating_user.id,
                                        user = updating_user,
                                        value=pay, 
                                        value_before=current_user_balance, 
                                        value_after=current_user_balance+pay,
                                        status='trying')
            updating_user.balance += pay
            
            if updating_user.balance<0:
                raise IssufisientFunds
            
            session.execute(Select(User.balance).filter_by(id=u.id)).scalar_one()
            session.commit()
            self.notify_observers(payitem)
        
        return current_user_balance
    

    def add_payment(self, u: User, pay: float) -> float:
        
        if pay<=0.0:
            raise ValueError
        
        return self.make_payment(u, pay)
        
    
    def spend_payment(self, u: User, pay: float) -> float:
        
        if pay>=0.0:
            raise ValueError
        return self.make_payment(u, u.loyalty * pay)
    
    def event(self, hot_item: Historyoftasks) -> None:
        user_id = hot_item.user.id
        user_item = self.get_user_by_id(user_id)
        pay = -1 * hot_item.cost * user_item.loyalty
        self.spend_payment(user_item, pay)
        


class EmailAlreadyExists(Exception):
    pass

class UnknownUser(Exception):
    pass

class IssufisientFunds(Exception):
    pass
    


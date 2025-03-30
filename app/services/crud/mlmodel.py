from services.crud.observer import Observable
from models.historyoftasks import Historyoftasks
from typing import Optional
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, Select

class mlmodelcrud(Observable):
    __cost_per_result = 0.0
    observers = []

    def __init__(self, engine: Engine) -> None:
        super().__init__()
        self.engine = engine

    def create_session(self) -> Session:
        Session = sessionmaker(self.engine)
        return Session()
    
    @property
    def cost_per_result(self) -> float:
        return self.__cost_per_result
    
    @cost_per_result.setter
    def cost_per_result(self, cost: float) -> None:
        if cost<0:
            raise ValueError
        self.__cost_per_result = cost

    def do_result(self, task: Historyoftasks) -> dict:
        task.cost = self.cost_per_result
        task.status = 'trying'
        #here are doing something about ml for get result
        task.result = ''
        self.notify_observers(task)
        return {'message': 'success'}
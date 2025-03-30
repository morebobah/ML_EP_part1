from services.crud.histories import histories
from models.historyoftasks import Historyoftasks
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, Select
from sqlalchemy.exc import SQLAlchemyError
from services.crud.mlmodel import mlmodelcrud
from copy import deepcopy


class historyofmlmodelscrud(histories):

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def create_session(self) -> Session:
        Session = sessionmaker(self.engine)
        return Session()
    
    def event(self, hot_item: Historyoftasks) -> None:
        self.create_event(hot_item)

    def get_events(self, filter: dict) -> list:
        with self.create_session() as session:
            try:
                query = Select(Historyoftasks).filter_by(**filter)
                result = session.execute(query)
                record = result.all()
                return record
            except SQLAlchemyError as e:
                raise
    
    def create_event(self, hot_item: Historyoftasks) -> Historyoftasks:
        local_hot_item = deepcopy(hot_item)
        with self.create_session() as session:
            session.add(local_hot_item)
            session.commit()
            session.refresh(local_hot_item)
        return hot_item
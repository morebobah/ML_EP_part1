from services.crud.histories import histories
from models.historyofpayments import Historyofpayments
from services.crud.user import usercrud
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, Select
from sqlalchemy.exc import SQLAlchemyError


class historyofpaymentscrud(histories):

    def __init__(self, u: usercrud, engine: Engine) -> None:
        u.register(self)
        self.engine = engine
    
    def create_session(self) -> Session:
        Session = sessionmaker(self.engine)
        return Session()

    def event(self, hop_item: Historyofpayments) -> None:
        self.create_event(hop_item)


    def get_events(self, filter: dict) -> list:
        with self.create_session() as session:
            try:
                query = Select(Historyofpayments).filter_by(**filter)
                result = session.execute(query)
                record = result.all()
                return record
            except SQLAlchemyError as e:
                raise
    
    
    def create_event(self, hop_item: Historyofpayments) -> Historyofpayments:
        with self.create_session() as session:
            local_hop_item = session.merge(hop_item)
            session.add(local_hop_item)
            session.commit()
            result_hop_item = session.refresh(local_hop_item)
        return result_hop_item
    
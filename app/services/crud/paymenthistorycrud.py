from models.paymenthistory import PaymentHistory
from models.user import User
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from database.database import session_maker

class PaymentHistoryCRUD():
    model = PaymentHistory

    @classmethod
    def find_one_or_none(cls, filters: BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_dict)
                result = session.execute(query)
                record = result.scalar_one_or_none()
                return record
            except SQLAlchemyError as e:
                raise

    @classmethod
    def find_all_payments(cls):
        with session_maker() as session:
            query = select(cls.model)
            Payments = session.execute(query)
            return Payments.scalars().all()
        
    @classmethod
    def find_all_by_user(cls, user: User):
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(user_id=user.id).order_by(cls.model.processed.desc())
                Payments = session.execute(query)
                return Payments.scalars().all()
            except SQLAlchemyError as e:
                raise


    @classmethod
    def add(cls, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        with session_maker() as session:
            session.add(new_instance)
            try:
                session.commit()
                session.refresh(new_instance)
            except SQLAlchemyError as e:
                session.rollback()
                raise e
        return new_instance


    @classmethod
    def update_status_by_id(cls, id: BaseModel, new_status: BaseModel):
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(id=id)
                result = session.execute(query)
                record = result.scalar_one_or_none()
                record.status = new_status
                session.commit()
                session.refresh(record)
                return record
            except SQLAlchemyError as e:
                raise

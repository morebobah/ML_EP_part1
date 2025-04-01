from models.taskshistory import TasksHistory
from models.user import User
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from database.database import session_maker

class TasksHistoryCRUD:
    model = TasksHistory

    @classmethod
    def find_all_tasks(cls):
        with session_maker() as session:
            query = select(cls.model)
            Tasks = session.execute(query)
            return Tasks.scalars().all()
        
    @classmethod
    def find_all_by_user(cls, user: User):
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(user_id=user.id)
                Tasks = session.execute(query)
                return Tasks.scalars().all()
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
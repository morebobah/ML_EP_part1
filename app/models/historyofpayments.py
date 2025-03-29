from datetime import datetime
from sqlalchemy.sql import func
from models.user import User
from sqlalchemy import text, ForeignKey, DateTime
from database.database import Base, int_pk, created_at, updated_at, float_value
from sqlalchemy.orm import Mapped, mapped_column, relationship




class Historyofpayments(Base):
    __tablename__ = 'historyofpayments'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", 
                                                    ondelete='CASCADE', 
                                                    onupdate='CASCADE'))
    user = relationship(User)
    value: Mapped[float_value]
    value_before: Mapped[float_value]
    value_after: Mapped[float_value]
    created: Mapped[created_at]
    processed: Mapped[updated_at]
    status: Mapped[str]
    
    def __repr__(self) -> str:
        return f"id={self.id} from={self.value_before} with={self.value} to={self.value_after} status={self.status} at={self.processed}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
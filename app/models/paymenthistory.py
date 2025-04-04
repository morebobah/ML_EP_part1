from datetime import datetime
from sqlalchemy.sql import func
from models.user import User
from sqlalchemy import text, ForeignKey, DateTime
from database.database import Base, int_pk, created_at, updated_at, float_zero
from sqlalchemy.orm import Mapped, mapped_column, relationship




class PaymentHistory(Base):
    __tablename__ = 'paymenthistory'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", 
                                                    ondelete='CASCADE', 
                                                    onupdate='CASCADE'))
    user = relationship(User)
    value: Mapped[float_zero]
    value_before: Mapped[float_zero]
    value_after: Mapped[float_zero]
    created: Mapped[created_at]
    processed: Mapped[updated_at]
    status: Mapped[str]
    
    def __repr__(self) -> str:
        return f"id={self.id} from={self.value_before} with={self.value} to={self.value_after} status={self.status} at={self.processed}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
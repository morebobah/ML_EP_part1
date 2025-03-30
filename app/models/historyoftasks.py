from datetime import datetime
from sqlalchemy.sql import func
from models.user import User
from sqlalchemy import text, ForeignKey, DateTime, Integer
from database.database import Base, int_pk, updated_at, float_zero
from sqlalchemy.orm import Mapped, mapped_column, relationship




class Historyoftasks(Base):
    __tablename__ = 'historyoftasks'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", 
                                                    ondelete='CASCADE', 
                                                    onupdate='CASCADE'))
    user = relationship(User)
    image: Mapped[str]
    processed: Mapped[updated_at]
    status: Mapped[str]
    result: Mapped[str]
    cost: Mapped[float_zero]
    
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id} value={self.image} status={self.status} started={self.processed})"
    
    def __str__(self) -> str:
        return self.__repr__()
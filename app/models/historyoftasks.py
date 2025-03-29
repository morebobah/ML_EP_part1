from datetime import datetime
from sqlalchemy.sql import func
from models.user import User
from sqlalchemy import text, ForeignKey, DateTime, Integer
from database.database import Base, int_pk, created_at, updated_at
from sqlalchemy.orm import Mapped, mapped_column, relationship




class Historyotasks(Base):
    __tablename__ = 'historyoftasks'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", 
                                                    ondelete='CASCADE', 
                                                    onupdate='CASCADE'))
    user = relationship(User)
    value: Mapped[str]
    created: Mapped[created_at]
    processed: Mapped[updated_at]
    status: Mapped[str]
    result: Mapped[str]
    
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id} value={self.value} status={self.status} started={self.created})"
    
    def __str__(self) -> str:
        return f"Payment (id={self.id}) {self.value} {self.status}"
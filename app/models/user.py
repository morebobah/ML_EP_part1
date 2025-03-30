from sqlalchemy import text
from sqlalchemy import event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base, int_pk, str_uniq, float_zero, float_one, bool_val

class User(Base):
    __tablename__='users'
    
    id: Mapped[int_pk]
    email: Mapped[str_uniq]
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    balance: Mapped[float_zero]
    loyalty: Mapped[float_one]
    is_admin: Mapped[bool_val]

    extend_existing = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __str__(self) -> str:
        return f"{self.id} - {self.first_name} {self.last_name}"
  
@event.listens_for(Base.metadata, 'after_create')
def create_update_rule(target, conn, **kw):
    users = []
    for idx in range(5):
        users.append(User(email=f'user{idx}@mydb.one', 
                      first_name=f'User{idx}', 
                      last_name=f'Fortest{idx}', 
                      password=f'pw{idx}', 
                      balance=0.0))
    Session = sessionmaker(conn)
    session = Session()
    is_admin = True
    for user_item in users:
        exists = session.query(User).filter(User.email == user_item.email).first()
        if not exists:
            if is_admin:
                user_item.is_admin = is_admin
                is_admin = False
            session.add(user_item)
    session.commit()
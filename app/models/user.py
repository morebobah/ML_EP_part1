from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column

class User:
    id: Mapped[int] = Annotated[int, mapped_column(primary_key=True)]
    email: Mapped[str] = Annotated[str, mapped_column(unique=True, nullable=False)]
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    extend_existing = True

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
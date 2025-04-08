from pydantic import BaseModel, EmailStr, Field
import re

class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=3, max_length=50, description="Пароль, от 3 до 50 знаков")

class SUserRegister(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    email: EmailStr
    password: str = Field(..., min_length=3, max_length=50, description="Пароль, от 3 до 50 знаков")

class SUser(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    last_name: str = Field(..., min_length=3, max_length=50, description="Фамилия, от 3 до 50 символов")
    email: EmailStr
    password: str = Field(..., min_length=3, max_length=50, description="Пароль, от 3 до 50 знаков")
    is_admin: bool = Field(...)
    balance: float = Field(...)
    loyalty: float = Field(...)

class SUserID(BaseModel):
    id: int = Field(...)

class SUserEmail(BaseModel):
    email: EmailStr

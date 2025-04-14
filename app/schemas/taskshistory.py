from pydantic import BaseModel, EmailStr, Field
import re

class STasksHistory(BaseModel):
    user_id: int = Field(...)
    image: str = Field(...)
    status: str = Field(...)
    result: str = Field(...)
    cost: float = Field(...)


class STaskComplete(BaseModel):
    task_id: int = Field(...)
    user_id: int = Field(...)
    result: str = Field(...)
    cost: float = Field(...)
    key: str = Field(...)


class STaskID(BaseModel):
    id: int = Field(...)

class STasksInfo(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)

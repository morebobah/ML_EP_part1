from pydantic import BaseModel, EmailStr, Field
import re

class STasksHistory(BaseModel):
    user_id: int = Field(...)
    image: str = Field(...)
    status: str = Field(...)
    result: str = Field(...)
    cost: float = Field(...)
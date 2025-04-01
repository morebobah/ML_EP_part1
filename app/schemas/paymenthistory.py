from pydantic import BaseModel, EmailStr, Field
import re

class SPaymentHistory(BaseModel):
    user_id: int = Field(...)
    value: float = Field(...)
    value_after: float = Field(...)
    value_before: float = Field(...)
    status: str = Field(...)
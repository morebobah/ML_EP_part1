from pydantic import BaseModel, EmailStr, Field
import re

class SBalance(BaseModel):
    balance: float = Field(...)

class SLoyalty(BaseModel):
    balance: float = Field(...)

class SBalancePlus(BaseModel):
    balance: float = Field(..., gt=0)

class SBalanceInfo(BaseModel):
    id: int = Field(...)
    user_id: int = Field(...)
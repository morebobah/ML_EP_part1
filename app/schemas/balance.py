from pydantic import BaseModel, EmailStr, Field
import re

class SBalance(BaseModel):
    balance: float = Field(...)

class SLoyalty(BaseModel):
    balance: float = Field(...)
from pydantic import BaseModel,EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime


class CreateUser(BaseModel):
    email:EmailStr
    name:str
 
class UserResponse(BaseModel):
    id:UUID
    name:str
    email:str

class UserLogin(BaseModel):
    email:EmailStr

class UserOut(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    company_id: Optional[UUID]
    created_at: datetime
class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

    model_config = {"from_attributes": True}


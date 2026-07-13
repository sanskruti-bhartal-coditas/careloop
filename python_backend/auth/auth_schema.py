from pydantic import BaseModel,EmailStr
from uuid import UUID


class CreateUser(BaseModel):
    email:EmailStr
    name:str
 
class UserResponse(BaseModel):
    id:UUID
    name:str
    email:str

class UserLogin(BaseModel):
    email:EmailStr



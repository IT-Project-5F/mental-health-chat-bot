from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email_address: Optional[str] = None
    password: Optional[str] = None
    status: Optional[bool] = None
    location: Optional[str] = None

class AdminCreate(BaseModel):
    username: str
    password: str
    email_address: str
    location: Optional[str] = "System"

class User(UserBase):
    id: int
    status: bool
    email_address: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True
        
class AuxillaryUser(UserBase):
    id: int
    username: str
    email_address: Optional[str]
    location: Optional[str]

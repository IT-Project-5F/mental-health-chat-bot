from pydantic import BaseModel 

class UserBase(BaseModel): 
    username : str 
    
class UserCreate(UserBase): 
    password : str 

class UserResponse(UserBase): 
    id : int 
    class Config : 
       from_attribute = True
from sqlalchemy import Boolean, Column, Integer, String, Enum
from auth.Database import Base 

class User(Base): 
  __tablename__ = "UserInformations" 
  id = Column(Integer, primary_key = True, index = True) 
  username = Column(String, unique = True, index = True)
  email_address = Column(String, unique = True)  
  hashed_password = Column(String) 
  status = Column(Boolean, default = True)
  location = Column(String)
  role = Column(
    Enum("user", "admin", name="user_roles"), 
    default="user", 
    nullable = False
  )
  previous_chat_context = Column(String)


class AuxillaryUser(Base): 
  __tablename__ = "AuxillaryUser" 
  id = Column(Integer, primary_key = True, index = True) 
  username =Column(String, unique = True, index = True)
  email_address = Column(String, unique = True) 
  hashed_password = Column(String)
  location = Column(String)
    
  
  
  
  
  
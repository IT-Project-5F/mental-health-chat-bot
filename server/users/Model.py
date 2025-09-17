from sqlalchemy import Boolean, Column, Integer, String 
from auth.Database import Base 

class User(Base): 
  __tablename__ = "UserInformations" 
  id = Column(Integer, primary_key = True, index = True) 
  username = Column(String, unique = True, index = True)
  email_address = Column(String, unique = True)  
  hashed_password = Column(String) 
  status = Column(Boolean, default = True)
  location = Column(String)
  previous_chat_context = Column(String)

  
  
  
  
  
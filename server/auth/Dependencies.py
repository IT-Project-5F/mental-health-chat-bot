from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer 
from typing import Annotated
from jwt import InvalidTokenError
import jwt
from sqlalchemy.orm import Session
from .Model import TokenData 
from users.Model import User, AuxillaryUser
from .Database import sessionLocal, engine, Base 
from .Utils import get_password_hash, verify_passowrd, create_access_token, ALGORITHM, SECRET_KEY
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/api/auth/login")

def get_database(): 
  database = sessionLocal() 
  try: 
      yield database 
  finally : 
      database.close()

def get_auxillary_user(db : Session, username : str): 
    return db.query(AuxillaryUser).filter(AuxillaryUser.username == username).first() 

def get_user(db : Session, username : str): 
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db : Session, username : str, password : str) -> User | bool : 
    user = get_user(db, username) 
    if not user : 
        return False 
    if not verify_passowrd(password, user.hashed_password) : 
        return False 
    return user 

def get_current_user(db : Annotated[Session, Depends(get_database)], 
                     token : Annotated[str, Depends(oauth2_scheme)]) -> User : 
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail = "Could not validate credentials", 
        headers = {"WWW-Authenticate" : "Bearer"}, 
    )
    try : 
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        username = payload.get("sub")
        aim = payload.get("aim")
        if username is None or aim == "reset": 
            raise credentials_exception
        token_data = TokenData(username = username) 
    except InvalidTokenError : 
        raise credentials_exception 
    user = get_user(db, username = token_data.username)
    if user is None : 
        raise credentials_exception
    return user

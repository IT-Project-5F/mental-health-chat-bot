from passlib.context import CryptContext 
from datetime import datetime, timedelta, timezone 
import jwt 
import os 

SECRET_KEY = os.getenv('SECRET_KEY') 
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def verify_passowrd(plain_password : str, hashed_password : str) -> bool : 
    return pwd_context.verify(plain_password, hashed_password) 

def get_password_hash(password : str) -> str : 
    return pwd_context.hash(password) 

def create_access_token(data : dict, expires_delta : timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta : 
        expire = datetime.now(timezone.utc) + expires_delta 
    else : 
        expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM) 
    return encode_jwt
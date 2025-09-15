from fastapi import APIRouter, Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordRequestForm
from .Dependencies import get_database, authenticate_user, create_access_token, get_user 
from .Model import Token 
from sqlalchemy.orm import Session
from .Schemas import UserCreate, UserResponse
from typing import Annotated
from users.Model import User 
from .Utils import get_password_hash

router = APIRouter() 


@router.post("/login", response_model = Token) 
async def login_for_access_token(
    form_data : Annotated[OAuth2PasswordRequestForm, Depends()], 
    db : Annotated[Session, Depends(get_database)]
) -> Token : 
    user = authenticate_user(db, form_data.username, form_data.password) 
    if not user : 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Incorrect username or password", 
            headers = {"WWW-Authenticate" : 'Bearer'}, 
        )
    access_token = create_access_token( 
       data = {"sub" : user.username, "role": "chat"}
    )
    return Token(access_token = access_token, token_type = "bearer") 

@router.post("/signup", response_model = UserResponse) 
async def signup(user : UserCreate, db : Annotated[Session, Depends(get_database)]): 
   db_user = get_user(db, user.username)
   if db_user : 
       raise HTTPException(status_code = 400, detail=  "User already registered") 
   hash_password = get_password_hash(user.password)
   db_user = User(username = user.username, hashed_password = hash_password)
   db.add(db_user)
   db.commit()
   db.refresh(db_user)
   return db_user
   
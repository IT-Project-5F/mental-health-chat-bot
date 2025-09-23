from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .Dependencies import get_database, authenticate_user, create_access_token, get_user, get_auxillary_user
from .Model import Token
from sqlalchemy.orm import Session
from .Schemas import UserCreate, UserResponse
from typing import Annotated
from users.Model import User, AuxillaryUser
from .Utils import get_password_hash
import os
from logging import getLogger

logger = getLogger(__name__)

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

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: Annotated[Session, Depends(get_database)]):
    # Check if user already exists
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already registered"
        )
    
    # Check if user is already in auxiliary table
    auxillary_user = get_auxillary_user(db, user.username)
    if auxillary_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User signup already pending approval"
        )
    
    hash_password = get_password_hash(user.password)
    
    # Create temporary user in auxiliary table
    temporary_db_user = AuxillaryUser(
        username=user.username,
        hashed_password=hash_password,
        email_address=user.email_address if user.email_address else None,
        location=user.location if user.location else None
    )
    
    try:
        db.add(temporary_db_user)
        db.commit()
        db.refresh(temporary_db_user)
        return temporary_db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user signup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing signup request"
        )
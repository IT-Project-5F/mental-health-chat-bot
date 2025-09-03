from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.Dependencies import get_current_user, get_database
from .Schemas import User
from .Model import User as UserModel

router = APIRouter()

@router.get("/me", response_model = User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
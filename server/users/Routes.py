from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from auth.Dependencies import get_current_user, get_database
from auth.Utils import get_password_hash
from .Schemas import User, UserUpdate
from .Model import User as UserModel

router = APIRouter()

@router.get("/me", response_model = User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[User])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_user: UserModel = Depends(get_current_user)
):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_database),
    current_user: UserModel = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_database),
    current_user: UserModel = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return None
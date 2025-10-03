from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, List
from sqlalchemy.orm import Session
from typing import List
from auth.Schemas import UserResponse
from auth.Dependencies import get_current_user, get_database, get_auxillary_user, get_user
from auth.Utils import get_password_hash
from .Schemas import User, UserUpdate, AuxillaryUser, PasswordUpdateRequest
from .Model import User as UserModel, AuxillaryUser as AuxiliaryUserModel
import resend
from logging import getLogger
from dotenv import load_dotenv
from Utils import *

load_dotenv()


logger = getLogger(__name__)

router = APIRouter()

'''
This sections is dedicated to user managmement functionalities and should only be used by authenicated users with once exception
case of verified user trying to update their own password 
'''

@router.get("/me", response_model=User)
async def read_users_me(current_admin: UserModel = Depends(get_current_user)):
    """Get current user's profile"""
    return current_admin

@router.get("/", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_admin : UserModel = Depends(get_current_user)  # Added authentication
):
    """List all users (requires authentication)"""
    return await db.query(UserModel).offset(skip).limit(limit).all()

@router.get("/pending", response_model=List[AuxillaryUser])
async def list_pending_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
    current_admin : UserModel = Depends(get_current_user)
):
    """List pending user applications (requires authentication)"""
    return await db.query(AuxiliaryUserModel).offset(skip).limit(limit).all()

@router.put("/reset_password", status_code = status.HTTP_204_NO_CONTENT)
async def update_password(
    password_data : PasswordUpdateRequest,
    db: Session = Depends(get_database),
):
    """Update current user's password securely"""
    # Verify current password
    user = await get_user(db, password_data.username)
    if not user or user.username != password_data.username :
        raise HTTPException(
           status_code = status.HTTP_404_NOT_FOUND,
           detail = "User not found",
        )
    try:
        # Update password
        user.hashed_password = get_password_hash(password_data.new_password)
        db.commit()
        db.refresh(user)

        # Send notification email
        if user.email_address:
            subject, html = EmailNotificationService.get_password_reset_email()
            if not await EmailNotificationService.send_email(user.email_address, subject, html):
                logger.warning(f"Password updated but email notification failed for user {user.username}")

        logger.info(f"Password updated successfully for user {user.username}")
        return None

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating password for user {user.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating password"
        )

@router.put("/{user_id}", status_code = status.HTTP_204_NO_CONTENT)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_database),
    current_admin: UserModel = Depends(get_current_user),
):
    """Update user information"""
    user = await db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    try:
        update_data = user_update.dict(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        # Update fields
        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        # Send notification email
        if user.email_address:
            subject, html = EmailNotificationService.get_account_update_email()
            if not await EmailNotificationService.send_email(user.email_address, subject, html):
                logger.warning(f"User updated but email notification failed for user {user.username}")
        logger.info(f"User {user.username} updated successfully")
        return None

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user"
        )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_database),
    current_admin: UserModel = Depends(get_current_user)
):
    """Delete a user"""
    user = await db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        db.delete(user)
        db.commit()
        logger.info(f"User {user.username} deleted successfully")
        return None
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user"
        )

@router.post("/accept/{username}", response_model=UserResponse)
async def accept_user(
    username: str,
    db: Annotated[Session, Depends(get_database)],
    current_admin: UserModel = Depends(get_current_user)  # Added authentication
):
    """Accept a pending user application"""

    auxillary_db_user = await get_auxillary_user(db, username)
    if auxillary_db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pending user not found"
        )

    # Check if user already exists in main table
    existing_user = await get_user(db, username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists in main system"
        )

    try:
        # Create the main user
        db_user = UserModel(
            username=auxillary_db_user.username,
            hashed_password=auxillary_db_user.hashed_password,
            email_address=auxillary_db_user.email_address,
            location=auxillary_db_user.location
        )

        # Add user to main table
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Remove from auxiliary table
        db.delete(auxillary_db_user)
        db.commit()

        # Send welcome email
        if auxillary_db_user.email_address:
            subject, html = EmailNotificationService.get_welcome_email()
            if not await EmailNotificationService.send_email(auxillary_db_user.email_address, subject, html):
                logger.warning(f"User accepted but welcome email failed for {username}")

        logger.info(f"User {username} accepted successfully")
        return db_user
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error accepting user {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing user acceptance"
        )

@router.delete("/decline/{username}")
async def decline_user(
    username: str,
    db: Annotated[Session, Depends(get_database)],
    current_admin: UserModel = Depends(get_current_user)  # Added authentication
):
    """Decline a pending user application"""
    # Add admin check if needed
    auxillary_db_user = await get_auxillary_user(db, username)
    if auxillary_db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pending user not found"
        )

    email_address = auxillary_db_user.email_address
    
    try:
        db.delete(auxillary_db_user)
        db.commit()

        # Send rejection email
        if email_address:
            subject, html = EmailNotificationService.get_rejection_email()
            if not await EmailNotificationService.send_email(email_address, subject, html):
                logger.warning(f"User declined but rejection email failed for {username}")

        logger.info(f"User {username} declined successfully")
        return {"message": "User application declined successfully"}
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error declining user {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing user decline"
        )
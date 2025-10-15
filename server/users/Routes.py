from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
from typing import List
from auth.Schemas import UserResponse
from auth.Dependencies import get_current_user, get_database, get_auxillary_user, get_user
from auth.Utils import get_password_hash
from .Schemas import User, UserUpdate, AdminCreate
from .Model import User as UserModel, AuxillaryUser
import resend
import os
from logging import getLogger
from dotenv import load_dotenv

load_dotenv()

logger = getLogger(__name__)

router = APIRouter()


@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=List[User])
def list_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_database),
):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@router.get("/pending", response_model=List[User])
def list_pending_users(
        skip: int = 0,
        limit: int = 0,
        db: Session = Depends(get_database)
):
    return db.query(AuxillaryUser).offset(skip).limit(limit).all()


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


@router.post("/accept", response_model=UserResponse)
async def accept_user(username: str, db: Annotated[Session, Depends(get_database)]):
    auxillary_db_user = get_auxillary_user(db, username)
    if auxillary_db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pending user not found"
        )

    # Check if user already exists in main table
    existing_user = get_user(db, username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists in main system"
        )

    # Create the main user
    db_user = UserModel(
        username=auxillary_db_user.username,
        hashed_password=auxillary_db_user.hashed_password,
        email_address=auxillary_db_user.email_address,
        location=auxillary_db_user.location
    )

    email_address = auxillary_db_user.email_address

    try:
        # Add user to main table
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Remove from auxiliary table
        db.delete(auxillary_db_user)
        db.commit()

        # Send acceptance email if email address is provided
        if email_address:
            try:
                r = resend.Emails.send({
                    "from": "Welcome <onboarding@resend.dev>",
                    "to": ["foxtrotfive026@gmail.com"],
                    "subject": "Welcome! Your account has been approved",
                    "html": """
                    <h2>Congratulations!</h2>
                    <p>Your account has been approved and you now have full access to the system.</p>
                    <p>You can now log in using your credentials.</p>
                    <p>Welcome aboard!</p>
                    """
                })
                logger.info(f"Welcome email sent successfully to {email_address}")
            except Exception as email_error:
                db.rollback()
                logger.error(f"Failed to send welcome email to {email_address}: {email_error}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Error while sending accepted emails")

        return db_user

    except Exception as e:
        db.rollback()
        logger.error(f"Error accepting user {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing user acceptance"
        )


@router.delete("/decline/{username}")
async def decline_user(username: str, db: Annotated[Session, Depends(get_database)]):
    auxillary_db_user = get_auxillary_user(db, username)
    if auxillary_db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pending user not found"
        )

    email_address = auxillary_db_user.email_address

    try:
        db.delete(auxillary_db_user)
        db.commit()

        # Send rejection email if email address is provided
        if email_address:
            try:
                r = resend.Emails.send({
                    "from": "Sorry <onboarding@resend.dev>",
                    "to": ["foxtrotfive026@gmail.com"],
                    "subject": "Application Update",
                    "html": """
                    <h2>Application Status Update</h2>
                    <p>Thank you for your interest in our system.</p>
                    <p>Unfortunately, we are unable to approve your application at this time.</p>
                    <p>If you have any questions, please feel free to contact us.</p>
                    """
                })
                logger.info(f"Rejection email sent to {email_address}")
            except Exception as email_error:
                db.rollback()
                logger.error(f"Failed to send rejection email to {email_address}: {email_error}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail="Error while sending accepted emails")

        return {"message": "User application declined successfully"}

    except Exception as e:
        db.rollback()
        logger.error(f"Error declining user {username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing user decline"
        )


@router.post("/create-admin", response_model=User)
def create_admin_user(
        admin_data: AdminCreate,
        db: Session = Depends(get_database),
        current_user: UserModel = Depends(get_current_user)
):
    """
    Create a new admin user. Only existing admin users can create new admin users.
    """
    # Check if current user is admin
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can create new admin users"
        )

    # Check if username already exists
    existing_user = get_user(db, admin_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    try:
        # Create new admin user
        hashed_password = get_password_hash(admin_data.password)
        new_admin = UserModel(
            username=admin_data.username,
            email_address=admin_data.email_address,
            hashed_password=hashed_password,
            status=True,
            location=admin_data.location,
            role="admin",
            previous_chat_context=""
        )

        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)

        logger.info(f"New admin user created: {admin_data.username} by {current_user.username}")
        return new_admin

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating admin user {admin_data.username}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating admin user"
        )
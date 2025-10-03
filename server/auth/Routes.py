from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .Dependencies import get_database, authenticate_user, create_access_token, get_user, get_auxillary_user
from .Model import Token
from sqlalchemy.orm import Session
from .Schemas import UserCreate, UserResponse
from typing import Annotated
from users.Model import AuxillaryUser
from .Utils import get_password_hash
import resend
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
       data = {"aim" : "using", "sub" : user.username, "role": user.role}
    )
    return Token(access_token = access_token, token_type = "bearer") 

@router.post("/reset/{username}")
async def reset_inform(
    username: str,
    db: Annotated[Session, Depends(get_database)]
):
    # Find user
    user = get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cannot find user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email_address = user.email_address
    if not email_address:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no registered email address",
        )

    user_details = {
        "aim" : "reset",
        "username": user.username,
        "user_email": user.email_address,
    }

    reset_token = create_access_token(
        user_details,
        password_reset=True
    )

    # Email content with proper token inclusion
    subject = "Reset password instructions"
    reset_url = f"http://localhost:3000/reset?token={reset_token}"  # Include the actual token
    html = f"""
    <h2>Password Reset</h2>
    <p>Hello {user.username},</p>
    <p>You have requested a password reset. Please click the link below to reset your password:</p>
    <p><a href="{reset_url}">Reset Your Password</a></p>
    <p>If the link doesn't work, you can copy and paste this URL into your browser:</p>
    <p>{reset_url}</p>
    <p>This link will expire in 10 minutes for security reasons.</p>
    <p>If you did not request this password reset, please ignore this email.</p>
    <p>If you have any questions, please feel free to contact us.</p>
    <br>
    <p>Best regards,<br>Support Team</p>
    """

    try:
        r = resend.Emails.send({
            "from": "Support <onboarding@resend.dev>",
            "to": [email_address],
            "subject": subject,
            "html": html,
        })
        logger.info(f"Reset email sent to {email_address}")
    except Exception as email_error:
        logger.error(f"Failed to send reset email to {email_address}: {email_error}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while sending reset email",
        )

    # Security: Don't return the actual token or email in the response
    return {"message": "If the username exists and has an email address, a reset link has been sent"}



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
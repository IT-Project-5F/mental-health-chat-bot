from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .Dependencies import get_database, authenticate_user, create_access_token, get_user, get_auxillary_user
from .Model import Token
from sqlalchemy.orm import Session
from .Schemas import UserCreate, UserResponse, UserResetPassword
from typing import Annotated
from users.Model import AuxillaryUser
import jwt
from .Utils import get_password_hash, SECRET_KEY, ALGORITHM
import resend
from logging import getLogger

logger = getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[Session, Depends(get_database)]
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )
    return Token(
        access_token = access_token,
        token_type = "bearer",
        username = user.username,
        email_address = user.email_address,
        role =  user.role
    )


@router.put("/reset/{username}")
async def reset_inform(
        username: str,
        db: Annotated[Session, Depends(get_database)]
):
    # Generic response to prevent user enumeration
    generic_response = {
        "message": "If the username exists and has a registered email address, a password reset link has been sent."
    }
    try:
        # Find user
        user = get_user(db, username)
        if not user or not user.email_address:
            # Don't reveal whether user exists
            logger.info(f"Reset requested for non-existent or email-less user: {username}")
            raise HTTPException(
              status_code = status.HTTP_404_NOT_FOUND,
              detail = "Cannot find user in the database"
            )
        # Check if there's an unexpired token
        if user.reset_token:
            try:
                # Verify if token is still valid
                jwt.decode(user.reset_token, SECRET_KEY, algorithms=[ALGORITHM])
                # Token is still valid
                logger.info(f"Valid reset token already exists for user: {username}")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="A reset link was recently sent. Please check your email or wait before requesting another.",
                )
            except jwt.ExpiredSignatureError:
                # Token is expired, clear it and allow new reset
                logger.info(f"Expired reset token found for user: {username}, clearing it")
                user.reset_token = None
                db.commit()
            except jwt.InvalidTokenError:
                # Token is invalid, clear it and allow new reset
                logger.info(f"Invalid reset token found for user: {username}, clearing it")
                user.reset_token = None
                db.commit()
            except Exception as e:
                # Other errors, log and clear token
                logger.error(f"Unexpected error validating reset token: {e}")
                user.reset_token = None
                db.commit()

        user_details = {
            "username": user.username,
            "user_email": user.email_address,
        }

        reset_token = create_access_token(
            user_details,
            password_reset=True
        )

        user.reset_token = reset_token
        db.commit()
        db.refresh(user)

        # Email content
        subject = "Reset password instructions"
        reset_url = f"http://localhost:3000/reset?token={reset_token}"
        html = f"""
        <h2>Password Reset Request</h2>
        <p>Hello {user.username},</p>
        <p>You have requested to reset your password. Please click the link below to proceed:</p>
        <p><a href="{reset_url}">Reset Your Password</a></p>
        <p>If the link doesn't work, copy and paste this URL into your browser:</p>
        <p>{reset_url}</p>
        <p>This link will expire in 10 minutes for security reasons.</p>
        <p><strong>If you did not request this password reset, please ignore this email and consider changing your password.</strong></p>
        <br>
        <p>Best regards,<br>Support Team</p>
        """

        # Send email (using test email for development)
        r = resend.Emails.send({
            "from": "Support <onboarding@resend.dev>",
            "to": ["foxtrotfive026@gmail.com"],  # Test email for development
            "subject": subject,
            "html": html,
        })
        logger.info(f"Reset email sent successfully for user: {username}")

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error processing reset request: {e}")
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Internal server error : {e}"
        )

    return generic_response


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


@router.put("/confirm_reset", response_model=UserResponse)
async def confirm_password_reset(
        password_reset_details: UserResetPassword,
        db: Annotated[Session, Depends(get_database)]
):
    """Confirm password reset with token"""
    try:
        # Extract and validate input
        token = password_reset_details.token
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token not included"
            )

        username = password_reset_details.username
        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username not provided"
            )

        new_password = password_reset_details.new_password
        if not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password not provided"
            )

        # Verify JWT token
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithm = ALGORITHM
            )
            token_username = payload.get("username")
            if token_username != username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Token does not match username"
                )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        # Get user from database
        user = get_user(db, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify stored token matches
        if user.reset_token != token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )

        user.hashed_password = get_password_hash(new_password)
        user.reset_token = None
        db.commit()
        db.refresh(user)
        logger.info(f"Password successfully reset for user: {username}")

        # Send notification email
        if user.email_address:
            subject = "Your password has been reset successfully"
            html_content = """
                <h2>Password Reset Successful</h2>
                <p>Hello,</p>
                <p>Your password has been reset successfully. You can now log in with your new credentials.</p>
                <p>If you did not request this change, please contact our support team immediately.</p>
                <br/>
                <p>Best regards,<br/>The Support Team</p>
                """
            try:
                    resend.Emails.send({
                        "from": "Support <onboarding@resend.dev>",
                        "to": ["foxtrotfive026@gmail.com"],
                        "subject": subject,
                        "html": html_content,
                    })
                    logger.info(f"Email sent successfully")
                    return True
            except Exception as e:
                    logger.error(f"Failed to send email : {e}")
                    return False

        logger.info(f"Password updated successfully for user {user.username}")
        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error confirming password reset: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password"
        )
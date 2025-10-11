import resend
from logging import getLogger
from dotenv import load_dotenv

load_dotenv()
logger = getLogger(__name__)


class EmailNotificationService:
    """Service class for handling email notifications"""
    
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str) -> bool:
        """Send email and return success status"""
        try:
            resend.Emails.send({
                "from": "Support <onboarding@resend.dev>",
                "to": [to_email], 
                "subject": subject,
                "html": html_content,
            })
            logger.info(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    @staticmethod
    def get_password_reset_email() -> tuple[str, str]:
        subject = "Your password has been reset successfully"
        html = """
        <h2>Password Reset Successful</h2>
        <p>Hello,</p>
        <p>Your password has been reset successfully. You can now log in with your new credentials.</p>
        <p>If you did not request this change, please contact our support team immediately.</p>
        <br/>
        <p>Best regards,<br/>The Support Team</p>
        """
        return subject, html

    @staticmethod
    def get_account_update_email() -> tuple[str, str]:
        subject = "Your account details have been updated"
        html = """
        <h2>Account Updated</h2>
        <p>Hello,</p>
        <p>Your account information has been updated successfully.</p>
        <p>If you did not request this change, please contact our support team immediately.</p>
        <br/>
        <p>Best regards,<br/>The Support Team</p>
        """
        return subject, html

    @staticmethod
    def get_welcome_email() -> tuple[str, str]:
        subject = "Welcome! Your account has been approved"
        html = """
        <h2>Congratulations!</h2>
        <p>Your account has been approved and you now have full access to the system.</p>
        <p>You can now log in using your credentials.</p>
        <p>Welcome aboard!</p>
        """
        return subject, html

    @staticmethod
    def get_rejection_email() -> tuple[str, str]:
        subject = "Application Update"
        html = """
        <h2>Application Status Update</h2>
        <p>Thank you for your interest in our system.</p>
        <p>Unfortunately, we are unable to approve your application at this time.</p>
        <p>If you have any questions, please feel free to contact us.</p>
        """
        return subject, html
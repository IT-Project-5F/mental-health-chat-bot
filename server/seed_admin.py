"""
Admin user seed script - Creates default admin user if it doesn't exist
"""
import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import select
from auth.Database import engine
from users.Model import User
from auth.Utils import get_password_hash

def create_admin_user():
    """Create admin user if it doesn't exist"""
    with Session(engine) as session:
        try:
            # Check if admin user already exists
            stmt = select(User).where(User.username == "admin")
            existing_admin = session.execute(stmt).scalar_one_or_none()

            if existing_admin:
                print("Admin user already exists")
                return

            # Create admin user
            hashed_password = get_password_hash("password123")
            admin_user = User(
                username="admin",
                email_address="admin@example.com",
                hashed_password=hashed_password,
                status=True,
                location="System",
                role="admin",
                previous_chat_context=""
            )

            session.add(admin_user)
            session.commit()
            print("Admin user created successfully:")
            print("  Username: admin")
            print("  Password: password123")
            print("  Role: admin")

        except Exception as e:
            print(f"Error creating admin user: {e}")
            session.rollback()

if __name__ == "__main__":
    print("Creating admin user...")
    create_admin_user()
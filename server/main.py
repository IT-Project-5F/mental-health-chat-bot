import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from auth.Routes import router as auth_router
from users.Routes import router as users_router
from chat.Routes import router as chat_router
from database.Routes import router as database_router
from auth.Database import Base, engine
import jwt
from jwt import PyJWTError
from auth.Utils import SECRET_KEY, ALGORITHM

Base.metadata.create_all(bind=engine)

# Seed admin user on startup
def seed_admin_user():
    """Ensure admin user exists"""
    try:
        from sqlalchemy.orm import Session
        from sqlalchemy import select
        from users.Model import User
        from auth.Utils import get_password_hash

        with Session(engine) as session:
            # Check if admin user exists
            stmt = select(User).where(User.username == "admin")
            existing_admin = session.execute(stmt).scalar_one_or_none()

            if not existing_admin:
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
                print("✅ Admin user created: username=admin, password=password123")
            else:
                print("✅ Admin user already exists")
    except Exception as e:
        print(f"❌ Error seeding admin user: {e}")

# Seed admin user
seed_admin_user()

app = FastAPI(title="Mental Health Chat Bot API", version="1.0.0")

app.include_router(auth_router, prefix='/api/auth', tags=["auth"])
app.include_router(users_router, prefix='/api/users', tags=["users"])
app.include_router(chat_router, prefix='/api/chat', tags=["chat"])
app.include_router(database_router, prefix='/api/database', tags=["database"])

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    """Unified authentication middleware for user and admin endpoints"""

    # Define path permissions for different user types
    path_permissions = {
        "/api/users/": ["admin"],
        "/api/database/": ["admin"],
    }

    required_roles = None
    for path, roles in path_permissions.items():
        if request.url.path.startswith(path):
            required_roles = roles
            break

    if required_roles:
        authorization = request.headers.get("Authorization")
        if not authorization:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing Authorization header"}
            )

        try:
            auth_parts = authorization.split()
            if len(auth_parts) != 2:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authorization header format. Expected 'Bearer <token>'"}
                )

            scheme, token = auth_parts
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid authentication scheme. Expected 'Bearer'"}
                )

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            # Handle password reset tokens
            if payload.get("aim") == "reset":
                username = payload.get("username")
                user_email = payload.get("user_email")
                if not username or not user_email:
                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Invalid token payload"}
                    )
                request.state.user = {
                    "aim": "reset",
                    "username": username,
                    "email": user_email
                }
            else:
                # Handle regular authentication tokens
                user_role = payload.get("role")
                if user_role not in required_roles:
                    return JSONResponse(
                        status_code=403,
                        content={"detail": f"Access denied. Required roles: {required_roles}"}
                    )
                request.state.user = {
                    "aim": "using",
                    "username": payload.get("sub"),
                    "role": user_role
                }

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token has expired"}
            )
        except PyJWTError as e:
            return JSONResponse(
                status_code=401,
                content={"detail": f"Invalid token: {str(e)}"}
            )

    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"message": "Mental Health Chat Bot API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

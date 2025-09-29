import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth.Routes import router as auth_router
from users.Routes import router as users_router
from chat.Routes import router as chat_router
from database.Routes import router as database_router
from auth.Database import Base, engine
import jwt
from jwt import PyJWTError

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

Base.metadata.create_all(bind=engine)

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
    path_permissions = { 
        "/api/chat/": ["user"],
        "/api/users/" : ["user"] 
    }
    required_roles = None
    for path, roles in path_permissions.items():
        if request.url.path.startswith(path):
            required_roles = roles
            break
    if required_roles:
        authorization = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code = 401,
                detail = "Missing Authorization header"
            )

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code = 401,
                    detail = "Invalid authentication scheme"
                )  
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("aim") == "reset": 
                username = payload.get("username")
                user_email = payload.get("user_email")
                if not username or not user_email: 
                    raise HTTPException( 
                        status_code = 401, 
                        detail =  "Invalid token payload"
                    )  
                request.state.user = {
                   "aim" : "reset",  
                   "username" : username, 
                   "email" : user_email
                }     
            else:
                user_role = payload.get("role")
                if user_role not in required_roles:
                    raise HTTPException(
                        status_code=403,
                        detail = f"Access denied. Required roles: {required_roles}"
                    )
                
                request.state.user = {
                    "aim" : "using", 
                    "username": payload.get("sub"),
                    "role": user_role
                }

        except PyJWTError as e:
            return HTTPException(
                status_code=401,
                detail =  f"Invalid token: {str(e)}"
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

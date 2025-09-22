import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.Routes  import router as auth_router
from users.Routes import router as users_router
from chat.Routes  import router as chat_router
from auth.Database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mental Health Chat Bot API", version="1.0.0")

app.include_router(auth_router, prefix  = '/api/auth', tags  = ["auth"]) 
app.include_router(users_router, prefix = '/api/users', tags = ["users"])
app.include_router(chat_router,  prefix = '/api/chat', tags  = ["chat"])

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Mental Health Chat Bot API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

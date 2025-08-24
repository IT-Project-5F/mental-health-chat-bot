import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging
import uuid
from datetime import datetime, timedelta
import asyncio
from rag_service import process_input_with_retrieval_continuous
from tasks import cleanup_expired_sessions, SESSION_TTL_HOURS, SESSION_INACTIVITY_MINUTES, MAX_SESSIONS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mental Health Chat Bot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for chat sessions with cleanup
chat_sessions: Dict[str, dict] = {}

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    
class ChatResponse(BaseModel):
    response: str
    session_id: str
    error: Optional[str] = None

class SessionRequest(BaseModel):
    pass

class SessionResponse(BaseModel):
    session_id: str
    created_at: str

class Message(BaseModel):
    role: str
    content: str
    timestamp: str

class ChatHistory(BaseModel):
    session_id: str
    messages: List[Message]

@app.get("/")
def read_root():
    return {"message": "Mental Health Chat Bot API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/sessions", response_model=SessionResponse)
async def create_session():
    """
    Create a new chat session
    """
    session_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    chat_sessions[session_id] = {
        "created_at": timestamp,
        "last_activity": timestamp,
        "messages": []
    }
    
    logger.info(f"Created new session: {session_id}")
    return SessionResponse(session_id=session_id, created_at=timestamp)

@app.get("/api/sessions/{session_id}/history", response_model=ChatHistory)
async def get_chat_history(session_id: str):
    """
    Get chat history for a session
    """
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return ChatHistory(
        session_id=session_id,
        messages=chat_sessions[session_id]["messages"]
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process user chat message using RAG system with conversation history
    """
    try:
        # Create new session if none provided
        if not request.session_id:
            session_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            chat_sessions[session_id] = {
                "created_at": timestamp,
                "last_activity": timestamp,
                "messages": []
            }
            logger.info(f"Created new session: {session_id}")
        else:
            session_id = request.session_id
            if session_id not in chat_sessions:
                raise HTTPException(status_code=404, detail="Session not found")
        
        logger.info(f"Processing chat request for session {session_id}: {request.message[:100]}...")
        
        # Update last activity time
        chat_sessions[session_id]["last_activity"] = datetime.now().isoformat()
        
        # Get conversation history
        conversation_history = chat_sessions[session_id]["messages"]
        
        # Add user message to history
        user_message = Message(
            role="user",
            content=request.message,
            timestamp=datetime.now().isoformat()
        )
        conversation_history.append(user_message.dict())
        
        # Process the message with RAG and conversation context
        response = process_input_with_retrieval_continuous(
            request.message, 
            [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history[:-1]]
        )
        
        # Add assistant response to history
        assistant_message = Message(
            role="assistant",
            content=response,
            timestamp=datetime.now().isoformat()
        )
        conversation_history.append(assistant_message.dict())
        
        logger.info("Successfully processed chat request")
        return ChatResponse(response=response, session_id=session_id)
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test")
def test_endpoint():
    """
    Test endpoint to verify API is working
    """
    return {"message": "API is working correctly"}

@app.get("/api/sessions/stats")
async def get_session_stats():
    """
    Get statistics about current sessions
    """
    return {
        "total_sessions": len(chat_sessions),
        "max_sessions": MAX_SESSIONS,
        "ttl_hours": SESSION_TTL_HOURS,
        "inactivity_minutes": SESSION_INACTIVITY_MINUTES
    }


@app.on_event("startup")
async def startup_event():
    """
    Start background tasks on application startup
    """
    asyncio.create_task(cleanup_expired_sessions(chat_sessions))
    logger.info("Started session cleanup background task")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)

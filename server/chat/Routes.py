from fastapi import APIRouter, HTTPException
from .RAG_Service import process_with_intelligent_fallback
from .Utils import get_topk_similar_docs, get_embeddings_vector
from guardrails import Guard
from .Model import *
import logging
from tasks import cleanup_expired_sessions, SESSION_TTL_HOURS, SESSION_INACTIVITY_MINUTES, MAX_SESSIONS
import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from geocoding_service import extract_and_geocode_from_service_data

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chat_sessions: Dict[str, dict] = {}

@router.post("/sessions", response_model=SessionResponse)
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

@router.get("/sessions/{session_id}/history", response_model=ChatHistory)
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

@router.post("/", response_model=ChatResponse)
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

        # Get similar documents for geocoding
        tuple_related_docs = get_topk_similar_docs(get_embeddings_vector(request.message), k=3)
        related_docs = []
        for document in tuple_related_docs :
           related_docs.append(document['service'])

        # Process the message with RAG and conversation context
        response = process_with_intelligent_fallback(
            request.message,
            [{"role": msg["role"], "content": msg["content"]} for msg in conversation_history[:-1]]
        )

        # Extract and geocode addresses from the service data
        markers = []
        try:
            markers = await extract_and_geocode_from_service_data(related_docs)
            logger.info(f"Generated {len(markers)} map markers")
        except Exception as e:
            logger.warning(f"Error generating map markers: {str(e)}")

        # Add assistant response to history
        assistant_message = Message(
            role="assistant",
            content=response,
            timestamp=datetime.now().isoformat()
        )
        conversation_history.append(assistant_message.dict())

        logger.info("Successfully processed chat request")
        return ChatResponse(response=response, session_id=session_id, markers=markers)
    
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
def test_endpoint():
    """
    Test endpoint to verify API is working
    """
    return {"message": "API is working correctly"}

@router.get("/sessions/stats")
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


@router.on_event("startup")
async def startup_event():
    """
    Start background tasks on application startup
    """
    asyncio.create_task(cleanup_expired_sessions(chat_sessions))
    logger.info("Started session cleanup background task")
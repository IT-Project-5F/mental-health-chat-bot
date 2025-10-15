from pydantic import BaseModel
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class MapMarker(BaseModel):
    id: int
    position: List[float]  # [lat, lng]
    title: str
    address: str
    details: Dict

class ChatResponse(BaseModel):
    response: str
    session_id: str
    markers: Optional[List[MapMarker]] = None
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
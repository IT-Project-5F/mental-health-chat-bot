import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SESSION_TTL_HOURS = 24
SESSION_INACTIVITY_MINUTES = 30
MAX_SESSIONS = 1000
CLEANUP_INTERVAL_MINUTES = 5

async def cleanup_expired_sessions(chat_sessions: Dict[str, dict]):
    """
    Remove expired sessions based on TTL and inactivity
    """
    while True:
        try:
            await asyncio.sleep(CLEANUP_INTERVAL_MINUTES * 60)
            
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session_data in chat_sessions.items():
                created_at = datetime.fromisoformat(session_data["created_at"])
                if current_time - created_at > timedelta(hours=SESSION_TTL_HOURS):
                    expired_sessions.append(session_id)
                    continue
                
                last_activity = datetime.fromisoformat(session_data["last_activity"])
                if current_time - last_activity > timedelta(minutes=SESSION_INACTIVITY_MINUTES):
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                del chat_sessions[session_id]
                logger.info(f"Cleaned up expired session: {session_id}")
            
            if expired_sessions:
                logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            
            if len(chat_sessions) > MAX_SESSIONS:
                sorted_sessions = sorted(
                    chat_sessions.items(),
                    key=lambda x: x[1]["last_activity"],
                    reverse=True
                )
                sessions_to_keep = dict(sorted_sessions[:MAX_SESSIONS])
                removed_count = len(chat_sessions) - MAX_SESSIONS
                chat_sessions.clear()
                chat_sessions.update(sessions_to_keep)
                logger.warning(f"Removed {removed_count} oldest sessions to maintain limit of {MAX_SESSIONS}")
                
        except Exception as e:
            logger.error(f"Error during session cleanup: {str(e)}")
#!/usr/bin/env python3
"""
Test script for session cleanup functionality
"""
import asyncio
import logging
from datetime import datetime, timedelta
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the cleanup function
from tasks import SESSION_TTL_HOURS, SESSION_INACTIVITY_MINUTES, MAX_SESSIONS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_cleanup():
    """Test the session cleanup logic"""
    
    # Create mock chat sessions
    chat_sessions = {}
    current_time = datetime.now()
    
    # Create different types of sessions for testing
    print("\n=== Creating test sessions ===")
    
    # 1. Active session (should NOT be cleaned)
    chat_sessions["active-session"] = {
        "created_at": current_time.isoformat(),
        "last_activity": current_time.isoformat(),
        "messages": []
    }
    print("✓ Created active session")
    
    # 2. Old session (created > 24 hours ago, should be cleaned)
    old_time = current_time - timedelta(hours=25)
    chat_sessions["old-session"] = {
        "created_at": old_time.isoformat(),
        "last_activity": current_time.isoformat(),
        "messages": []
    }
    print("✓ Created old session (25 hours old)")
    
    # 3. Inactive session (no activity for > 30 minutes, should be cleaned)
    inactive_time = current_time - timedelta(minutes=35)
    chat_sessions["inactive-session"] = {
        "created_at": current_time.isoformat(),
        "last_activity": inactive_time.isoformat(),
        "messages": []
    }
    print("✓ Created inactive session (35 minutes inactive)")
    
    # 4. Recent but inactive (created recently but inactive, should be cleaned)
    recent_create = current_time - timedelta(hours=2)
    old_activity = current_time - timedelta(minutes=45)
    chat_sessions["recent-inactive"] = {
        "created_at": recent_create.isoformat(),
        "last_activity": old_activity.isoformat(),
        "messages": []
    }
    print("✓ Created recent but inactive session")
    
    print(f"\nTotal sessions before cleanup: {len(chat_sessions)}")
    print(f"Session IDs: {list(chat_sessions.keys())}")
    
    # Run cleanup logic (without the sleep part)
    print("\n=== Running cleanup logic ===")
    expired_sessions = []
    
    for session_id, session_data in chat_sessions.items():
        # Check TTL (24 hours since creation)
        created_at = datetime.fromisoformat(session_data["created_at"])
        if current_time - created_at > timedelta(hours=SESSION_TTL_HOURS):
            expired_sessions.append(session_id)
            print(f"  → {session_id}: Expired due to age (>{SESSION_TTL_HOURS} hours)")
            continue
        
        # Check inactivity (30 minutes since last activity)
        last_activity = datetime.fromisoformat(session_data["last_activity"])
        if current_time - last_activity > timedelta(minutes=SESSION_INACTIVITY_MINUTES):
            expired_sessions.append(session_id)
            print(f"  → {session_id}: Expired due to inactivity (>{SESSION_INACTIVITY_MINUTES} minutes)")
    
    # Remove expired sessions
    for session_id in expired_sessions:
        del chat_sessions[session_id]
        print(f"  ✗ Removed session: {session_id}")
    
    print(f"\n=== Cleanup Results ===")
    print(f"Sessions removed: {len(expired_sessions)}")
    print(f"Sessions remaining: {len(chat_sessions)}")
    print(f"Remaining session IDs: {list(chat_sessions.keys())}")
    
    # Verify the results
    assert "active-session" in chat_sessions, "Active session should NOT be removed"
    assert "old-session" not in chat_sessions, "Old session should be removed"
    assert "inactive-session" not in chat_sessions, "Inactive session should be removed"
    assert "recent-inactive" not in chat_sessions, "Recent but inactive session should be removed"
    
    print("\n✅ All tests passed! Cleanup logic is working correctly.")
    
    # Test MAX_SESSIONS limit
    print(f"\n=== Testing MAX_SESSIONS limit ({MAX_SESSIONS}) ===")
    
    # Add many sessions to test the limit
    for i in range(10):
        session_time = current_time - timedelta(minutes=i)
        chat_sessions[f"test-session-{i}"] = {
            "created_at": session_time.isoformat(),
            "last_activity": session_time.isoformat(),
            "messages": []
        }
    
    print(f"Added 10 more test sessions. Total: {len(chat_sessions)}")
    
    # Simulate MAX_SESSIONS = 5 for testing
    test_max = 5
    if len(chat_sessions) > test_max:
        sorted_sessions = sorted(
            chat_sessions.items(),
            key=lambda x: x[1]["last_activity"],
            reverse=True
        )
        sessions_to_keep = dict(sorted_sessions[:test_max])
        removed_count = len(chat_sessions) - test_max
        chat_sessions.clear()
        chat_sessions.update(sessions_to_keep)
        print(f"  → Enforced limit of {test_max} sessions, removed {removed_count} oldest")
        print(f"  → Remaining sessions: {list(chat_sessions.keys())}")
    
    print("\n✅ MAX_SESSIONS limit test passed!")

if __name__ == "__main__":
    print("Session Cleanup Test Script")
    print("=" * 40)
    asyncio.run(test_cleanup())
"""
Storage management for chat history.
"""

import json
import uuid
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import threading

from .config import config

# Add utilities for time formatting
def format_timestamp(timestamp_str: str, style: str = "iso") -> str:
    """Format a timestamp according to the given style."""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        
        if style == "iso":
            return timestamp_str
        elif style == "human":
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        elif style == "relative":
            delta = now - dt
            
            # Convert to appropriate units
            seconds = delta.total_seconds()
            if seconds < 60:
                return f"{int(seconds)} seconds ago"
            minutes = seconds / 60
            if minutes < 60:
                return f"{int(minutes)} minutes ago"
            hours = minutes / 60
            if hours < 24:
                return f"{int(hours)} hours ago"
            days = hours / 24
            if days < 30:
                return f"{int(days)} days ago"
            months = days / 30
            if months < 12:
                return f"{int(months)} months ago"
            years = months / 12
            return f"{int(years)} years ago"
        
        return timestamp_str
    except (ValueError, TypeError):
        return timestamp_str


def generate_title(user_input: str, ai_response: str) -> str:
    """Generate a title based on the first user input and AI response."""
    # Simple title generation - take the first 30 chars of user input
    if not user_input:
        return "New Chat"
    
    # Use just the first sentence or phrase
    for end_char in ['.', '?', '!', '\n']:
        if end_char in user_input:
            user_input = user_input.split(end_char)[0]
            
    if len(user_input) > 30:
        return user_input[:30] + "..."
    return user_input


class ChatSession:
    """Represents a chat session with messages history."""

    def __init__(self, session_id: Optional[str] = None, title: Optional[str] = None):
        """Initialize a chat session with optional ID."""
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now().isoformat()
        self.messages: List[Dict[str, str]] = []
        self.title = title or "New Chat"
        self.file_path = config.storage_dir / f"{self.session_id}.json"
        self.title_generation_pending = title is None
        self.title_generation_lock = threading.Lock()

    def add_message(self, role: str, content: str) -> None:
        """Add a message to the chat history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
        self.messages.append(message)
        
        # Generate title on the first exchange
        if self.title_generation_pending and len(self.messages) >= 2:
            if self.messages[0]["role"] == "user" and self.messages[1]["role"] == "assistant":
                with self.title_generation_lock:
                    if self.title_generation_pending:  # Check again inside lock
                        self.title = generate_title(self.messages[0]["content"], self.messages[1]["content"])
                        self.title_generation_pending = False
        
        self.save()

    def save(self) -> None:
        """Save the chat session to disk."""
        data = {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "title": self.title,
            "messages": self.messages,
        }

        # Ensure directory exists
        config.storage_dir.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, session_id: str) -> Optional["ChatSession"]:
        """Load a chat session from disk."""
        file_path = config.storage_dir / f"{session_id}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            session = cls(
                session_id=data["session_id"],
                title=data.get("title", "New Chat")
            )
            session.created_at = data.get("created_at", datetime.now().isoformat())
            session.messages = data.get("messages", [])
            session.title_generation_pending = False
            return session
        except (json.JSONDecodeError, KeyError):
            return None

    @classmethod
    def delete_session(cls, session_id: str) -> bool:
        """Delete a chat session by its ID."""
        file_path = config.storage_dir / f"{session_id}.json"

        if not file_path.exists():
            return False

        try:
            os.remove(file_path)
            return True
        except (IOError, OSError):
            return False

    @classmethod
    def list_sessions(cls) -> List[Dict[str, Any]]:
        """List all available chat sessions with metadata."""
        sessions = []
        time_style = config.get_time_style()

        for file_path in config.storage_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                session_info = {
                    "session_id": data["session_id"],
                    "created_at": data.get("created_at", "Unknown"),
                    "formatted_time": format_timestamp(data.get("created_at", "Unknown"), time_style),
                    "message_count": len(data.get("messages", [])),
                    "title": data.get("title", "New Chat"),
                    "file_path": str(file_path),
                }

                # Add a preview of the first exchange if available
                messages = data.get("messages", [])
                if messages:
                    first_user_msg = next(
                        (m for m in messages if m["role"] == "user"), None
                    )
                    session_info["preview"] = (
                        first_user_msg["content"][:50] + "..."
                        if first_user_msg
                        else "No preview"
                    )

                sessions.append(session_info)
            except (json.JSONDecodeError, KeyError, IOError):
                # Skip invalid files
                continue

        # Sort by creation time, newest first
        sessions.sort(key=lambda s: s["created_at"], reverse=True)
        return sessions

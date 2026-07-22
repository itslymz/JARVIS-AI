"""Short-term conversation memory."""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import deque


class Message:
    """Represents a single message in conversation memory."""

    def __init__(self, role: str, content: str, timestamp: datetime | None = None):
        self.role = role  # 'user' or 'assistant'
        self.content = content
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
        }


class ShortTermMemory:
    """Short-term conversation memory.
    
    Stores recent conversation context with configurable size limit.
    Older messages are automatically removed when limit is exceeded.
    """

    def __init__(self, max_size: int = 100):
        """Initialize short-term memory.
        
        Args:
            max_size: Maximum number of messages to store
        """
        self.max_size = max_size
        self.messages: deque = deque(maxlen=max_size)

    def add_message(self, role: str, content: str) -> None:
        """Add message to memory.
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
        """
        message = Message(role, content)
        self.messages.append(message)

    def get_context(self, limit: int | None = None) -> List[Dict[str, Any]]:
        """Get conversation context.
        
        Args:
            limit: Maximum number of recent messages to return
            
        Returns:
            List of messages as dictionaries
        """
        messages = list(self.messages)
        if limit:
            messages = messages[-limit:]
        return [m.to_dict() for m in messages]

    def clear(self) -> None:
        """Clear all messages from memory."""
        self.messages.clear()

    def get_last_n_messages(self, n: int) -> List[Dict[str, Any]]:
        """Get last n messages.
        
        Args:
            n: Number of recent messages
            
        Returns:
            List of last n messages
        """
        return [m.to_dict() for m in list(self.messages)[-n:]]

    def size(self) -> int:
        """Get number of messages in memory."""
        return len(self.messages)

    def is_empty(self) -> bool:
        """Check if memory is empty."""
        return len(self.messages) == 0

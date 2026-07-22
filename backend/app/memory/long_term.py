"""Long-term knowledge memory.

Stores facts, knowledge, and information that JARVIS learns over time.
Implemented with SQLAlchemy ORM.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.database import Memory


class LongTermMemory:
    """Long-term knowledge memory.
    
    Stores facts and learned information persistently in the database.
    """

    def __init__(self, db_session: AsyncSession):
        """Initialize long-term memory.
        
        Args:
            db_session: SQLAlchemy async session
        """
        self.db = db_session

    async def store(
        self,
        user_id: int,
        content: str,
        memory_type: str = "long_term",
        importance_score: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Memory:
        """Store knowledge in long-term memory.
        
        Args:
            user_id: User ID
            content: Memory content
            memory_type: Type of memory
            importance_score: Importance score (0-1)
            metadata: Additional metadata
            
        Returns:
            Created Memory object
        """
        memory = Memory(
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            importance_score=importance_score,
            metadata=metadata or {},
        )
        self.db.add(memory)
        await self.db.commit()
        await self.db.refresh(memory)
        return memory

    async def retrieve(
        self,
        user_id: int,
        memory_type: Optional[str] = None,
        limit: int = 10,
    ) -> List[Memory]:
        """Retrieve memories.
        
        Args:
            user_id: User ID
            memory_type: Optional memory type filter
            limit: Maximum results
            
        Returns:
            List of memories
        """
        query = select(Memory).where(Memory.user_id == user_id)
        
        if memory_type:
            query = query.where(Memory.memory_type == memory_type)
        
        query = query.order_by(Memory.importance_score.desc()).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(
        self,
        memory_id: int,
        **kwargs,
    ) -> Optional[Memory]:
        """Update memory.
        
        Args:
            memory_id: Memory ID
            **kwargs: Fields to update
            
        Returns:
            Updated Memory or None if not found
        """
        memory = await self.db.get(Memory, memory_id)
        if memory:
            for key, value in kwargs.items():
                if hasattr(memory, key):
                    setattr(memory, key, value)
            memory.updated_at = datetime.utcnow()
            await self.db.commit()
            await self.db.refresh(memory)
        return memory

    async def delete(self, memory_id: int) -> bool:
        """Delete memory.
        
        Args:
            memory_id: Memory ID
            
        Returns:
            True if deleted, False otherwise
        """
        memory = await self.db.get(Memory, memory_id)
        if memory:
            await self.db.delete(memory)
            await self.db.commit()
            return True
        return False

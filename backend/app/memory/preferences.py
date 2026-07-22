"""User preferences memory.

Stores learned user preferences and behavior patterns.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.database import UserPreferences


class PreferencesMemory:
    """User preferences memory.
    
    Tracks and learns user preferences over time.
    """

    def __init__(self, db_session: AsyncSession):
        """Initialize preferences memory.
        
        Args:
            db_session: SQLAlchemy async session
        """
        self.db = db_session

    async def get_preferences(self, user_id: int) -> Optional[UserPreferences]:
        """Get user preferences.
        
        Args:
            user_id: User ID
            
        Returns:
            UserPreferences or None
        """
        query = select(UserPreferences).where(UserPreferences.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_preferences(
        self,
        user_id: int,
        **kwargs,
    ) -> UserPreferences:
        """Update user preferences.
        
        Args:
            user_id: User ID
            **kwargs: Preferences to update
            
        Returns:
            Updated UserPreferences
        """
        prefs = await self.get_preferences(user_id)
        if prefs:
            for key, value in kwargs.items():
                if hasattr(prefs, key):
                    setattr(prefs, key, value)
            prefs.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(prefs)
        return prefs

    async def learn_preference(
        self,
        user_id: int,
        preference_key: str,
        preference_value: Any,
    ) -> None:
        """Learn a new user preference.
        
        Args:
            user_id: User ID
            preference_key: Preference key
            preference_value: Preference value
        """
        prefs = await self.get_preferences(user_id)
        if prefs and hasattr(prefs, preference_key):
            setattr(prefs, preference_key, preference_value)
            prefs.updated_at = datetime.utcnow()
            await self.db.commit()

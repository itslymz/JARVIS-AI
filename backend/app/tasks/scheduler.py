"""Scheduler for recurring and scheduled tasks."""

from typing import Optional, Dict, Any, Callable, List
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import uuid


class ScheduleFrequency(str, Enum):
    """Schedule frequency enumeration."""
    ONCE = "once"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class ScheduledTask:
    """Represents a scheduled task."""

    def __init__(
        self,
        name: str,
        frequency: ScheduleFrequency,
        scheduled_time: datetime,
        action: str,
        params: Optional[Dict[str, Any]] = None,
    ):
        """Initialize scheduled task.
        
        Args:
            name: Task name
            frequency: Schedule frequency
            scheduled_time: Next scheduled execution time
            action: Action to execute
            params: Action parameters
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.frequency = frequency
        self.scheduled_time = scheduled_time
        self.action = action
        self.params = params or {}
        self.last_executed: Optional[datetime] = None
        self.is_active = True
        self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "frequency": self.frequency.value,
            "scheduled_time": self.scheduled_time.isoformat(),
            "action": self.action,
            "is_active": self.is_active,
            "last_executed": self.last_executed.isoformat() if self.last_executed else None,
            "created_at": self.created_at.isoformat(),
        }


class Scheduler:
    """Manages scheduled task execution."""

    def __init__(self):
        """Initialize scheduler."""
        self.scheduled_tasks: Dict[str, ScheduledTask] = {}
        self.running = False

    async def start(self) -> bool:
        """Start scheduler.
        
        Returns:
            True if started
        """
        if self.running:
            return False
        self.running = True
        asyncio.create_task(self._scheduler_loop())
        return True

    async def stop(self) -> bool:
        """Stop scheduler.
        
        Returns:
            True if stopped
        """
        self.running = False
        return True

    async def add_task(
        self,
        name: str,
        frequency: ScheduleFrequency,
        scheduled_time: datetime,
        action: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> ScheduledTask:
        """Add a scheduled task.
        
        Args:
            name: Task name
            frequency: Schedule frequency
            scheduled_time: Next execution time
            action: Action to execute
            params: Action parameters
            
        Returns:
            Created ScheduledTask
        """
        task = ScheduledTask(name, frequency, scheduled_time, action, params)
        self.scheduled_tasks[task.id] = task
        return task

    async def remove_task(self, task_id: str) -> bool:
        """Remove a scheduled task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if removed
        """
        if task_id in self.scheduled_tasks:
            del self.scheduled_tasks[task_id]
            return True
        return False

    async def get_task(self, task_id: str) -> Optional[ScheduledTask]:
        """Get scheduled task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            ScheduledTask or None
        """
        return self.scheduled_tasks.get(task_id)

    async def list_tasks(self) -> List[ScheduledTask]:
        """List all scheduled tasks.
        
        Returns:
            List of ScheduledTasks
        """
        return list(self.scheduled_tasks.values())

    async def get_next_execution(self, task_id: str) -> Optional[datetime]:
        """Get next execution time for task.
        
        Args:
            task_id: Task ID
            
        Returns:
            Next execution time or None
        """
        task = self.scheduled_tasks.get(task_id)
        if task:
            return task.scheduled_time
        return None

    async def _scheduler_loop(self) -> None:
        """Main scheduler loop.
        
        Runs continuously and executes tasks when their scheduled time arrives.
        """
        while self.running:
            try:
                now = datetime.utcnow()
                
                for task_id, task in self.scheduled_tasks.items():
                    if (
                        task.is_active
                        and task.scheduled_time <= now
                    ):
                        # Execute task
                        await self._execute_task(task)
                        
                        # Calculate next execution time
                        task.scheduled_time = self._calculate_next_execution(
                            task.frequency,
                            task.scheduled_time,
                        )
                
                # Sleep for 1 minute before checking again
                await asyncio.sleep(60)
            except Exception as e:
                print(f"Scheduler error: {e}")
                await asyncio.sleep(60)

    async def _execute_task(self, task: ScheduledTask) -> bool:
        """Execute a scheduled task.
        
        Args:
            task: ScheduledTask to execute
            
        Returns:
            True if executed successfully
        """
        try:
            # TODO: Dispatch to appropriate handlers based on action
            task.last_executed = datetime.utcnow()
            return True
        except Exception as e:
            print(f"Failed to execute scheduled task: {e}")
            return False

    def _calculate_next_execution(
        self,
        frequency: ScheduleFrequency,
        current_time: datetime,
    ) -> datetime:
        """Calculate next execution time.
        
        Args:
            frequency: Schedule frequency
            current_time: Current scheduled time
            
        Returns:
            Next execution time
        """
        if frequency == ScheduleFrequency.ONCE:
            return current_time + timedelta(days=365)  # Effectively never
        elif frequency == ScheduleFrequency.HOURLY:
            return current_time + timedelta(hours=1)
        elif frequency == ScheduleFrequency.DAILY:
            return current_time + timedelta(days=1)
        elif frequency == ScheduleFrequency.WEEKLY:
            return current_time + timedelta(weeks=1)
        elif frequency == ScheduleFrequency.MONTHLY:
            return current_time + timedelta(days=30)
        elif frequency == ScheduleFrequency.YEARLY:
            return current_time + timedelta(days=365)
        else:
            return current_time + timedelta(days=1)

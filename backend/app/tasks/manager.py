"""Task manager for planning and executing multi-step tasks."""

from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from enum import Enum
import asyncio
import uuid


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class Task:
    """Represents a single task."""

    def __init__(
        self,
        name: str,
        description: str = "",
        steps: Optional[List[Dict[str, Any]]] = None,
    ):
        """Initialize task.
        
        Args:
            name: Task name
            description: Task description
            steps: List of task steps
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.steps = steps or []
        self.status = TaskStatus.PENDING
        self.current_step = 0
        self.created_at = datetime.utcnow()
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.result: Optional[Any] = None
        self.error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "current_step": self.current_step,
            "total_steps": len(self.steps),
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress": (self.current_step / len(self.steps) * 100) if self.steps else 0,
        }


class TaskManager:
    """Manages task planning and execution."""

    def __init__(self, max_concurrent_tasks: int = 3):
        """Initialize task manager.
        
        Args:
            max_concurrent_tasks: Maximum concurrent tasks
        """
        self.max_concurrent_tasks = max_concurrent_tasks
        self.tasks: Dict[str, Task] = {}
        self.running_tasks: List[str] = []
        self.queue: List[str] = []

    async def create_task(
        self,
        name: str,
        description: str = "",
        steps: Optional[List[Dict[str, Any]]] = None,
    ) -> Task:
        """Create a new task.
        
        Args:
            name: Task name
            description: Task description
            steps: List of steps
            
        Returns:
            Created Task
        """
        task = Task(name, description, steps)
        self.tasks[task.id] = task
        self.queue.append(task.id)
        return task

    async def execute_task(self, task_id: str) -> bool:
        """Execute a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if successful
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if len(self.running_tasks) >= self.max_concurrent_tasks:
            return False  # Queue is full

        try:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.utcnow()
            self.running_tasks.append(task_id)

            # Execute steps
            for idx, step in enumerate(task.steps):
                task.current_step = idx + 1
                action = step.get("action")
                params = step.get("params", {})

                # Execute step action
                # This would be customized based on step type
                await self._execute_step(action, params)

            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.utcnow()
            self.running_tasks.remove(task_id)
            return True

        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.utcnow()
            if task_id in self.running_tasks:
                self.running_tasks.remove(task_id)
            return False

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if cancelled
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.utcnow()

        if task_id in self.running_tasks:
            self.running_tasks.remove(task_id)
        if task_id in self.queue:
            self.queue.remove(task_id)

        return True

    async def pause_task(self, task_id: str) -> bool:
        """Pause a task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if paused
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if task.status == TaskStatus.RUNNING:
            task.status = TaskStatus.PAUSED
            return True
        return False

    async def resume_task(self, task_id: str) -> bool:
        """Resume a paused task.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if resumed
        """
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        if task.status == TaskStatus.PAUSED:
            task.status = TaskStatus.RUNNING
            return True
        return False

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID.
        
        Args:
            task_id: Task ID
            
        Returns:
            Task or None
        """
        return self.tasks.get(task_id)

    async def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
    ) -> List[Task]:
        """List tasks.
        
        Args:
            status: Optional status filter
            
        Returns:
            List of tasks
        """
        tasks = list(self.tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)

    async def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status.
        
        Returns:
            Queue status dictionary
        """
        return {
            "running": len(self.running_tasks),
            "queued": len(self.queue),
            "max_concurrent": self.max_concurrent_tasks,
            "capacity": len(self.queue) + len(self.running_tasks),
        }

    async def _execute_step(self, action: str, params: Dict[str, Any]) -> Any:
        """Execute a single step.
        
        Args:
            action: Action name
            params: Action parameters
            
        Returns:
            Step result
        """
        # This would dispatch to appropriate handlers
        # For now, just return success
        return {"status": "success"}

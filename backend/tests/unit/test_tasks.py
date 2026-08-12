"""Unit tests for task manager."""

import pytest
from datetime import datetime, timedelta
from app.tasks.manager import Task, TaskManager, TaskStatus
from app.tasks.scheduler import Scheduler, ScheduleFrequency


@pytest.fixture
def task_manager():
    """Create task manager instance."""
    return TaskManager()


@pytest.fixture
def scheduler():
    """Create scheduler instance."""
    return Scheduler()


@pytest.mark.asyncio
async def test_create_task(task_manager):
    """Test creating a task."""
    task = await task_manager.create_task(
        "Test Task",
        "Test Description",
        [{"action": "print", "params": {"text": "Hello"}}],
    )
    assert task.name == "Test Task"
    assert task.status == TaskStatus.PENDING


@pytest.mark.asyncio
async def test_get_task(task_manager):
    """Test getting a task."""
    task = await task_manager.create_task("Test Task")
    retrieved = await task_manager.get_task(task.id)
    assert retrieved is not None
    assert retrieved.id == task.id


@pytest.mark.asyncio
async def test_list_tasks(task_manager):
    """Test listing tasks."""
    await task_manager.create_task("Task 1")
    await task_manager.create_task("Task 2")
    tasks = await task_manager.list_tasks()
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_cancel_task(task_manager):
    """Test cancelling a task."""
    task = await task_manager.create_task("Test Task")
    result = await task_manager.cancel_task(task.id)
    assert result is True
    assert task.status == TaskStatus.CANCELLED


@pytest.mark.asyncio
async def test_add_scheduled_task(scheduler):
    """Test adding scheduled task."""
    scheduled_time = datetime.utcnow() + timedelta(hours=1)
    task = await scheduler.add_task(
        "Scheduled Task",
        ScheduleFrequency.DAILY,
        scheduled_time,
        "print",
    )
    assert task.name == "Scheduled Task"
    assert task.frequency == ScheduleFrequency.DAILY


@pytest.mark.asyncio
async def test_list_scheduled_tasks(scheduler):
    """Test listing scheduled tasks."""
    scheduled_time = datetime.utcnow() + timedelta(hours=1)
    await scheduler.add_task("Task 1", ScheduleFrequency.DAILY, scheduled_time, "print")
    await scheduler.add_task("Task 2", ScheduleFrequency.WEEKLY, scheduled_time, "print")
    tasks = await scheduler.list_tasks()
    assert len(tasks) == 2

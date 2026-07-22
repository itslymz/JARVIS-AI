"""Unit tests for memory systems."""

import pytest
from app.memory.short_term import ShortTermMemory
from app.memory.procedural import ProceduralMemory, Procedure


def test_short_term_memory():
    """Test short-term memory."""
    memory = ShortTermMemory(max_size=5)

    # Add messages
    memory.add_message("user", "Hello")
    memory.add_message("assistant", "Hi there!")

    # Check size
    assert memory.size() == 2

    # Get context
    context = memory.get_context()
    assert len(context) == 2
    assert context[0]["role"] == "user"
    assert context[0]["content"] == "Hello"

    # Clear memory
    memory.clear()
    assert memory.is_empty()


def test_short_term_memory_overflow():
    """Test short-term memory max size."""
    memory = ShortTermMemory(max_size=2)

    # Add more than max
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Response 1")
    memory.add_message("user", "Message 2")

    # Should only have 2 messages
    assert memory.size() == 2
    context = memory.get_context()
    assert context[0]["content"] == "Response 1"
    assert context[1]["content"] == "Message 2"


def test_procedural_memory():
    """Test procedural memory."""
    memory = ProceduralMemory()

    # Store procedure
    steps = [
        {"action": "check_email"},
        {"action": "reply"},
    ]
    procedure = memory.store_procedure(
        name="email_check",
        description="Check and reply to emails",
        steps=steps,
    )

    assert procedure.name == "email_check"
    assert len(procedure.steps) == 2

    # Get procedure
    retrieved = memory.get_procedure("email_check")
    assert retrieved is not None
    assert retrieved.name == "email_check"

    # Record success
    assert memory.record_success("email_check")
    assert procedure.success_count == 1

    # Get success rate
    rate = memory.get_success_rate("email_check")
    assert rate == 1.0

    # Record failure
    assert memory.record_failure("email_check")
    rate = memory.get_success_rate("email_check")
    assert rate == 0.5


def test_list_procedures():
    """Test listing procedures."""
    memory = ProceduralMemory()

    # Add multiple procedures
    memory.store_procedure("proc1", "Procedure 1", [])
    memory.store_procedure("proc2", "Procedure 2", [])

    procedures = memory.list_procedures()
    assert len(procedures) == 2

"""Procedural memory for learned behaviors and routines.

Stores procedures, workflows, and learned patterns.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class Procedure:
    """Represents a learned procedure or workflow."""

    def __init__(
        self,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
        success_count: int = 0,
        failure_count: int = 0,
    ):
        self.name = name
        self.description = description
        self.steps = steps
        self.success_count = success_count
        self.failure_count = failure_count
        self.created_at = datetime.utcnow()
        self.last_used = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
        }


class ProceduralMemory:
    """Procedural memory for learned behaviors.
    
    Stores procedures, workflows, and behavior patterns that JARVIS learns.
    """

    def __init__(self):
        """Initialize procedural memory."""
        self.procedures: Dict[str, Procedure] = {}

    def store_procedure(
        self,
        name: str,
        description: str,
        steps: List[Dict[str, Any]],
    ) -> Procedure:
        """Store a learned procedure.
        
        Args:
            name: Procedure name
            description: Procedure description
            steps: List of procedure steps
            
        Returns:
            Stored Procedure
        """
        procedure = Procedure(name, description, steps)
        self.procedures[name] = procedure
        return procedure

    def get_procedure(self, name: str) -> Optional[Procedure]:
        """Get a procedure by name.
        
        Args:
            name: Procedure name
            
        Returns:
            Procedure or None
        """
        return self.procedures.get(name)

    def list_procedures(self) -> List[Procedure]:
        """List all procedures.
        
        Returns:
            List of procedures
        """
        return list(self.procedures.values())

    def record_success(self, name: str) -> bool:
        """Record successful procedure execution.
        
        Args:
            name: Procedure name
            
        Returns:
            True if recorded
        """
        procedure = self.get_procedure(name)
        if procedure:
            procedure.success_count += 1
            procedure.last_used = datetime.utcnow()
            return True
        return False

    def record_failure(self, name: str) -> bool:
        """Record failed procedure execution.
        
        Args:
            name: Procedure name
            
        Returns:
            True if recorded
        """
        procedure = self.get_procedure(name)
        if procedure:
            procedure.failure_count += 1
            procedure.last_used = datetime.utcnow()
            return True
        return False

    def get_success_rate(self, name: str) -> Optional[float]:
        """Get procedure success rate.
        
        Args:
            name: Procedure name
            
        Returns:
            Success rate (0-1) or None
        """
        procedure = self.get_procedure(name)
        if procedure:
            total = procedure.success_count + procedure.failure_count
            if total > 0:
                return procedure.success_count / total
        return None

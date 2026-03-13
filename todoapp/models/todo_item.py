"""
models/todo_item.py
-------------------
A single to-do item.  Inherits BaseModel and therefore MUST implement
to_dict / from_dict — the ABC enforces this at class-definition time.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from todoapp.models.base import BaseModel


@dataclass
class TodoItem(BaseModel):
    """Represents one task."""

    title: str
    description: str = ""
    done: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TodoItem":
        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            done=data.get("done", False),
            created_at=datetime.fromisoformat(data["created_at"]),
        )

"""
models/todo_list.py
-------------------
A named, ordered collection of TodoItems.
Also inherits BaseModel — demonstrating that the ABC works for
composite models just as well as simple ones.
"""

from __future__ import annotations

import uuid
from typing import Any, Iterator

from todoapp.models.base import BaseModel
from todoapp.models.todo_item import TodoItem


class TodoList(BaseModel):
    """A named list that owns zero-or-more TodoItems."""

    def __init__(self, name: str = "My Tasks", id: str | None = None) -> None:
        self.name = name
        self.id: str = id or str(uuid.uuid4())
        self._items: list[TodoItem] = []

    def add(self, item: TodoItem) -> None:
        self._items.append(item)

    def remove(self, item_id: str) -> bool:
        before = len(self._items)
        self._items = [i for i in self._items if i.id != item_id]
        return len(self._items) < before

    def get(self, item_id: str) -> TodoItem | None:
        return next((i for i in self._items if i.id == item_id), None)

    def __iter__(self) -> Iterator[TodoItem]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "items": [item.to_dict() for item in self._items],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TodoList":
        todo_list = cls(name=data.get("name", "My Tasks"), id=data.get("id"))
        for item_data in data.get("items", []):
            todo_list.add(TodoItem.from_dict(item_data))
        return todo_list

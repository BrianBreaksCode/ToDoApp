"""
repositories/todo_list_repository.py
-------------------------------------
Protocol (structural interface) for TodoList persistence.
Any class that implements these methods satisfies the interface —
no explicit inheritance required.
"""

from __future__ import annotations

from typing import Protocol

from todoapp.models.todo_list import TodoList


class TodoListRepository(Protocol):
    def save(self, todo_list: TodoList) -> None:
        """Insert or update a TodoList and all its items."""
        ...

    def get(self, list_id: str) -> TodoList | None:
        """Return the TodoList with the given id, or None if not found."""
        ...

    def get_all(self) -> list[TodoList]:
        """Return every stored TodoList with its items."""
        ...

    def delete(self, list_id: str) -> bool:
        """Delete a TodoList and its items. Returns True if a row was removed."""
        ...

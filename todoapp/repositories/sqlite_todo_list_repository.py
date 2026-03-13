"""
repositories/sqlite_todo_list_repository.py
--------------------------------------------
SQLite-backed implementation of TodoListRepository.

Schema
------
todo_lists  : id TEXT PK, name TEXT
todo_items  : id TEXT PK, list_id TEXT FK, title TEXT, description TEXT,
              done INTEGER, created_at TEXT
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from todoapp.models.todo_item import TodoItem
from todoapp.models.todo_list import TodoList


_DDL = """
CREATE TABLE IF NOT EXISTS todo_lists (
    id   TEXT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS todo_items (
    id          TEXT PRIMARY KEY,
    list_id     TEXT NOT NULL REFERENCES todo_lists(id) ON DELETE CASCADE,
    title       TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    done        INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);
"""


class SqliteTodoListRepository:
    def __init__(self, db_path: Path | str) -> None:
        self._conn = sqlite3.connect(db_path)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(_DDL)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def save(self, todo_list: TodoList) -> None:
        with self._conn:
            self._conn.execute(
                "INSERT INTO todo_lists (id, name) VALUES (?, ?)"
                " ON CONFLICT(id) DO UPDATE SET name = excluded.name",
                (todo_list.id, todo_list.name),
            )
            # Replace all items for this list in one shot.
            self._conn.execute(
                "DELETE FROM todo_items WHERE list_id = ?", (todo_list.id,)
            )
            self._conn.executemany(
                "INSERT INTO todo_items (id, list_id, title, description, done, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?)",
                [
                    (
                        item.id,
                        todo_list.id,
                        item.title,
                        item.description,
                        int(item.done),
                        item.created_at.isoformat(),
                    )
                    for item in todo_list
                ],
            )

    def get(self, list_id: str) -> TodoList | None:
        row = self._conn.execute(
            "SELECT id, name FROM todo_lists WHERE id = ?", (list_id,)
        ).fetchone()
        if row is None:
            return None
        return self._build_todo_list(row)

    def get_all(self) -> list[TodoList]:
        rows = self._conn.execute(
            "SELECT id, name FROM todo_lists"
        ).fetchall()
        return [self._build_todo_list(row) for row in rows]

    def delete(self, list_id: str) -> bool:
        with self._conn:
            cursor = self._conn.execute(
                "DELETE FROM todo_lists WHERE id = ?", (list_id,)
            )
        return cursor.rowcount > 0

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "SqliteTodoListRepository":
        return self

    def __exit__(self, *_) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_todo_list(self, list_row: tuple) -> TodoList:
        list_id, name = list_row
        todo_list = TodoList(name=name, id=list_id)
        item_rows = self._conn.execute(
            "SELECT id, title, description, done, created_at"
            " FROM todo_items WHERE list_id = ? ORDER BY rowid",
            (list_id,),
        ).fetchall()
        for id_, title, description, done, created_at in item_rows:
            todo_list.add(
                TodoItem(
                    id=id_,
                    title=title,
                    description=description,
                    done=bool(done),
                    created_at=datetime.fromisoformat(created_at),
                )
            )
        return todo_list

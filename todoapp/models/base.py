"""
models/base.py
--------------
Defines the abstract base class for all data models in the app.
"""

from abc import ABC, abstractmethod
from typing import Any, Self


class BaseModel(ABC):
    """Abstract base for every model in this app."""

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of this model."""
        ...

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Reconstruct a model instance from a dict."""
        ...

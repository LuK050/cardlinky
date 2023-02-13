from __future__ import annotations
import enum
from typing import Optional


class Enum(enum.Enum):
    @classmethod
    def from_value(cls, value: str) -> Optional[Enum]:
        value = value.lower()
        for i in cls:
            if i.value.name.lower() == value:
                return i
        return None

from __future__ import annotations
import enum
from typing import Optional


class Enum(enum.Enum):
    @classmethod
    def from_name(cls, name: str) -> Optional[Enum]:
        name = name.upper()
        for i in cls:
            if i.name == name:
                return i
        return None

import enum
from typing import Optional


class StrEnum(enum.StrEnum):
    @classmethod
    def from_name(cls, name: str) -> Optional[str]:
        name = name.upper()
        for i in cls:
            if i == name:
                return i
        return None

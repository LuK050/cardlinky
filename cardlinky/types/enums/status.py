from enum import StrEnum


class Status(StrEnum):
    NEW: str = "NEW"
    PROCESS: str = "PROCESS"
    SUCCESS: str = "SUCCESS"
    FAIL: str = "FAIL"

    @classmethod
    def from_name(cls, name: str):
        for i in Status:
            if i == name:
                return i
        return None




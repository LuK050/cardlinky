from enum import StrEnum


class Status(StrEnum):
    NEW: str = "NEW"
    MODERATING: str = "MODERATING"
    PROCESS: str = "PROCESS"
    UNDERPAID: str = "UNDERPAID"
    SUCCESS: str = "SUCCESS"
    OVERPAID: str = "OVERPAID"
    FAIL: str = "FAIL"
    ERROR: str = "ERROR"
    DECLINED: str = "DECLINED"

    @classmethod
    def from_name(cls, name: str):
        name = name.upper()
        for i in Status:
            if i == name:
                return i
        return None




from cardlinky.types.enums.enum import Enum


class Status(Enum):
    NEW: str = "NEW"
    MODERATING: str = "MODERATING"
    PROCESS: str = "PROCESS"
    UNDERPAID: str = "UNDERPAID"
    SUCCESS: str = "SUCCESS"
    OVERPAID: str = "OVERPAID"
    FAIL: str = "FAIL"
    ERROR: str = "ERROR"
    DECLINED: str = "DECLINED"

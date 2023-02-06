from enum import StrEnum


class BillType(StrEnum):
    """
    Type of payment link shows how many payments it could receive.
    'normal' type means that only one successful payment could be received for this link.
    'multi' type means that many payments could be received with one link.
    """
    NORMAL: str = "NORMAL"
    MULTI: str = "MULTI"

    @classmethod
    def from_name(cls, name: str):
        for i in BillType:
            if i == name:
                return i
        return None




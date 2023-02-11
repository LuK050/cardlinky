from enum import StrEnum


class AccountType(StrEnum):
    CREDIT_CARD: str = "CREDIT_CARD"

    @classmethod
    def from_name(cls, name: str):
        name = name.upper()
        for i in AccountType:
            if i == name:
                return i
        return None




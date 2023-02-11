from enum import StrEnum


class AccountType(StrEnum):
    CREDIT_CARD: str = "credit_card"

    @classmethod
    def from_name(cls, name: str):
        name = name.upper()
        for i in AccountType:
            if i == name:
                return i
        return None




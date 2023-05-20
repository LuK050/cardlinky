from pydantic import BaseModel

from cardlinky.types.enums.currency import Currency


class Balance(BaseModel):
    """
    :param currency: Currency - Currency of balance
    :param balance_available: float - Available balance
    :param balance_locked: float - Locked balance for payout
    :param balance_hold: float - Fees
    """

    currency: Currency
    balance_available: float
    balance_locked: float
    balance_hold: float

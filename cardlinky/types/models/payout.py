import datetime
from dataclasses import dataclass

from cardlinky.types.enums.status import Status
from cardlinky.types.enums.currency import Currency


@dataclass
class Payout:
    """
    :param id: str - Unique ID of payout
    :param status: enums.Status - Payout status
    :param amount: float - Payout amount
    :param commission: float - Fees
    :param account_identifier: str - Account to which money will be sent
    :param currency: enums.Currency - Currency
    :param created_at: datetime.datetime - Date and time
    """

    id: str
    status: Status
    amount: float
    commission: float
    account_identifier: str
    currency: Currency
    created_at: datetime.datetime


@dataclass
class PayoutStatus:
    """
    :param id: str - Unique ID of payout
    :param status: enums.Status - Payout status
    :param amount: float - Payout amount
    :param commission: float - Fees
    :param account_identifier: str - Account to which money will be sent
    :param currency: enums.Currency - Currency
    :param created_at: datetime.datetime - Date and time
    :param success: bool - Payout status
    """

    id: str
    status: Status
    amount: float
    commission: float
    account_identifier: str
    currency: Currency
    created_at: datetime.datetime
    success: bool


import datetime
from typing import Optional
from pydantic import BaseModel

from cardlinky.types.enums.status import Status
from cardlinky.types.enums.currency import Currency


class Payment(BaseModel):
    """
    :param id: str - Unique payment ID
    :param bill_id: str - Unique bill ID
    :param status: enums.Status - Status of payment
    :param amount: float - Total payment amount
    :param commission: float - Total payment commission
    :param currency_in: enums.Currency - Payment currency
    :param account_amount: float - Total account amount
    :param account_currency_code: enums.Currency - Account currency
    :param from_card: str - Payer's card
    :param created_at: datetime.datetime - Creation date and time
    :param error_code: Optional[int] - Error code
    :param error_message: Optional[str] - Error message
    """

    id: str
    bill_id: str
    status: Status
    amount: float
    commission: float
    currency_in: Currency
    account_amount: float
    account_currency_code: Currency
    from_card: str
    created_at: datetime.datetime
    error_code: Optional[int] = None
    error_message: Optional[str] = None


class PaymentStatus(BaseModel):
    """
    :param id: str - Unique payment ID
    :param bill_id: str - Unique bill ID
    :param status: enums.Status - Status of payment
    :param amount: float - Bill amount
    :param commission: float - Commission amount
    :param currency_in: enums.Currency - Payment currency
    :param account_amount: float - Total account amount
    :param account_currency_code: enums.Currency - Account currency
    :param from_card: str - Payer's card number
    :param created_at: datetime.datetime - Creation date and time
    :param created_at: datetime.datetime - Creation date and time
    :param success: bool - Payment status
    """

    id: str
    bill_id: str
    status: Status
    amount: float
    commission: float
    currency_in: Currency
    account_amount: float
    account_currency_code: Currency
    from_card: str
    created_at: datetime.datetime
    success: bool

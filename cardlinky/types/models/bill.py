import datetime
from dataclasses import dataclass

from cardlinky.types.enums.status import Status
from cardlinky.types.enums.currency import Currency
from cardlinky.types.enums.bill_type import BillType


@dataclass
class Bill:
    """
    :param id: str - Unique bill id
    :param status: Status - Bill status
    :param active: boll - Is bill active
    :param amount: float - Bill amount
    :param type: BillType - Bill type. 'Normal' type accepts only one payment. 'Multi' type accepts unlimited number of payments.
    :param currency_in: Currency - Payment currency
    :param created_at: datetime.datetime - Creation date and time
    """

    id: str
    status: Status
    active: bool
    amount: float
    type: BillType
    currency_in: Currency
    created_at: datetime.datetime


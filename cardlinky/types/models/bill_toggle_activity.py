import datetime
from dataclasses import dataclass

from cardlinky.types.enums.status import Status
from cardlinky.types.enums.currency import Currency
from cardlinky.types.enums.bill_type import BillType

@dataclass
class BillToggleActivity:
    """
    :param id: str - Unique bill id
    :param active: bool - Bill activity flag
    :param status: Status - Bill status
    :param amount: float - Bill amount
    :param type: BillType - Type of bill. NORMAL is for onetime payments and MULTI is for infinity number of payments
    :param created_at: datetime.datetime - Bill creation date and time
    :param currency_in: Currency - Currency
    :param success: bool - This flag indicates status of request
    """

    id: str
    active: bool
    status: Status
    amount: float
    type: BillType
    created_at: datetime.datetime
    currency_in: Currency
    success: bool


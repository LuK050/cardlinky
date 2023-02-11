import datetime
from dataclasses import dataclass

from cardlinky.types.enums.status import Status
from cardlinky.types.enums.currency import Currency
from cardlinky.types.enums.bill_type import BillType


@dataclass
class Bill:
    """
    :param id: str - Unique bill id
    :param status: enums.Status - Bill status
    :param active: boll - Is bill active
    :param amount: float - Bill amount
    :param type: enums.BillType - Bill type. 'Normal' type accepts only one payment. 'Multi' type accepts unlimited number of payments.
    :param currency_in: enums.Currency - Payment currency
    :param created_at: datetime.datetime - Creation date and time
    """

    id: str
    status: Status
    active: bool
    amount: float
    type: BillType
    currency_in: Currency
    created_at: datetime.datetime


@dataclass
class BillCreate:
    """
    :param success: bool - Payment status
    :param link_url: str - Link to the page with QR-code. Example: https://cardlink.link/link/5QWlqB2kKJ
    :param link_page_url: str - Link to the payment page. Example: https://cardlink.link/transfer/5QWlqB2kKJ
    :param bill_id: str - Unique bill ID
    """

    success: bool
    link_url: str
    link_page_url: str
    bill_id: str


@dataclass
class BillStatus:
    """
    :param id: str - Unique bill id
    :param status: enums.Status - Bill status
    :param active: boll - Is bill active
    :param amount: float - Bill amount
    :param type: enums.BillType - Bill type. 'Normal' type accepts only one payment. 'Multi' type accepts unlimited number of payments
    :param currency_in: enums.Currency - Payment currency
    :param created_at: datetime.datetime - Creation date and time
    :param created_at: datetime.datetime - Creation date and time
    :param success: bool - Payment status
    """

    id: str
    status: Status
    active: bool
    amount: float
    type: BillType
    currency_in: Currency
    created_at: datetime.datetime
    success: bool


@dataclass
class BillToggleActivity:
    """
    :param id: str - Unique bill id
    :param active: bool - Bill activity flag
    :param status: enums.Status - Bill status
    :param amount: float - Bill amount
    :param type: enums.BillType - Type of bill. NORMAL is for onetime payments and MULTI is for infinity number of payments
    :param created_at: datetime.datetime - Bill creation date and time
    :param currency_in: enums.Currency - Currency
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

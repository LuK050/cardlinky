from dataclasses import dataclass


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


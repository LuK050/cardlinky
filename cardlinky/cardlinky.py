import datetime
import requests
from typing import Optional, MutableMapping, Mapping, Union, Any, List

from cardlinky.types.exceptions import *
from cardlinky.types.models.bill import Bill
from cardlinky.types.models.payment import Payment
from cardlinky.types.models.bill_status import BillStatus
from cardlinky.types.models.bill_create import BillCreate
from cardlinky.types.models.bill_toggle_activity import BillToggleActivity
from cardlinky.types.enums.status import Status
from cardlinky.types.enums.bill_type import BillType
from cardlinky.types.enums.currency import Currency


_BASE_URL: str = "https://cardlink.link/api/v1/"


class Cardlinky:
    """
    To get started, you need to create a store and get an API token on https://cardlink.link/

    :param token: str - Your API token
    :param base_url: Optional[str] - Custom base url. Default: https://cardlink.link/api/v1/
    """

    def __init__(self, token: str, base_url: Optional[str] = None):
        self.token: str = token
        self.base_url: str = base_url if base_url is not None else _BASE_URL
        self.headers: Mapping = {
            "Authorization": f"Bearer {self.token}"
        }

    def _get(self, path: str, data: MutableMapping[str, Union[str, int, bool]]) -> MutableMapping[str, Any]:
        response = requests.get(
            url=self.base_url + path,
            headers=self.headers,
            json=data,
        )
        json = response.json()

        if not json["success"]:
            if "errors" in tuple(json.keys()):
                error = tuple(json["errors"].values())[0][0]

                if error in tuple(exceptions.keys()):
                    raise exceptions[tuple(json["errors"].values())[0][0]]
                raise ValueError(error)
            else:
                raise exceptions[json["message"]]

        return json

    def _post(self, path: str, data: MutableMapping[str, Union[str, int, bool]]) -> MutableMapping[str, Any]:
        response = requests.post(
            url=self.base_url + path,
            headers=self.headers,
            json=data,
        )
        json = response.json()

        if not json["success"]:
            if "errors" in tuple(json.keys()):
                error = tuple(json["errors"].values())[0][0]

                if error in tuple(exceptions.keys()):
                    raise exceptions[tuple(json["errors"].values())[0][0]]
                raise ValueError(error)
            else:
                raise exceptions[json["message"]]

        return json

    def create_bill(self, amount: float, shop_id: str, order_id: Optional[str] = None,
                    description: Optional[str] = None, type: Optional[BillType] = None,
                    currency_in: Optional[Currency] = None, custom: Optional[str] = None,
                    name: Optional[str] = None) -> BillCreate:
        """
        How to create a bill.
        https://cardlink.link/en/reference/api#bill-create

        :param amount: float - Payment amount
        :param shop_id: str - Unique shop ID
        :param order_id: Optional[str] - Unique order ID. Will be sent within Postback
        :param description: Optional[str] - Description of payment
        :param type: Optional[BillType] - Type of payment link shows how many payments it could receive
        :param currency_in: Optional[Currency] - Currency that customer sees during payment process
        :param custom: str - You can send any string value in this field and it will be returned within postback
        :param name: str - Please specify the purpose of the payment. It will be shown on the payment form
        :return: models.BillCreate
        """

        response = self._post("bill/create", {
            "amount": amount,
            "order_id": order_id,
            "description": description,
            "shop_id": shop_id,
            "custom": custom,
            "name": name,
        } | ({"type": type.value} if type is not None else {})
          | ({"type": currency_in.value} if currency_in is not None else {}))

        return BillCreate(**response)

    def toggle_bill_activity(self, id: str, active: bool) -> BillToggleActivity:
        """
        You can deactivate and activate bills using this APO.
        Use your merchant token for the authentication.
        https://cardlink.link/en/reference/api#bill-toggle

        :param id: str - Unique bill id
        :param active: bool - Deactivate or activate bill
        :return: models.BillToggleActivity
        """

        response = self._post("bill/toggle_activity", {
            "id": id,
            "active": int(active),
        })
        response["status"] = Status.from_name(response["status"])
        response["type"] = BillType.from_name(response["type"])
        response["created_at"] = datetime.datetime.strptime(response["created_at"], "%Y-%m-%d %H:%M:%S")
        response["currency_in"] = Currency.from_name(response["currency_in"])

        return BillToggleActivity(**response)

    def get_bill_payments(self, id: str) -> List[Payment]:
        """
        Get information about payments for one bill.
        https://cardlink.link/en/reference/api#bill-payments

        :param id: str - Unique bill id
        :return: List[Payment]
        """

        response = self._get("bill/payments", {
            "id": id,
        })

        for i, payment in enumerate(response["data"]):
            payment["status"] = Status.from_name(payment["status"])
            payment["created_at"] = datetime.datetime.strptime(payment["created_at"], "%Y-%m-%d %H:%M:%S")
            payment["currency_in"] = Currency.from_name(payment["currency_in"])
            payment["account_currency_code"] = Currency.from_name(payment["account_currency_code"])
            response["data"][i] = Payment(**payment)

        return response["data"]

    def search_bill(self, shop_id: str, start_date: Optional[datetime.datetime] = None,
                    finish_date: Optional[datetime.datetime] = None) -> List[Bill]:
        """
        Search by bills.
        https://cardlink.link/en/reference/api#bill-search

        :param shop_id: str - Unique shop ID
        :param start_date: Optional[datetime.datetime] - Start date
        :param finish_date: Optional[datetime.datetime] - End date
        :return: List[Payment]
        """

        response = self._get("bill/search", {
            "shop_id": shop_id,
        } | ({"start_date": start_date.strftime("%Y-%m-%d")} if start_date is not None else {})
          | ({"finish_date": finish_date.strftime("%Y-%m-%d")} if finish_date is not None else {}))

        for i, bill in enumerate(response["data"]):
            bill["status"] = Status.from_name(bill["status"])
            bill["type"] = BillType.from_name(bill["type"])
            bill["created_at"] = datetime.datetime.strptime(bill["created_at"], "%Y-%m-%d %H:%M:%S")
            bill["currency_in"] = Currency.from_name(bill["currency_in"])
            response["data"][i] = Bill(**bill)

        return response["data"]

    def get_bill_status(self, id: str) -> BillStatus:
        """
        Get bill info and status.
        https://cardlink.link/en/reference/api#bill-status

        :param id: str - Unique bill ID
        :return: models.BillStatus
        """

        response = self._get("bill/status", {
            "id": id,
        })
        response["status"] = Status.from_name(response["status"])
        response["type"] = BillType.from_name(response["type"])
        response["created_at"] = datetime.datetime.strptime(response["created_at"], "%Y-%m-%d %H:%M:%S")
        response["currency_in"] = Currency.from_name(response["currency_in"])

        return BillStatus(**response)

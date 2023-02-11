import datetime
import requests
from typing import Optional, MutableMapping, Mapping, Union, Any, List

from cardlinky.types.exceptions import exceptions
from cardlinky.types.models.balance import Balance
from cardlinky.types.models.payout import Payout, PayoutStatus
from cardlinky.types.models.payment import Payment, PaymentStatus
from cardlinky.types.models.bill import Bill, BillCreate, BillStatus, BillToggleActivity
from cardlinky.types.enums.status import Status
from cardlinky.types.enums.currency import Currency
from cardlinky.types.enums.bill_type import BillType
from cardlinky.types.enums.account_type import AccountType


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

    @staticmethod
    def __handle_error(json: Mapping[str, Any]) -> None:
        if not json["success"]:
            if "errors" in tuple(json.keys()):
                error = tuple(json["errors"].values())[0][0]

                if error in tuple(exceptions.keys()):
                    raise exceptions[tuple(json["errors"].values())[0][0]]
                raise ValueError(error)
            else:
                error = json["message"]

                if json["message"] in tuple(exceptions.keys()):
                    raise exceptions[json["message"]]
                raise ValueError(error)

    def _get(self, path: str, data: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        response = requests.get(
            url=self.base_url + path,
            headers=self.headers,
            json=data,
        )
        json = response.json()
        self.__handle_error(json)

        return json

    def _post(self, path: str, data: MutableMapping[str, Union[str, int, bool]]) -> MutableMapping[str, Any]:
        response = requests.post(
            url=self.base_url + path,
            headers=self.headers,
            json=data,
        )
        json = response.json()
        self.__handle_error(json)

        return json

    def create_bill(self, amount: float, shop_id: str, order_id: Optional[str] = None,
                    description: Optional[str] = None, bill_type: Optional[BillType] = None,
                    currency_in: Optional[Currency] = None, custom: Optional[str] = None,
                    name: Optional[str] = None) -> BillCreate:
        """
        How to create a bill.
        https://cardlink.link/en/reference/api#bill-create

        :param amount: float - Payment amount
        :param shop_id: str - Unique shop ID
        :param order_id: Optional[str] - Unique order ID. Will be sent within Postback
        :param description: Optional[str] - Description of payment
        :param bill_type: Optional[enums.BillType] - Type of payment link shows how many payments it could receive
        :param currency_in: Optional[enums.Currency] - Currency that customer sees during payment process
        :param custom: str - You can send any string value in this field, and it will be returned within postback
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
        } | ({"type": bill_type.name} if bill_type is not None else {})
                              | ({"currency_in": currency_in.name} if currency_in is not None else {}))

        return BillCreate(**response)

    def toggle_bill_activity(self, bill_id: str, active: bool) -> BillToggleActivity:
        """
        You can deactivate and activate bills using this APO.
        Use your merchant token for the authentication.
        https://cardlink.link/en/reference/api#bill-toggle

        :param bill_id: str - Unique bill id
        :param active: bool - Deactivate or activate bill
        :return: models.BillToggleActivity
        """

        response = self._post("bill/toggle_activity", {
            "id": bill_id,
            "active": int(active),
        })
        response["status"] = Status.from_name(response["status"])
        response["type"] = BillType.from_name(response["type"])
        response["created_at"] = datetime.datetime.strptime(response["created_at"], "%Y-%m-%d %H:%M:%S")
        response["currency_in"] = Currency.from_name(response["currency_in"])

        return BillToggleActivity(**response)

    def get_bill_payments(self, bill_id: str) -> List[Payment]:
        """
        Get information about payments for one bill.
        https://cardlink.link/en/reference/api#bill-payments

        :param bill_id: str - Unique bill id
        :return: List[models.Payment]
        """

        response = self._get("bill/payments", {
            "id": bill_id,
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
        :return: List[models.Bill]
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

    def get_bill_status(self, bill_id: str) -> BillStatus:
        """
        Get bill info and status.
        https://cardlink.link/en/reference/api#bill-status

        :param bill_id: str - Unique bill ID
        :return: models.BillStatus
        """

        response = self._get("bill/status", {
            "id": bill_id,
        })
        response["status"] = Status.from_name(response["status"])
        response["type"] = BillType.from_name(response["type"])
        response["created_at"] = datetime.datetime.strptime(response["created_at"], "%Y-%m-%d %H:%M:%S")
        response["currency_in"] = Currency.from_name(response["currency_in"])

        return BillStatus(**response)

    def search_payment(self, shop_id: str, start_date: Optional[datetime.datetime] = None,
                       finish_date: Optional[datetime.datetime] = None) -> List[Payment]:
        """
        Search payment.
        https://cardlink.link/en/reference/api#payment-search

        :param shop_id: str - Unique shop ID
        :param start_date: Optional[datetime.datetime] - Start date
        :param finish_date: Optional[datetime.datetime] - End date
        :return: List[models.Payment]
        """

        response = self._get("payment/search", {
            "shop_id": shop_id,
        } | ({"start_date": start_date.strftime("%Y-%m-%d")} if start_date is not None else {})
                             | ({"finish_date": finish_date.strftime("%Y-%m-%d")} if finish_date is not None else {}))

        for i, payment in enumerate(response["data"]):
            payment["status"] = Status.from_name(payment["status"])
            payment["created_at"] = datetime.datetime.strptime(payment["created_at"], "%Y-%m-%d %H:%M:%S")
            payment["currency_in"] = Currency.from_name(payment["currency_in"])
            payment["account_currency_code"] = Currency.from_name(payment["account_currency_code"])
            response["data"][i] = Payment(**payment)

        return response["data"]

    def get_payment_status(self, payment_id: str) -> PaymentStatus:
        """
        Get status of payment.
        https://cardlink.link/en/reference/api#payment-status

        :param payment_id: str - Unique payment ID
        :return: models.PaymentStatus
        """

        response = self._get("payment/status", {
            "id": payment_id,
        })
        response["status"] = Status.from_name(response["status"])
        response["created_at"] = datetime.datetime.strptime(response["created_at"], "%Y-%m-%d %H:%M:%S")
        response["currency_in"] = Currency.from_name(response["currency_in"])

        return PaymentStatus(**response)

    def get_balance(self) -> List[Balance]:
        """
        You can request information about your current balance state using this API.
        Use your merchant token for the authentication.
        https://cardlink.link/en/reference/api#merchant-balance

        :return: List[models.Balance]
        """

        response = self._get("merchant/balance", {})

        for i, balance in enumerate(response["balances"]):
            balance["currency"] = Currency.from_name(balance["currency"])
            response["balances"][i] = Balance(**balance)

        return response["balances"]

    def create_personal_payout(self, amount: float, payout_account_id: str) -> List[Payout]:
        """
        In order to withdraw money you need to create a payout.
        The amount of payout can be split depending on payout account type.
        In this case you will get a list with payouts.
        https://cardlink.link/en/reference/api#personal-payout-create

        :param amount: float - Payout amount
        :param payout_account_id: str - Unique ID of payout account. Money will be sent to this account
        :return: List[Payout]
        """

        response = self._post("payout/personal/create", {
            "amount": amount,
            "payout_account_id": payout_account_id,
        })

        for i, payout in enumerate(response["data"]):
            payout["payout"] = Status.from_name(payout["payout"])
            payout["currency"] = Currency.from_name(payout["currency"])
            payout["created_at"] = datetime.datetime.strptime(payout["created_at"], "%Y-%m-%d %H:%M:%S")
            response["balances"][i] = Balance(**payout)

        return response["data"]

    def create_regular_payout(self, amount: float, currency: Currency, account_type: AccountType,
                              account_identifier: str, card_holder: str) -> List[Payout]:
        """
        Attention: You need to request access to this API method from Support Team.
        Payout to cards using your account balance.
        Your request can be split if amount is too large. In this case you will see a list of payouts.
        https://cardlink.link/en/reference/api#regular-payout-create

        :param amount: float - Payout amount
        :param currency: models.Currency - Currency
        :param account_type: models.AccountType - Account type for payout
        :param account_identifier: str - Account ID
        :param card_holder: str - Cardholder name. Only for account_type=models.AccountType.CREDIT_CARD.
        :return: List[Payout]
        """

        response = self._post("payout/regular/create", {
            "amount": amount,
            "currency": currency.name,
            "account_type": account_type.name,
            "account_identifier": account_identifier,
            "card_holder": card_holder,
        })

        for i, payout in enumerate(response["data"]):
            payout["payout"] = Status.from_name(payout["payout"])
            payout["currency"] = Currency.from_name(payout["currency"])
            payout["created_at"] = datetime.datetime.strptime(payout["created_at"], "%Y-%m-%d %H:%M:%S")
            response["balances"][i] = Balance(**payout)

        return response["data"]

    def search_payout(self, start_date: Optional[datetime.datetime] = None,
                      finish_date: Optional[datetime.datetime] = None) -> List[Payout]:
        """
        You can request all your payouts using this method.
        https://cardlink.link/en/reference/api#payout-search

        :param start_date: Optional[datetime.datetime] - Start date for search
        :param finish_date: Optional[datetime.datetime] - End date for search
        :return: List[models.Payout]
        """

        response = self._get("payout/search", {}
                             | ({"start_date": start_date.strftime("%Y-%m-%d")} if start_date is not None else {})
                             | ({"finish_date": finish_date.strftime("%Y-%m-%d")} if finish_date is not None else {}))

        for i, payout in enumerate(response["data"]):
            payout["payout"] = Status.from_name(payout["payout"])
            payout["currency"] = Currency.from_name(payout["currency"])
            payout["created_at"] = datetime.datetime.strptime(payout["created_at"], "%Y-%m-%d %H:%M:%S")
            response["balances"][i] = Balance(**payout)

        return response["data"]

    def get_payout_status(self, payout_id: str) -> PayoutStatus:
        """
        You can request a status of any payout operation.
        https://cardlink.link/en/reference/api#payout-status

        :param payout_id: str - Unique payout ID
        :return: PayoutStatus
        """

        response = self._get("payout/status", {
            "id": payout_id,
        })
        response["status"] = Status.from_name(response["status"])
        response["currency"] = Currency.from_name(response["currency_in"])
        response["created_at"] = datetime.datetime.strptime(response["created_at"], "%Y-%m-%d %H:%M:%S")

        return PayoutStatus(**response)

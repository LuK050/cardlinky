class Unauthenticated(Exception):
    ...


class MerchantNotFound(Exception):
    ...


class InvalidAmount(Exception):
    ...


class MerchantBanned(Exception):
    ...


class ShopNotFound(Exception):
    ...


class ShopNotEnabled(Exception):
    ...


class AccessDenied(Exception):
    ...


class NoPayout(Exception):
    ...


class GeneralError(Exception):
    ...


class BillNotFound(Exception):
    ...


class MerchantSubscriptionInactive(Exception):
    ...


class MerchantSubscriptionNotFound(Exception):
    ...


class BillIsFinished(Exception):
    ...


class TooManyPayments(Exception):
    ...


class TooManyBills(Exception):
    ...


exceptions = {
    "Unauthenticated": Unauthenticated("Invalid API Token"),
    "api:error.merchant_not_found": MerchantNotFound("Merchant is not found in the System"),
    "api:error.invalid_amount": InvalidAmount("Invalid amount"),
    "api:error.merchant_banned": MerchantBanned("Merchant is blocked"),
    "api:error.shop_not_found": ShopNotFound("Shop is not found in the System"),
    "api:error.shop_not_enabled": ShopNotEnabled("Merchant is deactivated"),
    "api:error.access_denied": AccessDenied("Merchant doesn't have access to the shop"),
    "api:error.no_payout": NoPayout("Can't payout in the given currency"),
    "api:error.general_error": GeneralError("Internal error"),
    "api:error.bill_not_found": BillNotFound("Bill doesn't exist"),
    "api:error.merchant_subscription_inactive": MerchantSubscriptionInactive("Subscription is not active"),
    "api:error.merchant_subscription_not_found": MerchantSubscriptionNotFound("Merchant doesn't have a subscription"),
    "api:error.bill_is_finished": BillIsFinished("Bill is paid in case of NORMAL bill"),
    "api:error.too_many_payments": TooManyPayments("You are trying to get too many payments in one request."),
    "api:error.too_many_bills": TooManyBills("You are trying to request too many bills at once."),
}






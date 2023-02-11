# cardlinky
<a href="https://pypi.org/project/cardlinky/"><img src="https://img.shields.io/pypi/v/cardlinky?style=flat-square"></a> <img src="https://img.shields.io/pypi/pyversions/cardlinky?style=flat-square"> 

📘 [Official documentation](https://cardlink.link/reference/api)

## Usage
First of all, you need to create a store in the system https://cardlink.link/. After confirmation, you will be able to get a token and a shop ID to work with the API.

### Creating a bill and getting a payment link:
```py
from cardlinky import Cardlinky


def print_bill_url(token: str, shop_id: str, amount: float) -> None:
    # Creating an instance of the class
    cardlinky = Cardlinky(token)

    # Create a bill and save it
    bill = cardlinky.create_bill(amount=amount, shop_id=shop_id)

    # Getting a payment link and printing
    print(bill.link_url)


print_bill_url("YOUR-TOKEN", "YOUR-SHOP-ID", 100.0)
# https://cardlink.link/link/GkLWvKx3
```

### Getting a bill status:
```py
from cardlinky import Cardlinky


def print_bill_status(token: str, id: str) -> None:
    # Creating an instance of the class
    cardlinky = Cardlinky(token)

    # Create a bill and save it
    bill_status = cardlinky.get_bill_status(id=id)

    # Getting a status and printing
    print(bill_status.status)


print_bill_status("YOUR-TOKEN", "BILL-ID")
# NEW
```

## Installation
```sh
pip install cardlinky
```
### Dependencies:
Package  | Version
-------- | ----------
`requests` | `>=2.28.2` 


# GrizzlySMS - Python Library

GrizzlySMS is a simple and powerful Python library to interact with the GrizzlySMS API. Easily rent phone numbers, check prices, manage your balance, and handle errors using API-KEY.

## Features

- Rent Status Check
- Get Phone Numbers
- Price Lookup by Country & Service
- Account Balance Check
- Error Handling

## Installation

Install with `pip`:

```bash
pip install GrizzlySMS
```

## Usage

```python
from GrizzlySMS import GrizzlySMS

# Initialize
api_key = "KEY-aPi"
grizzly = GrizzlySMS(api_key)

# Get Rent Status
rent_status = grizzly.get_rent_status("your_rent_id")
print(rent_status)

# Get Rent Prices
prices = grizzly.get_rent_prices("select-service-plug", "US", 240)
print(prices)
```

## License

MIT License APPROVED ✅.

## PyPi

Available on PyPi:

```bash
pip install GrizzlySMS
```

---

Made with ❤️ by [d9c](https://pypi.com/d9c)

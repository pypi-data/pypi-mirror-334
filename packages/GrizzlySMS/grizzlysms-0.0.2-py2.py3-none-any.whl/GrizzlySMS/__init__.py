"""
from GrizzlySMS-API import GrizzlySMS
api_key = "YOUR_API_KEY"
grizzly = GrizzlySMS(api_key)
rent_id = "your_rent_id"
try:
    rent_status = grizzly.get_rent_status(rent_id)
    print("Rent Status:", rent_status)
except APIError as e:
    print(f"API Error: {e}")
service = "select-service-plug"
country = "US"
time = 240
try:
    rent_prices = grizzly.get_rent_prices(service, country, time)
    print("Rent Prices:", rent_prices)
except APIError as e:
    print(f"API Error: {e}")
try:
    number_data = grizzly.get_number(service, country)
    print("Number Data:", number_data)
except APIError as e:
    print(f"API Error: {e}")
try:
    balance_data = grizzly.get_balance()
    print("Balance:", balance_data)
except APIError as e:
    print(f"API Error: {e}")
try:
    rent_status_by_id = grizzly.get_rent_status_by_id(rent_id)
    print("Rent Status by ID:", rent_status_by_id)
except APIError as e:
    print(f"API Error: {e}")
try:
    rent_prices_by_country = grizzly.get_rent_prices_by_country(service, country, time)
    print("Rent Prices by Country:", rent_prices_by_country)
except APIError as e:
    print(f"API Error: {e}")
[[[ Example Of Use ]]]
"""

from .grizzly import GrizzlySMS

__version__ = '0.0.2'
user_ ='ILY'
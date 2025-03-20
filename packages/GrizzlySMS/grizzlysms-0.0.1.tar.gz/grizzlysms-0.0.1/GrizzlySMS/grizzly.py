import requests
import json
from .errors import APIError, BadKeyError, NoIdRentError, InvalidPhoneError, ServerError, InvalidTimeError, BadCountryError, BadServiceError, NoNumbersError

class GrizzlySMS:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.grizzlysms.com/stubs/handler_api.php"

    def get_rent_status(self, rent_id):
        params = {
            'api_key': self.api_key,
            'action': 'getRentStatus',
            'id': rent_id#https://GrizzlySMS.com/Rent or SMTH idk.
        }
        response = requests.get(self.base_url, params=params)
        return self._handle_response(response)

    def get_rent_prices(self, service, country, time):
        params = {
            'api_key': self.api_key,
            'action': 'getRentPrices',
            'service': service,
            'country': country,
            'rent_time': time
        }
        response = requests.get(self.base_url, params=params)
        return self._handle_response(response)

    def get_number(self, service, country):
        params = {
            'api_key': self.api_key,
            'action': 'getNumber',
            'service': service,
            'country': country
        }
        response = requests.get(self.base_url, params=params)
        return self._handle_response(response)

    def get_balance(self):
        params = {
            'api_key': self.api_key,
            'action': 'getBalance'
        }
        response = requests.get(self.base_url, params=params)
        return self._handle_response(response)

    def get_rent_status_by_id(self, rent_id):
        params = {
            'api_key': self.api_key,
            'action': 'getRentStatus',
            'id': rent_id
        }
        response = requests.get(self.base_url, params=params)
        return self._handle_response(response)

    def get_rent_prices_by_country(self, service, country, time):
        params = {
            'api_key': self.api_key,
            'action': 'getRentPrices',
            'service': service,
            'country': country,
            'rent_time': time
        }
        response = requests.get(self.base_url, params=params)
        return self._handle_response(response)

    def _handle_response(self, response):
        try:
            data = response.json()
            
            if data.get("status") == "error":
                self._handle_error(data)
            
            return data
        except json.JSONDecodeError:
            print(f"Response text: {response.text}")
            return {"error": "Response is not in JSON format"}
        except Exception as e:
            print(f"Error: {e}")
            return {"error": str(e)}

    def _handle_error(self, data):
        error_code = data.get("error", "")
        if error_code == "BAD_KEY":
            raise BadKeyError()
        elif error_code == "NO_ID_RENT":
            raise NoIdRentError()
        elif error_code == "INVALID_PHONE":
            raise InvalidPhoneError()
        elif error_code == "SERVER_ERROR":
            raise ServerError()
        elif error_code == "INVALID_TIME":
            raise InvalidTimeError()
        elif error_code == "BAD_COUNTRY":
            raise BadCountryError()
        elif error_code == "BAD_SERVICE":
            raise BadServiceError()
        elif error_code == "NO_NUMBERS":
            raise NoNumbersError()
        else:
            raise APIError("Unknown error occurred.")
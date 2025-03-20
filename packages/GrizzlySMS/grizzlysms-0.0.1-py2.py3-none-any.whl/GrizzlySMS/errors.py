class APIError(Exception):
    def __init__(self, message="An error occurred with the API"):
        self.message = message
        super().__init__(self.message)

class BadKeyError(APIError):
    def __init__(self, message="Bad API Key. Please check your key."):
        self.message = message
        super().__init__(self.message)

class NoIdRentError(APIError):
    def __init__(self, message="No ID Rent. Please check your rent ID."):
        self.message = message
        super().__init__(self.message)

class InvalidPhoneError(APIError):
    def __init__(self, message="Invalid Phone ID Rent."):
        self.message = message
        super().__init__(self.message)

class ServerError(APIError):
    def __init__(self, message="Server error. Please try again later."):
        self.message = message
        super().__init__(self.message)

class InvalidTimeError(APIError):
    def __init__(self, message="Invalid rental time. Please check the time parameter."):
        self.message = message
        super().__init__(self.message)

class BadCountryError(APIError):
    def __init__(self, message="Bad country code. Please check the country code."):
        self.message = message
        super().__init__(self.message)

class BadServiceError(APIError):
    def __init__(self, message="Bad service code. Please check the service code."):
        self.message = message
        super().__init__(self.message)

class NoNumbersError(APIError):
    def __init__(self, message="No Nums available. Try again later."):
        self.message = message
        super().__init__(self.message)
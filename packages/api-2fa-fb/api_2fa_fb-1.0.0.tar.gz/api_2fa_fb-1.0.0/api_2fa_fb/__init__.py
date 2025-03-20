import requests

# API URL to fetch OTP
api = r"https://2fa.fb.rip/api/otp/"

class authy:
    """Class for handling two-factor authentication (2FA) by retrieving OTP from an API."""

    def __init__(self, code):
        """
        Initialize the Authy object with a secret code.

        :param code: The secret code used to retrieve the OTP.
        """
        self.code = code
        self.url = api
        self.__fetch__()  # Automatically fetch OTP data upon initialization

    def __fetch__(self):
        """Send a request to the API and store the response as JSON."""
        self.response = requests.get(self.url + self.code).json()

    def get_otp(self):
        """Extract and return the OTP from the API response."""
        return self.response['data']['otp']

    def get_exist(self):
        """Retrieve the remaining time for the OTP before expiration."""
        return self.response['data']['timeRemaining']
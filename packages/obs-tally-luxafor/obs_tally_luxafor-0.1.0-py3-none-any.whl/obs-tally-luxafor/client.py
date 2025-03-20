import requests
from urllib.parse import urljoin

class LuxaforClient:
    def __init__(self, base_url: str, secret_token: str, timeout: int = 5):
        """
        Initialize the Luxafor API client.

        Args:
            base_url (str): The base URL of the API (e.g., "http://127.0.0.1:5383").
            secret_token (str): The secret token used for authorization.
            timeout (int): Request timeout in seconds.
        """
        self.base_url = base_url.rstrip('/')
        self.secret_token = secret_token
        self.timeout = timeout
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.secret_token}"
        }

    def _post(self, endpoint: str, payload: dict) -> bool:
        """
        Send a POST request to the specified endpoint with a JSON payload.

        Args:
            endpoint (str): The API endpoint (e.g., "/brightness").
            payload (dict): The JSON payload to send.

        Returns:
            bool: True if the request was successful (HTTP 200), otherwise False.
        """
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                return True
            else:
                print(f"Error: {endpoint} responded with {response.status_code} - {response.text}")
                return False
        except requests.RequestException as e:
            print(f"Request to {url} failed: {e}")
            return False

    def change_color(self, color: str) -> bool:
        """
        Change the color.

        Args:
            color (str): The color value in hexadecimal (e.g., "#FF0000").

        Returns:
            bool: True if the request was successful.
        """
        endpoint = "/color"
        payload = {"color": color}
        return self._post(endpoint, payload)

    def play_pattern(self, pattern_id: string) -> bool:
        """
        Play a lighting pattern.

        Args:
            pattern_id (int): The ID of the pattern to play.

        Returns:
            bool: True if the request was successful.
        """
        endpoint = "/pattern/play"
        payload = {"id": pattern_id}
        return self._post(endpoint, payload)

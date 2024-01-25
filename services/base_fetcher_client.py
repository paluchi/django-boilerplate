import logging
import requests
from typing import Dict, Optional


class BaseFetcherClient:
    """
    Base client class for handling HTTP requests with common headers and API key.
    """

    def __init__(
        self, base_url: str, api_key: str, headers: Optional[Dict[str, str]] = None
    ) -> None:
        """Initialize a new instance of the BaseClient class."""
        self.base_url = base_url
        self.api_key = api_key
        self.headers = headers if headers else {}

    def send_request(
        self, endpoint: str, params: Dict[str, str], method: str = "GET"
    ) -> Optional[Dict]:
        """
        Send an HTTP request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            params (Dict[str, str]): The query parameters.
            method (str): HTTP method (GET, POST, etc.).

        Returns:
            Optional[Dict]: The response data, or None if an error occurs.
        """
        url = f"{self.base_url}/{endpoint}"
        params["api_key"] = self.api_key  # Add the API key to the parameters

        response = requests.request(
            method, url, headers=self.headers, params=params, timeout=10
        )
        response.raise_for_status()
        return response.json().get("data")

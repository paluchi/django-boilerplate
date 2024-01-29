from typing import Dict, Optional, Any  # noqa: I001

import requests


class BaseFetcher:
    """Base client class for handling HTTP requests."""

    def __init__(
        self,
        base_url: str,
        base_headers: Optional[Dict[str, str]] = None,
    ) -> None:
        """Initialize a new instance of the BaseClient class."""
        self.base_url = base_url
        self.headers = base_headers if base_headers else {}

    def send_request(  # noqa: WPS211
        self,
        endpoint: str,
        req_params: Optional[Dict[str, str]],
        headers: Optional[Dict[str, str]],
        method: str = "GET",
        **kwargs: Any,
    ) -> Optional[Dict]:
        """
        Send an HTTP request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            req_params (Dict[str, str]): The query parameters.
            headers (Optional[Dict[str, str]]): The headers to be passed as overrides.
            method (str): HTTP method (GET, POST, etc.).

        Returns:
            Optional[Dict]: The response data, or None if an error occurs.
        """
        url = f"{self.base_url}/{endpoint}"

        headers = dict(
            **self.headers if self.headers else {},
            **headers if headers else {},
        )

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=req_params,
            timeout=10,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()

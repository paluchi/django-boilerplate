import logging
import os
from typing import Dict, Optional

import requests


class HunterClient:
    """
    A client for interacting with the Hunter API.

    This class provides methods for verifying email deliverability, counting domain emails,
    searching for emails associated with a domain, and finding email addresses based on
    first name, last name, and domain.
    """

    def __init__(self) -> None:
        """Initialize a new instance of the HunterClient class."""
        self.base_url: str = os.getenv("HUNTER_API_URL", "")
        self.api_key: str = os.getenv("HUNTER_API_KEY", "")

    def verify_email(self, email: str) -> Optional[Dict]:
        """Verify if an email is deliverable."""
        try:
            url: str = (
                f"{self.base_url}/email-verifier?email={email}&api_key={self.api_key}"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raises a HTTPError if the response status code is 4xx or 5xx

            return response.json().get("data")
        except Exception as error:
            logging.error(f"An unexpected error occurred: {error}")
            return None

    def count_domain_emails(self, domain: str) -> Optional[Dict]:
        """Count the number of emails for a given domain."""
        try:
            url: str = (
                f"{self.base_url}/email-count?domain={domain}&api_key={self.api_key}"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json().get("data")
        except Exception as error:
            logging.error(f"An unexpected error occurred: {error}")
            return None

    def domain_search(self, domain: str) -> Optional[Dict]:
        """Search for emails associated with a given domain."""
        try:
            url: str = (
                f"{self.base_url}/domain-search?domain={domain}&api_key={self.api_key}"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json().get("data")
        except Exception as error:
            logging.error(f"An unexpected error occurred: {error}")
            return None

    def find_email(
        self,
        first_name: str,
        last_name: str,
        domain: str,
    ) -> Optional[Dict]:
        """Find an email address based on first name, last name, and domain."""
        try:
            url: str = (
                f"{self.base_url}/email-finder?first_name={first_name}"
                f"&last_name={last_name}&domain={domain}&api_key={self.api_key}"
            )
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return response.json().get("data")
        except Exception as error:
            logging.error(f"An unexpected error occurred: {error}")
            return None

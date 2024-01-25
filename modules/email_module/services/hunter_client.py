import os
from typing import Dict, Optional
from services.base_fetcher_client import BaseFetcherClient


class HunterClient(BaseFetcherClient):
    """
    Client for interacting with the Hunter API.
    """

    def __init__(self) -> None:
        """Initialize a new instance of the HunterClient class."""
        super().__init__(
            base_url=os.getenv("HUNTER_API_URL", ""),
            api_key=os.getenv("HUNTER_API_KEY", ""),
        )

    def verify_email(self, email: str) -> Optional[Dict]:
        """Verify if an email is deliverable."""
        params = {"email": email}
        return self.send_request("email-verifier", params)

    def count_domain_emails(self, domain: str) -> Optional[Dict]:
        """Count the number of emails for a given domain."""
        params = {"domain": domain}
        return self.send_request("email-count", params)

    def domain_search(self, domain: str) -> Optional[Dict]:
        """Search for emails associated with a given domain."""
        params = {"domain": domain}
        return self.send_request("domain-search", params)

    def find_email(
        self,
        first_name: str,
        last_name: str,
        domain: str,
    ) -> Optional[Dict]:
        """Find an email address based on first name, last name, and domain."""
        params = {
            "first_name": first_name,
            "last_name": last_name,
            "domain": domain,
        }
        return self.send_request("email-finder", params)

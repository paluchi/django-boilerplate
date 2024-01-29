import os
from typing import Dict, Optional, Any

from utils.base_fetcher import BaseFetcher
from utils.client_services_manager.client_services_manager import ClientServicesManager


class HunterClient(BaseFetcher, ClientServicesManager):
    """
    Client for interacting with the Hunter API.

    Dynamic methods:
        - verify_email({email: str})
        - count_domain_emails({domain: str})
        - domain_search({domain: str})
        - find_email({first_name: str, last_name: str, domain: str})
    """

    def __init__(self) -> None:
        """Initialize the HunterClient with necessary configurations."""
        BaseFetcher.__init__(self, base_url=os.getenv("HUNTER_API_URL", ""))
        ClientServicesManager.__init__(self)
        self.api_key = os.getenv("HUNTER_API_KEY", "")

    def some_random_method_or_service_handler(self):
        """Provide an example of an additional method or service handler."""
        # Implementation here

    def _default_service_method_handler(
        self,
        endpoint: str,
        req_params: Optional[Dict[str, Any]] = None,
        req_headers: Optional[Dict[str, Any]] = None,
    ):
        """Handle default service methods and enrich the request with the API key."""
        enriched_params = {**req_params, "api_key": self.api_key}
        response = self.send_request(endpoint, enriched_params, headers=req_headers)
        return response.get("data", {})

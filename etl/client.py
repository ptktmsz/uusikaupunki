import logging
import requests
from typing import Optional

class DigitrafficClient:
    def __init__(self) -> None:
        self.base_url = "https://rata.digitraffic.fi/api/v1"
        self.logger = logging.getLogger("DigitrafficClient")

    def _make_request(self, endpoint: str) -> Optional[requests.Response]:
        """Private helper method to handle multiple different calls."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error {e} when getting data from {url}")
            return None

    def get_train_trip(self, date: str, train: str) -> dict:
        return self._make_request(f"trains/{date}/{train}").json()[0]

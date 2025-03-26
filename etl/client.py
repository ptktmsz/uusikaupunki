import logging
import requests

class DigitrafficClient:
    def __init__(self) -> None:
        self.base_url = "https://rata.digitraffic.fi/api/v1"
        self.session = requests.Session()
        self.logger = logging.getLogger("DigitrafficClient")

    def _make_request(self, endpoint: str) -> list | dict | None:
        """Private helper method to handle multiple different calls."""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self.session.get(url, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error {e} when getting data from {url}")
            return None

    def get_train_trip(self, date: str, train: str) -> dict:
        """
        Method for obtaining the data about the complete trip of a particular train on a selected date.
        :param date: date in YYYY-MM-DD format.
        :param train: ID of the train.
        :return: raw json converted into dictionary.
        """
        return self._make_request(f"trains/{date}/{train}")[0]

    def get_stations(self) -> list:
        """
        Method for obtaining the complete list of stations.
        :return: raw json converted into list.
        """
        return self._make_request("metadata/stations")

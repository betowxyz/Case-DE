import logging
import time

import requests

logger = logging.getLogger(__name__)


class API:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        token = self._authenticate(username, password)
        self.headers = {"Authorization": f"Bearer {token}"}

    def _authenticate(self, username: str, password: str) -> str:
        response = requests.post(
            f"{self.base_url}/auth",
            json={"username": username, "password": password},
            timeout=30,
        )

        response.raise_for_status()

        return response.json()["token"]

    def get(self, endpoint: str, retries: int = 3) -> None:
        url = self.base_url + endpoint

        for attempt in range(retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                logger.warning("Attempt %s failed: %s", attempt + 1, e)

                if attempt == retries - 1:
                    raise

                time.sleep(2)

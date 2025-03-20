"""
Base faucet implementation that handles common functionality for all faucets.

This module defines a BaseFaucet class that implements common methods and attributes
for all blockchain faucet implementations, reducing code duplication.
"""

from abc import ABC
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BaseFaucet(ABC):
    """Base class for all faucet implementations."""

    TOKEN_TICKER: str  # pylint: disable=C0103
    FAUCET_NAME: str  # pylint: disable=C0103
    FAUCET_URL: str  # pylint: disable=C0103

    def claim(self, address) -> bool:
        """
        Send a request to claim tokens from the faucet for the given address.

        Args:
            address (str): The blockchain address to receive tokens

        Returns:
            bool: True if the claim was successful, False otherwise
        """
        payload = {
            "address": address,
            # "token": os.getenv("CAPTCHA_TOKEN"), # Required reCAPTCHA token
        }

        response = requests.post(self.FAUCET_URL, json=payload, timeout=10)

        success = response.status_code == 200
        if success:
            print(f"Success: Address {address} processed on {self.FAUCET_NAME} faucet")
        else:
            if response.headers.get("Content-Type") == "application/json":
                print(
                    f"Failed: Address {address} on {self.FAUCET_NAME}"
                    " - "
                    f"Status: {response.status_code}, Response: {response.json()}"
                )
            else:
                print(
                    f"Failed: Address {address} on {self.FAUCET_NAME}"
                    " - "
                    f"Status: {response.status_code}, Response: {response.text}"
                )
        return success

import json
import os

import httpx
import requests

from urllib import parse
from typing import List

from pydantic import AnyHttpUrl, TypeAdapter

from addrx.model.address_model import Address


class AddrXCore:
    """Wrapper for binding pelias/libpostal service."""

    def __init__(self, url: str, exclude_address_types: list = None):
        """TryPostal configuration.

        Args:
            url: URL of the Libpostal service.
            exclude_address_types: List of types of address which are not
                                    required in the output. values of these
                                    types will be None in the output.

                                    Default is None, All address types
                                    will be present in the output.

        """
        self.service_url: AnyHttpUrl = self._validate_url(url)
        self.exclude_address_types = exclude_address_types

    @staticmethod
    def _validate_url(url: str) -> AnyHttpUrl:
        """Validate the URL parameter.

        Args:
            url: URL parameter.
        Returns: Parsed URL parameter.
        """
        return TypeAdapter(AnyHttpUrl).validate_python(url)

    def construct_url(self, method: str, address: str) -> AnyHttpUrl:
        """Construct the request url for the specified method and address.

        Args:
            method: Libpostal method to call.
            address: Address to assess.

        Returns: Request URL.

        """
        query = parse.urlencode({"address": address})

        return self._validate_url(
            os.path.join(str(self.service_url), f"{method}?{query}")
        )

    def libpostal_check(self):
        """Checks the availability of the Libpostal service.

        Sends a GET request to the "/ping" endpoint of Libpostal service to verify its reachability.
        Raises a ConnectionError if the service is unreachable or if any request
        exception occurs.

        Raises:
            ConnectionError: If the Libpostal service is unreachable or a request
            exception occurs.```
        """
        health_check_url = os.path.join(str(self.service_url), "ping")
        try:
            response = requests.get(health_check_url, timeout=5)
            if response.status_code != 200:
                raise ConnectionError(
                    f"Libpostal service at {self.service_url} is unreachable: Received status code {response.status_code}"
                )
        except requests.RequestException as e:
            raise ConnectionError(
                f"Libpostal service at {self.service_url} is unreachable: {e}"
            )

    def parse(self, address: str) -> Address:
        """Parse an address with Libpostal.

        Args:
            address: Address to parse, in plain text.

        Returns: Parsed address.

        """
        self.libpostal_check()
        request_url = self.construct_url(method="parse", address=address)
        response = requests.get(request_url)
        response_text = json.loads(response.text)

        return Address(
            exclude_types=self.exclude_address_types,
            **{el["label"]: el["value"] for el in response_text},
        )

    async def async_parse(self, addresses: List[str]) -> List[dict]:
        """Parse a list of addresses with Libpostal asynchronously.

        Args:
            addresses: List of addresses to parse, in plain text.

        Returns: List of parsed addresses.
        """
        self.libpostal_check()
        results = []
        async with httpx.AsyncClient() as client:
            for address in addresses:
                request_url = self.construct_url(method="parse", address=address)
                response = await client.get(str(request_url))
                response_text = json.loads(response.text)

                results.append(
                    Address(
                        exclude_types=self.exclude_address_types,
                        **{el["label"]: el["value"] for el in response_text},
                    )
                )
        return results

    def expand(self, address: str) -> List[str]:
        """Expand an address with Libpostal.

        Args:
            address: Address to expand, in plain text.

        Returns: Expanded address.

        """
        request_url = self.construct_url(method="expand", address=address)
        response = requests.get(request_url)
        response_text = json.loads(response.text)
        
        return response_text


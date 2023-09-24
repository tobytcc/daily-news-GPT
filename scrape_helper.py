"""
this module contains general function and classes which may be
useful for any form of webscraping
"""

import requests
from bs4 import BeautifulSoup


class HTTPConnectionError(Exception):
    """
    just a dummy class for catching connection error exception
    """


def make_request(url: str) -> BeautifulSoup:
    """
    helper function for the module to make a request and return a bs4 obj.
    if status_code != 200, raise connection error
    """
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise HTTPConnectionError(
            f"Failed to connect to {url}. Status code: {response.status_code}"
        )
    return BeautifulSoup(response.content, "html.parser")

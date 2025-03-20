"""
This module contains the endpoints of the Promiedos API.
"""


class PromiedosEndpoints:
    """
    A class to represent the endpoints of the Promiedos API.
    """

    def __init__(self, base_url: str = "https://api.promiedos.com.ar/") -> None:
        self.base_url = base_url

    @property
    def events_endpoint(self) -> str:
        """
        Get the events endpoint.
        """
        return self.base_url + "games/{date}"

    @property
    def match_endpoint(self) -> str:
        """
        Get the match endpoint.
        """
        return self.base_url + "gamecenter/{id}"

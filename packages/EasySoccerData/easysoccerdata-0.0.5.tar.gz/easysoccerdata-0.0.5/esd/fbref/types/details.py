"""
This module contains the data types and functions for parsing match details.
"""

from dataclasses import dataclass, field
import lxml


@dataclass
class MatchDetails:
    """
    A class to represent a match details.
    """

    id: str = field(default=None)


def parse_match_details(data: lxml.html.HtmlElement) -> MatchDetails:
    """
    TODO: Parse the match report data.
    """
    print(data)
    return MatchDetails()

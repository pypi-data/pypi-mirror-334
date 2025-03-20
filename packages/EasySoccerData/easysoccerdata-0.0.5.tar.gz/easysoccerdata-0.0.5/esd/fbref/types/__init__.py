"""
Contains the types for the FBRef service.
"""

from .match import Match, parse_matchs
from .details import MatchDetails, parse_match_details

__all__ = [
    "Match",
    "parse_matchs",
    "MatchDetails",
    "parse_match_details",
]

"""
Promiedos module.
"""

from .client import PromiedosClient
from .types import (
    Event,
    Match,
    Team,
    League,
    Color,
    Status,
    MatchStatus,
    MainOdds,
    OddsOption,
    TVNetwork,
    Scores,
    Player,
    Players,
    Lineups,
    LineupTeam,
    MatchStats,
    MatchEvents,
)

__all__ = [
    "PromiedosClient",
    "Event",
    "Match",
    "Team",
    "League",
    "Color",
    "Status",
    "MatchStatus",
    "MainOdds",
    "OddsOption",
    "TVNetwork",
    "Scores",
    "Player",
    "Players",
    "Lineups",
    "LineupTeam",
    "MatchStats",
    "MatchEvents",
]

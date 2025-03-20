"""
Contains the types for the Sofascore service.
"""

from .event import Event, parse_events, parse_event
from .team import Team, parse_team
from .player import Player, parse_player
from .match_stats import MatchStats, parse_match_stats
from .lineup import Lineups, PlayerLineup, TeamColor, TeamLineup, parse_lineups
from .tournament import Tournament, parse_tournaments, parse_tournament
from .season import Season, parse_seasons, parse_season
from .bracket import Bracket, parse_bracket, parse_brackets
from .standing import Standing, parse_standing, parse_standings
from .incident import Incident, IncidentType, parse_incident, parse_incidents
from .top import TopPlayersMatch, parse_top_players_match
from .entity import EntityType
from .categories import Category


__all__ = [
    "Event",
    "parse_events",
    "parse_event",
    "Tournament",
    "parse_tournaments",
    "parse_tournament",
    "TopPlayersMatch",
    "parse_top_players_match",
    "Incident",
    "IncidentType",
    "parse_incident",
    "parse_incidents",
    "Standing",
    "parse_standing",
    "parse_standings",
    "Season",
    "parse_seasons",
    "parse_season",
    "Bracket",
    "parse_bracket",
    "parse_brackets",
    "Team",
    "parse_team",
    "Player",
    "parse_player",
    "MatchStats",
    "parse_match_stats",
    "Lineups",
    "PlayerLineup",
    "TeamColor",
    "TeamLineup",
    "parse_lineups",
    "EntityType",
    "Category",
]

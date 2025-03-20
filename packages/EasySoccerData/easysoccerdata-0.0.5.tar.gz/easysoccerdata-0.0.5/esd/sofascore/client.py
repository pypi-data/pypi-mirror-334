"""
This module contains the client class for interacting with the Sofascore API.
"""

from __future__ import annotations
from .service import SofascoreService
from .types import (
    EntityType,
    Event,
    Team,
    Player,
    MatchStats,
    Lineups,
    Category,
    Tournament,
    Season,
    Bracket,
    Standing,
    Incident,
    TopPlayersMatch,
)


class SofascoreClient:
    """
    A class to represent the client for interacting with the Sofascore API.
    """

    def __init__(self) -> None:
        """
        Initializes the Sofascore client.
        """
        self.__service = SofascoreService()

    def get_events(self, date: str = None, live: bool = False) -> list[Event]:
        """
        Get the scheduled events.

        Args:
            date (str): The date of the events in the format "YYYY-MM-DD".
            live (bool): Whether to get the live events (more precise).

        Returns:
            list[Event]: The scheduled events.
        """
        if live:
            return self.__service.get_live_events()
        return self.__service.get_events(date)

    def get_event(self, event_id: int) -> Event:
        """
        Get the event information.

        Args:
            event_id (int): The event id.

        Returns:
            Event: The event information.
        """
        return self.__service.get_event(event_id)

    def get_match_incidents(self, event_id: int) -> list[Incident]:
        """
        Get the events of a match.

        Args:
            event_id (int): The event id.

        Returns:
            list[Incident]: The match incidents.
        """
        return self.__service.get_match_incidents(event_id)

    def get_match_top_players(self, event_id: int) -> TopPlayersMatch:
        """
        Get the top players of a match.

        Args:
            event_id (int): The event id.

        Returns:
            TopPlayersMatch: The match top players.
        """
        return self.__service.get_match_top_players(event_id)

    def get_match_stats(self, event_id: int) -> MatchStats:
        """
        Get the match statistics by event id.

        Args:
            event_id (int): The event id (also known as match id).

        Returns:
            MatchStats: The match statistics.
        """
        return self.__service.get_match_stats(event_id)

    def get_match_lineups(self, event_id: int) -> Lineups:
        """
        Get the match lineups.

        Args:
            event_id (int): The event id.

        Returns:
            Lineups: The match lineups.
        """
        return self.__service.get_match_lineups(event_id)

    def get_team(self, team_id: int) -> Team:
        """
        Get detailed information about a team.

        Args:
            team_id (int): The team id.

        Returns:
            TeamEx: The team information.
        """
        team: Team = self.__service.get_team(team_id)
        players: list[Player] = self.__service.get_team_players(team_id)
        team.players = players
        return team

    def get_team_players(self, team_id: int) -> list[Player]:
        """
        Get the players of a team.

        Args:
            team_id (int): The team id.

        Returns:
            list[Player]: The players of the team.
        """
        return self.__service.get_team_players(team_id)

    def get_tournaments(self, category_id: Category) -> list[Tournament]:
        """
        Get the tournaments by category.
        TODO: maybe add a argument to include seasons.

        Args:
            category_id (Category): The category id.

        Returns:
            list[Tournament]: The tournaments.
        """
        return self.__service.get_tournaments_by_category(category_id)

    def get_tournament_seasons(self, tournament_id: int) -> list[Season]:
        """
        Get the seasons of a tournament.

        Args:
            tournament_id (int): The tournament id.

        Returns:
            list[Season]: The seasons of the tournament.
        """
        return self.__service.get_tournament_seasons(tournament_id)

    def get_tournament_brackets(
        self, tournament_id: int | Tournament, season_id: int | Season
    ) -> list[Bracket]:
        """
        Get the tournament bracket.

        Args:
            tournament_id (int, Tournament): The tournament id.
            season_id (int, Season): The season id.

        Returns:
            list[Bracket]: The tournament bracket.
        """
        return self.__service.get_tournament_bracket(tournament_id, season_id)

    def get_tournament_standings(
        self, tournament_id: int | Tournament, season_id: int | Season
    ) -> list[Standing]:
        """
        Get the tournament standings.

        Args:
            tournament_id (int, Tournament): The tournament id.
            season_id (int, Season): The season id.

        Returns:
            list[Standing]: The tournament standings.
        """
        return self.__service.get_tournament_standings(tournament_id, season_id)

    def search(
        self, query: str, entity: str | EntityType = EntityType.ALL
    ) -> list[Event | Team | Player | Tournament]:
        """
        Search query for matches, teams, players, and tournaments.

        Args:
            query (str): The search query.
            entity (str, EntityType): The entity type to search for.

        Returns:
            list[Event | Team | Player | Tournament]: The search results.
        """
        if isinstance(entity, str):
            entity = EntityType(entity)
        return self.__service.search(query, entity)

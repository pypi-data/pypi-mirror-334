"""
This module contains the definition of the MatchStats class.
"""

from dataclasses import dataclass, field


@dataclass
class StatsItem:
    """
    The stats item data.
    """

    home_value: str = field(default=0)
    home_percentage: str = field(default=0)
    away_value: str = field(default=0)
    away_percentage: str = field(default=0)


@dataclass
class MatchStats:
    """
    The match stats data.
    """

    total_shots: StatsItem = field(default=StatsItem)
    shots_on_target: StatsItem = field(default=StatsItem)
    possession: StatsItem = field(default=StatsItem)
    free_kicks: StatsItem = field(default=StatsItem)
    corners: StatsItem = field(default=StatsItem)
    offsides: StatsItem = field(default=StatsItem)
    yellow_cards: StatsItem = field(default=StatsItem)
    red_cards: StatsItem = field(default=StatsItem)
    fouls: StatsItem = field(default=StatsItem)


def parse_stats(stat: dict[str, any]) -> StatsItem:
    """
    Parse the stats data.
    """
    return StatsItem(
        home_value=stat["values"][0],
        away_value=stat["values"][1],
        home_percentage=stat["percentages"][0],
        away_percentage=stat["percentages"][1],
    )


def parse_match_stats(data: list[dict]) -> MatchStats:
    """
    Parse the match stats data.

    Args:
        data (list[dict]): The match stats data.

    Returns:
        MatchStats: The match stats
    """
    if not data or len(data) == 0:
        return MatchStats()
    stats_map = {
        "Total Remates": "total_shots",
        "Remates al arco": "shots_on_target",
        "Posesión": "possession",
        "Saques de falta": "free_kicks",
        "Saques de Esquina": "corners",
        "Fueras de Juego": "offsides",
        "Faltas": "fouls",
        "Tarjetas Amarillas": "yellow_cards",
        "Tarjetas Rojas": "red_cards",
    }

    parsed_stats = {}
    for stat in data:
        key = stats_map.get(stat["name"], None)
        if key:
            parsed_stats[key] = parse_stats(stat)

    return MatchStats(**parsed_stats)

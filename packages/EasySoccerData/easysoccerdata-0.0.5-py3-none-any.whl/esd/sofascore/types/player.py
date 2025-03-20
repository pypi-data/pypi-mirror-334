"""
Player dataclass and parser.
"""

from dataclasses import dataclass, field


@dataclass
class Player:
    """
    Player dataclass
    """

    name: str = field(default=None)
    slug: str = field(default=None)
    short_name: str = field(default=None)
    position: str = field(default=None)
    jersey_number: str = field(default=None)
    height: int = field(default=0)
    preferred_foot: str = field(default=None)
    gender: str = field(default=None)
    id: int = field(default=0)
    shirt_number: int = field(default=0)
    date_of_birth: int = field(default=0)
    contract_until: int = field(default=0)
    market_value: int = field(default=0)  # proposed
    """
    userCount: int
    market_value_raw: ProposedMarketValueRaw = field(
        default_factory=ProposedMarketValueRaw
    )
    fieldTranslations: Dict[str, Dict[str, str]]

    def parse_proposed_market_value_raw(data: dict) -> ProposedMarketValueRaw:
        return ProposedMarketValueRaw(value=data["value"], currency=data["currency"])

    @dataclass
    class ProposedMarketValueRaw:
        value: int = field(default=0)
        currency: str = field(default=None)
"""


def parse_player(data: dict) -> Player:
    """
    Parse player data.

    Args:
        data (dict): Player data.

    Returns:
        Player: Player dataclass.
    """
    return Player(
        name=data.get("name", None),
        slug=data.get("slug", None),
        short_name=data.get("shortName", None),
        position=data.get("position", None),
        jersey_number=data.get("jerseyNumber", None),
        height=data.get("height", 0),
        preferred_foot=data.get("preferredFoot", None),
        gender=data.get("gender", None),
        id=data.get("id", 0),
        shirt_number=data.get("shirtNumber", 0),
        date_of_birth=data.get("dateOfBirthTimestamp", 0),
        contract_until=data.get("contractUntilTimestamp", 0),
        market_value=data.get("proposedMarketValue", 0),
        # userCount=data["userCount"],
        # market_value_raw=parse_proposed_market_value_raw(
        #     data["proposedMarketValueRaw"]
        # ),
        # fieldTranslations=data["fieldTranslations"],
    )

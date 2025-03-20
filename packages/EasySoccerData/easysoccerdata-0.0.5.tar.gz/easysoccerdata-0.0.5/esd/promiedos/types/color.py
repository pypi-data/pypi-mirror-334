"""
Color dataclass
"""

from dataclasses import dataclass, field


@dataclass
class Color:
    """
    Color dataclass
    """

    color: str = field(default=None)
    text_color: str = field(default=None)


def parse_color(data: dict) -> Color:
    """
    Parse the colors data.
    """
    return Color(color=data.get("color", ""), text_color=data.get("text_color", ""))

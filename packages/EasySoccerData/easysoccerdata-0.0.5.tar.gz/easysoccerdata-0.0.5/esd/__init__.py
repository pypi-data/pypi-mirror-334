"""
EasySoccerData - A Python easy-to-use library for soccer data analysis from multiple sources.
This package is not affiliated with any of the sources used to extract data.

Usage example:
```python
from esd import SofascoreClient
client = SofascoreClient()
events = client.get_events()
for event in events:
    print(event)
```
"""

from .sofascore import SofascoreClient
from .promiedos import PromiedosClient
from .fbref import FBrefClient


__all__ = [
    "SofascoreClient",
    "PromiedosClient",
    "FBrefClient",
]

__version__ = "0.0.5"
__description__ = (
    "A simple python package for extracting real-time soccer data "
    "from diverse online sources, providing essential statistics and insights."
)
__author__ = "Manuel Cabral"
__title__ = "EasySoccerData"
__license__ = "GPL-3.0"

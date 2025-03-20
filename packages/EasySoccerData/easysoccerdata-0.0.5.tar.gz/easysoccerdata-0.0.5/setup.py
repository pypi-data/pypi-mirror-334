from pathlib import Path
from setuptools import setup, find_packages
from esd import (
    __version__,
    __author__,
    __title__,
    __license__,
    __description__,
)

here = Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name=__title__,
    version=__version__,
    author=__author__,
    license=__license__,
    description=__description__,
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/manucabral/EasySoccerData",
    project_urls={
        "Bug Tracker": "https://github.com/manucabral/EasySoccerData/issues",
        "Documentation": "https://github.com/manucabral/EasySoccerData/blob/main/README.md",
        "Source Code": "https://github.com/manucabral/EasySoccerData/tree/main/esd",
    },
    python_requires=">=3.9",
    install_requires=[
        "httpx==0.28.1",
    ],
    keywords=[
        "fifa",
        "ranking",
        "soccer",
        "data",
        "soccerdata",
        "football",
        "worldcup",
        "fifaranking",
        "footballdata",
        "europaleague",
        "championsleague",
        "scraper",
        "webscraper",
        "soccerstats",
        "soccerstatistics",
        "socceranalysis",
        "footballstats",
        "footballstatistics",
        "footballanalysis",
        "soccerapi",
        "footballapi",
        "soccerdatabase",
    ],
    clasisfiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Football",
        "Topic :: Soccer",
        "Topic :: FIFA",
        "Topic :: FIFA Ranking",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

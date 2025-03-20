<h1 align="center">EasySoccerData</h1>

<p align="center">
<img alt="PyPI - Version" src="https://img.shields.io/pypi/v/EasySoccerData?color=00329e">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/EasySoccerData?color=009903">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/manucabral/easysoccerdata/pylint.yml">
<img alt="GitHub License" src="https://img.shields.io/github/license/manucabral/easysoccerdata">
</p>

<p align="center">
A simple python package for extracting real-time soccer/football data from diverse online sources, providing essential statistics and insights.
</p>


> [!IMPORTANT]  
> Currently in the early development phase. Please take this into consideration.

# Installation
```
pip install EasySoccerData
```

# Usage

Using Sofascore
```py
import esd

client = esd.SofascoreClient()
events = client.get_events(live=True)
for event in events:
    print(event)
```

[How to search for matches, teams, tournaments, and players](https://github.com/manucabral/EasySoccerData/blob/main/examples/sofascore/search_matchs.py)

[How to get tournament brackets](https://github.com/manucabral/EasySoccerData/blob/main/examples/sofascore/tournament_bracket.py)

[How to get live match statistics](https://github.com/manucabral/EasySoccerData/blob/main/examples/sofascore/get_live_matchs.py)


Check out [Sofascore module examples](https://github.com/manucabral/EasySoccerData/tree/main/examples/sofascore/)

Now using FBRef
```py
import esd

client = esd.FBrefClient()
matchs = client.get_matchs()
for match in matchs:
    print(match)
```

Check out [FBref module examples](https://github.com/manucabral/EasySoccerData/tree/main/examples/fbref/)

Using Promiedos
```py
import esd

client = esd.PromiedosClient()
events = client.get_events()
for event in events:
    print(event)
```

Check out [Promiedos module examples](https://github.com/manucabral/EasySoccerData/tree/main/examples/promiedos/)

Simple demonstration of a live table using Sofascore module (see [source code](https://github.com/manucabral/EasySoccerData/blob/main/examples/live_table.py))
<p align="center">
<img src="https://github.com/manucabral/EasySoccerData/blob/main/assets/sofascore-live-table.gif" width="550" title="LiveTableUsingSofascore">
</p>


# Supported modules

| Name | Implemented |
| :---  | :---: |
| Sofascore   | ✔️ |
| FBref    | ✔️ |
| Promiedos    | ✔️ |
| Understat | ❌ |
...
> Keep in mind that it is still under active development.

### Constributions
All constributions, bug reports or fixes and ideas are welcome.

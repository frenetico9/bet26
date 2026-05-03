"""
Subpackage containing connectors to various public football data APIs.

Each module in this package exposes a `get_matches(date)` function which takes
a `datetime.date` object and returns a list of dictionaries. Each dictionary
must contain at least the following keys:

    - home_team: The name of the home team.
    - away_team: The name of the away team.
    - league: The league or competition name.
    - match_time: The scheduled kick‑off time in ISO 8601 format or an empty
      string if unknown.
    - home_goals_avg: Optional float representing the average number of goals
      scored by the home team in recent games. Can be None if not available.
    - away_goals_avg: Optional float representing the average number of goals
      scored by the away team in recent games. Can be None if not available.

The aggregator in predictor.py will combine results from multiple sources,
deduplicate them and prepare them for further analysis. Not all sources will
provide all fields; missing values can be left as None.

IMPORTANT: The data‑fetching functions defined here rely on external HTTP
requests. They have not been executed in this environment because outgoing
requests are blocked. Users deploying this project must ensure their
environment allows HTTP requests, or inject their own data for testing.
"""

from datetime import date
from typing import List, Dict

from .scorebat import get_matches as scorebat_matches
from .openligadb import get_matches as openligadb_matches
from .thesportsdb import get_matches as thesportsdb_matches
from .worldcup import get_matches as worldcup_matches

__all__ = [
    "get_all_sources",
    "scorebat_matches",
    "openligadb_matches",
    "thesportsdb_matches",
    "worldcup_matches",
]


def get_all_sources() -> Dict[str, callable]:
    """Return a mapping of human‑readable source names to connector functions."""
    return {
        "scorebat": scorebat_matches,
        "openligadb": openligadb_matches,
        "thesportsdb": thesportsdb_matches,
        "worldcup": worldcup_matches,
    }
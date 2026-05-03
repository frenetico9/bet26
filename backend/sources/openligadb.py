"""
Connector for the OpenLigaDB API.

OpenLigaDB is an open database of German football match results. Its API
documentation is available at https://www.openligadb.de/api. Unlike many other
football APIs, OpenLigaDB does not require authentication. You can retrieve
matches for a specific league and season via endpoints such as:

    https://api.openligadb.de/getmatchdata/bl1/2023

where `bl1` refers to the Bundesliga and `2023` refers to the season.

For simplicity, this connector fetches the current Bundesliga season and
filters matches by date. The match list can include past and future fixtures.

Note: The OpenLigaDB API returns German timezone dates; you may need to adjust
for your local timezone when integrating.
"""
from datetime import date as Date, datetime
from typing import List, Dict
import requests


LEAGUE = "bl1"  # Bundesliga
SEASON = "2023"  # Example season; update as needed
API_URL = f"https://api.openligadb.de/getmatchdata/{LEAGUE}/{SEASON}"


def get_matches(selected_date: Date) -> List[Dict]:
    """Fetch Bundesliga matches scheduled on the specified date.

    Parameters
    ----------
    selected_date: date
        The date for which to retrieve matches.

    Returns
    -------
    List[dict]
        A list of dictionaries containing match details. Missing average goal
        statistics are set to None.
    """
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
    except Exception:
        return []

    try:
        data = resp.json()
    except Exception:
        return []

    matches: List[Dict] = []
    for match in data:
        match_date_str = match.get("MatchDateTime")
        if not match_date_str:
            continue
        try:
            match_dt = datetime.fromisoformat(match_date_str)
        except ValueError:
            continue
        if match_dt.date() != selected_date:
            continue
        team1 = match.get("Team1", {}).get("TeamName") or "Unknown"
        team2 = match.get("Team2", {}).get("TeamName") or "Unknown"
        league_name = "Bundesliga"
        matches.append({
            "home_team": team1,
            "away_team": team2,
            "league": league_name,
            "match_time": match_dt.isoformat(),
            "home_goals_avg": None,
            "away_goals_avg": None,
        })
    return matches
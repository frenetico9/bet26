"""
Connector for the WorldCupJSON API.

WorldCupJSON provides an open API for FIFA World Cup and Women’s World Cup data.
It offers match information, results and statistics without requiring an API
key. Documentation is available at https://github.com/estiens/worldcup-json.

This connector fetches matches on a specific date. Note that the API only
contains data for tournaments that have already taken place; therefore, this
source is primarily useful for historical analysis.
"""
from datetime import date as Date
from typing import List, Dict
import requests


API_URL = "https://worldcupjson.net/matches"


def get_matches(selected_date: Date) -> List[Dict]:
    """Retrieve World Cup matches that took place on a particular date.

    Parameters
    ----------
    selected_date: date
        Date for which to retrieve matches.

    Returns
    -------
    List[dict]
        A list of match dictionaries conforming to the standard schema.
    """
    params = {"by_date": selected_date.isoformat()}
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
    except Exception:
        return []
    try:
        data = resp.json()
    except Exception:
        return []
    matches: List[Dict] = []
    for match in data:
        home = match.get("home_team")
        away = match.get("away_team")
        if not home or not away:
            continue
        home_team = home.get("name") or "Unknown"
        away_team = away.get("name") or "Unknown"
        stage = match.get("stage_name", "World Cup")
        datetime_str = match.get("datetime")  # Already ISO format
        matches.append({
            "home_team": home_team,
            "away_team": away_team,
            "league": stage,
            "match_time": datetime_str,
            "home_goals_avg": None,
            "away_goals_avg": None,
        })
    return matches
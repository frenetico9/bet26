"""
Connector for TheSportsDB API.

TheSportsDB offers a range of endpoints for retrieving sports data. While many
operations require an API key, some endpoints allow access using a default key
of `1`, which is intended for testing and personal use. One such endpoint is
`eventsday.php`, which returns events for a given day and sport category.

Example URL:
    https://www.thesportsdb.com/api/v1/json/1/eventsday.php?d=2026-05-03&c=Soccer

See https://www.thesportsdb.com/api.php for more details.
"""
from datetime import date as Date
from typing import List, Dict
import requests


API_URL = "https://www.thesportsdb.com/api/v1/json/1/eventsday.php"


def get_matches(selected_date: Date) -> List[Dict]:
    """Fetch soccer events on the given date from TheSportsDB.

    Parameters
    ----------
    selected_date: date
        The date for which to fetch events.

    Returns
    -------
    List[dict]
        A list of match dictionaries matching the standard schema. Average
        goals fields are left as None because this endpoint does not provide
        historical performance data.
    """
    params = {
        "d": selected_date.isoformat(),
        "c": "Soccer",
    }
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
    except Exception:
        return []
    try:
        data = resp.json()
    except Exception:
        return []
    events = data.get("events") or []
    matches: List[Dict] = []
    for ev in events:
        home = ev.get("strHomeTeam")
        away = ev.get("strAwayTeam")
        if not home or not away:
            continue
        league = ev.get("strLeague") or ev.get("strEvent") or "Unknown"
        time_str = ev.get("dateEvent")
        # `timeEvent` may be null if the kick‑off time is not specified
        time_event = ev.get("strTime") or "00:00:00"
        match_time = f"{time_str}T{time_event}"
        matches.append({
            "home_team": home,
            "away_team": away,
            "league": league,
            "match_time": match_time,
            "home_goals_avg": None,
            "away_goals_avg": None,
        })
    return matches
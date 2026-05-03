"""
Connector for the Scorebat video API.

Scorebat provides a public API (https://www.scorebat.com/video-api/) that
returns recent and upcoming football matches along with video highlights. The
endpoint does not require an API key. Each item in the response includes a
`title` field (e.g. "Team A vs Team B"), a `competition` object with the
competition name and a `date` string in ISO 8601 format.

This module exposes a `get_matches(date)` function which filters the list of
matches to those scheduled on the specified date.

Note: Network requests are disabled in the current environment, so this
connector has not been executed here. The code is provided for completeness.
"""
from datetime import date as Date, datetime
from typing import List, Dict, Optional
import requests


API_URL = "https://www.scorebat.com/video-api/v1/"


def parse_title(title: str) -> Optional[tuple[str, str]]:
    """Extract home and away team names from a title string.

    Scorebat titles use the format "HomeTeam vs AwayTeam". If the format
    differs, this function returns None.
    """
    if " vs " not in title:
        return None
    home, away = title.split(" vs ", 1)
    return home.strip(), away.strip()


def get_matches(selected_date: Date) -> List[Dict]:
    """Fetch matches for the specified date from Scorebat.

    Parameters
    ----------
    selected_date: date
        The date for which to fetch matches.

    Returns
    -------
    List[dict]
        A list of match dictionaries adhering to the format described in
        sources/__init__.py.
    """
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
    except Exception as exc:
        # In a production system you might log this exception
        return []

    try:
        data = resp.json()
    except Exception:
        return []

    matches: List[Dict] = []
    for item in data:
        date_str = item.get("date")
        if not date_str:
            continue
        try:
            match_dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        if match_dt.date() != selected_date:
            continue
        title = item.get("title", "")
        parsed = parse_title(title)
        if not parsed:
            continue
        home_team, away_team = parsed
        competition = item.get("competition", {})
        league = competition.get("name", "Unknown")
        matches.append({
            "home_team": home_team,
            "away_team": away_team,
            "league": league,
            "match_time": match_dt.isoformat(),
            # Scorebat API does not provide pre‑match average goals, so these
            # fields are left as None for later computation.
            "home_goals_avg": None,
            "away_goals_avg": None,
        })
    return matches
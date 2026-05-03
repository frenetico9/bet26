"""
Heuristic predictor for football multi‑bet suggestions.

This module defines a simple workflow for aggregating match fixtures from
multiple sources and estimating the probability that both teams will score
(BTTS) and that the match will have more than 2.5 total goals. The approach
illustrated here is intentionally straightforward and designed to be easy to
extend. In a production system you would likely replace these heuristics with
model‑based predictions trained on historical data.

The core entrypoint is `generate_bet_suggestions`, which returns a sorted list
of match suggestions for a particular date.
"""
from __future__ import annotations

import math
from datetime import date as Date
from typing import List, Dict

from .sources import get_all_sources


def logistic(x: float) -> float:
    """Compute the logistic function (sigmoid) for a real number."""
    return 1.0 / (1.0 + math.exp(-x))


# Average goals per league. These values were derived from historical
# performance in major competitions and serve as priors for the prediction.
LEAGUE_AVG_GOALS = {
    "Bundesliga": 3.2,
    "Premier League": 2.9,
    "La Liga": 2.5,
    "Serie A": 2.6,
    "Ligue 1": 2.8,
    "World Cup": 2.6,
}


def compute_probability(home_avg: float, away_avg: float, league: str) -> float:
    """
    Estimate the probability that both teams will score and the match total
    will exceed 2.5 goals.

    This function uses a logistic transformation on a weighted sum of the
    average goals scored by both teams and a league‑specific baseline. The
    coefficients were chosen heuristically to reflect that matches with higher
    scoring teams and leagues with higher average goals are more likely to
    produce BTTS + over 2.5 results.
    """
    league_avg = LEAGUE_AVG_GOALS.get(league, 2.7)
    # Combine team and league averages. Subtract 2.2 so that matches with
    # combined averages around typical levels get a baseline probability ~0.5.
    x = 0.6 * (home_avg + away_avg - 2.2) + 0.3 * (league_avg - 2.7)
    return logistic(x)


def aggregate_matches(selected_date: Date) -> List[Dict]:
    """
    Collect matches from all registered sources.

    Parameters
    ----------
    selected_date: date
        The date for which to collect fixtures.

    Returns
    -------
    List[dict]
        A list of match dictionaries. When duplicate matches are encountered
        across sources, the first occurrence is kept.
    """
    sources = get_all_sources()
    aggregated: List[Dict] = []
    seen_keys = set()
    for name, fetcher in sources.items():
        try:
            matches = fetcher(selected_date)
        except Exception:
            continue
        for match in matches:
            key = (match["home_team"].lower(), match["away_team"].lower(), match["match_time"])
            if key in seen_keys:
                continue
            seen_keys.add(key)
            aggregated.append(match)
    return aggregated


def enrich_matches(matches: List[Dict]) -> List[Dict]:
    """
    Fill in missing average goal values with conservative defaults.

    If a match dictionary lacks `home_goals_avg` or `away_goals_avg`, this
    function substitutes a default value of 1.2 for the home team and 1.0 for
    the away team. These defaults reflect the fact that home teams tend to
    score slightly more than away teams.
    """
    for match in matches:
        if match.get("home_goals_avg") is None:
            match["home_goals_avg"] = 1.2
        if match.get("away_goals_avg") is None:
            match["away_goals_avg"] = 1.0
    return matches


def generate_bet_suggestions(selected_date: Date, limit: int = 10) -> List[Dict]:
    """
    Aggregate matches for the given date, compute BTTS+over2.5 probabilities
    and return the top suggestions sorted by descending probability.

    Parameters
    ----------
    selected_date: date
        The date on which to generate bet suggestions.
    limit: int
        Number of suggestions to return. Default is 10.

    Returns
    -------
    List[dict]
        A list of suggestion dictionaries with the following keys: home_team,
        away_team, league, match_time, probability_bt_and_over25, suggestion.
    """
    matches = aggregate_matches(selected_date)
    matches = enrich_matches(matches)
    suggestions: List[Dict] = []
    for match in matches:
        prob = compute_probability(match["home_goals_avg"], match["away_goals_avg"], match["league"])
        suggestions.append({
            "home_team": match["home_team"],
            "away_team": match["away_team"],
            "league": match["league"],
            "match_time": match["match_time"],
            "probability_bt_and_over25": round(prob, 4),
            "suggestion": "Ambas marcam + Mais de 2.5 gols",
        })
    # Sort by probability descending and take the top `limit`
    suggestions.sort(key=lambda x: x["probability_bt_and_over25"], reverse=True)
    return suggestions[:limit]
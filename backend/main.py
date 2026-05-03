"""
Main entrypoint for the backend API.

This file defines a simple FastAPI application that aggregates football match data
from multiple public sources and applies basic heuristics to recommend multi-bet
selections (e.g. Both Teams To Score and Over 2.5 goals). The application
exposes endpoints that the React frontend can consume.

NOTE: External HTTP requests are blocked in the execution environment used to
generate this project, so the data-fetching functions defined in the sources
module cannot be executed here. They are provided as examples of how to call
public APIs that do not require authentication. Users running this code on
their own machines will be able to retrieve live data. During development,
mock data can be injected into the aggregator to test the prediction pipeline.

To run the backend locally:

    pip install -r requirements.txt
    uvicorn main:app --reload

The API will be available at http://localhost:8000
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel

from .predictor import generate_bet_suggestions

app = FastAPI(title="Football Multi‑Bet Predictor", version="1.0.0")

# Configure CORS so that the React frontend can access the API when served
# from a different port (e.g. http://localhost:1234).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchSuggestion(BaseModel):
    """Model representing a bet suggestion returned by the API."""

    home_team: str
    away_team: str
    league: str
    match_time: str
    probability_bt_and_over25: float
    suggestion: str


class SuggestionsResponse(BaseModel):
    """Wrapper for a list of match suggestions."""

    date: str
    suggestions: List[MatchSuggestion]


@app.get("/api/suggestions", response_model=SuggestionsResponse)
def get_suggestions(query_date: Optional[str] = None, limit: int = 10):
    """
    Return multi‑bet suggestions for a given date.

    Parameters
    ----------
    query_date: Optional[str]
        Date in ISO format (YYYY‑MM‑DD). If omitted, the current date in the
        server's timezone will be used.
    limit: int
        Maximum number of suggestions to return. The default value is 10.

    Returns
    -------
    SuggestionsResponse
        An object containing the request date and a list of match suggestions.
    """
    if query_date:
        try:
            selected_date = datetime.strptime(query_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("query_date must be in YYYY‑MM‑DD format")
    else:
        selected_date = date.today()

    # Generate suggestions using the predictor. In practice this will
    # aggregate matches from various public APIs, compute features and
    # probabilities, and return an ordered list.
    suggestions = generate_bet_suggestions(selected_date, limit=limit)

    return SuggestionsResponse(
        date=selected_date.isoformat(),
        suggestions=[MatchSuggestion(**s) for s in suggestions],
    )
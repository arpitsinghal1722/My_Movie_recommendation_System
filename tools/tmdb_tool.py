"""tools/tmdb_tool.py — TMDB API client + LangChain Tool."""
from __future__ import annotations
import os, time, logging
from typing import Optional
import requests
from dotenv import load_dotenv
from langchain.tools import tool
from pydantic import BaseModel, Field
from utils.helpers import format_movie_results

load_dotenv()
logger = logging.getLogger("movie_react_agent.tmdb")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
TMDB_API_KEY  = os.getenv("TMDB_API_KEY", "")

class TMDBAPIKeyError(Exception): pass
class TMDBNetworkError(Exception): pass
class TMDBRateLimitError(Exception): pass
class TMDBEmptyResultsError(Exception): pass

class TMDBClient:
    def __init__(self, api_key=TMDB_API_KEY, timeout=10, max_retries=3):
        if not api_key: raise TMDBAPIKeyError("TMDB_API_KEY not set in .env")
        self._key = api_key; self._timeout = timeout; self._retries = max_retries
        self._session = requests.Session()
        self._session.params = {"api_key": self._key}

    def _get(self, endpoint, params):
        url = f"{TMDB_BASE_URL}{endpoint}"
        logger.debug("TMDB GET %s params=%s", url, params)
        for attempt in range(1, self._retries + 1):
            try:
                r = self._session.get(url, params=params, timeout=self._timeout)
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt == self._retries: raise TMDBNetworkError(str(e))
                time.sleep(2 ** attempt); continue
            if r.status_code == 401: raise TMDBAPIKeyError("Invalid TMDB API key (HTTP 401)")
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", 5))
                if attempt == self._retries: raise TMDBRateLimitError("Rate limited")
                time.sleep(wait); continue
            if r.status_code >= 500:
                if attempt == self._retries: raise TMDBNetworkError(f"TMDB server error {r.status_code}")
                time.sleep(2 ** attempt); continue
            r.raise_for_status()
            return r.json()
        raise TMDBNetworkError("All retries exhausted")

    def discover_movies(self, genre_id=None, year_gte=None, year_lte=None,
                        certification=None, language=None, min_rating=None,
                        watch_provider_id=None, top_n=5, sort_by="vote_average.desc"):
        params = {"sort_by": sort_by, "vote_count.gte": 100, "include_adult": "false"}
        if genre_id:          params["with_genres"] = str(genre_id)
        if year_gte:          params["primary_release_date.gte"] = f"{year_gte}-01-01"
        if year_lte:          params["primary_release_date.lte"] = f"{year_lte}-12-31"
        if certification:     params["certification_country"]="US"; params["certification"]=certification
        if language:          params["with_original_language"] = language
        if min_rating:        params["vote_average.gte"] = str(min_rating)
        if watch_provider_id: params["with_watch_providers"]=str(watch_provider_id); params["watch_region"]="US"
        data    = self._get("/discover/movie", params)
        results = data.get("results", [])
        if not results: raise TMDBEmptyResultsError("No movies found. Try relaxing your filters.")
        logger.info("TMDB: %d results, returning top %d", len(results), top_n)
        return results[:top_n]

class MovieSearchInput(BaseModel):
    genre_id:         Optional[int]   = Field(None, description="TMDB genre ID. Horror=27,Comedy=35,Thriller=53,SciFi=878,Action=28,Drama=18,Family=10751,Crime=80,Romance=10749,Animation=16")
    year_gte:         Optional[int]   = Field(None, description="Min release year. '90s'→1990")
    year_lte:         Optional[int]   = Field(None, description="Max release year. '90s'→1999")
    certification:    Optional[str]   = Field(None, description="MPAA rating: G, PG, PG-13, R, NC-17")
    language:         Optional[str]   = Field(None, description="ISO 639-1 code: en, hi, ja, ko, fr")
    min_rating:       Optional[float] = Field(None, description="Min TMDB vote_average 0-10")
    watch_provider_id:Optional[int]   = Field(None, description="Streaming: Netflix=8, PrimeVideo=9, Disney+=337, Hulu=15")
    top_n:            int             = Field(5,    description="Number of results (1-20)", ge=1, le=20)

@tool(args_schema=MovieSearchInput)
def search_movies_tool(genre_id=None, year_gte=None, year_lte=None,
                       certification=None, language=None, min_rating=None,
                       watch_provider_id=None, top_n=5) -> str:
    """Search TMDB for real movies using filters. ALWAYS call this before recommending any movie."""
    logger.info("MovieSearchTool: genre=%s year=%s-%s cert=%s lang=%s rating=%s provider=%s top_n=%d",
                genre_id, year_gte, year_lte, certification, language, min_rating, watch_provider_id, top_n)
    try:
        client = TMDBClient()
        movies = client.discover_movies(genre_id=genre_id, year_gte=year_gte, year_lte=year_lte,
            certification=certification, language=language, min_rating=min_rating,
            watch_provider_id=watch_provider_id, top_n=top_n)
        return format_movie_results(movies)
    except TMDBAPIKeyError  as e: return f"[API KEY ERROR] {e}"
    except TMDBRateLimitError as e: return f"[RATE LIMIT] {e}"
    except TMDBNetworkError as e: return f"[NETWORK ERROR] {e}"
    except TMDBEmptyResultsError as e: return f"[NO RESULTS] {e}"
    except Exception as e: logger.exception(e); return f"[ERROR] {e}"

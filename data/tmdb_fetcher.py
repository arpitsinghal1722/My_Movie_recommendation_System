"""
data/tmdb_fetcher.py
====================
Batch-fetches 100+ real movies from TMDB across multiple genres/pages
and stores them in the local SQLite database.

Run manually:   python data/tmdb_fetcher.py
Auto-runs:      on first API server startup if DB has < 50 movies
"""
from __future__ import annotations
import os, sys, time, json, logging
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from dotenv import load_dotenv
load_dotenv()

from data.database import upsert_tmdb_movies, count_tmdb_movies, init_db

logger = logging.getLogger("movie_react_agent.fetcher")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

TMDB_KEY  = os.getenv("TMDB_API_KEY", "")
TMDB_BASE = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
TMDB_IMG  = "https://image.tmdb.org/t/p/w500"

GENRE_ID_TO_NAME = {
    28:"Action",12:"Adventure",16:"Animation",35:"Comedy",80:"Crime",
    99:"Documentary",18:"Drama",10751:"Family",14:"Fantasy",36:"History",
    27:"Horror",10402:"Music",9648:"Mystery",10749:"Romance",878:"Science Fiction",
    53:"Thriller",10752:"War",37:"Western"
}

# Fetch strategy: top-rated + popular across key genres and decades
FETCH_BATCHES = [
    # (endpoint, params_override)
    # --- Top-rated all time ---
    ("/movie/top_rated",  {}),
    # --- Popular ---
    ("/movie/popular",    {}),
    # --- Genre sweeps ---
    ("/discover/movie", {"with_genres":"27","sort_by":"vote_average.desc","vote_count.gte":"500"}),  # Horror
    ("/discover/movie", {"with_genres":"878","sort_by":"vote_average.desc","vote_count.gte":"500"}),  # Sci-Fi
    ("/discover/movie", {"with_genres":"35","sort_by":"vote_average.desc","vote_count.gte":"500"}),   # Comedy
    ("/discover/movie", {"with_genres":"28","sort_by":"vote_average.desc","vote_count.gte":"500"}),   # Action
    ("/discover/movie", {"with_genres":"18","sort_by":"vote_average.desc","vote_count.gte":"500"}),   # Drama
    ("/discover/movie", {"with_genres":"53","sort_by":"vote_average.desc","vote_count.gte":"500"}),   # Thriller
    ("/discover/movie", {"with_genres":"14","sort_by":"vote_average.desc","vote_count.gte":"500"}),   # Fantasy
    ("/discover/movie", {"with_genres":"80","sort_by":"vote_average.desc","vote_count.gte":"500"}),   # Crime
    ("/discover/movie", {"with_genres":"16","sort_by":"vote_average.desc","vote_count.gte":"500"}),   # Animation
    ("/discover/movie", {"with_genres":"10751","sort_by":"vote_average.desc","vote_count.gte":"200"}), # Family
    # --- Decade sweeps ---
    ("/discover/movie", {"primary_release_date.gte":"1980-01-01","primary_release_date.lte":"1989-12-31","sort_by":"vote_average.desc","vote_count.gte":"300"}),
    ("/discover/movie", {"primary_release_date.gte":"1990-01-01","primary_release_date.lte":"1999-12-31","sort_by":"vote_average.desc","vote_count.gte":"300"}),
    ("/discover/movie", {"primary_release_date.gte":"2000-01-01","primary_release_date.lte":"2009-12-31","sort_by":"vote_average.desc","vote_count.gte":"300"}),
    ("/discover/movie", {"primary_release_date.gte":"2010-01-01","primary_release_date.lte":"2019-12-31","sort_by":"vote_average.desc","vote_count.gte":"500"}),
    ("/discover/movie", {"primary_release_date.gte":"2020-01-01","sort_by":"vote_average.desc","vote_count.gte":"200"}),
    # --- Language sweeps ---
    ("/discover/movie", {"with_original_language":"hi","sort_by":"vote_average.desc","vote_count.gte":"200"}),  # Hindi
    ("/discover/movie", {"with_original_language":"ja","sort_by":"vote_average.desc","vote_count.gte":"200"}),  # Japanese
    ("/discover/movie", {"with_original_language":"ko","sort_by":"vote_average.desc","vote_count.gte":"200"}),  # Korean
    ("/discover/movie", {"with_original_language":"fr","sort_by":"vote_average.desc","vote_count.gte":"200"}),  # French
]


def _parse_movie(m: dict) -> dict:
    poster   = f"{TMDB_IMG}{m['poster_path']}"  if m.get("poster_path")   else None
    backdrop = f"https://image.tmdb.org/t/p/w780{m['backdrop_path']}" if m.get("backdrop_path") else None
    genres   = [GENRE_ID_TO_NAME.get(gid,"") for gid in m.get("genre_ids",[]) if gid in GENRE_ID_TO_NAME]
    return {
        "id":        m["id"],
        "title":     m.get("title",""),
        "year":      m.get("release_date","")[:4],
        "rating":    round(m.get("vote_average",0), 1),
        "vote_count":m.get("vote_count",0),
        "overview":  m.get("overview",""),
        "poster":    poster,
        "backdrop":  backdrop,
        "genres":    genres,
        "language":  m.get("original_language","en"),
        "tmdb_url":  f"https://www.themoviedb.org/movie/{m['id']}",
    }


def fetch_page(endpoint: str, extra_params: dict, page: int = 1) -> list[dict]:
    params = {"api_key": TMDB_KEY, "page": page, "include_adult": "false", **extra_params}
    try:
        r = requests.get(f"{TMDB_BASE}{endpoint}", params=params, timeout=12)
        if r.status_code == 429:
            retry = int(r.headers.get("Retry-After", 10))
            logger.warning("Rate limited — sleeping %ds", retry)
            time.sleep(retry)
            return fetch_page(endpoint, extra_params, page)
        if r.status_code == 200:
            return [_parse_movie(m) for m in r.json().get("results", [])]
    except Exception as e:
        logger.error("Fetch error %s: %s", endpoint, e)
    return []


def run_batch_fetch(target: int = 150) -> int:
    """Fetch movies until we have at least `target` in the DB."""
    if not TMDB_KEY:
        logger.error("TMDB_API_KEY not set — cannot fetch movies")
        return 0

    init_db()
    current = count_tmdb_movies()
    logger.info("Current DB count: %d, target: %d", current, target)

    if current >= target:
        logger.info("Already have %d movies — skipping fetch", current)
        return current

    total_saved = 0
    seen_ids    = set()

    for endpoint, extra in FETCH_BATCHES:
        if count_tmdb_movies() >= target:
            break
        for page in [1, 2]:  # 2 pages per batch = ~40 movies per batch
            movies = fetch_page(endpoint, extra, page)
            new_movies = [m for m in movies if m["id"] not in seen_ids]
            seen_ids.update(m["id"] for m in new_movies)
            saved = upsert_tmdb_movies(new_movies)
            total_saved += saved
            logger.info("  %s p%d → %d new (total DB: %d)", endpoint, page, saved, count_tmdb_movies())
            time.sleep(0.25)  # respect TMDB rate limit

    final = count_tmdb_movies()
    logger.info("Fetch complete. DB now has %d movies", final)
    return final


if __name__ == "__main__":
    count = run_batch_fetch(target=150)
    print(f"\n✅ Done! Database now has {count} movies.\n")

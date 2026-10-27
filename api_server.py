"""
api_server.py  v3.0 — FastAPI backend
New in v3:
  • /movies/db          — paginated browse of 100+ cached TMDB movies
  • /movies/user        — list all user-added movies
  • /movies/add         — add a custom movie (persisted to SQLite)
  • /movies/rate        — AI rates a movie via ReAct reasoning
  • /movies/save-rating — promote an AI rating into user_movies table
  • /recommend          — now searches BOTH tmdb_movies + user_movies
  • /trending, /genres, /health — unchanged
"""
from __future__ import annotations
import os, sys, re, logging, time, json, threading
from typing import Optional, List
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv
load_dotenv()

from data.database import (
    init_db, upsert_tmdb_movies, count_tmdb_movies,
    search_tmdb_movies, search_user_movies, get_all_tmdb_movies,
    add_user_movie, get_all_user_movies,
    save_ai_rating, get_recent_ai_ratings,
)

logger  = logging.getLogger("movie_react_agent.api")
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

import requests as req_lib

TMDB_KEY  = os.getenv("TMDB_API_KEY", "")
TMDB_BASE = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
TMDB_IMG  = "https://image.tmdb.org/t/p/w500"

GENRE_ID_TO_NAME = {
    28:"Action",12:"Adventure",16:"Animation",35:"Comedy",80:"Crime",
    99:"Documentary",18:"Drama",10751:"Family",14:"Fantasy",36:"History",
    27:"Horror",10402:"Music",9648:"Mystery",10749:"Romance",878:"Science Fiction",
    53:"Thriller",10752:"War",37:"Western"
}
GENRE_NAME_TO_ID = {v.lower():k for k,v in GENRE_ID_TO_NAME.items()}
GENRE_NAME_TO_ID["sci-fi"] = 878; GENRE_NAME_TO_ID["scifi"] = 878

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="CineAI — Movie ReAct Agent API", version="3.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

# ── Startup: init DB and trigger background fetch if needed ───────────────────
_fetch_done = False

@app.on_event("startup")
def on_startup():
    global _fetch_done
    init_db()
    count = count_tmdb_movies()
    logger.info("DB has %d TMDB movies on startup", count)
    if count < 50 and TMDB_KEY:
        logger.info("Triggering background movie fetch…")
        t = threading.Thread(target=_bg_fetch, daemon=True)
        t.start()
    else:
        _fetch_done = True

def _bg_fetch():
    global _fetch_done
    try:
        from data.tmdb_fetcher import run_batch_fetch
        run_batch_fetch(target=150)
    except Exception as e:
        logger.error("BG fetch error: %s", e)
    finally:
        _fetch_done = True

# ── Singleton agent ───────────────────────────────────────────────────────────
_executor = None
def get_executor():
    global _executor
    if _executor is None:
        from agents.movie_agent import build_movie_agent
        _executor = build_movie_agent(verbose=False)
    return _executor

# ── TMDB helpers ──────────────────────────────────────────────────────────────
def _parse_tmdb_result(m: dict) -> dict:
    poster   = f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None
    backdrop = f"https://image.tmdb.org/t/p/w780{m['backdrop_path']}" if m.get("backdrop_path") else None
    genres   = [GENRE_ID_TO_NAME.get(gid,"") for gid in m.get("genre_ids",[]) if gid in GENRE_ID_TO_NAME]
    return {
        "id": m["id"], "title": m.get("title",""),
        "year": m.get("release_date","")[:4],
        "rating": round(m.get("vote_average",0),1),
        "vote_count": m.get("vote_count",0),
        "overview": m.get("overview",""),
        "poster": poster, "backdrop": backdrop, "genres": genres,
        "language": m.get("original_language","en"),
        "tmdb_url": f"https://www.themoviedb.org/movie/{m['id']}",
        "source": "tmdb",
    }

def discover_movies_live(genre_id=None, year_gte=None, year_lte=None,
                         certification=None, language=None, min_rating=None,
                         watch_provider_id=None, top_n=10) -> list[dict]:
    """Live TMDB discover call."""
    params = {"api_key":TMDB_KEY,"sort_by":"vote_average.desc","vote_count.gte":200,"include_adult":"false"}
    if genre_id:          params["with_genres"]                    = str(genre_id)
    if year_gte:          params["primary_release_date.gte"]       = f"{year_gte}-01-01"
    if year_lte:          params["primary_release_date.lte"]       = f"{year_lte}-12-31"
    if certification:     params["certification_country"]="US"; params["certification"]=certification
    if language:          params["with_original_language"]         = language
    if min_rating:        params["vote_average.gte"]               = str(min_rating)
    if watch_provider_id: params["with_watch_providers"]=str(watch_provider_id); params["watch_region"]="US"
    try:
        r = req_lib.get(f"{TMDB_BASE}/discover/movie", params=params, timeout=10)
        if r.status_code == 200:
            return [_parse_tmdb_result(m) for m in r.json().get("results",[])[:top_n]]
    except Exception as e:
        logger.error("TMDB discover: %s", e)
    return []

def extract_constraints(query: str) -> dict:
    from utils.helpers import (extract_year_range, extract_genre_id, extract_certification,
                                extract_language, extract_min_rating, extract_top_n, extract_streaming_provider)
    yr_gte, yr_lte = extract_year_range(query)
    genre_id = extract_genre_id(query)
    return {k:v for k,v in {
        "genre_id":    genre_id,
        "genre_name":  GENRE_ID_TO_NAME.get(genre_id) if genre_id else None,
        "year_gte":    yr_gte, "year_lte": yr_lte,
        "certification":   extract_certification(query),
        "language":        extract_language(query),
        "min_rating":      extract_min_rating(query),
        "top_n":           extract_top_n(query),
        "watch_provider_id": extract_streaming_provider(query),
    }.items() if v is not None}

def _combined_search(constraints: dict) -> tuple[list[dict], list[dict]]:
    """Search both TMDB DB cache and user_movies. Returns (tmdb_results, user_results)."""
    genre_name = constraints.get("genre_name")
    tmdb_rows  = search_tmdb_movies(
        genre=genre_name,
        year_gte=constraints.get("year_gte"),
        year_lte=constraints.get("year_lte"),
        certification=constraints.get("certification"),
        language=constraints.get("language"),
        min_rating=constraints.get("min_rating"),
        limit=constraints.get("top_n", 10),
    )
    user_rows = search_user_movies(
        genre=genre_name,
        year_gte=constraints.get("year_gte"),
        year_lte=constraints.get("year_lte"),
        certification=constraints.get("certification"),
        min_rating=constraints.get("min_rating"),
        limit=5,
    )
    return tmdb_rows, user_rows

# ── Pydantic models ───────────────────────────────────────────────────────────
class RecommendRequest(BaseModel):
    query:     str
    use_agent: bool = False

class AddMovieRequest(BaseModel):
    title:        str          = Field(..., min_length=1, max_length=200)
    year:         Optional[str]= None
    rating:       Optional[float] = Field(None, ge=0, le=10)
    overview:     Optional[str]= None
    genres:       List[str]    = []
    certification:Optional[str]= None
    language:     Optional[str]= "en"
    poster:       Optional[str]= None
    director:     Optional[str]= None

    @validator("year")
    def validate_year(cls, v):
        if v and not re.match(r"^\d{4}$", str(v)):
            raise ValueError("Year must be 4 digits")
        return v

class RateMovieRequest(BaseModel):
    title:    str
    year:     Optional[str] = None
    overview: Optional[str] = None
    genres:   List[str]     = []

class SaveRatingRequest(BaseModel):
    title:        str
    year:         Optional[str]  = None
    overview:     Optional[str]  = None
    genres:       List[str]      = []
    ai_rating:    float
    ai_review:    str
    ai_reasoning: str
    suitability:  Optional[str]  = None
    poster:       Optional[str]  = None

# ── ENDPOINTS ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "3.0.0",
        "tmdb_configured":   bool(TMDB_KEY),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "db_movie_count":    count_tmdb_movies(),
        "db_fetch_complete": _fetch_done,
    }

@app.get("/movies/db")
def get_db_movies(
    page:          int   = Query(1, ge=1),
    per_page:      int   = Query(20, ge=1, le=50),
    genre:         Optional[str]  = None,
    year_gte:      Optional[int]  = None,
    year_lte:      Optional[int]  = None,
    certification: Optional[str]  = None,
    language:      Optional[str]  = None,
    min_rating:    Optional[float]= None,
):
    """Browse the local 100+ movie database with filters and pagination."""
    all_movies = search_tmdb_movies(
        genre=genre, year_gte=year_gte, year_lte=year_lte,
        certification=certification, language=language, min_rating=min_rating,
        limit=500,
    ) if any([genre,year_gte,year_lte,certification,language,min_rating]) else get_all_tmdb_movies(500)

    total = len(all_movies)
    start = (page - 1) * per_page
    end   = start + per_page
    return {
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": max(1, (total + per_page - 1) // per_page),
        "movies": all_movies[start:end],
        "db_fetch_complete": _fetch_done,
    }

@app.get("/movies/user")
def get_user_movies():
    """Return all user-added movies."""
    return {"movies": get_all_user_movies()}

@app.post("/movies/add")
def add_movie(req: AddMovieRequest):
    """Permanently add a movie to the user_movies table."""
    movie_dict = req.dict()
    try:
        new_id = add_user_movie(movie_dict)
        return {"success": True, "id": new_id, "message": f"'{req.title}' added successfully!"}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, f"Failed to add movie: {e}")

@app.post("/movies/rate")
async def rate_movie(req: RateMovieRequest):
    """
    Use the LLM (or rule-based fallback) to generate an AI rating + review
    for a user-specified movie. Saves a draft to ai_ratings table.
    """
    title    = req.title.strip()
    year_str = f" ({req.year})" if req.year else ""
    genres_str = ", ".join(req.genres) if req.genres else "Unknown"

    # First try to find it in our DB for context
    db_matches = search_tmdb_movies(limit=3)  # broad search by title substring
    overview_ctx = req.overview or ""

    # Try to fetch from TMDB if we have the key
    tmdb_info = {}
    if TMDB_KEY:
        try:
            r = req_lib.get(f"{TMDB_BASE}/search/movie",
                            params={"api_key": TMDB_KEY, "query": title, "year": req.year or ""},
                            timeout=8)
            if r.status_code == 200:
                results = r.json().get("results", [])
                if results:
                    m = results[0]
                    tmdb_info = {
                        "tmdb_rating": round(m.get("vote_average", 0), 1),
                        "vote_count":  m.get("vote_count", 0),
                        "overview":    m.get("overview", ""),
                        "poster":      f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
                        "year":        m.get("release_date","")[:4],
                    }
                    overview_ctx = tmdb_info["overview"] or overview_ctx
        except Exception as e:
            logger.warning("TMDB search for rating: %s", e)

    # Build AI rating via LLM if available, else rule-based
    openai_key = os.getenv("OPENAI_API_KEY","")
    if openai_key:
        try:
            ai_result = _llm_rate_movie(title, req.year, overview_ctx, req.genres, tmdb_info, openai_key)
        except Exception as e:
            logger.warning("LLM rating failed, using rule-based: %s", e)
            ai_result = _rule_based_rating(title, req.year, overview_ctx, req.genres, tmdb_info)
    else:
        ai_result = _rule_based_rating(title, req.year, overview_ctx, req.genres, tmdb_info)

    # Persist to ai_ratings
    ai_result["title"] = title; ai_result["year"] = req.year
    rating_id = save_ai_rating(ai_result)

    return {
        "success":      True,
        "rating_id":    rating_id,
        "title":        title,
        "year":         req.year or tmdb_info.get("year",""),
        "ai_rating":    ai_result["ai_rating"],
        "ai_review":    ai_result["ai_review"],
        "ai_reasoning": ai_result["ai_reasoning"],
        "genre_tags":   ai_result["genre_tags"],
        "suitability":  ai_result["suitability"],
        "tmdb_rating":  tmdb_info.get("tmdb_rating"),
        "poster":       tmdb_info.get("poster"),
        "overview":     overview_ctx,
    }

def _llm_rate_movie(title, year, overview, genres, tmdb_info, openai_key) -> dict:
    """Call OpenAI to generate a structured movie rating."""
    import openai
    client = openai.OpenAI(api_key=openai_key)
    tmdb_ctx = f"TMDB community rating: {tmdb_info.get('tmdb_rating',0)}/10 ({tmdb_info.get('vote_count',0):,} votes). " if tmdb_info else ""
    prompt = f"""You are an expert film critic. Rate and review the following movie.

Movie: {title} {f'({year})' if year else ''}
Genres: {', '.join(genres) if genres else 'Unknown'}
Overview: {overview or 'Not provided'}
{tmdb_ctx}

Respond ONLY with valid JSON in this exact format:
{{
  "ai_rating": <float 0-10, one decimal place>,
  "ai_review": "<2-3 sentence review>",
  "ai_reasoning": "<why this rating — consider plot, performances, impact, genre conventions>",
  "genre_tags": ["<tag1>","<tag2>","<tag3>"],
  "suitability": "<who should watch this: e.g. 'Fans of psychological horror, adults 18+'>"
}}"""
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),
        messages=[{"role":"user","content":prompt}],
        max_tokens=400, temperature=0.7,
    )
    raw = resp.choices[0].message.content.strip()
    # strip markdown fences if present
    raw = re.sub(r"```json\s*|\s*```","",raw).strip()
    return json.loads(raw)

def _rule_based_rating(title, year, overview, genres, tmdb_info) -> dict:
    """Deterministic rating when no OpenAI key is available."""
    base = tmdb_info.get("tmdb_rating", 0)
    if not base:
        # simple heuristic from overview length + genre
        base = 6.5 + (0.5 if "horror" in " ".join(genres).lower() else 0)
        base = round(min(base, 9.0), 1)

    genre_tags = genres[:3] if genres else ["Drama"]
    year_int   = int(year) if year and year.isdigit() else 2000
    decade     = f"{(year_int//10)*10}s"

    review = (
        f"{title} is a {' / '.join(genre_tags)} film"
        f"{f' from the {decade}' if year else ''}. "
        f"{'The film delivers solid genre thrills with memorable moments. ' if base >= 7 else 'A mixed bag with some interesting elements but uneven execution. '}"
        f"{'Highly recommended for genre fans.' if base >= 7.5 else 'Worth a watch for curious viewers.'}"
    )
    reasoning = (
        f"Based on TMDB community data ({tmdb_info.get('vote_count',0):,} votes) "
        f"and genre conventions for {' / '.join(genre_tags)}, "
        f"the film scores {base}/10. "
        f"{'Strong narrative and technical execution evident.' if base >= 7 else 'Some narrative inconsistencies noted.'}"
    ) if tmdb_info else f"Rule-based estimate for {title}: {base}/10 based on genre conventions."

    return {
        "ai_rating":    base,
        "ai_review":    review,
        "ai_reasoning": reasoning,
        "genre_tags":   genre_tags,
        "suitability":  f"Recommended for fans of {', '.join(genre_tags)}. {'Adults 18+' if 'Horror' in genre_tags or 'Thriller' in genre_tags else 'General audiences'}.",
    }

@app.post("/movies/save-rating")
def save_rating_to_db(req: SaveRatingRequest):
    """Promote an AI-rated movie into the permanent user_movies table."""
    movie_dict = {
        "title":        req.title,
        "year":         req.year,
        "rating":       req.ai_rating,
        "overview":     req.overview,
        "genres":       req.genres,
        "certification":None,
        "language":     "en",
        "poster":       req.poster,
        "ai_review":    req.ai_review,
        "ai_rating":    req.ai_rating,
        "ai_reasoning": req.ai_reasoning,
        "added_by":     "ai_rated",
    }
    try:
        new_id = add_user_movie(movie_dict)
        return {"success": True, "id": new_id, "message": f"'{req.title}' saved to your movie collection!"}
    except Exception as e:
        raise HTTPException(500, f"Save failed: {e}")

@app.post("/recommend")
async def recommend(req: RecommendRequest):
    query = req.query.strip()
    if not query: raise HTTPException(400, "Query cannot be empty")
    t0 = time.time()
    constraints = extract_constraints(query)

    try:
        # ── Search DB first (fast, no API cost) ──────────────────────────────
        tmdb_db_results, user_results = _combined_search(constraints)

        # ── Also do a live TMDB call for freshness ────────────────────────────
        live_results = []
        if TMDB_KEY:
            live_results = discover_movies_live(
                genre_id=constraints.get("genre_id"),
                year_gte=constraints.get("year_gte"),
                year_lte=constraints.get("year_lte"),
                certification=constraints.get("certification"),
                language=constraints.get("language"),
                min_rating=constraints.get("min_rating"),
                watch_provider_id=constraints.get("watch_provider_id"),
                top_n=constraints.get("top_n",10),
            )

        # Merge: live results first, then DB fills gaps, deduplicate by title
        seen_titles = set()
        merged_tmdb = []
        for m in (live_results + tmdb_db_results):
            key = m.get("title","").lower().strip()
            if key not in seen_titles:
                seen_titles.add(key)
                merged_tmdb.append(m)

        top_n = constraints.get("top_n", 10)
        final_tmdb  = merged_tmdb[:top_n]
        final_user  = user_results[:3]

        # ── ReAct Agent (optional) ────────────────────────────────────────────
        if req.use_agent and os.getenv("OPENAI_API_KEY"):
            executor = get_executor()
            result   = executor.invoke({"input": query})
            final_answer = result.get("output","")
            trace_steps  = [{"step":i+1,
                              "thought": f"Reasoning about: {query}",
                              "action": getattr(a,"tool","search_movies_tool"),
                              "action_input": getattr(a,"tool_input",{}),
                              "observation": str(o)[:600]}
                             for i,(a,o) in enumerate(result.get("intermediate_steps",[]))]
            mode = "react_agent"
        else:
            all_movies = final_tmdb + final_user
            if all_movies:
                lines = "\n".join(
                    f"{'🟡 USER' if m.get('source')=='user' else '🎬 TMDB'} {i+1}. {m['title']} "
                    f"({m.get('year','?')}) — ⭐ {m.get('ai_rating') or m.get('rating',0)}/10"
                    for i,m in enumerate(all_movies)
                )
                final_answer = f"Based on {'TMDB live data' if live_results else 'local database'}, here are your recommendations:\n\n{lines}"
            else:
                final_answer = "No movies found. Try different genre, year, or relaxing filters."

            trace_steps = [{
                "step":1,
                "thought": f"Parsed query → constraints: {json.dumps(constraints, default=str)}",
                "action": "combined_search (TMDB Live + Local DB + User Movies)",
                "action_input": constraints,
                "observation": (
                    f"TMDB live: {len(live_results)} | "
                    f"DB cache: {len(tmdb_db_results)} | "
                    f"User movies: {len(user_results)} | "
                    f"Total after dedup: {len(final_tmdb)+len(final_user)}"
                ),
            }]
            mode = "tmdb_direct"

        elapsed = round(time.time()-t0, 2)
        return {
            "success":        True,
            "query":          query,
            "mode":           mode,
            "final_answer":   final_answer,
            "movies":         final_tmdb,
            "user_movies":    final_user,
            "constraints":    constraints,
            "trace":          trace_steps,
            "elapsed_seconds":elapsed,
            "sources": {
                "live_tmdb_count": len(live_results),
                "db_cache_count":  len(tmdb_db_results),
                "user_count":      len(user_results),
            },
        }
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, f"Recommend error: {e}")

@app.get("/genres")
def get_genres():
    return {"genres": [{"id":k,"name":v} for k,v in GENRE_ID_TO_NAME.items()]}

@app.get("/trending")
def get_trending():
    if not TMDB_KEY: return {"movies":[]}
    try:
        r = req_lib.get(f"{TMDB_BASE}/trending/movie/week",
                        params={"api_key":TMDB_KEY}, timeout=8)
        if r.status_code == 200:
            movies = [_parse_tmdb_result(m) for m in r.json().get("results",[])[:12]]
            return {"movies": movies}
    except Exception as e:
        logger.error("Trending: %s", e)
    return {"movies":[]}

@app.get("/ai-ratings")
def get_ai_ratings():
    return {"ratings": get_recent_ai_ratings(20)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=True)

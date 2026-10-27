"""
data/database.py
================
SQLite-based persistent storage for:
  1. Cached TMDB movies (100+ batch-fetched)
  2. User-added movies
  3. AI-generated ratings/reviews

All tables persist across restarts. Thread-safe via connection-per-call pattern.
"""
from __future__ import annotations
import sqlite3, json, os, logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger("movie_react_agent.db")

DB_PATH = Path(__file__).parent / "movies.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create all tables if they don't exist."""
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS tmdb_movies (
            id            INTEGER PRIMARY KEY,
            tmdb_id       INTEGER UNIQUE,
            title         TEXT NOT NULL,
            year          TEXT,
            rating        REAL DEFAULT 0,
            vote_count    INTEGER DEFAULT 0,
            overview      TEXT,
            poster        TEXT,
            backdrop      TEXT,
            genres        TEXT,   -- JSON array
            certification TEXT,
            language      TEXT,
            runtime       INTEGER,
            director      TEXT,
            cast_list     TEXT,   -- JSON array
            tagline       TEXT,
            tmdb_url      TEXT,
            fetched_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS user_movies (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            title         TEXT NOT NULL,
            year          TEXT,
            rating        REAL DEFAULT 0,
            overview      TEXT,
            genres        TEXT,   -- JSON array
            certification TEXT,
            language      TEXT DEFAULT 'en',
            poster        TEXT,
            director      TEXT,
            added_by      TEXT DEFAULT 'user',
            ai_review     TEXT,
            ai_rating     REAL,
            ai_reasoning  TEXT,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS ai_ratings (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            movie_title   TEXT NOT NULL,
            movie_year    TEXT,
            ai_rating     REAL,
            ai_review     TEXT,
            ai_reasoning  TEXT,
            genre_tags    TEXT,
            suitability   TEXT,
            saved_to_db   INTEGER DEFAULT 0,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_tmdb_title   ON tmdb_movies(title);
        CREATE INDEX IF NOT EXISTS idx_user_title   ON user_movies(title);
        CREATE INDEX IF NOT EXISTS idx_tmdb_genre   ON tmdb_movies(genres);
        CREATE INDEX IF NOT EXISTS idx_tmdb_rating  ON tmdb_movies(rating);
        """)
    logger.info("DB initialised at %s", DB_PATH)


# ── TMDB cache operations ─────────────────────────────────────────────────────

def upsert_tmdb_movies(movies: list[dict]) -> int:
    """Insert or update a batch of TMDB movies. Returns count saved."""
    saved = 0
    with get_conn() as conn:
        for m in movies:
            try:
                conn.execute("""
                    INSERT INTO tmdb_movies
                        (tmdb_id,title,year,rating,vote_count,overview,poster,backdrop,
                         genres,certification,language,runtime,director,cast_list,tagline,tmdb_url)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(tmdb_id) DO UPDATE SET
                        rating=excluded.rating, vote_count=excluded.vote_count,
                        overview=excluded.overview, poster=excluded.poster,
                        fetched_at=CURRENT_TIMESTAMP
                """, (
                    m.get("id"), m.get("title",""), m.get("year",""),
                    m.get("rating",0), m.get("vote_count",0), m.get("overview",""),
                    m.get("poster"), m.get("backdrop"),
                    json.dumps(m.get("genres",[])),
                    m.get("certification"), m.get("language","en"),
                    m.get("runtime"), m.get("director"),
                    json.dumps(m.get("cast",[])),
                    m.get("tagline",""), m.get("tmdb_url","")
                ))
                saved += 1
            except Exception as e:
                logger.warning("Upsert failed for %s: %s", m.get("title"), e)
    return saved


def count_tmdb_movies() -> int:
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM tmdb_movies").fetchone()[0]


def search_tmdb_movies(
    genre: Optional[str] = None,
    year_gte: Optional[int] = None,
    year_lte: Optional[int] = None,
    certification: Optional[str] = None,
    language: Optional[str] = None,
    min_rating: Optional[float] = None,
    limit: int = 20,
) -> list[dict]:
    clauses, params = [], []
    if genre:
        clauses.append("genres LIKE ?"); params.append(f"%{genre}%")
    if year_gte:
        clauses.append("CAST(year AS INTEGER) >= ?"); params.append(year_gte)
    if year_lte:
        clauses.append("CAST(year AS INTEGER) <= ?"); params.append(year_lte)
    if certification:
        clauses.append("certification = ?"); params.append(certification)
    if language:
        clauses.append("language = ?"); params.append(language)
    if min_rating:
        clauses.append("rating >= ?"); params.append(min_rating)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql   = f"SELECT * FROM tmdb_movies {where} ORDER BY rating DESC LIMIT ?"
    params.append(limit)

    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_tmdb_row_to_dict(r) for r in rows]


def get_all_tmdb_movies(limit: int = 200) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM tmdb_movies ORDER BY rating DESC LIMIT ?", (limit,)).fetchall()
    return [_tmdb_row_to_dict(r) for r in rows]


def _tmdb_row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["genres"]    = json.loads(d.get("genres") or "[]")
    d["cast"]      = json.loads(d.get("cast_list") or "[]")
    d["source"]    = "tmdb"
    return d


# ── User movie operations ─────────────────────────────────────────────────────

def add_user_movie(movie: dict) -> int:
    """Insert a user-added movie. Returns new row id."""
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO user_movies
                (title,year,rating,overview,genres,certification,language,poster,director,ai_review,ai_rating,ai_reasoning)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            movie.get("title",""), movie.get("year",""),
            movie.get("rating",0), movie.get("overview",""),
            json.dumps(movie.get("genres",[])),
            movie.get("certification",""), movie.get("language","en"),
            movie.get("poster",""), movie.get("director",""),
            movie.get("ai_review"), movie.get("ai_rating"),
            movie.get("ai_reasoning"),
        ))
        return cur.lastrowid


def get_all_user_movies() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM user_movies ORDER BY created_at DESC").fetchall()
    return [_user_row_to_dict(r) for r in rows]


def search_user_movies(
    genre: Optional[str] = None,
    year_gte: Optional[int] = None,
    year_lte: Optional[int] = None,
    certification: Optional[str] = None,
    min_rating: Optional[float] = None,
    limit: int = 20,
) -> list[dict]:
    clauses, params = [], []
    if genre:
        clauses.append("genres LIKE ?"); params.append(f"%{genre}%")
    if year_gte:
        clauses.append("CAST(year AS INTEGER) >= ?"); params.append(year_gte)
    if year_lte:
        clauses.append("CAST(year AS INTEGER) <= ?"); params.append(year_lte)
    if certification:
        clauses.append("certification = ?"); params.append(certification)
    if min_rating:
        clauses.append("COALESCE(ai_rating, rating) >= ?"); params.append(min_rating)

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql   = f"SELECT * FROM user_movies {where} ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    with get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_user_row_to_dict(r) for r in rows]


def _user_row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["genres"] = json.loads(d.get("genres") or "[]")
    d["source"] = "user"
    return d


# ── AI rating operations ──────────────────────────────────────────────────────

def save_ai_rating(data: dict) -> int:
    with get_conn() as conn:
        cur = conn.execute("""
            INSERT INTO ai_ratings (movie_title,movie_year,ai_rating,ai_review,ai_reasoning,genre_tags,suitability,saved_to_db)
            VALUES (?,?,?,?,?,?,?,0)
        """, (data.get("title"), data.get("year"), data.get("ai_rating"),
              data.get("ai_review"), data.get("ai_reasoning"),
              json.dumps(data.get("genre_tags",[])), data.get("suitability","")))
        return cur.lastrowid


def get_recent_ai_ratings(limit: int = 20) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM ai_ratings ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]

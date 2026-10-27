"""utils/helpers.py — Constraint extraction, logging, formatting."""
from __future__ import annotations
import logging, os, re, sys
from pathlib import Path
from typing import Optional

def setup_logging() -> logging.Logger:
    log_level = getattr(logging, os.getenv("LOG_LEVEL","INFO").upper(), logging.INFO)
    log_file  = os.getenv("LOG_FILE", "logs/agent.log")
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    logging.basicConfig(level=log_level, format=fmt,
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(log_file, encoding="utf-8")])
    return logging.getLogger("movie_react_agent")

logger = setup_logging()

GENRE_MAP: dict[str, int] = {
    "action":28,"adventure":12,"animation":16,"comedy":35,"crime":80,
    "documentary":99,"drama":18,"family":10751,"fantasy":14,"history":36,
    "horror":27,"music":10402,"mystery":9648,"romance":10749,
    "science fiction":878,"sci-fi":878,"scifi":878,"thriller":53,"war":10752,"western":37,
}
CERTIFICATION_MAP = {"g":"G","pg":"PG","pg13":"PG-13","pg-13":"PG-13","r":"R","nc17":"NC-17","nc-17":"NC-17"}
LANGUAGE_MAP = {"english":"en","hindi":"hi","japanese":"ja","korean":"ko","french":"fr","spanish":"es","german":"de","tamil":"ta","telugu":"te"}
STREAMING_MAP = {"netflix":8,"amazon prime":9,"prime video":9,"disney+":337,"disney plus":337,"hulu":15,"max":384,"hbo max":384}

def extract_year_range(text: str) -> tuple[Optional[int], Optional[int]]:
    text = text.lower()
    m = re.search(r"\b(19|20)?(\d0)s\b", text)
    if m:
        prefix = m.group(1) or ("20" if int(m.group(2)) < 20 else "19")
        if not m.group(1) and m.group(2) == "20": prefix = "20"
        start = int(prefix + m.group(2))
        return (start, start + 9)
    m2 = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    if m2: y = int(m2.group(1)); return (y, y)
    return (None, None)

def extract_genre_id(text: str) -> Optional[int]:
    t = text.lower()
    for name, gid in GENRE_MAP.items():
        if name in t: return gid
    return None

def extract_certification(text: str) -> Optional[str]:
    t = text.lower().replace(" ","")
    for alias, cert in CERTIFICATION_MAP.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", t): return cert
    return None

def extract_language(text: str) -> Optional[str]:
    t = text.lower()
    for name, code in LANGUAGE_MAP.items():
        if name in t: return code
    return None

def extract_streaming_provider(text: str) -> Optional[int]:
    t = text.lower()
    for name, pid in STREAMING_MAP.items():
        if name in t: return pid
    return None

def extract_min_rating(text: str) -> Optional[float]:
    m = re.search(r"(?:above|over|minimum|min\s+rating(?:\s+of)?)\s+(\d+(?:\.\d+)?)", text.lower())
    return float(m.group(1)) if m else None

def extract_top_n(text: str) -> int:
    m = re.search(r"\btop\s+(\d+)\b|\b(\d+)\s+(?:movies?|films?|recommendations?)\b", text.lower())
    if m: return max(1, min(int(m.group(1) or m.group(2)), 20))
    return 5

def format_movie_results(movies: list[dict]) -> str:
    if not movies: return "No movies found matching the given criteria."
    lines = ["=" * 55, f"Found {len(movies)} movie(s):", "=" * 55]
    for i, m in enumerate(movies, 1):
        year = m.get("release_date","")[:4] or "N/A"
        lines.append(f"\n{i}. {m.get('title','?')} ({year})\n"
                     f"   Rating  : {m.get('vote_average',0)}/10 ({m.get('vote_count',0):,} votes)\n"
                     f"   TMDB ID : {m.get('id','N/A')}\n"
                     f"   Overview: {m.get('overview','')[:180]}")
    lines.append("=" * 55)
    return "\n".join(lines)

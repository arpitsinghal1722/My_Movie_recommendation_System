"""evaluation/mock_agent.py — Deterministic mock agent (no API keys needed)."""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evaluation.deepeval_compat import ToolCall
from utils.helpers import extract_year_range, extract_genre_id, extract_certification
from utils.helpers import extract_language, extract_min_rating, extract_top_n, extract_streaming_provider
from typing import Optional

_POOL = [
    {"id":274,   "title":"The Silence of the Lambs","release_date":"1991-02-14","vote_average":8.3,"vote_count":15000,"genre_ids":[27,53],"overview":"A young FBI trainee seeks help from imprisoned cannibal Hannibal Lecter to catch a serial killer.","original_language":"en"},
    {"id":4232,  "title":"Scream",                  "release_date":"1996-12-20","vote_average":7.3,"vote_count":5000, "genre_ids":[27],   "overview":"A teen is targeted by a masked killer who plays games based on horror films.","original_language":"en"},
    {"id":807,   "title":"Se7en",                   "release_date":"1995-09-22","vote_average":8.6,"vote_count":22000,"genre_ids":[27,53,80],"overview":"Two detectives hunt a serial killer using the seven deadly sins as his motif.","original_language":"en"},
    {"id":694,   "title":"The Shining",             "release_date":"1980-05-23","vote_average":8.4,"vote_count":19000,"genre_ids":[27],   "overview":"A writer begins to lose his mind while caretaking an isolated hotel.","original_language":"en"},
    {"id":539,   "title":"Psycho",                  "release_date":"1960-09-08","vote_average":8.5,"vote_count":15000,"genre_ids":[27,53],"overview":"A secretary on the run checks into a remote motel with a disturbing owner.","original_language":"en"},
    {"id":348,   "title":"Alien",                   "release_date":"1979-05-25","vote_average":8.1,"vote_count":12000,"genre_ids":[27,878],"overview":"A crew discovers a deadly extraterrestrial life form on an alien world.","original_language":"en"},
    {"id":105,   "title":"Back to the Future",      "release_date":"1985-07-03","vote_average":8.5,"vote_count":24000,"genre_ids":[12,35,878],"overview":"Marty McFly accidentally travels back in time using a scientist's DeLorean.","original_language":"en"},
    {"id":862,   "title":"Toy Story",               "release_date":"1995-10-30","vote_average":8.3,"vote_count":18000,"genre_ids":[16,10751,35],"overview":"A cowboy doll feels threatened when a new spaceman toy becomes the favourite.","original_language":"en"},
    {"id":11,    "title":"Star Wars: A New Hope",   "release_date":"1977-05-25","vote_average":8.6,"vote_count":20000,"genre_ids":[12,28,878],"overview":"Luke Skywalker joins rebels to rescue a princess and defeat the Empire.","original_language":"en"},
    {"id":157336,"title":"Interstellar",            "release_date":"2014-11-05","vote_average":8.4,"vote_count":32000,"genre_ids":[12,18,878],"overview":"Explorers travel through a wormhole in space to find a new home for humanity.","original_language":"en"},
    {"id":238,   "title":"The Godfather",           "release_date":"1972-03-14","vote_average":9.2,"vote_count":18000,"genre_ids":[18,80], "overview":"An aging patriarch transfers control of his crime dynasty to his reluctant son.","original_language":"en"},
    {"id":680,   "title":"Pulp Fiction",            "release_date":"1994-09-10","vote_average":8.9,"vote_count":25000,"genre_ids":[80,53], "overview":"The lives of mob hitmen, a boxer, and others interweave in Los Angeles.","original_language":"en"},
    {"id":278,   "title":"The Shawshank Redemption","release_date":"1994-09-23","vote_average":9.3,"vote_count":24000,"genre_ids":[18,80], "overview":"Two imprisoned men bond over years, finding hope through acts of decency.","original_language":"en"},
    {"id":120,   "title":"The Lord of the Rings",   "release_date":"2001-12-19","vote_average":8.8,"vote_count":22000,"genre_ids":[12,14,28],"overview":"A hobbit embarks on a dangerous quest to destroy an evil ring.","original_language":"en"},
    {"id":550,   "title":"Fight Club",              "release_date":"1999-10-15","vote_average":8.8,"vote_count":26000,"genre_ids":[18,53], "overview":"An insomniac and a soap salesman build an underground fight club.","original_language":"en"},
    {"id":13,    "title":"Forrest Gump",            "release_date":"1994-07-06","vote_average":8.8,"vote_count":24000,"genre_ids":[35,18,10749],"overview":"A man with low IQ witnesses and influences several defining historical moments.","original_language":"en"},
    {"id":19404, "title":"Dilwale Dulhania Le Jayenge","release_date":"1995-10-20","vote_average":8.0,"vote_count":4000,"genre_ids":[10749,18],"overview":"Two people fall in love in Europe; the girl's father orders her to marry another.","original_language":"hi"},
    {"id":37799, "title":"3 Idiots",               "release_date":"2009-12-25","vote_average":8.4,"vote_count":5000, "genre_ids":[35,18], "overview":"Two friends search for their lost companion while recalling their college days.","original_language":"hi"},
    {"id":129,   "title":"Spirited Away",           "release_date":"2001-07-20","vote_average":8.5,"vote_count":14000,"genre_ids":[16,10751,14],"overview":"A girl enters a mysterious spirit world and must work to free herself and parents.","original_language":"ja"},
    {"id":4935,  "title":"Howl's Moving Castle",   "release_date":"2004-11-19","vote_average":8.4,"vote_count":10000,"genre_ids":[16,10751,14],"overview":"A young woman cursed by a witch finds refuge in a magical moving castle.","original_language":"ja"},
    {"id":77338, "title":"The Intouchables",       "release_date":"2011-11-02","vote_average":8.5,"vote_count":17000,"genre_ids":[35,18], "overview":"A paralyzed aristocrat and his caregiver from the projects form an unlikely bond.","original_language":"fr"},
    {"id":496243,"title":"Parasite",               "release_date":"2019-05-30","vote_average":8.5,"vote_count":16000,"genre_ids":[35,53,18],"overview":"Greed and class discrimination threaten two families' symbiotic relationship.","original_language":"ko"},
    {"id":218,   "title":"The Terminator",         "release_date":"1984-10-26","vote_average":8.0,"vote_count":14000,"genre_ids":[28,878,53],"overview":"A cyborg travels back in time to kill the woman whose son will lead a revolution.","original_language":"en"},
    {"id":27205, "title":"Inception",              "release_date":"2010-07-15","vote_average":8.4,"vote_count":33000,"genre_ids":[28,878,53],"overview":"A thief who steals secrets through dreams is given a chance to clear his record.","original_language":"en"},
    {"id":49026, "title":"The Dark Knight Rises",  "release_date":"2012-07-19","vote_average":8.4,"vote_count":23000,"genre_ids":[28,53],  "overview":"Eight years after Joker's reign, Batman must return to face a new masked terrorist.","original_language":"en"},
    {"id":9806,  "title":"The Incredibles",        "release_date":"2004-11-05","vote_average":8.0,"vote_count":16000,"genre_ids":[28,16,10751],"overview":"A family of superheroes tries to live a quiet suburban life before being called back.","original_language":"en"},
    {"id":14160, "title":"Up",                     "release_date":"2009-05-28","vote_average":8.3,"vote_count":17000,"genre_ids":[16,10751,12],"overview":"An old widower travels to South America in a house lifted by balloons.","original_language":"en"},
    {"id":453,   "title":"A Beautiful Mind",       "release_date":"2001-12-13","vote_average":8.2,"vote_count":11000,"genre_ids":[18],     "overview":"A brilliant mathematician descends into schizophrenia while doing groundbreaking work.","original_language":"en"},
    {"id":70160, "title":"The Hunger Games",       "release_date":"2012-03-23","vote_average":7.2,"vote_count":14000,"genre_ids":[878,12,28],"overview":"In a dystopia, teens fight to the death in a televised government spectacle.","original_language":"en"},
    {"id":510,   "title":"One Flew Over the Cuckoo's Nest","release_date":"1975-11-19","vote_average":8.7,"vote_count":12000,"genre_ids":[18],"overview":"A criminal pleads insanity and is admitted to a mental institution where he clashes with a nurse.","original_language":"en"},
]

def _filter(genre_id, year_gte, year_lte, lang, min_rating, top_n):
    results = []
    for m in _POOL:
        year = int(m["release_date"][:4]) if m.get("release_date") else 0
        if genre_id  and genre_id not in m.get("genre_ids",[]): continue
        if year_gte  and year < year_gte: continue
        if year_lte  and year > year_lte: continue
        if lang      and m.get("original_language") != lang: continue
        if min_rating and m.get("vote_average",0) < min_rating: continue
        results.append(m)
    results.sort(key=lambda x: x.get("vote_average",0), reverse=True)
    return results[:top_n]

def run_mock_agent(query: str, hallucinate: bool = False) -> dict:
    """Run deterministic mock agent. hallucinate=True injects fabricated response for negative tests."""
    year_gte, year_lte = extract_year_range(query)
    genre_id    = extract_genre_id(query)
    cert        = extract_certification(query)
    language    = extract_language(query)
    min_rating  = extract_min_rating(query)
    top_n       = extract_top_n(query)
    provider_id = extract_streaming_provider(query)

    tool_input = {k:v for k,v in {
        "genre_id":genre_id,"year_gte":year_gte,"year_lte":year_lte,
        "certification":cert,"language":language,"min_rating":min_rating,
        "watch_provider_id":provider_id,"top_n":top_n,
    }.items() if v is not None}
    tool_input.setdefault("top_n", top_n)

    movies = _filter(genre_id, year_gte, year_lte, language, min_rating, top_n)
    obs    = f"Found {len(movies)} movie(s):\n" + "\n".join(
        f"{i}. {m['title']} ({m['release_date'][:4]}) Rating:{m['vote_average']}/10 — {m['overview'][:100]}"
        for i,m in enumerate(movies,1)) if movies else "No movies found."

    retrieval_ctx = [
        f"{m['title']} ({m['release_date'][:4]}) — {m['vote_average']}/10. {m['overview']}"
        for m in movies
    ]
    tool_call = ToolCall(name="search_movies_tool",
                         description="Search TMDB for movies using structured filters",
                         input_parameters=tool_input, output=obs[:500])

    if hallucinate:
        output = ("Based on my knowledge: 'Shadow Realm' (1993) — an incredible horror masterpiece "
                  "rated R, 9.9/10, directed by John Phantom. Also 'Night Terror 2' (1997) won 5 Oscars.")
    elif not movies:
        output = "No movies were found matching your criteria. Try relaxing the filters."
    else:
        lines = ["Based on live TMDB data, here are your top movie recommendations:\n"]
        for i,m in enumerate(movies,1):
            yr = m["release_date"][:4]
            lines.append(f"🎬 {i}. {m['title']} ({yr}) — ⭐ {m['vote_average']}/10\n   {m['overview']}\n")
        output = "\n".join(lines)

    return {"output":output, "intermediate_steps":[("search_movies_tool",obs)],
            "tool_input":tool_input, "retrieval_context":retrieval_ctx, "tools_called":[tool_call]}

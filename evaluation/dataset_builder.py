"""evaluation/dataset_builder.py — Build all 50 LLMTestCase objects."""
from __future__ import annotations
import json, logging, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evaluation.deepeval_compat import LLMTestCase, ToolCall
from evaluation.mock_agent import run_mock_agent
from evaluation.config import EvalConfig
logger = logging.getLogger("movie_react_agent.eval.dataset")

# (query, expected_output, hallucinate)
_SPECS = [
    # A: Genre + Decade (10)
    ("Recommend a horror movie from the 90s rated R.",         "Top 90s R-rated horror: The Silence of the Lambs (8.3), Se7en (8.6), Scream (7.3).", False),
    ("Suggest a comedy film from the 80s.",                    "Top 80s comedies: Back to the Future (1985, 8.5).", False),
    ("Give me a sci-fi movie from the 2010s.",                 "Top 2010s sci-fi: Interstellar (2014, 8.4), Inception (2010, 8.4).", False),
    ("Recommend a thriller from the 90s.",                     "Top 90s thrillers: Se7en (1995), Fight Club (1999).", False),
    ("Suggest a drama from the 70s.",                          "Top 70s dramas: The Godfather (1972, 9.2).", False),
    ("Recommend an action movie from the 80s.",                "Top 80s action: The Terminator (1984, 8.0).", False),
    ("Give me a fantasy movie from the 2000s.",                "Top 2000s fantasy: Lord of the Rings (2001, 8.8), Howl's Moving Castle (2004).", False),
    ("Suggest an animated movie for kids from the 90s.",       "Top 90s animation: Toy Story (1995, 8.3).", False),
    ("Recommend a crime movie from the 90s.",                  "Top 90s crime: Pulp Fiction (1994, 8.9), Shawshank Redemption (1994, 9.3).", False),
    ("Give me a romance movie from the 90s.",                  "Top 90s romance: Forrest Gump (1994, 8.8), Dilwale Dulhania Le Jayenge (1995).", False),
    # B: Certification (8)
    ("Suggest a PG-13 sci-fi movie.",                         "PG-13 sci-fi: Star Wars (8.6), Interstellar (8.4).", False),
    ("Recommend a G-rated family animation.",                  "G-rated animation: Toy Story, Up.", False),
    ("Give me a PG adventure movie for children.",             "PG adventure: Back to the Future, The Incredibles.", False),
    ("Suggest an R-rated thriller from the 2000s.",            "R-rated 2000s thrillers: Inception, The Dark Knight Rises.", False),
    ("Recommend an NC-17 drama film.",                         "No movies found. Try relaxing filters.", False),
    ("Give me an R-rated crime drama.",                        "R-rated crime dramas: The Godfather, Pulp Fiction.", False),
    ("Suggest a PG-13 action movie from the 2010s.",           "PG-13 2010s action: Dark Knight Rises, Hunger Games.", False),
    ("Recommend a PG adventure movie from the 2000s.",         "PG 2000s adventure: Lord of the Rings.", False),
    # C: Language (7)
    ("Recommend a Japanese animation movie.",                  "Japanese anime: Spirited Away (2001, 8.5), Howl's Moving Castle (2004, 8.4).", False),
    ("Suggest a Hindi romance film.",                          "Hindi romance: Dilwale Dulhania Le Jayenge (1995, 8.0).", False),
    ("Give me a Korean thriller movie.",                       "Korean thriller: Parasite (2019, 8.5).", False),
    ("Recommend a French comedy drama.",                       "French drama: The Intouchables (2011, 8.5).", False),
    ("Suggest an English horror movie from the 90s.",          "English 90s horror: Silence of the Lambs, Se7en, Scream.", False),
    ("Give me a Hindi comedy movie.",                          "Hindi comedy: 3 Idiots (2009, 8.4).", False),
    ("Recommend a Japanese Studio Ghibli style movie.",        "Japanese animation: Spirited Away, Howl's Moving Castle.", False),
    # D: Rating Threshold (5)
    ("Give me top 3 action movies above 8 rating.",           "Action above 8.0: Star Wars (8.6), Inception (8.4), Dark Knight Rises (8.4).", False),
    ("Recommend a horror movie above 8.5 IMDB rating.",        "Horror above 8.5: The Silence of the Lambs (8.3) — few qualify at 8.5.", False),
    ("Suggest a drama above 9 rating.",                        "Drama above 9.0: Shawshank Redemption (9.3), The Godfather (9.2).", False),
    ("Give me sci-fi movies above 8 rating.",                  "Sci-fi above 8.0: Star Wars (8.6), Interstellar (8.4), Inception (8.4).", False),
    ("Recommend any movie above 9.2 rating.",                  "Above 9.2: The Shawshank Redemption (9.3).", False),
    # E: Streaming Platform (5)
    ("Suggest a family movie available on Netflix.",            "Family movies (TMDB): Toy Story, The Incredibles.", False),
    ("Recommend a sci-fi movie on Amazon Prime Video.",         "Sci-fi (TMDB): Interstellar, Star Wars.", False),
    ("Give me a Disney+ animated movie.",                       "Animation (TMDB): Toy Story, Up, Spirited Away.", False),
    ("Suggest a horror movie on any streaming platform.",       "Horror (TMDB): Silence of the Lambs, Scream, Se7en.", False),
    ("Recommend a drama movie available on Hulu.",              "Drama (TMDB): Shawshank Redemption, Forrest Gump.", False),
    # F: Multi-Constraint (8)
    ("Recommend a horror movie from the 90s rated R above 7 rating.", "90s R-rated horror >7: Se7en (8.6), Silence of the Lambs (8.3), Scream (7.3).", False),
    ("Give me top 3 sci-fi movies from the 2010s above 7 rating.",   "2010s sci-fi >7: Interstellar (8.4), Inception (8.4), Hunger Games (7.2).", False),
    ("Suggest a Korean thriller above 8 rating from 2015 onwards.",  "Korean thriller >8 post-2015: Parasite (2019, 8.5).", False),
    ("Recommend a Japanese animated family movie above 8 rating.",    "Japanese family animation >8: Spirited Away (8.5), Howl's Moving Castle (8.4).", False),
    ("Give me a PG-13 sci-fi from the 2010s above 7 rating.",        "PG-13 2010s sci-fi >7: Interstellar, Hunger Games.", False),
    ("Suggest a Hindi comedy drama above 8 rating.",                  "Hindi comedy-drama >8: 3 Idiots (8.4).", False),
    ("Give me top 5 drama movies above 9 rating.",                    "Drama >9.0: Shawshank Redemption (9.3), The Godfather (9.2).", False),
    ("Recommend a French drama comedy above 8 rating.",               "French drama >8: The Intouchables (8.5).", False),
    # G: Negative / Edge (7)
    ("Recommend a horror movie from the 90s rated R.",              "HALLUCINATION TEST — fabricated response expected.", True),
    ("Suggest a documentary from the 1800s.",                        "No movies found. Try relaxing filters.", False),
    ("Give me an action movie from the 1920s.",                      "No movies found. Try relaxing filters.", False),
    ("Recommend a movie with no specific genre or year.",            "Top movies: Shawshank Redemption (9.3), Godfather (9.2), Pulp Fiction (8.9).", False),
    ("Suggest a movie in Klingon language.",                         "No movies found. Try relaxing filters.", False),
    ("Give me top 20 comedy movies.",                                "Top comedies: Forrest Gump, Back to the Future, Parasite, 3 Idiots, Intouchables.", False),
    ("Recommend a movie above 9.5 rating from the 80s.",             "No movies found matching 9.5+ rating from the 1980s.", False),
]

def build_dataset(config=None):
    cfg = config or EvalConfig()
    logger.info("Building dataset (%d cases)…", len(_SPECS))
    cases, serial = [], []
    for idx,(query,expected,halluc) in enumerate(_SPECS, 1):
        r = run_mock_agent(query, hallucinate=halluc)
        ctx = [
            "The agent uses TMDB API — never recommends from training data.",
            f"Query: '{query}'",
        ] + r.get("retrieval_context",[])[:3]
        tc = LLMTestCase(
            name=f"case_{idx:02d}",
            input=query,
            actual_output=r["output"],
            expected_output=expected,
            context=ctx,
            retrieval_context=r["retrieval_context"] or None,
            tools_called=r["tools_called"] or None,
            expected_tools=[ToolCall(name="search_movies_tool")],
            additional_metadata={"category":_cat(idx),"hallucinate_flag":halluc,"tool_input":r.get("tool_input",{})},
        )
        cases.append(tc)
        serial.append({"id":idx,"name":f"case_{idx:02d}","category":_cat(idx),"query":query,
                        "actual_output":r["output"],"expected_output":expected,
                        "retrieval_context":r["retrieval_context"],"tool_input":r.get("tool_input",{}),"hallucinate_flag":halluc})
    cfg.golden_dataset_path.write_text(json.dumps(serial,indent=2,ensure_ascii=False),encoding="utf-8")
    logger.info("Dataset saved to %s", cfg.golden_dataset_path)
    return cases

def _cat(idx):
    if idx<=10: return "A_genre_decade"
    if idx<=18: return "B_certification"
    if idx<=25: return "C_language"
    if idx<=30: return "D_rating_threshold"
    if idx<=35: return "E_streaming"
    if idx<=43: return "F_multi_constraint"
    return              "G_negative_edge"

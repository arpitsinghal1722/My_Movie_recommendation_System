# 🎬 Movie ReAct Agent — DeepEval Report
**Generated:** 2026-08-17 05:24:59 | **Status:** ❌ FAIL | **Pass Rate:** 2.0%

## Per-Metric Summary

| Metric | Avg Score | Pass Rate | Threshold | Status |
|--------|-----------|-----------|-----------|--------|
| AnswerRelevancy | 0.105 | 2.0% | 0.70 | ❌ |
| Faithfulness | 1.000 | 100.0% | 0.70 | ✅ |
| Hallucination | 0.136 | 80.0% | 0.30 | ⚠️ |
| ContextualPrecision | 0.980 | 98.0% | 0.60 | ⚠️ |
| ContextualRecall | 0.621 | 66.0% | 0.60 | ❌ |
| ToolUsageVerification | 1.000 | 100.0% | 1.00 | ✅ |
| ConstraintValidation | 1.000 | 100.0% | 0.75 | ✅ |
| InstructionFollowing | 0.984 | 100.0% | 0.70 | ✅ |
| ResponseCompleteness | 0.993 | 100.0% | 0.60 | ✅ |
| HallucinationGuard | 0.980 | 98.0% | 0.90 | ⚠️ |

## By Category
| Category | Pass Rate | Passed/Total |
|----------|-----------|--------------|
| A_genre_decade | 0.0% ❌ | 0/10 |
| B_certification | 12.5% ❌ | 1/8 |
| C_language | 0.0% ❌ | 0/7 |
| D_rating_threshold | 0.0% ❌ | 0/5 |
| E_streaming | 0.0% ❌ | 0/5 |
| F_multi_constraint | 0.0% ❌ | 0/8 |
| G_negative_edge | 0.0% ❌ | 0/7 |

## Detailed Results

### ❌ case_01 [A_genre_decade]
**Query:** Recommend a horror movie from the 90s rated R.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.333 | ❌ | Query tokens in output: 1/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 0.800 | ✅ | Expected tokens in context: 4/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Silence', 'Hannibal Lecter'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Se7en (1995) — ⭐ 8.6/10
   Two detectives hunt a serial killer using the seven

### ❌ case_02 [A_genre_decade]
**Query:** Suggest a comedy film from the 80s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.667 | ✅ | Expected tokens in context: 2/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Marty McFly'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Back to the Future (1985) — ⭐ 8.5/10
   Marty McFly accidentally travels back 

### ❌ case_03 [A_genre_decade]
**Query:** Give me a sci-fi movie from the 2010s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.143 | ✅ | Hallucinated sentences: 1/7 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 1.000 | ✅ | Expected tokens in context: 2/2 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Hunger Games'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Interstellar (2014) — ⭐ 8.4/10
   Explorers travel through a wormhole in space

### ❌ case_04 [A_genre_decade]
**Query:** Recommend a thriller from the 90s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/8 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 4/4 |
| ContextualRecall | 0.667 | ✅ | Expected tokens in context: 2/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~4 movies (top_n=5,available=4), ~4 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Pulp Fiction', 'Los Angeles', 'Fight Club', 'The Silence', 'Hanni |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Pulp Fiction (1994) — ⭐ 8.9/10
   The lives of mob hitmen, a boxer, and others

### ❌ case_05 [A_genre_decade]
**Query:** Suggest a drama from the 70s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.500 | ❌ | Expected tokens in context: 1/2 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Godfather', 'One Flew Over', "Cuckoo's Nest"] found in TMDB c |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Godfather (1972) — ⭐ 9.2/10
   An aging patriarch transfers control of his

### ❌ case_06 [A_genre_decade]
**Query:** Recommend an action movie from the 80s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.500 | ❌ | Expected tokens in context: 1/2 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Terminator'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Terminator (1984) — ⭐ 8.0/10
   A cyborg travels back in time to kill the 

### ❌ case_07 [A_genre_decade]
**Query:** Give me a fantasy movie from the 2000s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.143 | ✅ | Hallucinated sentences: 1/7 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 0.833 | ✅ | Expected tokens in context: 5/6 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Lord', 'Spirited Away', "Howl's Moving Castle"] found in TMDB |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Lord of the Rings (2001) — ⭐ 8.8/10
   A hobbit embarks on a dangerous que

### ❌ case_08 [A_genre_decade]
**Query:** Suggest an animated movie for kids from the 90s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/10 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.000 | ❌ | Expected tokens in context: 0/2 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: year_gte=✅; year_lte=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'Pulp Fiction', 'Los Angeles', 'Fight  |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_09 [A_genre_decade]
**Query:** Recommend a crime movie from the 90s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/6 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 0.800 | ✅ | Expected tokens in context: 4/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'Pulp Fiction', 'Los Angeles'] found i |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_10 [A_genre_decade]
**Query:** Give me a romance movie from the 90s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.200 | ✅ | Hallucinated sentences: 1/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.833 | ✅ | Expected tokens in context: 5/6 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Forrest Gump', 'Dilwale Dulhania Le Jayenge'] found in TMDB conte |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Forrest Gump (1994) — ⭐ 8.8/10
   A man with low IQ witnesses and influences s

### ✅ case_11 [B_certification]
**Query:** Suggest a PG-13 sci-fi movie.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 1.000 | ✅ | Query tokens in output: 1/1 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.100 | ✅ | Hallucinated sentences: 1/10 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 1.000 | ✅ | Expected tokens in context: 3/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Star Wars:', 'New Hope', 'Luke Skywalker', 'Marty McFly'] found i |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Star Wars: A New Hope (1977) — ⭐ 8.6/10
   Luke Skywalker joins rebels to resc

### ❌ case_12 [B_certification]
**Query:** Recommend a G-rated family animation.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.333 | ❌ | Query tokens in output: 1/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/10 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.333 | ❌ | Expected tokens in context: 1/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Spirited Away', "Howl's Moving Castle", 'Toy Story', 'South Ameri |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Spirited Away (2001) — ⭐ 8.5/10
   A girl enters a mysterious spirit world and

### ❌ case_13 [B_certification]
**Query:** Give me a PG adventure movie for children.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.100 | ✅ | Hallucinated sentences: 1/10 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.500 | ❌ | Expected tokens in context: 2/4 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Lord', 'Star Wars:', 'New Hope', 'Luke Skywalker', 'Marty McF |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Lord of the Rings (2001) — ⭐ 8.8/10
   A hobbit embarks on a dangerous que

### ❌ case_14 [B_certification]
**Query:** Suggest an R-rated thriller from the 2000s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/3 |
| Faithfulness | 1.000 | ✅ | No context. |
| Hallucination | 0.000 | ✅ | Short/no context. |
| ContextualPrecision | 1.000 | ✅ | No context. |
| ContextualRecall | 1.000 | ✅ | No expected/context. |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | No results expected; answer correctly says so. |
| HallucinationGuard | 1.000 | ✅ | No context — check skipped. |
> No movies were found matching your criteria. Try relaxing the filters.

### ❌ case_15 [B_certification]
**Query:** Recommend an NC-17 drama film.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/1 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/11 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.000 | ❌ | Expected tokens in context: 0/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather', 'Fight Club', 'Forres |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_16 [B_certification]
**Query:** Give me an R-rated crime drama.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.333 | ❌ | Query tokens in output: 1/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/8 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 4/4 |
| ContextualRecall | 0.667 | ✅ | Expected tokens in context: 4/6 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~4 movies (top_n=5,available=4), ~4 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction', 'Los  |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_17 [B_certification]
**Query:** Suggest a PG-13 action movie from the 2010s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.143 | ✅ | Hallucinated sentences: 1/7 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 0.833 | ✅ | Expected tokens in context: 5/6 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Dark Knight Rises', 'The Hunger Games'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Inception (2010) — ⭐ 8.4/10
   A thief who steals secrets through dreams is gi

### ❌ case_18 [B_certification]
**Query:** Recommend a PG adventure movie from the 2000s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.250 | ✅ | Hallucinated sentences: 1/4 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.667 | ✅ | Expected tokens in context: 2/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Lord', 'South America'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Lord of the Rings (2001) — ⭐ 8.8/10
   A hobbit embarks on a dangerous que

### ❌ case_19 [C_language]
**Query:** Recommend a Japanese animation movie.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.200 | ✅ | Hallucinated sentences: 1/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.714 | ✅ | Expected tokens in context: 5/7 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; language=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Spirited Away', "Howl's Moving Castle"] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Spirited Away (2001) — ⭐ 8.5/10
   A girl enters a mysterious spirit world and

### ❌ case_20 [C_language]
**Query:** Suggest a Hindi romance film.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.600 | ✅ | Expected tokens in context: 3/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; language=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Dilwale Dulhania Le Jayenge'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Dilwale Dulhania Le Jayenge (1995) — ⭐ 8.0/10
   Two people fall in love in Eu

### ❌ case_21 [C_language]
**Query:** Give me a Korean thriller movie.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.333 | ❌ | Expected tokens in context: 1/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; language=✅ |
| InstructionFollowing | 0.800 | ✅ | 4/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles [] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Parasite (2019) — ⭐ 8.5/10
   Greed and class discrimination threaten two fami

### ❌ case_22 [C_language]
**Query:** Recommend a French comedy drama.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.333 | ❌ | Expected tokens in context: 1/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; language=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Intouchables'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Intouchables (2011) — ⭐ 8.5/10
   A paralyzed aristocrat and his caregiver

### ❌ case_23 [C_language]
**Query:** Suggest an English horror movie from the 90s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.333 | ❌ | Query tokens in output: 1/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 0.800 | ✅ | Expected tokens in context: 4/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 4/4 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅; language=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Silence', 'Hannibal Lecter'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Se7en (1995) — ⭐ 8.6/10
   Two detectives hunt a serial killer using the seven

### ❌ case_24 [C_language]
**Query:** Give me a Hindi comedy movie.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.333 | ❌ | Expected tokens in context: 1/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; language=✅ |
| InstructionFollowing | 0.800 | ✅ | 4/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles [] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. 3 Idiots (2009) — ⭐ 8.4/10
   Two friends search for their lost companion whil

### ❌ case_25 [C_language]
**Query:** Recommend a Japanese Studio Ghibli style movie.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/4 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.200 | ✅ | Hallucinated sentences: 1/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.714 | ✅ | Expected tokens in context: 5/7 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: language=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Spirited Away', "Howl's Moving Castle"] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Spirited Away (2001) — ⭐ 8.5/10
   A girl enters a mysterious spirit world and

### ❌ case_26 [D_rating_threshold]
**Query:** Give me top 3 action movies above 8 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.200 | ❌ | Query tokens in output: 1/5 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.143 | ✅ | Hallucinated sentences: 1/7 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 0.375 | ❌ | Expected tokens in context: 3/8 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=3,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Lord', 'Star Wars:', 'New Hope', 'Luke Skywalker'] found in T |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Lord of the Rings (2001) — ⭐ 8.8/10
   A hobbit embarks on a dangerous que

### ❌ case_27 [D_rating_threshold]
**Query:** Recommend a horror movie above 8.5 IMDB rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/4 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.000 | ❌ | Expected tokens in context: 0/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; min_rating=✅ |
| InstructionFollowing | 0.800 | ✅ | 4/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles [] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Se7en (1995) — ⭐ 8.6/10
   Two detectives hunt a serial killer using the seven

### ❌ case_28 [D_rating_threshold]
**Query:** Suggest a drama above 9 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.200 | ✅ | Hallucinated sentences: 1/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.600 | ✅ | Expected tokens in context: 3/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_29 [D_rating_threshold]
**Query:** Give me sci-fi movies above 8 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.250 | ❌ | Query tokens in output: 1/4 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.100 | ✅ | Hallucinated sentences: 1/10 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.800 | ✅ | Expected tokens in context: 4/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Star Wars:', 'New Hope', 'Luke Skywalker', 'Marty McFly'] found i |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Star Wars: A New Hope (1977) — ⭐ 8.6/10
   Luke Skywalker joins rebels to resc

### ❌ case_30 [D_rating_threshold]
**Query:** Recommend any movie above 9.2 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.200 | ✅ | Hallucinated sentences: 1/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.667 | ✅ | Expected tokens in context: 2/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_31 [E_streaming]
**Query:** Suggest a family movie available on Netflix.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.333 | ❌ | Query tokens in output: 1/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/10 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.750 | ✅ | Expected tokens in context: 3/4 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Spirited Away', "Howl's Moving Castle", 'Toy Story', 'South Ameri |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Spirited Away (2001) — ⭐ 8.5/10
   A girl enters a mysterious spirit world and

### ❌ case_32 [E_streaming]
**Query:** Recommend a sci-fi movie on Amazon Prime Video.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.250 | ❌ | Query tokens in output: 1/4 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.100 | ✅ | Hallucinated sentences: 1/10 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.750 | ✅ | Expected tokens in context: 3/4 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Star Wars:', 'New Hope', 'Luke Skywalker', 'Marty McFly'] found i |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Star Wars: A New Hope (1977) — ⭐ 8.6/10
   Luke Skywalker joins rebels to resc

### ❌ case_33 [E_streaming]
**Query:** Give me a Disney+ animated movie.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/11 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.000 | ❌ | Expected tokens in context: 0/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | No constraints detected — full score. |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction', 'Los  |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_34 [E_streaming]
**Query:** Suggest a horror movie on any streaming platform.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/4 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.125 | ✅ | Hallucinated sentences: 1/8 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.400 | ❌ | Expected tokens in context: 2/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shining', 'The Silence', 'Hannibal Lecter'] found in TMDB con |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Se7en (1995) — ⭐ 8.6/10
   Two detectives hunt a serial killer using the seven

### ❌ case_35 [E_streaming]
**Query:** Recommend a drama movie available on Hulu.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/11 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.667 | ✅ | Expected tokens in context: 4/6 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather', 'Fight Club', 'Forres |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_36 [F_multi_constraint]
**Query:** Recommend a horror movie from the 90s rated R above 7 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.200 | ❌ | Query tokens in output: 1/5 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 0.800 | ✅ | Expected tokens in context: 4/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 4/4 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Silence', 'Hannibal Lecter'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Se7en (1995) — ⭐ 8.6/10
   Two detectives hunt a serial killer using the seven

### ❌ case_37 [F_multi_constraint]
**Query:** Give me top 3 sci-fi movies from the 2010s above 7 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.167 | ❌ | Query tokens in output: 1/6 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.143 | ✅ | Hallucinated sentences: 1/7 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 1.000 | ✅ | Expected tokens in context: 4/4 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 4/4 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=3,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Hunger Games'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Interstellar (2014) — ⭐ 8.4/10
   Explorers travel through a wormhole in space

### ❌ case_38 [F_multi_constraint]
**Query:** Suggest a Korean thriller above 8 rating from 2015 onwards.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/6 |
| Faithfulness | 1.000 | ✅ | No context. |
| Hallucination | 0.000 | ✅ | Short/no context. |
| ContextualPrecision | 1.000 | ✅ | No context. |
| ContextualRecall | 1.000 | ✅ | No expected/context. |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 5/5 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅; language=✅; min_rat |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | No results expected; answer correctly says so. |
| HallucinationGuard | 1.000 | ✅ | No context — check skipped. |
> No movies were found matching your criteria. Try relaxing the filters.

### ❌ case_39 [F_multi_constraint]
**Query:** Recommend a Japanese animated family movie above 8 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/5 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.200 | ✅ | Hallucinated sentences: 1/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.625 | ✅ | Expected tokens in context: 5/8 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: genre_id=✅; language=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Spirited Away', "Howl's Moving Castle"] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Spirited Away (2001) — ⭐ 8.5/10
   A girl enters a mysterious spirit world and

### ❌ case_40 [F_multi_constraint]
**Query:** Give me a PG-13 sci-fi from the 2010s above 7 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/4 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.143 | ✅ | Hallucinated sentences: 1/7 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 3/3 |
| ContextualRecall | 1.000 | ✅ | Expected tokens in context: 3/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 4/4 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~3 movies (top_n=5,available=3), ~3 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Hunger Games'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Interstellar (2014) — ⭐ 8.4/10
   Explorers travel through a wormhole in space

### ❌ case_41 [F_multi_constraint]
**Query:** Suggest a Hindi comedy drama above 8 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/5 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.250 | ❌ | Expected tokens in context: 1/4 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: genre_id=✅; language=✅; min_rating=✅ |
| InstructionFollowing | 0.800 | ✅ | 4/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles [] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. 3 Idiots (2009) — ⭐ 8.4/10
   Two friends search for their lost companion whil

### ❌ case_42 [F_multi_constraint]
**Query:** Give me top 5 drama movies above 9 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.200 | ❌ | Query tokens in output: 1/5 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.200 | ✅ | Hallucinated sentences: 1/5 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 2/2 |
| ContextualRecall | 0.750 | ✅ | Expected tokens in context: 3/4 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 2/2 constraints matched: genre_id=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~2 movies (top_n=5,available=2), ~2 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_43 [F_multi_constraint]
**Query:** Recommend a French drama comedy above 8 rating.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/5 |
| Faithfulness | 1.000 | ✅ | Years in output: {'20'}, matched in context: {'20'} |
| Hallucination | 0.333 | ❌ | Hallucinated sentences: 1/3 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 1/1 |
| ContextualRecall | 0.333 | ❌ | Expected tokens in context: 1/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: genre_id=✅; language=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~1 movies (top_n=5,available=1), ~1 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Intouchables'] found in TMDB context |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Intouchables (2011) — ⭐ 8.5/10
   A paralyzed aristocrat and his caregiver

### ❌ case_44 [G_negative_edge]
**Query:** Recommend a horror movie from the 90s rated R.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.667 | ❌ | Query tokens in output: 2/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19'}, matched in context: {'19'} |
| Hallucination | 0.667 | ❌ | Hallucinated sentences: 2/3 |
| ContextualPrecision | 0.000 | ❌ | Context chunks used: 0/3 |
| ContextualRecall | 0.000 | ❌ | Expected tokens in context: 0/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 0.667 | ✅ | Expected ~3 movies (top_n=5,available=3), ~2 detected. |
| HallucinationGuard | 0.000 | ❌ | ❌ Hallucinated titles: ["Shadow Realm'", 'John Phantom', 'Night Terror'] (not in |
> Based on my knowledge: 'Shadow Realm' (1993) — an incredible horror masterpiece rated R, 9.9/10, directed by John Phantom. Also 'Night Terror 2' (1997

### ❌ case_45 [G_negative_edge]
**Query:** Suggest a documentary from the 1800s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | No context. |
| Hallucination | 0.000 | ✅ | Short/no context. |
| ContextualPrecision | 1.000 | ✅ | No context. |
| ContextualRecall | 1.000 | ✅ | No expected/context. |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | No results expected; answer correctly says so. |
| HallucinationGuard | 1.000 | ✅ | No context — check skipped. |
> No movies were found matching your criteria. Try relaxing the filters.

### ❌ case_46 [G_negative_edge]
**Query:** Give me an action movie from the 1920s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | No context. |
| Hallucination | 0.000 | ✅ | Short/no context. |
| ContextualPrecision | 1.000 | ✅ | No context. |
| ContextualRecall | 1.000 | ✅ | No expected/context. |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | No results expected; answer correctly says so. |
| HallucinationGuard | 1.000 | ✅ | No context — check skipped. |
> No movies were found matching your criteria. Try relaxing the filters.

### ❌ case_47 [G_negative_edge]
**Query:** Recommend a movie with no specific genre or year.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.333 | ❌ | Query tokens in output: 1/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/11 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 1.000 | ✅ | Expected tokens in context: 5/5 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | No constraints detected — full score. |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction', 'Los  |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_48 [G_negative_edge]
**Query:** Suggest a movie in Klingon language.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/2 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.000 | ✅ | Hallucinated sentences: 0/11 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 5/5 |
| ContextualRecall | 0.000 | ❌ | Expected tokens in context: 0/3 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | No constraints detected — full score. |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~5 movies (top_n=5,available=5), ~5 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['The Shawshank Redemption', 'The Godfather', 'Pulp Fiction', 'Los  |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. The Shawshank Redemption (1994) — ⭐ 9.3/10
   Two imprisoned men bond over yea

### ❌ case_49 [G_negative_edge]
**Query:** Give me top 20 comedy movies.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.333 | ❌ | Query tokens in output: 1/3 |
| Faithfulness | 1.000 | ✅ | Years in output: {'19', '20'}, matched in context: {'19', '20'} |
| Hallucination | 0.077 | ✅ | Hallucinated sentences: 1/13 |
| ContextualPrecision | 1.000 | ✅ | Context chunks used: 6/6 |
| ContextualRecall | 0.875 | ✅ | Expected tokens in context: 7/8 |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 1/1 constraints matched: genre_id=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | Expected ~6 movies (top_n=20,available=6), ~6 detected. |
| HallucinationGuard | 1.000 | ✅ | ✅ All titles ['Forrest Gump', 'Marty McFly', 'The Intouchables', 'Toy Story'] fo |
> Based on live TMDB data, here are your top movie recommendations:

🎬 1. Forrest Gump (1994) — ⭐ 8.8/10
   A man with low IQ witnesses and influences s

### ❌ case_50 [G_negative_edge]
**Query:** Recommend a movie above 9.5 rating from the 80s.
| Metric | Score | Pass | Reason |
|--------|-------|------|--------|
| AnswerRelevancy | 0.000 | ❌ | Query tokens in output: 0/3 |
| Faithfulness | 1.000 | ✅ | No context. |
| Hallucination | 0.000 | ✅ | Short/no context. |
| ContextualPrecision | 1.000 | ✅ | No context. |
| ContextualRecall | 1.000 | ✅ | No expected/context. |
| ToolUsageVerification | 1.000 | ✅ | ✅ search_movies_tool was called (['search_movies_tool']) |
| ConstraintValidation | 1.000 | ✅ | 3/3 constraints matched: year_gte=✅; year_lte=✅; min_rating=✅ |
| InstructionFollowing | 1.000 | ✅ | 5/5 format rules: non_empty=✅; has_year_or_noresults=✅; has_rating_or_noresults= |
| ResponseCompleteness | 1.000 | ✅ | No results expected; answer correctly says so. |
| HallucinationGuard | 1.000 | ✅ | No context — check skipped. |
> No movies were found matching your criteria. Try relaxing the filters.

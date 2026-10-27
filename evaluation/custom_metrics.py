"""
evaluation/custom_metrics.py
==============================
5 project-specific DeepEval metrics (no LLM calls — all rule-based):

1. ToolUsageVerificationMetric  — Did agent call search_movies_tool? (binary 0/1)
2. ConstraintValidationMetric   — Were query constraints correctly mapped to tool params?
3. InstructionFollowingMetric   — Does output have title, year, rating, no refusal phrases?
4. ResponseCompletenessMetric   — Are enough movies returned (matches top_n request)?
5. HallucinationGuardMetric     — Are all movie titles in output grounded in TMDB context?
"""
from __future__ import annotations
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from typing import Optional
from evaluation.deepeval_compat import LLMTestCase, BaseMetric
from utils.helpers import extract_year_range, extract_genre_id, extract_certification, extract_language, extract_min_rating, extract_top_n


class ToolUsageVerificationMetric(BaseMetric):
    """PASS if search_movies_tool appears in tools_called. FAIL = hallucination."""
    def __init__(self, threshold=1.0):
        self.threshold = threshold
        self.score = self.reason = self.success = None

    def measure(self, test_case: LLMTestCase, *a, **kw) -> float:
        tools = [t.name for t in (test_case.tools_called or [])]
        if "search_movies_tool" in tools:
            self.score=1.0; self.success=True
            self.reason=f"✅ search_movies_tool was called ({tools})"
        else:
            self.score=0.0; self.success=False
            self.reason=f"❌ search_movies_tool NOT called — possible hallucination. tools={tools}"
        return self.score

    async def a_measure(self, tc, *a, **kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "ToolUsageVerification"


class ConstraintValidationMetric(BaseMetric):
    """Score = constraints correctly passed to tool / constraints detected in query."""
    def __init__(self, threshold=0.75):
        self.threshold=threshold; self.score=self.reason=self.success=None

    def measure(self, test_case: LLMTestCase, *a, **kw) -> float:
        query      = test_case.input
        tool_input = (test_case.additional_metadata or {}).get("tool_input", {})
        expected   = {}
        yr_gte, yr_lte = extract_year_range(query)
        if yr_gte is not None:
            expected["year_gte"] = tool_input.get("year_gte") == yr_gte
            expected["year_lte"] = tool_input.get("year_lte") == yr_lte
        gid = extract_genre_id(query)
        if gid: expected["genre_id"] = tool_input.get("genre_id") == gid
        cert = extract_certification(query)
        if cert: expected["certification"] = tool_input.get("certification") == cert
        lang = extract_language(query)
        if lang: expected["language"] = tool_input.get("language") == lang
        minr = extract_min_rating(query)
        if minr: expected["min_rating"] = abs((tool_input.get("min_rating") or 0) - minr) < 0.1

        if not expected:
            self.score=1.0; self.success=True; self.reason="No constraints detected — full score."
            return 1.0
        matched = sum(1 for v in expected.values() if v)
        self.score = matched / len(expected)
        self.reason = f"{matched}/{len(expected)} constraints matched: {'; '.join(f'{k}={'✅' if v else '❌'}' for k,v in expected.items())}"
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, tc, *a, **kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "ConstraintValidation"


class InstructionFollowingMetric(BaseMetric):
    """Check output format rules: non-empty, has year, has rating, no refusal phrases, has title."""
    FORBIDDEN = ["i cannot","i can't","i don't have access","i am unable","as an ai","i have no information"]
    YEAR_RE   = re.compile(r"\b(19|20)\d{2}\b")
    RATE_RE   = re.compile(r"\d+\.\d+/10|\d+/10|⭐")
    TITLE_RE  = re.compile(r"[A-Z][a-z]+(?: [A-Z][a-z]+)+")

    def __init__(self, threshold=0.70):
        self.threshold=threshold; self.score=self.reason=self.success=None

    def measure(self, test_case: LLMTestCase, *a, **kw) -> float:
        out = (test_case.actual_output or "").strip()
        lo  = out.lower()
        no_res = any(p in lo for p in ("no movies","not found","could not find","no results"))
        checks = {
            "non_empty":              len(out) > 20,
            "has_year_or_noresults":  bool(self.YEAR_RE.search(out)) or no_res,
            "has_rating_or_noresults":bool(self.RATE_RE.search(out)) or no_res,
            "no_forbidden_phrases":   not any(f in lo for f in self.FORBIDDEN),
            "has_title_or_noresults": bool(self.TITLE_RE.search(out)) or no_res,
        }
        passed = sum(1 for v in checks.values() if v)
        self.score   = passed / len(checks)
        self.reason  = f"{passed}/{len(checks)} format rules: " + "; ".join(f"{k}={'✅' if v else '❌'}" for k,v in checks.items())
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, tc, *a, **kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "InstructionFollowing"


class ResponseCompletenessMetric(BaseMetric):
    """Score = min(movies_returned, expected) / expected. Checks top_n is honoured."""
    def __init__(self, threshold=0.60):
        self.threshold=threshold; self.score=self.reason=self.success=None

    def measure(self, test_case: LLMTestCase, *a, **kw) -> float:
        out       = test_case.actual_output or ""
        ctx       = test_case.retrieval_context or []
        top_n     = extract_top_n(test_case.input)
        available = len(ctx)
        expected  = min(top_n, available) if available else 0
        no_res    = any(p in out.lower() for p in ("no movies","not found","could not find"))
        if expected == 0:
            self.score=1.0 if no_res else 0.3
            self.reason="No results expected; answer " + ("correctly says so." if no_res else "doesn't mention it.")
            self.success = self.score >= self.threshold; return self.score
        year_count = len(re.findall(r"\b(19|20)\d{2}\b", out))
        actual     = min(year_count, expected)
        self.score = min(actual / expected, 1.0)
        self.reason= f"Expected ~{expected} movies (top_n={top_n},available={available}), ~{actual} detected."
        self.success = self.score >= self.threshold
        return self.score

    async def a_measure(self, tc, *a, **kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "ResponseCompleteness"


class HallucinationGuardMetric(BaseMetric):
    """1.0 if all title-case phrases in output found in retrieval context, else 0.0 (strict binary)."""
    _TITLE = re.compile(r"\*{0,2}([A-Z][a-zA-Z':\-]+(?: [A-Z][a-zA-Z':\-]+)+)\*{0,2}")

    def __init__(self, threshold=0.90):
        self.threshold=threshold; self.score=self.reason=self.success=None

    def measure(self, test_case: LLMTestCase, *a, **kw) -> float:
        out = test_case.actual_output or ""
        ctx = " ".join(test_case.retrieval_context or []).lower()
        if not ctx:
            self.score=1.0; self.success=True; self.reason="No context — check skipped."; return 1.0
        candidates = [c for c in self._TITLE.findall(out) if len(c.split()) >= 2]
        hallucinated = [c for c in candidates if c.lower() not in ctx]
        if hallucinated:
            self.score=0.0; self.success=False
            self.reason=f"❌ Hallucinated titles: {hallucinated} (not in TMDB context)"
        else:
            self.score=1.0; self.success=True
            self.reason=f"✅ All titles {candidates} found in TMDB context"
        return self.score

    async def a_measure(self, tc, *a, **kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "HallucinationGuard"


def get_custom_metrics(config=None) -> list:
    from evaluation.config import EvalConfig
    cfg = config or EvalConfig()
    return [
        ToolUsageVerificationMetric(cfg.threshold_for("ToolUsageVerification")),
        ConstraintValidationMetric(cfg.threshold_for("ConstraintValidation")),
        InstructionFollowingMetric(cfg.threshold_for("InstructionFollowing")),
        ResponseCompletenessMetric(cfg.threshold_for("ResponseCompleteness")),
        HallucinationGuardMetric(cfg.threshold_for("HallucinationGuard")),
    ]

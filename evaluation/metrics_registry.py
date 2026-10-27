"""evaluation/metrics_registry.py — All metric instances (built-in + custom)."""
from __future__ import annotations
import re, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evaluation.deepeval_compat import LLMTestCase, BaseMetric
from evaluation.custom_metrics import get_custom_metrics
from evaluation.config import EvalConfig

class _AnswerRelevancy(BaseMetric):
    """Rule-based: fraction of query keywords found in output."""
    def __init__(self, threshold=0.70):
        self.threshold=threshold; self.score=self.reason=self.success=None
    def measure(self, tc: LLMTestCase, *a, **kw):
        stops = {"the","a","an","of","for","from","with","me","give","suggest","recommend","movie","film"}
        tokens = [t for t in re.findall(r"\b\w{3,}\b", tc.input.lower()) if t not in stops]
        if not tokens: self.score=1.0; self.reason="No tokens."; self.success=True; return 1.0
        out  = tc.actual_output.lower()
        found = sum(1 for t in tokens if t in out)
        self.score = found/len(tokens)
        self.reason = f"Query tokens in output: {found}/{len(tokens)}"
        self.success = self.score >= self.threshold; return self.score
    async def a_measure(self,tc,*a,**kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "AnswerRelevancy"

class _Faithfulness(BaseMetric):
    """Rule-based: years in output that also appear in retrieval_context."""
    def __init__(self, threshold=0.70):
        self.threshold=threshold; self.score=self.reason=self.success=None
    def measure(self, tc: LLMTestCase, *a, **kw):
        out = (tc.actual_output or "").lower()
        ctx = " ".join(tc.retrieval_context or []).lower()
        no_res = any(p in out for p in ("no movies","not found","could not find"))
        if not ctx:
            self.score=1.0 if no_res else 0.5; self.reason="No context."; self.success=self.score>=self.threshold; return self.score
        yout = set(re.findall(r"\b(19|20)\d{2}\b", out))
        yctx = set(re.findall(r"\b(19|20)\d{2}\b", ctx))
        if not yout:
            self.score=1.0 if no_res else 0.6; self.reason="No years in output."; self.success=self.score>=self.threshold; return self.score
        matched = yout & yctx
        self.score = len(matched)/len(yout)
        self.reason = f"Years in output: {yout}, matched in context: {matched}"
        self.success = self.score>=self.threshold; return self.score
    async def a_measure(self,tc,*a,**kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "Faithfulness"

class _Hallucination(BaseMetric):
    """Rule-based: fraction of output sentences with zero context overlap (lower=better)."""
    def __init__(self, threshold=0.30):
        self.threshold=threshold; self.score=self.reason=self.success=None
    def measure(self, tc: LLMTestCase, *a, **kw):
        out = tc.actual_output or ""
        ctx = " ".join(tc.retrieval_context or []).lower()
        sents = [s.strip() for s in re.split(r"[.!?\n]",out) if len(s.strip())>20]
        if not sents or not ctx:
            self.score=0.0; self.reason="Short/no context."; self.success=True; return 0.0
        hallu = sum(1 for s in sents if not any(w in ctx for w in re.findall(r"\b\w{4,}\b",s.lower())))
        self.score = hallu/len(sents)
        self.reason = f"Hallucinated sentences: {hallu}/{len(sents)}"
        self.success = self.score<=self.threshold; return self.score
    async def a_measure(self,tc,*a,**kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "Hallucination"

class _ContextualPrecision(BaseMetric):
    """Fraction of context chunks whose title appears in output."""
    def __init__(self, threshold=0.60):
        self.threshold=threshold; self.score=self.reason=self.success=None
    def measure(self, tc: LLMTestCase, *a, **kw):
        out = (tc.actual_output or "").lower(); chunks = tc.retrieval_context or []
        if not chunks: self.score=1.0; self.reason="No context."; self.success=True; return 1.0
        used = sum(1 for c in chunks if c.split("—")[0].strip().lower()[:12] in out)
        self.score=used/len(chunks); self.reason=f"Context chunks used: {used}/{len(chunks)}"
        self.success=self.score>=self.threshold; return self.score
    async def a_measure(self,tc,*a,**kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "ContextualPrecision"

class _ContextualRecall(BaseMetric):
    """Fraction of expected_output tokens found in retrieval_context."""
    def __init__(self, threshold=0.60):
        self.threshold=threshold; self.score=self.reason=self.success=None
    def measure(self, tc: LLMTestCase, *a, **kw):
        exp = (tc.expected_output or "").lower()
        ctx = " ".join(tc.retrieval_context or []).lower()
        if not exp or not ctx: self.score=1.0; self.reason="No expected/context."; self.success=True; return 1.0
        stops = {"from","that","with","this","movie","film","movies","films","here","are","your","top"}
        toks = [t for t in re.findall(r"\b[a-z]{4,}\b", exp) if t not in stops]
        if not toks: self.score=1.0; self.reason="No tokens."; self.success=True; return 1.0
        found = sum(1 for t in toks if t in ctx)
        self.score=found/len(toks); self.reason=f"Expected tokens in context: {found}/{len(toks)}"
        self.success=self.score>=self.threshold; return self.score
    async def a_measure(self,tc,*a,**kw): return self.measure(tc)
    def is_successful(self): return bool(self.success)
    @property
    def __name__(self): return "ContextualRecall"

def get_builtin_metrics(config=None):
    cfg = config or EvalConfig()
    return [
        _AnswerRelevancy(cfg.threshold_for("AnswerRelevancy")),
        _Faithfulness(cfg.threshold_for("Faithfulness")),
        _Hallucination(cfg.threshold_for("Hallucination")),
        _ContextualPrecision(cfg.threshold_for("ContextualPrecision")),
        _ContextualRecall(cfg.threshold_for("ContextualRecall")),
    ]

def get_all_metrics(config=None):
    cfg = config or EvalConfig()
    return get_builtin_metrics(cfg) + get_custom_metrics(cfg)

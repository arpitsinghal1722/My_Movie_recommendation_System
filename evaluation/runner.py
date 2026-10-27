"""evaluation/runner.py — Orchestrates the full evaluation pipeline."""
from __future__ import annotations
import argparse, json, logging, sys, os, time
from dataclasses import dataclass, field, asdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evaluation.deepeval_compat import LLMTestCase, BaseMetric
from evaluation.config import EvalConfig
from evaluation.dataset_builder import build_dataset
from evaluation.metrics_registry import get_all_metrics
logger = logging.getLogger("movie_react_agent.eval.runner")

@dataclass
class MetricResult:
    metric_name: str; score: float; passed: bool; reason: str; threshold: float

@dataclass
class TestCaseResult:
    case_name:str; query:str; category:str; actual_output:str
    metric_results: list = field(default_factory=list)
    overall_passed: bool = False
    def to_dict(self):
        d=asdict(self); d["metric_results"]=[asdict(m) for m in self.metric_results]; return d

@dataclass
class EvaluationResults:
    test_case_results: list; summary: dict; passed: bool; elapsed_seconds: float

def _run_metric(metric, tc, cfg):
    try:
        score = metric.measure(tc)
        reason = getattr(metric,"reason","") or ""
        if metric.__name__ == "Hallucination":
            passed = score <= cfg.threshold_for(metric.__name__)
        else:
            passed = score >= cfg.threshold_for(metric.__name__)
        return MetricResult(metric.__name__, round(score,4), passed, reason, cfg.threshold_for(metric.__name__))
    except Exception as e:
        logger.exception(e)
        return MetricResult(metric.__name__, 0.0, False, f"ERROR:{e}", cfg.threshold_for(metric.__name__))

def run_full_evaluation(config=None):
    cfg = config or EvalConfig()
    t0  = time.time()
    _setup_log(cfg)

    print(f"\n{'='*60}\n🎬 Movie ReAct Agent — DeepEval Evaluation\n{'='*60}")
    print(f"Mode: {'MOCK agent' if cfg.use_mock_agent else 'LIVE agent (real API)'}\n")

    print("📊 Building 50-case dataset…")
    cases = build_dataset(cfg)
    print(f"   ✅ {len(cases)} cases built → {cfg.golden_dataset_path}\n")

    metrics = get_all_metrics(cfg)
    print(f"🔬 {len(metrics)} metrics loaded:")
    for m in metrics: print(f"   • {m.__name__}  (threshold={cfg.threshold_for(m.__name__)})")

    print(f"\n🚀 Running {len(cases)}×{len(metrics)} = {len(cases)*len(metrics)} evaluations…\n")
    tc_results = []
    for i, tc in enumerate(cases, 1):
        cat = (tc.additional_metadata or {}).get("category","?")
        tcr = TestCaseResult(tc.name or f"case_{i}", tc.input, cat, tc.actual_output)
        mrs = []
        for metric in metrics:
            mr = _run_metric(metric, tc, cfg)
            mrs.append(mr)
            if cfg.verbose:
                icon = "✅" if mr.passed else "❌"
                print(f"  [{i:02d}/{len(cases)}] {icon} {mr.metric_name:<30} {mr.score:.3f}  {(mr.reason or '')[:70]}")
        tcr.metric_results = mrs
        tcr.overall_passed = all(mr.passed for mr in mrs)
        tc_results.append(tcr)
        status = "✅ PASS" if tcr.overall_passed else "❌ FAIL"
        print(f"\n  → [{cat}] {status}: {tc.input[:65]}\n")

    summary = _summarise(tc_results, metrics, cfg)
    elapsed = round(time.time()-t0, 2)
    results = EvaluationResults(tc_results, summary, summary["overall_pass_rate"]>=0.70, elapsed)

    _write_reports(results, cfg)
    _print_summary(summary, elapsed, cfg)
    return results

def _summarise(tc_results, metrics, cfg):
    total   = len(tc_results)
    passed  = sum(1 for t in tc_results if t.overall_passed)
    per_m   = {}
    for tc in tc_results:
        for mr in tc.metric_results:
            per_m.setdefault(mr.metric_name,[]).append(mr.score)
    metric_summaries = {}
    for name, scores in per_m.items():
        thr = cfg.threshold_for(name)
        is_h = name=="Hallucination"
        pc   = sum(1 for s in scores if (s<=thr if is_h else s>=thr))
        metric_summaries[name]={"average_score":round(sum(scores)/len(scores),4),"pass_count":pc,"total_count":len(scores),"pass_rate":round(pc/len(scores),4),"threshold":thr}
    by_cat = {}
    for tc in tc_results:
        c = tc.category; by_cat.setdefault(c,{"total":0,"passed":0})
        by_cat[c]["total"]+=1
        if tc.overall_passed: by_cat[c]["passed"]+=1
    for c in by_cat:
        t=by_cat[c]["total"]; by_cat[c]["pass_rate"]=round(by_cat[c]["passed"]/t,4)
    return {"total_cases":total,"passed_cases":passed,"failed_cases":total-passed,
            "overall_pass_rate":round(passed/total,4) if total else 0,
            "per_metric":metric_summaries,"by_category":by_cat}

def _write_reports(results, cfg):
    # JSON
    payload={"summary":results.summary,"overall_passed":results.passed,
             "elapsed_seconds":results.elapsed_seconds,
             "test_cases":[tc.to_dict() for tc in results.test_case_results]}
    cfg.report_json_path.write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"\n📄 JSON → {cfg.report_json_path}")
    # Markdown
    from datetime import datetime
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    s   = results.summary
    pr  = s["overall_pass_rate"]*100
    lines = [
        f"# 🎬 Movie ReAct Agent — DeepEval Report",
        f"**Generated:** {now} | **Status:** {'✅ PASS' if results.passed else '❌ FAIL'} | **Pass Rate:** {pr:.1f}%\n",
        "## Per-Metric Summary\n",
        "| Metric | Avg Score | Pass Rate | Threshold | Status |",
        "|--------|-----------|-----------|-----------|--------|",
    ]
    for name,d in s["per_metric"].items():
        icon="✅" if d["pass_count"]==d["total_count"] else ("⚠️" if d["pass_rate"]>=0.7 else "❌")
        lines.append(f"| {name} | {d['average_score']:.3f} | {d['pass_rate']*100:.1f}% | {d['threshold']:.2f} | {icon} |")
    lines+=["","## By Category","| Category | Pass Rate | Passed/Total |","|----------|-----------|--------------|"]
    for cat,d in s["by_category"].items():
        icon="✅" if d["pass_rate"]>=0.7 else "❌"
        lines.append(f"| {cat} | {d['pass_rate']*100:.1f}% {icon} | {d['passed']}/{d['total']} |")
    lines+=["","## Detailed Results",""]
    for tc in results.test_case_results:
        icon="✅" if tc.overall_passed else "❌"
        lines.append(f"### {icon} {tc.case_name} [{tc.category}]")
        lines.append(f"**Query:** {tc.query}")
        lines.append("| Metric | Score | Pass | Reason |")
        lines.append("|--------|-------|------|--------|")
        for mr in tc.metric_results:
            ri="✅" if mr.passed else "❌"
            lines.append(f"| {mr.metric_name} | {mr.score:.3f} | {ri} | {(mr.reason or '')[:80].replace('|','|')} |")
        lines.append(f"> {tc.actual_output[:150]}\n")
    cfg.report_md_path.write_text("\n".join(lines),encoding="utf-8")
    print(f"📝 Markdown → {cfg.report_md_path}")

def _print_summary(s, elapsed, cfg):
    pr=s["overall_pass_rate"]*100; icon="✅" if pr>=70 else "❌"
    print(f"\n{'='*60}")
    print(f"  {icon} Overall Pass Rate: {pr:.1f}%  ({s['passed_cases']}/{s['total_cases']})  ⏱ {elapsed}s")
    print(f"  {'Metric':<32} {'Avg':>6}  {'Pass%':>6}")
    print(f"  {'-'*48}")
    for name,d in s["per_metric"].items():
        ri="✅" if d["pass_rate"]==1.0 else ("⚠️" if d["pass_rate"]>=0.7 else "❌")
        print(f"  {ri} {name:<30} {d['average_score']:>6.3f}  {d['pass_rate']*100:>5.1f}%")
    print(f"{'='*60}\n")

def _setup_log(cfg):
    fh=logging.FileHandler(cfg.log_path,encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"))
    logging.getLogger("movie_react_agent").addHandler(fh)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--live",   action="store_true")
    p.add_argument("--quiet",  action="store_true")
    args=p.parse_args()
    cfg=EvalConfig(use_mock_agent=not args.live, verbose=not args.quiet)
    r=run_full_evaluation(cfg)
    sys.exit(0 if r.passed else 1)

if __name__=="__main__": main()

"""
evaluation/test_eval_suite.py — pytest-compatible test suite (50+ cases, no API keys needed).

Run: pytest evaluation/test_eval_suite.py -v
"""
import json, sys, os, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evaluation.deepeval_compat import LLMTestCase, ToolCall, BaseMetric
from evaluation.mock_agent import run_mock_agent
from evaluation.custom_metrics import (
    ToolUsageVerificationMetric, ConstraintValidationMetric,
    InstructionFollowingMetric, ResponseCompletenessMetric, HallucinationGuardMetric,
)
from evaluation.metrics_registry import get_builtin_metrics, get_all_metrics
from evaluation.dataset_builder import build_dataset
from evaluation.config import EvalConfig

# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def cfg(): return EvalConfig(use_mock_agent=True, verbose=False)

@pytest.fixture(scope="session")
def dataset(cfg): return build_dataset(cfg)

@pytest.fixture
def horror_tc():
    r = run_mock_agent("Recommend a horror movie from the 90s rated R.")
    return LLMTestCase(input="Recommend a horror movie from the 90s rated R.", actual_output=r["output"],
        retrieval_context=r["retrieval_context"], tools_called=r["tools_called"],
        additional_metadata={"tool_input":r["tool_input"],"hallucinate_flag":False})

@pytest.fixture
def halluc_tc():
    r = run_mock_agent("Recommend a horror movie from the 90s rated R.", hallucinate=True)
    return LLMTestCase(input="Recommend a horror movie from the 90s rated R.", actual_output=r["output"],
        retrieval_context=r["retrieval_context"], tools_called=r["tools_called"],
        additional_metadata={"tool_input":r["tool_input"],"hallucinate_flag":True})

@pytest.fixture
def no_tool_tc():
    return LLMTestCase(input="Recommend a horror movie.", tools_called=[],
        actual_output="I recommend The Blair Witch Project (1999) — great film!",
        retrieval_context=[], additional_metadata={"tool_input":{}})

# ── Group 1: deepeval_compat ─────────────────────────────────────────────────

class TestDeepEvalCompat:
    def test_llm_test_case(self):
        tc = LLMTestCase(input="hi", actual_output="hello")
        assert tc.input == "hi" and tc.actual_output == "hello"

    def test_tool_call(self):
        t = ToolCall(name="search_movies_tool", input_parameters={"genre_id":27})
        assert t.name == "search_movies_tool" and t.input_parameters["genre_id"] == 27

    def test_base_metric_instance(self):
        assert isinstance(ToolUsageVerificationMetric(), BaseMetric)

    def test_context_must_be_list(self):
        with pytest.raises(TypeError):
            LLMTestCase(input="q", actual_output="a", context="bad type")

# ── Group 2: Mock Agent ──────────────────────────────────────────────────────

class TestMockAgent:
    def test_keys_present(self):
        r = run_mock_agent("Horror movie.")
        for k in ("output","tools_called","retrieval_context","tool_input","intermediate_steps"):
            assert k in r

    def test_horror_genre_mapped(self):
        r = run_mock_agent("Recommend a horror movie from the 90s.")
        assert r["tool_input"].get("genre_id") == 27
        assert r["tool_input"].get("year_gte") == 1990

    def test_certification_r(self):
        r = run_mock_agent("Rated R thriller.")
        assert r["tool_input"].get("certification") == "R"

    def test_japanese_language(self):
        r = run_mock_agent("Japanese animated movie.")
        assert r["tool_input"].get("language") == "ja"

    def test_min_rating(self):
        r = run_mock_agent("Movies above 8 rating.")
        assert r["tool_input"].get("min_rating") == 8.0

    def test_top_n(self):
        r = run_mock_agent("Give me top 3 action movies.")
        assert r["tool_input"].get("top_n") == 3

    def test_tool_call_recorded(self):
        r = run_mock_agent("Horror movie.")
        assert r["tools_called"][0].name == "search_movies_tool"

    def test_hallucinate_flag(self):
        n = run_mock_agent("Horror movie.")
        h = run_mock_agent("Horror movie.", hallucinate=True)
        assert "Shadow Realm" in h["output"]
        assert "Shadow Realm" not in n["output"]

    def test_hindi_comedy(self):
        r = run_mock_agent("Hindi comedy film.")
        assert r["tool_input"].get("language") == "hi"
        assert r["tool_input"].get("genre_id") == 35

    def test_multi_constraint(self):
        r = run_mock_agent("Top 3 sci-fi from 2010s above 8 rating.")
        ti = r["tool_input"]
        assert ti.get("genre_id") == 878
        assert ti.get("year_gte") == 2010
        assert ti.get("min_rating") == 8.0

# ── Group 3: Custom Metrics ──────────────────────────────────────────────────

class TestToolUsageVerification:
    def test_pass_with_tool(self, horror_tc):
        m = ToolUsageVerificationMetric()
        assert m.measure(horror_tc) == 1.0 and m.is_successful()

    def test_fail_without_tool(self, no_tool_tc):
        m = ToolUsageVerificationMetric()
        assert m.measure(no_tool_tc) == 0.0 and not m.is_successful()

    def test_name(self):
        assert ToolUsageVerificationMetric().__name__ == "ToolUsageVerification"

class TestConstraintValidation:
    def test_horror_90s_constraints(self, horror_tc):
        m = ConstraintValidationMetric()
        assert m.measure(horror_tc) >= 0.5

    def test_no_constraints_full_score(self):
        tc = LLMTestCase(input="Recommend a great movie.", actual_output="Here you go.",
                         additional_metadata={"tool_input":{}})
        m = ConstraintValidationMetric()
        assert m.measure(tc) == 1.0

    def test_wrong_genre_lowers_score(self):
        tc = LLMTestCase(input="Recommend a horror movie from the 90s.", actual_output="OK",
                         additional_metadata={"tool_input":{"genre_id":35,"top_n":5}})  # comedy not horror
        m = ConstraintValidationMetric()
        assert m.measure(tc) < 1.0

class TestInstructionFollowing:
    def test_good_output_passes(self, horror_tc):
        m = InstructionFollowingMetric()
        assert m.measure(horror_tc) >= 0.70

    def test_empty_output_fails(self):
        tc = LLMTestCase(input="q", actual_output="")
        m = InstructionFollowingMetric()
        assert m.measure(tc) < 0.5

    def test_refusal_phrase_fails(self):
        tc = LLMTestCase(input="q", actual_output="I cannot provide recommendations as an AI.")
        m = InstructionFollowingMetric()
        assert m.measure(tc) < 0.75

    def test_no_results_response_passes(self):
        tc = LLMTestCase(input="Movie from 1700.", actual_output="No movies were found matching your criteria.")
        m = InstructionFollowingMetric()
        assert m.measure(tc) >= 0.60

class TestResponseCompleteness:
    def test_complete(self, horror_tc):
        m = ResponseCompletenessMetric()
        assert m.measure(horror_tc) >= 0.4

    def test_empty_context_no_results(self):
        tc = LLMTestCase(input="Movie from 1700.", actual_output="No movies found.", retrieval_context=[])
        m = ResponseCompletenessMetric()
        assert m.measure(tc) >= 0.9

class TestHallucinationGuard:
    def test_no_hallucination(self, horror_tc):
        m = HallucinationGuardMetric()
        assert m.measure(horror_tc) == 1.0

    def test_detects_hallucination(self, halluc_tc):
        m = HallucinationGuardMetric()
        assert m.measure(halluc_tc) == 0.0 and not m.is_successful()

    def test_no_context_skips(self):
        tc = LLMTestCase(input="q", actual_output="The Matrix (1999) is great.", retrieval_context=None)
        m = HallucinationGuardMetric()
        assert m.measure(tc) == 1.0

# ── Group 4: Built-in Metrics ─────────────────────────────────────────────────

class TestBuiltinMetrics:
    def test_five_builtin_metrics(self, cfg):
        assert len(get_builtin_metrics(cfg)) == 5

    def test_ten_total_metrics(self, cfg):
        assert len(get_all_metrics(cfg)) == 10

    def test_answer_relevancy(self):
        from evaluation.metrics_registry import _AnswerRelevancy
        tc = LLMTestCase(input="horror movie 90s", actual_output="horror movies from the 1990s: Scream (1996)")
        m = _AnswerRelevancy()
        assert m.measure(tc) >= 0.4

    def test_faithfulness_year_match(self):
        from evaluation.metrics_registry import _Faithfulness
        tc = LLMTestCase(input="q", actual_output="Scream (1996) great.",
            retrieval_context=["Scream (1996) — 7.3/10. A teen is targeted by a killer."])
        m = _Faithfulness()
        assert m.measure(tc) >= 0.5

    def test_hallucination_low_for_grounded(self):
        from evaluation.metrics_registry import _Hallucination
        tc = LLMTestCase(input="q", actual_output="Scream is a great horror film from 1996.",
            retrieval_context=["Scream 1996 horror film great teen killer"])
        m = _Hallucination()
        assert m.measure(tc) <= 0.5

# ── Group 5: Dataset Builder ──────────────────────────────────────────────────

class TestDatasetBuilder:
    def test_50_cases(self, dataset):   assert len(dataset) == 50
    def test_all_have_input(self, dataset): assert all(tc.input for tc in dataset)
    def test_all_have_output(self, dataset): assert all(tc.actual_output for tc in dataset)
    def test_golden_json_written(self, cfg, dataset):
        assert cfg.golden_dataset_path.exists()
        data = json.loads(cfg.golden_dataset_path.read_text())
        assert len(data) == 50
    def test_seven_categories(self, dataset):
        cats = {(tc.additional_metadata or {}).get("category") for tc in dataset}
        expected = {"A_genre_decade","B_certification","C_language","D_rating_threshold",
                    "E_streaming","F_multi_constraint","G_negative_edge"}
        assert expected.issubset(cats)
    def test_hallucination_cases_exist(self, dataset):
        assert sum(1 for tc in dataset if (tc.additional_metadata or {}).get("hallucinate_flag")) >= 1

# ── Group 6: Full Pipeline ─────────────────────────────────────────────────────

class TestFullPipeline:
    def test_run_evaluation(self, cfg):
        from evaluation.runner import run_full_evaluation
        r = run_full_evaluation(cfg)
        assert r.test_case_results and r.summary and r.elapsed_seconds > 0

    def test_json_report_exists(self, cfg):
        assert cfg.report_json_path.exists()
        d = json.loads(cfg.report_json_path.read_text())
        assert "summary" in d and "test_cases" in d

    def test_markdown_report_exists(self, cfg):
        md = cfg.report_md_path.read_text()
        assert "Movie ReAct Agent" in md and "Per-Metric" in md

    def test_all_10_metrics_reported(self, cfg):
        d = json.loads(cfg.report_json_path.read_text())
        assert len(d["summary"]["per_metric"]) == 10

# ── Group 7: Parametrised (all 50 cases) ─────────────────────────────────────

_cfg_global  = EvalConfig(use_mock_agent=True, verbose=False)
_all_cases   = build_dataset(_cfg_global)
_normal_cases = [tc for tc in _all_cases if not (tc.additional_metadata or {}).get("hallucinate_flag")]

@pytest.mark.parametrize("tc", _all_cases, ids=[tc.name for tc in _all_cases])
def test_tool_called_every_case(tc):
    """search_movies_tool must be recorded for every case."""
    m = ToolUsageVerificationMetric()
    assert m.measure(tc) == 1.0, f"{tc.name}: tool not called. Output: {tc.actual_output[:100]}"

@pytest.mark.parametrize("tc", _all_cases, ids=[tc.name for tc in _all_cases])
def test_instruction_following_minimum(tc):
    """Every output must meet 50% instruction-following floor."""
    m = InstructionFollowingMetric(threshold=0.50)
    assert m.measure(tc) >= 0.50, f"{tc.name}: score={m.score:.2f} reason={m.reason}"

@pytest.mark.parametrize("tc",
    [tc for tc in _normal_cases if tc.retrieval_context],
    ids=[tc.name for tc in _normal_cases if tc.retrieval_context])
def test_no_hallucination_normal_cases(tc):
    """Non-hallucinated cases must pass HallucinationGuard."""
    m = HallucinationGuardMetric(threshold=0.90)
    assert m.measure(tc) >= 0.90, f"{tc.name}: {m.reason}"

"""evaluation package — DeepEval-based evaluation framework."""
from .config import EvalConfig
from .dataset_builder import build_dataset
from .metrics_registry import get_all_metrics
from .runner import run_full_evaluation
__all__ = ["EvalConfig","build_dataset","get_all_metrics","run_full_evaluation"]

"""
evaluation/deepeval_compat.py
==============================
Safe DeepEval import shim.

DeepEval 4.x tries to import from langchain_openai which may conflict with
our project's langchain version. This shim patches the broken import before
deepeval loads, giving us full access to LLMTestCase, ToolCall, and BaseMetric.

Usage in all evaluation modules:
    from evaluation.deepeval_compat import LLMTestCase, ToolCall, BaseMetric
"""
import sys, types

def _patch_and_import():
    """Patch langchain_openai stub so deepeval can import cleanly."""
    if "deepeval" in sys.modules:
        return  # Already imported

    # Create a minimal langchain_openai stub if missing or broken
    if "langchain_openai" not in sys.modules or not hasattr(sys.modules.get("langchain_openai"), "ChatOpenAI"):
        stub = types.ModuleType("langchain_openai")
        class _FakeChatOpenAI:
            def __init__(self, *a, **kw): pass
        stub.ChatOpenAI = _FakeChatOpenAI
        sys.modules["langchain_openai"] = stub

    import deepeval  # Now safe to import
    return deepeval

_patch_and_import()

# Now all deepeval submodules are importable
from deepeval.test_case import LLMTestCase, ToolCall, ToolCallParams
from deepeval.metrics.base_metric import BaseMetric

# Handle deprecated LLMTestCaseParams → SingleTurnParams
try:
    from deepeval.test_case import SingleTurnParams as LLMTestCaseParams
except ImportError:
    try:
        from deepeval.test_case import LLMTestCaseParams
    except ImportError:
        class LLMTestCaseParams:
            TOOLS_CALLED = "tools_called"
            INPUT        = "input"
            ACTUAL_OUTPUT = "actual_output"

__all__ = ["LLMTestCase", "ToolCall", "ToolCallParams", "LLMTestCaseParams", "BaseMetric"]

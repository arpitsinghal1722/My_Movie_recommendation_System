"""evaluation/config.py — Central evaluation configuration."""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

EVAL_ROOT   = Path(__file__).parent
DATASET_DIR = EVAL_ROOT / "datasets"
REPORTS_DIR = EVAL_ROOT / "reports"
LOGS_DIR    = EVAL_ROOT / "logs"
for _d in (DATASET_DIR, REPORTS_DIR, LOGS_DIR): _d.mkdir(parents=True, exist_ok=True)

@dataclass
class EvalConfig:
    eval_model:     str  = field(default_factory=lambda: os.getenv("EVAL_MODEL","gpt-4o-mini"))
    use_mock_agent: bool = True
    verbose:        bool = True
    thresholds: dict = field(default_factory=lambda: {
        "AnswerRelevancy":       0.70,
        "Faithfulness":          0.70,
        "Hallucination":         0.30,  # lower is better
        "ContextualPrecision":   0.60,
        "ContextualRecall":      0.60,
        "ToolUsageVerification": 1.00,
        "ConstraintValidation":  0.75,
        "InstructionFollowing":  0.70,
        "ResponseCompleteness":  0.60,
        "HallucinationGuard":    0.90,
    })
    golden_dataset_path: Path = field(default_factory=lambda: DATASET_DIR/"golden_dataset.json")
    report_json_path:    Path = field(default_factory=lambda: REPORTS_DIR/"eval_report.json")
    report_md_path:      Path = field(default_factory=lambda: REPORTS_DIR/"eval_report.md")
    log_path:            Path = field(default_factory=lambda: LOGS_DIR/"evaluation.log")

    def threshold_for(self, name: str) -> float:
        return self.thresholds.get(name, 0.70)

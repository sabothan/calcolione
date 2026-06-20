"""Headless test runner for calcolione exercise inputs.

Runs a predefined set of inputs from a JSON file against the Exercise domain
layer, without starting the UI. Results are written to the calcolione log file.

Usage:
    python scripts/test_inputs.py
    python scripts/test_inputs.py --inputs scripts/test_inputs.json
    python scripts/test_inputs.py --inputs scripts/test_inputs.json --exercise calcolione/exercises.json
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Allow running from the project root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pint.errors import UndefinedUnitError, DimensionalityError, OffsetUnitCalculusError

from calcolione.exercise.exercise import Exercise
from calcolione.ui.base_ui import STYLE
from calcolione.utils import EXERCISE_FILE, LOG_FILE, get_logger

log = get_logger(__name__)

# Map prompt_toolkit class names to their hex color specs from STYLE.
# Strips the "class:" prefix for lookup.
COLOR_MAP: dict[str, str] = {
    key: val for key, val in STYLE.style_rules
}

DEFAULT_INPUTS_FILE = Path(__file__).resolve().parent / "test_inputs.json"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class CaseResult:
    """Holds the outcome of a single test case."""

    case_id: str
    description: str
    input: str
    expected_outcome: str
    actual_outcome: str
    feedback_class: str
    feedback_text: str
    exception_type: Optional[str] = None
    exception_message: Optional[str] = None
    matched_expectation: bool = False


# ---------------------------------------------------------------------------
# Outcome resolution
# ---------------------------------------------------------------------------

def _resolve_outcome(
    answer: str,
    exercise: Exercise,
) -> tuple[str, str, str, Optional[str], Optional[str]]:
    """Run one answer through the exercise domain layer and return outcome fields.

    Args:
        answer (str): The raw answer string.
        exercise (Exercise): The loaded exercise.

    Returns:
        tuple: (actual_outcome, feedback_class, feedback_text, exc_type, exc_message)
    """
    if not answer:
        return "no_change", "class:hint", "Enter your answer above.", None, None

    try:
        exercise.input_answer(answer=answer)
    except UndefinedUnitError as e:
        return "error_undefined_unit", "class:error", "Unknown unit", "UndefinedUnitError", str(e)
    except DimensionalityError as e:
        return "error_dimensionality", "class:error", "Incompatible dimensions", "DimensionalityError", str(e)
    except OffsetUnitCalculusError as e:
        return "error_offset_unit", "class:error", "Offset units not supported here", "OffsetUnitCalculusError", str(e)
    except AssertionError as e:
        return "error_assertion", "class:error", "Malformed expression", "AssertionError", str(e)
    except Exception as e:
        return "error_unexpected", "class:error", "Unexpected error", type(e).__name__, str(e)

    is_correct = exercise.evaluate_answer()
    if is_correct:
        return "correct", "class:correct", "Correct.", None, None
    else:
        return "wrong", "class:wrong", "Wrong! Try again.", None, None


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_tests(inputs_file: Path, exercise_file: Path) -> list[CaseResult]:
    """Run all test cases from the inputs JSON file.

    Args:
        inputs_file (Path): Path to the test inputs JSON.
        exercise_file (Path): Path to the exercise JSON.

    Returns:
        list[CaseResult]: Results for all cases.
    """
    with open(inputs_file, encoding="utf-8") as f:
        data = json.load(f)

    cases = data["cases"]
    results: list[CaseResult] = []

    log.info("=" * 60)
    log.info("calcolione headless test run")
    log.info("Inputs file : %s", inputs_file)
    log.info("Exercise    : %s", exercise_file)
    log.info("Cases       : %d", len(cases))
    log.info("=" * 60)

    for case in cases:
        # Reload exercise for each case so state doesn't bleed between runs
        exercise = Exercise.get_exercise_from_json(exercise_file)

        case_id = case["id"]
        description = case["description"]
        answer = case["input"]
        expected = case["expected_outcome"]

        actual, fb_class, fb_text, exc_type, exc_msg = _resolve_outcome(answer, exercise)
        matched = (actual == expected) or (expected == "unknown")

        result = CaseResult(
            case_id=case_id,
            description=description,
            input=answer,
            expected_outcome=expected,
            actual_outcome=actual,
            feedback_class=fb_class,
            feedback_text=fb_text,
            exception_type=exc_type,
            exception_message=exc_msg,
            matched_expectation=matched,
        )
        results.append(result)
        _log_result(result)

    _log_summary(results)
    return results


def _log_result(r: CaseResult) -> None:
    """Write a single case result to the log.

    Args:
        r (CaseResult): The case result to log.
    """
    status = "PASS" if r.matched_expectation else "FAIL"
    log.info("-" * 60)
    log.info("[%s] %s - %s", status, r.case_id, r.description)
    log.info("  input            : %r", r.input)
    log.info("  expected outcome : %s", r.expected_outcome)
    log.info("  actual outcome   : %s", r.actual_outcome)
    log.info("  feedback class   : %s", r.feedback_class)
    log.info("  feedback color   : %s", COLOR_MAP.get(r.feedback_class.removeprefix("class:"), "unknown"))
    log.info("  feedback text    : %s", r.feedback_text)
    if r.exception_type:
        log.info("  exception type   : %s", r.exception_type)
        log.info("  exception msg    : %s", r.exception_message)


def _log_summary(results: list[CaseResult]) -> None:
    """Write a summary of all results to the log.

    Args:
        results (list[CaseResult]): All case results.
    """
    passed = sum(1 for r in results if r.matched_expectation)
    failed = len(results) - passed
    log.info("=" * 60)
    log.info("SUMMARY: %d passed, %d failed out of %d cases", passed, failed, len(results))
    if failed:
        log.info("Failed cases:")
        for r in results:
            if not r.matched_expectation:
                log.info("  - %s (expected: %s, got: %s)", r.case_id, r.expected_outcome, r.actual_outcome)
    log.info("=" * 60)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    """Run the headless test suite.

    Returns:
        int: Exit code. 0 if all cases matched expectations, 1 otherwise.
    """
    parser = argparse.ArgumentParser(
        prog="test_inputs",
        description="Headless test runner for calcolione exercise inputs.",
        epilog=f"Results are written to {LOG_FILE}",
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        default=DEFAULT_INPUTS_FILE,
        help="Path to the test inputs JSON file (default: scripts/test_inputs.json)",
    )
    parser.add_argument(
        "--exercise",
        type=Path,
        default=EXERCISE_FILE,
        help="Path to the exercise JSON file (default: calcolione/exercises.json)",
    )
    args = parser.parse_args()

    if not args.inputs.is_file():
        print(f"Inputs file not found: {args.inputs}")
        return 1
    if not args.exercise.is_file():
        print(f"Exercise file not found: {args.exercise}")
        return 1

    results = run_tests(inputs_file=args.inputs, exercise_file=args.exercise)

    passed = sum(1 for r in results if r.matched_expectation)
    print(f"Results written to: {LOG_FILE}")
    print(f"{passed}/{len(results)} cases matched expectations")

    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
"""Easy task evaluator for math.py.

Set AGENTFLOW_TARGET to the absolute path of the code to evaluate.
Do not expose this private evaluator to the coding agent during a run.
"""
import importlib.util
import os
from pathlib import Path

import pytest

DEFAULT_TARGET = Path(__file__).resolve().parent.parent / "tasks" / "easy" / "math.py"
TARGET = Path(os.environ.get("AGENTFLOW_TARGET", str(DEFAULT_TARGET))).resolve()
spec = importlib.util.spec_from_file_location("agentflow_easy_target", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load target: {TARGET}")
math_task = importlib.util.module_from_spec(spec)
spec.loader.exec_module(math_task)


@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 8), (0, 0, 0), (-5, 2, -3), (1.25, 2.5, 3.75),
])
def test_addition(a, b, expected):
    assert math_task.addition(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 2), (0, 7, -7), (-5, -2, -3), (1.25, 2.5, -1.25),
])
def test_subtraction(a, b, expected):
    assert math_task.subtraction(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 15), (0, 12, 0), (-4, 3, -12), (2.5, 4, 10),
])
def test_multiplication(a, b, expected):
    assert math_task.multiplication(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b,expected", [
    (12, 3, 4), (7, 2, 3.5), (-12, 3, -4), (0, 5, 0),
])
def test_division(a, b, expected):
    assert math_task.division(a, b) == pytest.approx(expected)


def test_division_by_zero():
    with pytest.raises(ValueError):
        math_task.division(10, 0)

from __future__ import annotations

from pathlib import Path

import pytest

from patchguard.codeintel import (
    analyze_change_impact,
    build_call_graph,
    find_affected_callers,
)
from patchguard.crew import estimate_cost
from patchguard.policy import BudgetExceededError, Policy
from patchguard.tools import InspectChangeImpactTool
from patchguard.workspace import export_audit_replay, write_audit_replay, write_file


def test_call_graph_and_impact(tmp_path: Path):
    mod_a = """
def helper():
    return 42

def worker():
    val = helper()
    return val + 1
"""
    mod_b = """
from mod_a import worker

def main_app():
    return worker()
"""
    write_file(tmp_path, "mod_a.py", mod_a)
    write_file(tmp_path, "mod_b.py", mod_b)

    graph = build_call_graph(tmp_path)
    assert "mod_a.py:worker" in graph
    assert "helper" in graph["mod_a.py:worker"]

    callers = find_affected_callers(tmp_path, "worker")
    assert "mod_b.py:main_app" in callers

    impact = analyze_change_impact(tmp_path, ["mod_a.py"])
    assert "mod_a.py:worker" in impact
    assert "mod_b.py:main_app" in impact["mod_a.py:worker"]


def test_inspect_change_impact_tool(tmp_path: Path):
    write_file(tmp_path, "lib.py", "def compute(): return 1\n")
    write_file(tmp_path, "app.py", "def run(): return compute()\n")

    tool = InspectChangeImpactTool(workspace=str(tmp_path))
    res = tool.run("lib.py")
    assert "calls from" in res
    assert "app.py:run" in res

    empty_res = tool.run("nonexistent.py")
    assert empty_res == "No downstream callers impacted."


def test_policy_budget_guardrails():
    policy = Policy(max_tokens=1000, max_cost_usd=0.05)
    # Under limit
    policy.check_budget(total_tokens=500, estimated_cost=0.01)

    # Token limit exceeded
    with pytest.raises(BudgetExceededError, match="Token budget exceeded"):
        policy.check_budget(total_tokens=1500, estimated_cost=0.01)

    # Cost limit exceeded
    with pytest.raises(BudgetExceededError, match="Spend limit exceeded"):
        policy.check_budget(total_tokens=500, estimated_cost=0.10)


def test_estimate_cost():
    usage = {"prompt_tokens": 1_000_000, "completion_tokens": 1_000_000}
    gemini_cost = estimate_cost(usage, "gemini-1.5-flash")
    assert gemini_cost == 0.75

    ollama_cost = estimate_cost(usage, "ollama:llama3")
    assert ollama_cost == 0.0

    gpt_cost = estimate_cost(usage, "gpt-4o")
    assert gpt_cost == 12.5


def test_audit_replay(tmp_path: Path):
    write_file(tmp_path, "a.py", "print('hello')\n")
    replay = export_audit_replay(tmp_path)
    assert replay["files_count"] >= 1
    assert "a.py" in replay["files"]

    dest = write_audit_replay(tmp_path)
    assert dest.exists()
    assert dest.name == "AUDIT_REPLAY.json"

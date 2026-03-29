"""
Behavioral contract tests for agents.

Each YAML case under tests/cases/agents/ is run as an independent test.
In stub mode (default) the pre-written stub_response is checked against the
case assertions — free, deterministic, no API keys needed.
Pass --live (or set LIVE_LLM=true) to call the real model instead.
"""
from __future__ import annotations

import pytest

from conftest import _case_id, assert_contract_case, load_agent_cases

_CASES = load_agent_cases()


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(case) for case in _CASES])
def test_agent_contract(case: dict, live_mode: bool) -> None:
    """Assert that the agent response satisfies all contract assertions."""
    assert_contract_case(case, live_mode)

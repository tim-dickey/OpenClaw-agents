"""
Runner dispatch for the TDD framework.

run_case(case, mode) is the single call-site used by the pytest test files.
"""
from __future__ import annotations

from .stub_runner import run_stub


def run_case(case: dict, mode: str = "stub") -> str:
    """Execute *case* in the requested *mode* and return the response string.

    Parameters
    ----------
    case : dict
        Loaded YAML test case.
    mode : str
        "stub"  — return the pre-written stub_response (default, free, deterministic).
        "live"  — call the real LLM API (requires API key env var).
    """
    if mode == "live":
        from .live_runner import run_live  # deferred so missing packages don't break stub mode
        return run_live(case)
    return run_stub(case)

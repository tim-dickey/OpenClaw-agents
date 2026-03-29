"""
Stub runner — returns the pre-written stub_response from the test case.

This is the default execution mode: deterministic, free, and CI-safe.
It validates that the stub response itself satisfies the assertions, which
confirms the test case is internally coherent before any live model is involved.
"""
from __future__ import annotations


def run_stub(case: dict) -> str:
    """Return the stub_response field from *case*.

    Raises ValueError if the field is absent or empty so callers get a clear
    message instead of a silent pass.
    """
    response = case.get("stub_response", "")
    if not response or not str(response).strip():
        raise ValueError(
            f"Case {case.get('id', '<unknown>')!r} has no stub_response. "
            "Add one before running in stub mode."
        )
    return str(response).strip()

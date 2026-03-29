"""
Assertion helpers for TDD contract tests.

check_must_include and check_must_not_include each return a (possibly empty)
list of failure messages.  An empty list means all assertions passed.
"""
from __future__ import annotations

import re


def _matches(pattern: str, text: str) -> bool:
    """Return True if *pattern* appears in *text* (case-insensitive).

    Tries a plain substring match first; if that fails, also tries interpreting
    the pattern as a regular expression so callers can use either literal or
    regex-style patterns.
    """
    lowered = text.lower()
    lowered_pat = pattern.lower()
    if lowered_pat in lowered:
        return True
    try:
        return bool(re.search(lowered_pat, lowered))
    except re.error:
        return False


def check_must_include(response: str, patterns: list[str]) -> list[str]:
    """Return a failure message for every pattern NOT found in *response*."""
    failures: list[str] = []
    for pattern in patterns:
        if not _matches(pattern, response):
            failures.append(f"must_include pattern not found: {pattern!r}")
    return failures


def check_must_not_include(response: str, patterns: list[str]) -> list[str]:
    """Return a failure message for every pattern that IS found in *response*."""
    failures: list[str] = []
    for pattern in patterns:
        if _matches(pattern, response):
            failures.append(f"must_not_include pattern found: {pattern!r}")
    return failures

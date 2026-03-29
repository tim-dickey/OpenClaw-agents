# pyright: reportMissingImports=false, reportMissingModuleSource=false
# mypy: disable-error-code=import-not-found,import-untyped,no-any-unimported
# pylint: disable=redefined-outer-name
"""
conftest.py — shared fixtures, discovery helpers, and reusable assertions.

Discovers all YAML test cases under tests/cases/ and exposes:
  - `load_agent_cases()`
  - `load_sub_agent_cases()`
  - `load_agent_specs()`
  - `load_sub_agent_specs()`
  - `live_mode`
"""
from __future__ import annotations

import os
import pathlib

import frontmatter  # type: ignore[import-not-found]
import pytest
import yaml  # type: ignore[import-untyped]

from runner import run_case
from runner.assertions import check_must_include, check_must_not_include

_CASES_ROOT = pathlib.Path(__file__).parent / "cases"
_REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]


def normalize_ref(value: object) -> str:
    return str(value).strip().lower().replace(" ", "-").replace(".", "")


# ---------------------------------------------------------------------------
# CLI option
# ---------------------------------------------------------------------------

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--live",
        action="store_true",
        default=False,
        help="Run tests against a real LLM API instead of stub responses.",
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def live_mode(request: pytest.FixtureRequest) -> bool:
    """True when --live is passed or LIVE_LLM=true is set in the environment."""
    return request.config.getoption("--live") or os.environ.get("LIVE_LLM", "").lower() == "true"


# ---------------------------------------------------------------------------
# Case discovery helpers
# ---------------------------------------------------------------------------

def _load_cases(sub_dir: str) -> list[dict[str, object]]:
    """Load all *.yml files under cases/<sub_dir>/ and return them as dicts."""
    cases: list[dict[str, object]] = []
    root = _CASES_ROOT / sub_dir
    if not root.exists():
        return cases
    for path in sorted(root.rglob("*.yml")):
        with path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if data:
            data["_path"] = str(path.relative_to(_CASES_ROOT.parent)).replace("\\", "/")
            cases.append(data)
    return cases


def load_agent_cases() -> list[dict[str, object]]:
    return _load_cases("agents")


def load_sub_agent_cases() -> list[dict[str, object]]:
    return _load_cases("sub-agents")


# ---------------------------------------------------------------------------
# Spec discovery helpers
# ---------------------------------------------------------------------------

def _load_specs(root_dir: str, filename: str) -> list[dict[str, object]]:
    specs: list[dict[str, object]] = []
    root = _REPO_ROOT / root_dir
    if not root.exists():
        return specs

    for path in sorted(root.rglob(filename)):
        if "_template" in path.parts:
            continue
        post = frontmatter.load(str(path))
        aliases = {normalize_ref(path.parent.name)}
        name = post.metadata.get("name")
        if name:
            aliases.add(normalize_ref(name))
        specs.append(
            {
                "path": str(path.relative_to(_REPO_ROOT)).replace("\\", "/"),
                "folder": path.parent.name,
                "metadata": dict(post.metadata),
                "content": post.content,
                "aliases": aliases,
            }
        )
    return specs


def load_agent_specs() -> list[dict[str, object]]:
    return _load_specs("agents", "agent.md")


def load_sub_agent_specs() -> list[dict[str, object]]:
    return _load_specs("sub-agents", "sub-agent.md")


def build_alias_index(
    specs: list[dict[str, object]],
) -> tuple[dict[str, dict[str, object]], dict[str, list[str]]]:
    alias_index: dict[str, dict[str, object]] = {}
    duplicates: dict[str, list[str]] = {}

    for spec in specs:
        for alias in sorted(spec["aliases"]):
            existing = alias_index.get(alias)
            if existing and existing["path"] != spec["path"]:
                duplicates.setdefault(alias, [existing["path"]])
                if spec["path"] not in duplicates[alias]:
                    duplicates[alias].append(spec["path"])
                continue
            alias_index[alias] = spec

    return alias_index, duplicates


def build_declared_dependency_pairs(
    agent_specs: list[dict[str, object]],
    sub_agent_aliases: dict[str, dict[str, object]],
) -> list[dict[str, object]]:
    pairs: list[dict[str, object]] = []
    for agent_spec in agent_specs:
        refs = agent_spec["metadata"].get("sub_agents") or []
        if not isinstance(refs, list):
            continue
        for ref in refs:
            pairs.append(
                {
                    "agent": agent_spec,
                    "ref": ref,
                    "normalized_ref": normalize_ref(ref),
                    "sub_agent": sub_agent_aliases.get(normalize_ref(ref)),
                }
            )
    return pairs


# ---------------------------------------------------------------------------
# Parametrize and assertion helpers
# ---------------------------------------------------------------------------

def _case_id(case: dict[str, object]) -> str:
    """Human-readable pytest ID: <target-ref>/<case-id>."""
    ref = (case.get("target") or {}).get("ref", "unknown")
    return f"{ref}/{case.get('id', 'unknown')}"


def assert_contract_case(case: dict[str, object], is_live_mode: bool) -> None:
    """Run a behavioral contract case and fail on assertion mismatches."""
    mode = "live" if is_live_mode else "stub"
    response = run_case(case, mode=mode)

    assertions = case.get("assertions", {})
    must_include = assertions.get("must_include", [])
    must_not_include = assertions.get("must_not_include", [])

    failures = check_must_include(response, must_include) + check_must_not_include(response, must_not_include)
    if not failures:
        return

    case_id = case.get("id", "<unknown>")
    path = case.get("_path", "")
    failure_lines = "\n  ".join(failures)
    pytest.fail(f"Contract violations in {case_id!r} ({path}) [{mode} mode]:\n  {failure_lines}")

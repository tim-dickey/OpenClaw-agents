from __future__ import annotations

import pytest

from conftest import (
    build_alias_index,
    build_declared_dependency_pairs,
    load_agent_specs,
    load_sub_agent_specs,
    normalize_ref,
)

_AGENT_SPECS = load_agent_specs()
_SUB_AGENT_SPECS = load_sub_agent_specs()
_AGENT_ALIAS_INDEX, _AGENT_ALIAS_DUPLICATES = build_alias_index(_AGENT_SPECS)
_SUB_AGENT_ALIAS_INDEX, _SUB_AGENT_ALIAS_DUPLICATES = build_alias_index(_SUB_AGENT_SPECS)
_DECLARED_DEPENDENCIES = build_declared_dependency_pairs(_AGENT_SPECS, _SUB_AGENT_ALIAS_INDEX)


def _spec_id(spec: dict) -> str:
    return spec["metadata"].get("name") or spec["folder"]


def _dependency_id(pair: dict) -> str:
    return f"{_spec_id(pair['agent'])}->{pair['ref']}"


def test_agent_aliases_are_unique() -> None:
    assert not _AGENT_ALIAS_DUPLICATES, f"Duplicate agent aliases found: {_AGENT_ALIAS_DUPLICATES}"


def test_sub_agent_aliases_are_unique() -> None:
    assert not _SUB_AGENT_ALIAS_DUPLICATES, f"Duplicate sub-agent aliases found: {_SUB_AGENT_ALIAS_DUPLICATES}"


@pytest.mark.parametrize("agent_spec", _AGENT_SPECS, ids=[_spec_id(spec) for spec in _AGENT_SPECS])
def test_agents_do_not_declare_duplicate_sub_agents(agent_spec: dict) -> None:
    refs = agent_spec["metadata"].get("sub_agents") or []
    assert isinstance(refs, list), f"{agent_spec['path']} must use a list for sub_agents"

    normalized_refs: list[str] = []
    duplicates: list[str] = []
    for ref in refs:
        normalized = normalize_ref(ref)
        if normalized in normalized_refs:
            duplicates.append(str(ref))
        normalized_refs.append(normalized)

    assert not duplicates, f"{agent_spec['path']} has duplicate sub-agent refs: {duplicates}"


@pytest.mark.parametrize("sub_agent_spec", _SUB_AGENT_SPECS, ids=[_spec_id(spec) for spec in _SUB_AGENT_SPECS])
def test_sub_agents_do_not_declare_duplicate_compatible_parents(sub_agent_spec: dict) -> None:
    refs = sub_agent_spec["metadata"].get("parent_agent_compatible") or []
    assert isinstance(refs, list), f"{sub_agent_spec['path']} must use a list for parent_agent_compatible"

    normalized_refs: list[str] = []
    duplicates: list[str] = []
    for ref in refs:
        normalized = normalize_ref(ref)
        if normalized in normalized_refs:
            duplicates.append(str(ref))
        normalized_refs.append(normalized)

    assert not duplicates, f"{sub_agent_spec['path']} has duplicate parent-agent refs: {duplicates}"


@pytest.mark.parametrize("sub_agent_spec", _SUB_AGENT_SPECS, ids=[_spec_id(spec) for spec in _SUB_AGENT_SPECS])
def test_sub_agent_compatible_parents_resolve_to_known_agents(sub_agent_spec: dict) -> None:
    refs = sub_agent_spec["metadata"].get("parent_agent_compatible") or []
    assert isinstance(refs, list), f"{sub_agent_spec['path']} must use a list for parent_agent_compatible"

    unknown_refs = [ref for ref in refs if normalize_ref(ref) not in _AGENT_ALIAS_INDEX]
    assert not unknown_refs, f"{sub_agent_spec['path']} references unknown parent agents: {unknown_refs}"


@pytest.mark.parametrize("pair", _DECLARED_DEPENDENCIES, ids=[_dependency_id(pair) for pair in _DECLARED_DEPENDENCIES])
def test_declared_agent_dependencies_map_to_compatible_sub_agents(pair: dict) -> None:
    sub_agent_spec = pair["sub_agent"]
    assert sub_agent_spec is not None, (
        f"{pair['agent']['path']} references unknown sub-agent {pair['ref']!r}"
    )

    compatible_parents = sub_agent_spec["metadata"].get("parent_agent_compatible") or []
    compatible_aliases = {normalize_ref(ref) for ref in compatible_parents}
    assert compatible_aliases.intersection(pair["agent"]["aliases"]), (
        f"{pair['agent']['path']} declares sub-agent {pair['ref']!r}, but "
        f"{sub_agent_spec['path']} does not list the agent in parent_agent_compatible"
    )


def _hint_id(pair: dict) -> str:
    return f"{pair['sub_agent']['folder']}<-{pair['parent_ref']}"


def _build_optional_hint_pairs() -> list[dict]:
    pairs: list[dict] = []
    for sub_agent_spec in _SUB_AGENT_SPECS:
        parent_refs = sub_agent_spec["metadata"].get("parent_agent_compatible") or []
        if not isinstance(parent_refs, list):
            continue
        for parent_ref in parent_refs:
            pairs.append(
                {
                    "sub_agent": sub_agent_spec,
                    "parent_ref": parent_ref,
                    "normalized_parent": normalize_ref(parent_ref),
                    "parent_agent": _AGENT_ALIAS_INDEX.get(normalize_ref(parent_ref)),
                }
            )
    return pairs


_OPTIONAL_HINT_PAIRS = _build_optional_hint_pairs()


def test_optional_compatibility_hint_pairs_exist() -> None:
    assert _OPTIONAL_HINT_PAIRS, "No parent_agent_compatible hint pairs were discovered"


@pytest.mark.parametrize("pair", _OPTIONAL_HINT_PAIRS, ids=[_hint_id(pair) for pair in _OPTIONAL_HINT_PAIRS])
def test_optional_compatibility_hints_resolve_to_known_agents(pair: dict) -> None:
    assert pair["parent_agent"] is not None, (
        f"{pair['sub_agent']['path']} references unknown compatible parent {pair['parent_ref']!r}"
    )


def test_optional_compatibility_hints_align_with_declared_dependencies() -> None:
    """
    Compatibility hints are optional, but whenever a hinted parent *does*
    declare a sub-agent in `sub_agents`, the relationship must align.
    """
    violating_pairs: list[dict] = []
    checked_pairs: list[dict] = []

    for pair in _OPTIONAL_HINT_PAIRS:
        parent_agent = pair["parent_agent"]
        if parent_agent is None:
            # Unknown parent agents are handled by a separate test.
            continue

        declared_refs = parent_agent["metadata"].get("sub_agents") or []
        if not isinstance(declared_refs, list):
            # Malformed metadata; nothing we can reliably assert here.
            continue

        if not declared_refs:
            # Parent has no declared sub-agents; hints remain purely optional.
            continue

        declared_norm = {normalize_ref(ref) for ref in declared_refs}
        sub_aliases = {normalize_ref(pair["sub_agent"]["folder"])}
        if pair["sub_agent"]["metadata"].get("name"):
            sub_aliases.add(normalize_ref(pair["sub_agent"]["metadata"]["name"]))

        checked_pairs.append(pair)
        if not declared_norm.intersection(sub_aliases):
            violating_pairs.append(pair)

    if not checked_pairs:
        pytest.skip(
            "No optional compatibility hints have parents with declared sub_agents to validate alignment against"
        )

    assert not violating_pairs, (
        "Some optional compatibility hints do not align with declared sub_agents: "
        + ", ".join(
            f"{pair['sub_agent']['path']} -> {pair['parent_ref']!r}" for pair in violating_pairs
        )
    )


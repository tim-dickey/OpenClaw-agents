# pyright: reportMissingImports=false, reportMissingModuleSource=false
# mypy: disable-error-code=import-not-found,import-untyped,no-any-unimported
# pylint: disable=redefined-outer-name
import os
import re
import sys

import yaml  # type: ignore[import-untyped]

from spec_index import build_alias_index, load_specs, normalize_ref

VALID_TARGET_KINDS = {"agent", "sub-agent"}
VALID_SCENARIO_TYPES = {"golden-path", "negative-path"}
FIXTURE_FILE_NAMES = {"fixture.yml", "fixture.yaml"}
FIXTURE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def build_agent_index(error_list: list[str]) -> dict[str, object]:
    agent_entries = load_specs("agents", "agent.md", error_list)
    return build_alias_index(agent_entries, error_list, "agent")


def build_sub_agent_index(error_list: list[str]) -> dict[str, object]:
    sub_agent_entries = load_specs("sub-agents", "sub-agent.md", error_list)
    return build_alias_index(sub_agent_entries, error_list, "sub-agent")


def load_yaml(file_path: str) -> object:
    with open(file_path, "r", encoding="utf-8", errors="replace") as handle:
        return yaml.safe_load(handle)


def require_non_empty_string(error_list: list[str], fixture_path: str, data: dict[str, object], field_name: str) -> str | None:
    value = data.get(field_name)
    if not isinstance(value, str) or not value.strip():
        error_list.append(f"[{fixture_path}] Field '{field_name}' must be a non-empty string.")
        return None
    return value.strip()


def require_string_list(
    error_list: list[str],
    fixture_path: str,
    data: dict[str, object],
    field_name: str,
    require_non_empty: bool = True,
) -> list[str]:
    value = data.get(field_name)
    if not isinstance(value, list):
        error_list.append(f"[{fixture_path}] Field '{field_name}' must be an array of strings.")
        return []
    if require_non_empty and not value:
        error_list.append(f"[{fixture_path}] Field '{field_name}' must be a non-empty array of strings.")
        return []

    cleaned: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            error_list.append(f"[{fixture_path}] Field '{field_name}' must contain only non-empty strings.")
            return []
        cleaned.append(item.strip())

    return cleaned


def validate_fixture(
    fixture_path: str,
    data: object,
    agent_aliases: dict[str, object],
    sub_agent_aliases: dict[str, object],
    error_list: list[str],
) -> None:
    if not isinstance(data, dict):
        error_list.append(f"[{fixture_path}] Fixture file must parse to a YAML object.")
        return

    schema_version = data.get("schema_version")
    if schema_version != 1:
        error_list.append(f"[{fixture_path}] Field 'schema_version' must equal 1.")

    fixture_id = require_non_empty_string(error_list, fixture_path, data, "id")
    if fixture_id and not FIXTURE_ID_PATTERN.match(fixture_id):
        error_list.append(f"[{fixture_path}] Field 'id' must be kebab-case.")

    target = data.get("target")
    if not isinstance(target, dict):
        error_list.append(f"[{fixture_path}] Field 'target' must be an object.")
        target = {}

    target_kind = require_non_empty_string(error_list, fixture_path, target, "kind")
    target_ref = require_non_empty_string(error_list, fixture_path, target, "ref")

    if target_kind and target_kind not in VALID_TARGET_KINDS:
        error_list.append(
            f"[{fixture_path}] Invalid target.kind '{target_kind}'. Must be one of: {', '.join(sorted(VALID_TARGET_KINDS))}."
        )

    expected_directory = None
    if target_kind == "agent":
        expected_directory = os.path.normpath(os.path.join("evals", "agents"))
        if target_ref and normalize_ref(target_ref) not in agent_aliases:
            error_list.append(
                f"[{fixture_path}] Unknown agent reference '{target_ref}' in target.ref. "
                "Add a matching agent definition under agents/<category>/<name>/agent.md."
            )
    elif target_kind == "sub-agent":
        expected_directory = os.path.normpath(os.path.join("evals", "sub-agents"))
        if target_ref and normalize_ref(target_ref) not in sub_agent_aliases:
            error_list.append(
                f"[{fixture_path}] Unknown sub-agent reference '{target_ref}' in target.ref. "
                "Add a matching sub-agent definition under sub-agents/<category>/<name>/sub-agent.md."
            )

    if expected_directory:
        normalized_path = os.path.normpath(fixture_path)
        if not normalized_path.startswith(expected_directory + os.sep):
            error_list.append(
                f"[{fixture_path}] Fixture location does not match target.kind '{target_kind}'. "
                f"Place it under {expected_directory.replace(os.sep, '/')}/*."
            )

    scenario_type = require_non_empty_string(error_list, fixture_path, data, "scenario_type")
    if scenario_type and scenario_type not in VALID_SCENARIO_TYPES:
        error_list.append(
            f"[{fixture_path}] Invalid scenario_type '{scenario_type}'. "
            f"Must be one of: {', '.join(sorted(VALID_SCENARIO_TYPES))}."
        )

    require_non_empty_string(error_list, fixture_path, data, "intent")

    input_block = data.get("input")
    if not isinstance(input_block, dict):
        error_list.append(f"[{fixture_path}] Field 'input' must be an object.")
        input_block = {}
    require_non_empty_string(error_list, fixture_path, input_block, "user")
    context_value = input_block.get("context")
    if context_value is not None and (not isinstance(context_value, str) or not context_value.strip()):
        error_list.append(f"[{fixture_path}] Optional field 'input.context' must be a non-empty string when provided.")

    expected = data.get("expected")
    if not isinstance(expected, dict):
        error_list.append(f"[{fixture_path}] Field 'expected' must be an object.")
        expected = {}

    require_non_empty_string(error_list, fixture_path, expected, "outcome")
    require_string_list(error_list, fixture_path, expected, "must_include", True)
    require_string_list(error_list, fixture_path, expected, "must_not_include", False)

    if "notes" in data and (not isinstance(data.get("notes"), str) or not data.get("notes").strip()):
        error_list.append(f"[{fixture_path}] Optional field 'notes' must be a non-empty string when provided.")


errors: list[str] = []
agent_aliases = build_agent_index(errors)
sub_agent_aliases = build_sub_agent_index(errors)

for eval_root, _, eval_files in os.walk("evals"):
    for file_name in eval_files:
        if file_name == "README.md":
            continue
        if not file_name.endswith((".yml", ".yaml")):
            continue
        if file_name not in FIXTURE_FILE_NAMES:
            errors.append(f"[{os.path.join(eval_root, file_name)}] Fixture files must be named fixture.yml or fixture.yaml.")
            continue

        fixture_path = os.path.join(eval_root, file_name)
        try:
            fixture_data = load_yaml(fixture_path)
        except yaml.YAMLError as exc:
            errors.append(f"[{fixture_path}] Invalid YAML: {exc}")
            continue

        validate_fixture(fixture_path, fixture_data, agent_aliases, sub_agent_aliases, errors)

if errors:
    print("\n❌ Eval fixture validation failed:\n")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("✅ All eval fixture files passed validation.")

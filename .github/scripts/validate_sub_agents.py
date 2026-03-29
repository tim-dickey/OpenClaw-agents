import sys

from spec_index import build_alias_index, get_list_field, load_specs, normalize_ref

REQUIRED_FIELDS = [
    "name", "version", "author", "description",
    "category", "tags", "trigger_phrases", "output_format"
]

VALID_CATEGORIES = {"research", "communication", "productivity", "data", "developer"}
VALID_OUTPUT_FORMATS = {"text", "json", "markdown", "action"}

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Activation Criteria",
    "## Input Expected",
    "## Output Produced",
    "## Execution Steps",
    "## Error Handling",
    "## Customization Notes"
]

errors: list[str] = []
agent_entries = load_specs("agents", "agent.md", errors)
sub_agent_entries = load_specs("sub-agents", "sub-agent.md", errors)

agent_aliases = build_alias_index(agent_entries, errors, "agent")
build_alias_index(sub_agent_entries, errors, "sub-agent")

for sub_agent in sub_agent_entries:
    metadata = sub_agent.metadata
    content = sub_agent.content

    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] in [None, "", []]:
            errors.append(f"[{sub_agent.path}] Missing or empty required frontmatter field: '{field}'")

    if metadata.get("category") not in VALID_CATEGORIES:
        errors.append(
            f"[{sub_agent.path}] Invalid category '{metadata.get('category')}'. "
            f"Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )

    if metadata.get("output_format") not in VALID_OUTPUT_FORMATS:
        errors.append(
            f"[{sub_agent.path}] Invalid output_format '{metadata.get('output_format')}'. "
            f"Must be one of: {', '.join(sorted(VALID_OUTPUT_FORMATS))}"
        )

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"[{sub_agent.path}] Missing required section: '{section}'")

    parent_refs = get_list_field(metadata, "parent_agent_compatible")
    if parent_refs is None:
        errors.append(f"[{sub_agent.path}] Frontmatter field 'parent_agent_compatible' must be an array when provided.")
        continue

    seen_refs: set[str] = set()
    for parent_ref in parent_refs:
        ref_key = normalize_ref(parent_ref)
        if ref_key in seen_refs:
            errors.append(
                f"[{sub_agent.path}] Duplicate parent agent reference '{parent_ref}' in 'parent_agent_compatible'."
            )
            continue
        seen_refs.add(ref_key)

        if ref_key not in agent_aliases:
            errors.append(
                f"[{sub_agent.path}] Unknown parent agent reference '{parent_ref}' in 'parent_agent_compatible'. "
                "Add a matching agent definition under agents/<category>/<folder>/agent.md, or update this "
                "reference to match an existing folder name or agent 'name'."
            )

if errors:
    print("\n❌ Sub-agent validation failed:\n")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("✅ All sub-agent.md files passed validation.")

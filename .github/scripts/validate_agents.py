import sys

from spec_index import build_alias_index, get_list_field, load_specs, normalize_ref

REQUIRED_FIELDS = [
    "name", "version", "author", "description",
    "category", "tags", "comms_channels",
    "memory_profile", "heartbeat_enabled"
]

VALID_CATEGORIES = {"personal", "professional", "developer", "creative", "team"}

REQUIRED_SECTIONS = [
    "## Persona",
    "## Core Behaviors",
    "## Communication Style",
    "## Capabilities",
    "## Constraints",
    "## Memory Guidelines",
    "## Heartbeat Behavior",
    "## Customization Notes",
    "## Example Interactions"
]

errors: list[str] = []
agent_entries = load_specs("agents", "agent.md", errors)
sub_agent_entries = load_specs("sub-agents", "sub-agent.md", errors)

build_alias_index(agent_entries, errors, "agent")
sub_agent_aliases = build_alias_index(sub_agent_entries, errors, "sub-agent")

for agent in agent_entries:
    metadata = agent.metadata
    content = agent.content

    for field in REQUIRED_FIELDS:
        if field not in metadata or metadata[field] in [None, "", []]:
            errors.append(f"[{agent.path}] Missing or empty required frontmatter field: '{field}'")

    if metadata.get("category") not in VALID_CATEGORIES:
        errors.append(
            f"[{agent.path}] Invalid category '{metadata.get('category')}'. "
            f"Must be one of: {', '.join(sorted(VALID_CATEGORIES))}"
        )

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"[{agent.path}] Missing required section: '{section}'")

    if "## Example Interactions" in content:
        idx = content.index("## Example Interactions")
        example_body = content[idx + len("## Example Interactions"):]
        if len(example_body.strip()) < 50:
            errors.append(f"[{agent.path}] '## Example Interactions' section appears empty or too short.")

    sub_agents = get_list_field(metadata, "sub_agents")
    if sub_agents is None:
        errors.append(f"[{agent.path}] Frontmatter field 'sub_agents' must be an array when provided.")
        continue

    seen_refs: set[str] = set()
    for sub_agent_ref in sub_agents:
        ref_key = normalize_ref(sub_agent_ref)
        if ref_key in seen_refs:
            errors.append(f"[{agent.path}] Duplicate sub-agent reference '{sub_agent_ref}' in 'sub_agents'.")
            continue
        seen_refs.add(ref_key)

        sub_agent = sub_agent_aliases.get(ref_key)
        if sub_agent is None:
            errors.append(
                f"[{agent.path}] Unknown sub-agent reference '{sub_agent_ref}' in 'sub_agents'. "
                "Ensure there is a matching sub-agent definition under the 'sub-agents/' directory, "
                "and reference it by either its folder name or the sub-agent 'name' field."
            )
            continue

        parent_refs = get_list_field(sub_agent.metadata, "parent_agent_compatible")
        if parent_refs is None:
            errors.append(
                f"[{sub_agent.path}] Frontmatter field 'parent_agent_compatible' must be an array when provided."
            )
            continue

        compatible_aliases = {normalize_ref(parent_ref) for parent_ref in parent_refs}
        if not compatible_aliases.intersection(agent.aliases):
            expected = ", ".join(sorted(agent.aliases))
            errors.append(
                f"[{agent.path}] Sub-agent reference '{sub_agent_ref}' resolves to [{sub_agent.path}] "
                f"but that sub-agent does not declare compatibility with this agent. "
                f"Add one of the agent aliases ({expected}) to 'parent_agent_compatible'."
            )

if errors:
    print("\n❌ Agent validation failed:\n")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print("✅ All agent.md files passed validation.")

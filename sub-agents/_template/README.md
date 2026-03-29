# Sub-Agent Template

This folder contains the official template for creating new sub-agent definitions in the OpenClaw Agent Project.

## Files

- `sub-agent.md` — The master template that all sub-agent definitions must follow

## How to Use This Template

1. **Copy this folder** to the appropriate category directory:

   ```bash
   cp -r sub-agents/_template sub-agents/research/my-new-sub-agent
   ```

2. **Ensure** `sub-agent.md` remains named `sub-agent.md` — do not rename this file

3. **Fill in the frontmatter** — replace all empty `""` values with real content

4. **Write all required sections** with specific, useful content

5. **Add a `README.md`** in your sub-agent folder describing what it does

## Required Frontmatter Fields

| Field | Description |
| --- | --- |
| `name` | Display name of the sub-agent |
| `version` | Semantic version, start with `"1.0.0"` |
| `author` | Your GitHub username |
| `description` | One sentence summary |
| `category` | One of: `research`, `communication`, `productivity`, `data` |
| `tags` | List of descriptive tags |
| `parent_agent_compatible` | Parent agents that are allowed to delegate to this sub-agent |
| `trigger_phrases` | Example phrases that activate this sub-agent |
| `output_format` | One of: `text`, `json`, `markdown`, `action` |

## Dependency Mapping Guidance

- Use `parent_agent_compatible` to describe which parent agents may delegate to this sub-agent.
- Prefer parent agent display names from the agent's `name` field (for example, `Maxwell`), even though validators also accept folder slugs for backward compatibility.
- If this sub-agent is part of a larger chain, document the upstream workers or artifacts it expects in `Input Expected` and in the folder README.
- Keep compatible-parent declarations in sync with any parent agent that lists this sub-agent in its `sub_agents` frontmatter.

## Required Markdown Sections

Every `sub-agent.md` must include these sections:

- `## Purpose`
- `## Activation Criteria`
- `## Input Expected`
- `## Output Produced`
- `## Execution Steps`
- `## Error Handling`
- `## Customization Notes`

For the full specification, see [`docs/sub-agent-spec.md`](../../docs/sub-agent-spec.md).

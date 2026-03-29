# Sub-Agent Specification (`sub-agent.md` Format)

This document defines the full specification for the `sub-agent.md` format used by all sub-agent definitions in the OpenClaw Agent Project.

---

## Overview

Every sub-agent is defined by a single `sub-agent.md` file that contains:

1. **YAML frontmatter** (between `---` delimiters) — structured metadata
2. **Markdown body** — the sub-agent's purpose, activation criteria, input/output contract, and execution logic

---

## YAML Frontmatter Specification

```yaml
---
name: ""                          # Display name of the sub-agent (required)
version: "1.0.0"                  # Semantic version (required)
author: ""                        # GitHub username (required)
description: ""                   # One sentence summary (required)
category: ""                      # research | communication | productivity | data | developer (required)
tags: []                          # Descriptive tags
parent_agent_compatible: []       # Agent names this sub-agent pairs with
trigger_phrases: []               # Example phrases that activate this sub-agent (required)
output_format: ""                 # text | json | markdown | action (required)
skills_required: []               # OpenClaw skills this sub-agent needs
---

```

### Field Reference

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | ✅ Yes | The sub-agent's display name |
| `version` | string | ✅ Yes | Semantic version. Start at `"1.0.0"` |
| `author` | string | ✅ Yes | GitHub username of the contributor |
| `description` | string | ✅ Yes | One sentence describing what the sub-agent does |
| `category` | string | ✅ Yes | Must be one of: `research`, `communication`, `productivity`, `data`, `developer` |
| `tags` | array | ✅ Yes | Descriptive lowercase tags |
| `parent_agent_compatible` | array | No | Names of parent agents that work with this sub-agent. If provided, each entry must resolve to an existing agent definition in this repository (folder name or agent `name`). |
| `trigger_phrases` | array | ✅ Yes | Example phrases that cause a parent agent to delegate here |
| `output_format` | string | ✅ Yes | One of: `text`, `json`, `markdown`, `action` |
| `skills_required` | array | No | OpenClaw skills required by this sub-agent |

### Output Format Definitions

| Format | Description |
| --- | --- |
| `text` | Plain text response, no special formatting |
| `json` | Structured JSON object for machine consumption |
| `markdown` | Formatted markdown for display to users or parent agents |
| `action` | Triggers an OpenClaw action (send message, create event, etc.) |

---

## Markdown Body Specification

The body of `sub-agent.md` must include all of the following sections:

### `## Purpose`

One focused paragraph describing exactly what this sub-agent does. Be specific — a sub-agent does one thing well.

### `## Activation Criteria`

A bullet list of conditions under which a parent agent should delegate to this sub-agent. These should be specific enough that a parent agent can use them as routing rules.

### `## Input Expected`

A table describing all inputs this sub-agent accepts:

| Input | Type | Required | Description |
| --- | --- | --- | --- |
| `field_name` | string/integer/boolean | Yes/No | What this field contains |

### `## Output Produced`

Describe exactly what this sub-agent returns, including:

- The structure and format of the output
- A markdown template or JSON schema showing the expected output shape
- What to expect if results are partial or incomplete

### `## Execution Steps`

A numbered list of exactly what the sub-agent does when activated:

1. Receive and validate inputs
2. Execute core task
3. Format output
4. Return to parent agent or user

Be specific enough that someone could implement this sub-agent from scratch using these steps.

### `## Error Handling`

Describe how the sub-agent handles each failure mode:

- Missing required inputs
- Ambiguous requests
- Unavailable skills or services
- Partial or no results
- Data format errors

### `## Customization Notes`

Guidance for users who want to adapt this sub-agent:

- Which fields are safe to modify
- How to change output format or depth
- Integration options with external tools

---

## Validation

All `sub-agent.md` files are validated by CI. See [`.github/scripts/validate_sub_agents.py`](../.github/scripts/validate_sub_agents.py).

To validate locally:

```bash
pip install python-frontmatter
python .github/scripts/validate_sub_agents.py

```

# Agent Specification (`agent.md` Format)

This document defines the full specification for the `agent.md` format used by all agent personas in the OpenClaw Agent Project.

---

## Overview

Every agent is defined by a single `agent.md` file that contains:

1. **YAML frontmatter** (between `---` delimiters) — structured metadata about the agent
2. **Markdown body** — the actual persona definition, behaviors, and examples

---

## YAML Frontmatter Specification

```yaml
---
name: ""                          # Display name of the agent (required)
version: "1.0.0"                  # Semantic version (required)
author: ""                        # GitHub username of the author (required)
description: ""                   # One sentence summary (required)
category: ""                      # personal | professional | developer | creative | team (required)
tags: []                          # Descriptive tags, e.g. [productivity, scheduling]
openclaw_min_version: ""          # Optional minimum OpenClaw version required
comms_channels: []                # e.g. [telegram, discord, whatsapp, slack, imessage, signal]
skills_required: []               # OpenClaw skills this agent depends on
sub_agents: []                    # Sub-agent names this agent delegates to
model_recommendations:
  primary: ""                     # e.g. claude-3-5-sonnet, gpt-4o
  fallback: ""                    # Fallback model if primary is unavailable
memory_profile: ""                # minimal | standard | deep (required)
heartbeat_enabled: false          # true or false (required)
---

```

### Field Reference

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | ✅ Yes | The agent's display name (e.g., "Aria") |
| `version` | string | ✅ Yes | Semantic version number. Start at `"1.0.0"` |
| `author` | string | ✅ Yes | GitHub username of the contributor |
| `description` | string | ✅ Yes | One sentence describing what the agent does |
| `category` | string | ✅ Yes | Must be one of: `personal`, `professional`, `developer`, `creative`, `team` |
| `tags` | array | ✅ Yes | List of descriptive lowercase tags |
| `openclaw_min_version` | string | No | Minimum OpenClaw version required (e.g., `"1.2.0"`) |
| `comms_channels` | array | ✅ Yes | Chat channels the agent supports (at least one required) |
| `skills_required` | array | No | List of OpenClaw skill names required |
| `sub_agents` | array | No | Names of sub-agents this agent delegates to. If provided, each entry must resolve to an existing sub-agent definition in this repository (folder name or sub-agent `name`). |
| `model_recommendations.primary` | string | No | Recommended primary model (e.g., `claude-3-5-sonnet`) |
| `model_recommendations.fallback` | string | No | Fallback model if primary is unavailable |
| `memory_profile` | string | ✅ Yes | One of: `minimal`, `standard`, `deep` |
| `heartbeat_enabled` | boolean | ✅ Yes | Whether this agent uses OpenClaw's heartbeat feature |

### Memory Profile Definitions

| Profile | Description |
| --- | --- |
| `minimal` | Retains only critical preferences. Forgets most conversation history. |
| `standard` | Retains preferences, recurring patterns, and recent context. |
| `deep` | Full persistent memory. Retains contacts, history, commitments, and long-term context. |

---

## Markdown Body Specification

The body of `agent.md` must include all of the following sections, in order:

### `## Persona`

Write in second person ("You are...") as if briefing the AI on its role and character. Include:

- The agent's name and role
- Personality traits and values
- How the agent thinks about its job

### `## Core Behaviors`

A bullet list of specific behavioral rules. Each rule should be:

- Actionable and specific (not vague like "be helpful")
- Written as a directive ("Always...", "Never...", "When X, do Y")

### `## Communication Style`

Describe how the agent communicates:

- Tone (warm, formal, direct, casual)
- Response length defaults
- Formatting preferences (markdown, bullets, tables)
- Language register and vocabulary guidance

### `## Capabilities`

A bullet list of what this agent is specifically designed to do. Keep to concrete capabilities, not aspirations.

### `## Constraints`

A bullet list of what this agent must NOT do. Be specific about:

- Actions that require user confirmation
- Data the agent should not access or share
- Topics or domains outside its scope

### `## Memory Guidelines`

Describe the agent's memory behavior:

- What to remember long-term
- What to remember short-term
- What to forget immediately or after task completion

### `## Heartbeat Behavior`

If `heartbeat_enabled: true`, describe exactly what the agent does on each heartbeat trigger:

- What time(s) it fires
- What data it fetches
- What actions it takes
- What it sends to the user

If `heartbeat_enabled: false`, write "Not applicable."

### `## Customization Notes`

Guidance for users who want to adapt this agent:

- Which fields are safe to change
- How to adjust behavior without breaking it
- Common customization scenarios

### `## Example Interactions`

At least 2–3 sample prompt/response pairs showing the agent in realistic use. These must be:

- Complete and realistic (not just "User: Hello / Agent: Hi!")
- Representative of the agent's core capabilities
- Demonstrating the agent's communication style

---

## Validation

All `agent.md` files in this repository are automatically validated by the CI workflow. See [`.github/scripts/validate_agents.py`](../.github/scripts/validate_agents.py) for the validation logic.

To validate locally:

```bash
pip install python-frontmatter
python .github/scripts/validate_agents.py

```

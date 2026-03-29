# Agent Template

This folder contains the official template for creating new agent personas in the OpenClaw Agent Project.

## Files

- `agent.md` — The master template that all agent personas must follow

## How to Use This Template

1. **Copy this folder** to the appropriate category directory:

   ```bash
   cp -r agents/_template agents/personal/my-new-agent
   ```

2. **Ensure** `agent.md` remains named `agent.md` — do not rename this file

3. **Fill in the frontmatter** — replace all empty `""` values with real content

4. **Write the body sections** — replace all placeholder comments with real content

5. **Add a `README.md`** in your new agent folder describing what the agent does

6. **Test your agent** with a real OpenClaw instance before submitting a PR

## Required Frontmatter Fields

| Field | Description |
| --- | --- |
| `name` | Display name of the agent (e.g., "Aria") |
| `version` | Semantic version, start with `"1.0.0"` |
| `author` | Your GitHub username |
| `description` | One sentence summary of the agent |
| `category` | One of: `personal`, `professional`, `developer`, `creative`, `team` |
| `tags` | List of descriptive tags |
| `comms_channels` | Chat channels this agent is designed for |
| `sub_agents` | Optional list of required sub-agent folder slugs used by this agent |
| `memory_profile` | One of: `minimal`, `standard`, `deep` |
| `heartbeat_enabled` | `true` or `false` |

## Dependency Mapping Guidance

- Use `sub_agents` only for workers this agent actually depends on at runtime.
- Prefer sub-agent folder slugs in `sub_agents` (for example, `email-manager`), even though validators also accept the display `name` field for backward compatibility.
- In the agent README, list each required sub-agent with its category path so readers can find the install location quickly.
- If the agent orchestrates a chain of workers, describe which tasks route to which sub-agent in `Core Behaviors`, `Capabilities`, and the README Requirements section.

## Required Markdown Sections

Every `agent.md` must include these sections:

- `## Persona`
- `## Core Behaviors`
- `## Communication Style`
- `## Capabilities`
- `## Constraints`
- `## Memory Guidelines`
- `## Heartbeat Behavior`
- `## Customization Notes`
- `## Example Interactions` (must contain at least 2 real examples)

For the full specification, see [`docs/agent-spec.md`](../../docs/agent-spec.md).

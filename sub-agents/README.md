# Sub-Agents

Sub-agents are focused, task-specific modules that a parent agent can delegate to. They are designed to perform a single job well and return structured output that the parent agent (or user) can act on.

![Agent Actions](../Agent%20actions.png)

## Categories

| Category | Description |
| --- | --- |
| [communication/](./communication/) | Email, messaging, and communication management |
| [data/](./data/) | Data analysis, transformation, and insights |
| [developer/](./developer/) | Code generation, project planning, and code review |
| [productivity/](./productivity/) | Task tracking, project management, and scheduling |
| [research/](./research/) | Web research and information gathering |

## How Sub-Agents Work

A parent agent (like Maxwell or Velocity) delegates to a sub-agent when a specific task requires focused execution. For example:

- Maxwell delegates email triage to `email-manager`
- Hex delegates documentation lookup to `web-researcher`
- Velocity delegates task updates to `task-tracker`

Agents declare these required installs in their `sub_agents` frontmatter using sub-agent folder slugs such as `email-manager` or `task-tracker`. Sub-agents declare compatible parents in `parent_agent_compatible`, which allows chaining without forcing every compatible parent to depend on them.

Sub-agents can also be activated directly by the user without a parent agent.

## How to Use a Sub-Agent

1. Browse the category folders above to find the right sub-agent
2. Copy the `sub-agent.md` file to your OpenClaw sub-agents directory
3. Reference it in your parent agent's `sub_agents` field (or use it standalone)
4. Customize the `trigger_phrases` and `output_format` to match your workflow

If you are building a chain of agents and sub-agents, document both sides of the relationship: add the sub-agent slug to the parent agent's `sub_agents` list, and add the parent agent display name to the sub-agent's `parent_agent_compatible` list.

## Adding a New Sub-Agent

See [`_template/`](./_template/) for the official sub-agent template, and [`CONTRIBUTING.md`](../CONTRIBUTING.md) for contribution guidelines.

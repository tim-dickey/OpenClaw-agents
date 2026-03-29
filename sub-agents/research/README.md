# Research Sub-Agents

Research sub-agents handle information gathering, web research, and knowledge retrieval tasks on behalf of parent agents or users.

## Available Sub-Agents

| Sub-Agent | Description |
| --- | --- |
| [web-researcher](./web-researcher/) | Performs targeted web research and returns structured markdown summaries with sources |

## Use Cases

Research sub-agents are ideal when a parent agent needs to:

- Look up documentation, APIs, or best practices
- Find current information (news, prices, events)
- Verify factual claims before including them in output
- Research a topic to inform a recommendation or analysis

## Adding a Research Sub-Agent

Copy the template from [`sub-agents/_template/`](../_template/), place it in a new kebab-case folder here, and fill in all fields. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

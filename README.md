# OpenClaw Agents Project

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](./CONTRIBUTING.md)

> A community collection of downloadable, editable agent and sub-agent personas for use with [OpenClaw](https://openclaw.ai)

![OpenClaw Agent Project](./OpenClaw%20agent%20project.png)

---

## What is OpenClaw?

[OpenClaw](https://openclaw.ai) is an open-source personal AI assistant that runs on your own machine. It connects to any chat app — WhatsApp, Telegram, Discord, Slack, Signal, iMessage — and supports persistent memory, browser control, skills/plugins, and full system access. You own your AI, your data, and your agents.

---

## What Are Agents and Sub-Agents?

**Agents** are fully defined AI personas that you load into OpenClaw. Each agent has a unique name, personality, communication style, set of capabilities, and behavioral rules. Think of an agent as a dedicated team member with a specific role.

**Sub-agents** are focused, task-specific modules that a parent agent can delegate to. For example, an executive assistant agent might delegate email triage to an `email-manager` sub-agent, and research tasks to a `web-researcher` sub-agent. Sub-agents are designed to be composable and reusable.

---

## How to Use

1. **Clone this repository** (or browse it on GitHub)
2. **Browse** the [`agents/`](./agents/) or [`sub-agents/`](./sub-agents/) directories to find a persona that fits your needs
3. **Copy** `agent.md` into your OpenClaw agents directory (for sub-agents, place `sub-agent.md` under `sub-agents/`)
4. **Customize** the file to match your preferences, tone, and context
5. **Restart or hot-reload** your OpenClaw instance
6. **Engage** via your chosen chat channel — WhatsApp, Telegram, Discord, or others

For detailed setup instructions, see [`docs/getting-started.md`](./docs/getting-started.md).
For customization help, see [`docs/customization-guide.md`](./docs/customization-guide.md).
For executable behavioral contract tests, see [`tests/README.md`](./tests/README.md).

---

## Quality Signals

This repository now uses two complementary validation layers for agent behavior:

- [`evals/`](./evals/) holds deterministic offline fixtures with schema and target-reference validation only
- [`tests/`](./tests/) holds executable pytest-based behavioral contract tests for TDD workflows

Use fixtures to document intended behavior in a reviewable format, and use behavioral contract tests when you want runnable pass/fail checks.

---

## Table of Contents

- [agents/](./agents/) — Browse all agent personas by category

  - [agents/personal/](./agents/personal/) — Personal productivity agents
  - [agents/professional/](./agents/professional/) — Professional and workplace agents
  - [agents/developer/](./agents/developer/) — Developer-focused agents
  - [agents/creative/](./agents/creative/) — Creative writing and content agents
  - [agents/team/](./agents/team/) — Team collaboration agents

- [sub-agents/](./sub-agents/) — Browse all sub-agent modules by category

  - [sub-agents/research/](./sub-agents/research/) — Research and information gathering
  - [sub-agents/communication/](./sub-agents/communication/) — Email and messaging
  - [sub-agents/productivity/](./sub-agents/productivity/) — Task and project management
  - [sub-agents/data/](./sub-agents/data/) — Data analysis and insights

- [docs/](./docs/) — Full documentation

  - [Getting Started](./docs/getting-started.md)
  - [Agent Spec](./docs/agent-spec.md)
  - [Sub-Agent Spec](./docs/sub-agent-spec.md)
  - [Customization Guide](./docs/customization-guide.md)
  - [Roadmap](./ROADMAP.md)
- [tests/](./tests/) — Executable behavioral contract tests and TDD workflow

---

## Featured Agents

| Agent | Category | Description |
| --- | --- | --- |
| [Aria](./agents/personal/daily-briefing/) | Personal | Morning briefing agent — calendar, weather, news, tasks |
| [Maxwell](./agents/professional/executive-assistant/) | Professional | Executive assistant — email triage, scheduling, follow-ups |
| [Hex](./agents/developer/code-reviewer/) | Developer | Code reviewer — bugs, style, security, GitHub integration |
| [Lyra](./agents/creative/content-writer/) | Creative | Content writer — blog posts, social media, newsletters |
| [Velocity](./agents/team/scrum-master-coach/) | Team | Scrum Master \| Coach — Daily Scrum facilitation, Sprint Backlog tracking, impediment alerts |

---

## Featured Sub-Agents

Agents declare required sub-agent installs in frontmatter `sub_agents` using sub-agent folder slugs. If an agent README mentions a dependency, browse the matching category under `sub-agents/` to find it.

| Sub-Agent | Category | Description |
| --- | --- | --- |
| [web-researcher](./sub-agents/research/web-researcher/) | Research | Targeted web research with structured summaries |
| [email-manager](./sub-agents/communication/email-manager/) | Communication | Email triage and draft replies |
| [task-tracker](./sub-agents/productivity/task-tracker/) | Productivity | Task capture, categorization, and updates |
| [data-analyst](./sub-agents/data/data-analyst/) | Data | Data analysis with insights and anomaly flags |

---

## Contributing

We welcome contributions from the OpenClaw community! To submit a new agent or sub-agent:

1. Use the [new agent issue template](./.github/ISSUE_TEMPLATE/new-agent.md) to propose your idea
2. Fork this repo and create your agent using the [template](./agents/_template/)
3. Open a pull request — your submission will be automatically validated by CI

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full guidelines, quality standards, and naming conventions.

---

## License

This project is licensed under the [MIT License](./LICENSE). All contributed agents and sub-agents are shared under the same license unless otherwise noted.

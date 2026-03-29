# Getting Started with OpenClaw Agents

Welcome! This guide walks you through downloading and deploying an agent or sub-agent from this collection into your OpenClaw instance.

---

## Prerequisites

Before you begin, you'll need:

- **OpenClaw installed and running** on your machine

  - Download and installation instructions: [https://openclaw.ai](https://openclaw.ai)
  - Ensure OpenClaw is configured with at least one communication channel (Telegram, Discord, WhatsApp, Slack, Signal, or iMessage)

- **A GitHub account** (optional, for contributing back to the community)
- **Basic familiarity with editing text files** — agent files are simple markdown with YAML frontmatter

---

## Step 1: Browse the Collection

Start by browsing the [`agents/`](../agents/) or [`sub-agents/`](../sub-agents/) directories to find a persona that fits your needs.

Each agent and sub-agent has:

- A `README.md` describing what it does, its requirements, and usage tips
- An `agent.md` or `sub-agent.md` file that contains the actual persona definition

Take a few minutes to read the README before downloading — it will tell you which OpenClaw skills are required and which sub-agents need to be installed alongside it.

---

## Step 2: Download or Copy the Agent File

**Option A — Clone the repo (recommended):**

```bash
git clone https://github.com/<your-username-or-org>/OpenClaw-agents-project.git
cd OpenClaw-agents-project

```

This gives you the full collection locally, and makes it easy to pull updates as new agents are added.

**Option B — Download just the file:**

Navigate to the agent folder on GitHub, open `agent.md`, and click the **Raw** button. Then save the file to your machine.

---

## Step 3: Place the File in Your OpenClaw Directory

Copy the `agent.md` file into your OpenClaw agents directory. For sub-agents, place `sub-agent.md` under the `sub-agents/` folder inside that agents directory.

The default location varies by platform:

| Platform | Default Path |
| --- | --- |
| macOS | `~/.openclaw/agents/` |
| Linux | `~/.openclaw/agents/` |
| Windows | `%APPDATA%\OpenClaw\agents\` |

If you're unsure, check your OpenClaw config file or the OpenClaw documentation at [https://openclaw.ai](https://openclaw.ai).

**Recommended structure:**

```text
~/.openclaw/agents/
├── daily-briefing/
│   └── agent.md
├── executive-assistant/
│   └── agent.md
└── sub-agents/
    └── email-manager/
        └── sub-agent.md

```

---

## Step 4: Restart or Hot-Reload OpenClaw

After placing the file:

- **Full restart:** Stop and restart the OpenClaw process
- **Hot-reload (if supported):** Run `openclaw reload` or use the reload command in your OpenClaw admin interface

OpenClaw will detect the new agent file and make it available.

---

## Step 5: Engage via Your Chosen Chat Channel

Open your configured chat channel (Telegram, Discord, etc.) and address the agent by its configured name.

For example, if you installed the Aria daily briefing agent:

> "Hey Aria, give me my morning briefing."

If you installed Maxwell:

> "Maxwell, triage my inbox."

The agent will introduce itself on first use and may ask a few setup questions to personalize its behavior.

---

## Next Steps

- **Customize your agent:** See [`customization-guide.md`](./customization-guide.md) for how to adapt agent personas, memory settings, and behaviors
- **Install sub-agents:** If your agent requires sub-agents (check the `sub_agents` field in the frontmatter), install those too by repeating the steps above for each sub-agent file
- **Contribute your own:** If you create a great agent, share it with the community — see [`CONTRIBUTING.md`](../CONTRIBUTING.md)

---

## Troubleshooting

**The agent isn't responding:**

- Verify that OpenClaw is running and connected to your chat channel
- Check that the `agent.md` file is in the correct directory
- Ensure all required skills listed in `skills_required` are installed and configured

**The agent is responding but behaving unexpectedly:**

- Review the `agent.md` file — check the Persona and Core Behaviors sections
- Try clearing the agent's memory and starting fresh
- Open a [bug report](../issues/new?template=bug-report.md) if the issue seems like a problem with the agent definition itself

**Skills are missing:**

- Visit [https://openclaw.ai](https://openclaw.ai) for the skills directory and installation instructions

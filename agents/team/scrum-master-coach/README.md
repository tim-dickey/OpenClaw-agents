# Velocity — Scrum Master | Coach

**Category:** Team
**Agent file:** `agent.md`

## What Velocity Does

Velocity is your team's AI-powered Scrum Master | Coach. Designed for Discord and Slack, Velocity keeps your team aligned and Sprints on track:

- 🏃 **Daily Scrum** — Prompts the team, collects updates, posts a formatted summary
- 🚧 **Impediment detection** — Flags impediments immediately with @mentions to the relevant lead
- 📊 **Sprint tracking** — Monitors Sprint Backlog progress and flags items at risk of missing the Sprint Goal
- 📋 **Sprint health reports** — Mid-Sprint snapshots and end-of-Sprint summaries
- 🔄 **Task coordination** — Delegates task updates to the `task-tracker` sub-agent in the productivity catalog

## Quick Start

1. Copy `agent.md` to your OpenClaw agents directory
2. Install the `task-tracker` sub-agent from the productivity catalog (`sub-agents/productivity/task-tracker/`)
3. Configure your Discord or Slack workspace in OpenClaw
4. Set your Daily Scrum time and Sprint schedule
5. Prime Velocity with your team roster: "Our team is: Alice (frontend), Bob (backend), Carol (QA)"
6. Set Sprint details: "We run 2-week Sprints. Current Sprint started March 25."
7. Restart OpenClaw — Velocity will post to your #daily-scrum channel at the configured time

## Requirements

- OpenClaw with heartbeat support enabled
- Discord or Slack integration configured in OpenClaw
- Skills: `calendar`, `reminder`
- Sub-agent: [`task-tracker`](../../../sub-agents/productivity/task-tracker/) from the productivity catalog

## Notes

Velocity is optimized for small to medium engineering teams (2–15 people). For larger teams, consider running multiple Velocity instances per sub-team and aggregating summaries manually.

Velocity currently declares one required sub-agent dependency: `task-tracker`. When a README or spec mentions that dependency, look for it under `sub-agents/productivity/`.

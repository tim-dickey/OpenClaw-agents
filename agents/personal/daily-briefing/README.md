# Aria — Daily Briefing Agent

**Category:** Personal
**Agent file:** `agent.md`

## What Aria Does

Aria is your personal morning briefing agent. Every day at your configured time (default: 7:00 AM), she sends you a crisp, organized digest covering:

- 📅 Today's calendar events
- ☀️ Local weather and forecast
- 📰 Top news headlines (customizable by topic)
- ✅ Pending and overdue tasks

Aria is designed to get you oriented and ready for the day in under 60 seconds of reading.

## Quick Start

1. Copy `agent.md` to your OpenClaw agents directory
2. Edit the frontmatter to set your preferred `comms_channels`
3. Ensure these OpenClaw skills are installed: `calendar`, `weather`, `news`, `task-manager`
4. Restart OpenClaw — Aria will introduce herself and confirm your briefing time
5. You can also trigger a manual briefing anytime by messaging: "Hey Aria, give me my briefing"

## Customization Tips

- **Change briefing time:** Tell Aria "Set my briefing for 6:30 AM" or adjust the heartbeat config
- **Focus news topics:** Tell Aria "I only want tech and business news"
- **Adjust verbosity:** Tell Aria "Give me shorter briefings" or "I want more detail on my calendar"

## Requirements

- OpenClaw with heartbeat support enabled
- Skills: `calendar`, `weather`, `news`, `task-manager`
- At least one communication channel configured (Telegram, WhatsApp, Discord, Slack, or iMessage)

## Readiness Status

| Dimension | Status | Evidence |
| --- | --- | --- |
| Spec validation | Pass | `py -3.13 .github/scripts/validate_agents.py` |
| Dependency validation | Pass | Agent dependency checks pass; this agent currently declares no sub-agent dependencies |
| Fixture coverage | Present | `evals/agents/aria/golden-morning-briefing/fixture.yml` |
| Negative-path coverage | Present | `evals/agents/aria/negative-fabricated-briefing-data/fixture.yml` |

Readiness reflects static repository validation and offline fixture coverage only. It does not claim runtime or live model evaluation.

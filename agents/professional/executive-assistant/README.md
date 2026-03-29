# Maxwell — Executive Assistant Agent

**Category:** Professional
**Agent file:** `agent.md`

## What Maxwell Does

Maxwell is a professional-grade executive assistant agent designed for high-performing individuals who need intelligent support managing their professional lives. Maxwell handles:

- **Email triage** — Prioritizes, categorizes, and drafts responses (uses `email-manager` from the communication catalog)
- **Meeting scheduling** — Checks availability, sends invites, manages rescheduling
- **Follow-up tracking** — Remembers open action items and surfaces them proactively
- **Document summaries** — Reads and summarizes reports, meeting notes, and briefing documents
- **Daily digest** — Delivers a structured morning and end-of-day briefing

## Quick Start

1. Copy `agent.md` to your OpenClaw agents directory
2. Install the required skills: `email`, `calendar`, `document-reader`, `reminder`
3. Install the `email-manager` sub-agent from the communication catalog (`sub-agents/communication/email-manager/`)
4. Configure your email and calendar integrations in OpenClaw
5. Set your working hours and timezone in the heartbeat configuration
6. Restart OpenClaw — Maxwell will introduce himself and confirm your setup

## Requirements

- OpenClaw with heartbeat support enabled
- Skills: `email`, `calendar`, `document-reader`, `reminder`
- Sub-agent: [`email-manager`](../../../sub-agents/communication/email-manager/) from the communication catalog
- Email and calendar integrations configured in OpenClaw

## Readiness Status

| Dimension | Status | Evidence |
| --- | --- | --- |
| Spec validation | Pass | `py -3.13 .github/scripts/validate_agents.py` |
| Dependency validation | Pass | Agent `sub_agents` cross-reference check validates `email-manager` |
| Fixture coverage | Present | `evals/agents/maxwell/golden-inbox-triage/fixture.yml` |
| Negative-path coverage | Present | `evals/agents/maxwell/negative-send-without-approval/fixture.yml` |

Readiness reflects static repository validation and offline fixture coverage only. It does not claim runtime or live model evaluation.

## Notes

Maxwell uses a deep memory profile, meaning he retains information across sessions including key contacts, recurring commitments, and open action items. To clear his memory, use the OpenClaw memory management commands.

Maxwell currently declares `email-manager` as a required dependency. Other sub-agents may be compatible with Maxwell, but only entries listed in the agent's `sub_agents` frontmatter are required installs.

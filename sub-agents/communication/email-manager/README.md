# email-manager — Communication Sub-Agent

**Category:** Communication
**Sub-agent file:** `sub-agent.md`

## What email-manager Does

The email-manager sub-agent triages your inbox and drafts replies for review. When activated, it:

1. Fetches and reads your unread or recent emails
2. Categorizes them by priority: 🔴 High, 🟡 Medium, 🟢 Low
3. Returns a structured triage table with summaries
4. Drafts responses to high-priority emails for your approval

**Returns:** A markdown triage report with priority table and draft replies.

## Compatible Parent Agents

- [Maxwell](../../../agents/professional/executive-assistant/) — primary partner; Maxwell delegates all email tasks to this sub-agent

## Requirements

- Skill: `email` (required for inbox access and sending)
- Email account configured in OpenClaw settings

## Direct Usage

You can also use this sub-agent directly without Maxwell:

- "Process my inbox"
- "Triage my email — show me what's urgent"
- "Draft a reply to the email from Sarah about the Q1 report"

## Readiness Status

| Dimension | Status | Evidence |
| --- | --- | --- |
| Spec validation | Pass | `py -3.13 .github/scripts/validate_sub_agents.py` |
| Dependency validation | Pass | `parent_agent_compatible` cross-reference check validates Maxwell |
| Fixture coverage | Present | `evals/sub-agents/email-manager/golden-inbox-triage/fixture.yml` |
| Negative-path coverage | Present | `evals/sub-agents/email-manager/negative-send-without-approval/fixture.yml` |

Readiness reflects static repository validation and offline fixture coverage only. It does not claim runtime or live model evaluation.

## Notes

email-manager never sends emails autonomously. All draft replies are returned for your review and require explicit "send" confirmation. You can edit any draft before sending by saying "edit draft 1: [your changes]".

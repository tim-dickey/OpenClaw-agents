# task-tracker — Productivity Sub-Agent

**Category:** Productivity
**Sub-agent file:** `sub-agent.md`

## What task-tracker Does

The task-tracker sub-agent is the memory layer for action items. It captures tasks from conversations, maintains a structured task list, and returns formatted updates on demand.

**Actions supported:**

- `capture` — Add a new task with optional assignee, due date, and priority
- `update` — Change the status or details of an existing task
- `list` — Get a formatted task list filtered by status, assignee, or category
- `complete` — Mark a task as done
- `delete` — Remove a task

**Returns:** Markdown-formatted task confirmations and task lists.

## Compatible Parent Agents

- [Velocity](../../../agents/team/scrum-master-coach/) — captures action items from Daily Scrum responses
- [Maxwell](../../../agents/professional/executive-assistant/) — tracks professional commitments and follow-ups

## Requirements

- No additional skills required — task-tracker uses OpenClaw's built-in memory

## Direct Usage

You can also use this sub-agent directly:

- "Add task: Review Q1 report, due Friday, assigned to me"
- "What tasks do I have open?"
- "Mark TASK-007 as done"
- "Show me all blocked tasks"

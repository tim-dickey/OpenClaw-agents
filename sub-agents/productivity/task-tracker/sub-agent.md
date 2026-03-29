---
name: "task-tracker"
version: "1.0.0"
author: "openclaw-community"
description: "Captures, categorizes, and updates tasks from conversations or instructions, returning a structured task list in markdown."
category: "productivity"
tags: [tasks, productivity, action-items, tracking, scrum, sprint]
parent_agent_compatible: [Velocity, Maxwell]
trigger_phrases:
  - "add a task"
  - "track this"
  - "don't forget to"
  - "action item"
  - "mark as done"
  - "what tasks are open"
  - "update task status"
  - "show me the task list"
output_format: "markdown"
skills_required: []
---

# task-tracker — Productivity Sub-Agent

## Purpose

The task-tracker sub-agent captures, organizes, and tracks tasks from conversational input. It extracts action items from messages, categorizes them by status and priority, and maintains a running task list that parent agents can query and update.

It is the memory layer for tasks — bridging the gap between what gets said in a conversation and what actually gets done.

## Activation Criteria

A parent agent should delegate to task-tracker when:

- The user or a team member mentions an action item, to-do, or commitment
- A Daily Scrum or meeting produces a list of action items to capture
- The user asks to see their current open tasks or a sprint task list
- A task's status needs to be updated (started, completed, blocked, deprioritized)
- The parent agent needs a task list to include in a summary or report

## Input Expected

| Input | Type | Required | Description |
| --- | --- | --- | --- |
| `action` | string | Yes | One of: `capture`, `update`, `list`, `complete`, `delete` |
| `task_text` | string | Conditional | The task description (required for `capture`) |
| `task_id` | string | Conditional | Task identifier (required for `update`, `complete`, `delete`) |
| `assignee` | string | No | Person responsible for the task |
| `due_date` | string | No | Due date in ISO 8601 format (YYYY-MM-DD) |
| `priority` | string | No | One of: `high`, `medium`, `low`. Default: `medium` |
| `status` | string | No | One of: `open`, `in-progress`, `blocked`, `done`. Default: `open` |
| `category` | string | No | Optional grouping label (e.g., sprint name, project name) |

## Output Produced

**For `capture` and `update` actions**, returns a confirmation:

```markdown
✅ Task captured: [task description]

- ID: TASK-042
- Assignee: [name or unassigned]
- Due: [date or unset]
- Priority: Medium
- Status: Open

```

**For `list` action**, returns a structured task table:

```markdown
## Task List — [Category or "All Open Tasks"]
*Updated: [timestamp]*

### 🔴 High Priority
| ID | Task | Assignee | Due | Status |
| --- | --- | --- | --- | --- |
| TASK-001 | Fix login bug | Alice | Mar 30 | In Progress |

### 🟡 Medium Priority
[Same table format]

### 🟢 Low Priority
[Same table format]

---
**Summary:** [N] open tasks · [N] in progress · [N] blocked · [N] completed today

```

## Execution Steps

1. Parse the `action` from the input
2. **For `capture`:** Extract task description, assignee, due date, and priority from the input; assign a unique task ID; store the task; return confirmation
3. **For `update`:** Locate the task by `task_id`; apply the status or field changes; return updated task summary
4. **For `list`:** Retrieve all tasks matching the requested filter (open, by category, by assignee); format as the structured task table; return it
5. **For `complete`:** Mark the task as done; record the completion timestamp; return confirmation
6. **For `delete`:** Remove the task; return confirmation with a brief note of what was deleted

## Error Handling

- **Missing `action`:** Return an error: "I need to know what you'd like to do — capture a task, update one, or list tasks?"
- **`task_id` not found:** Return: "I couldn't find task [ID]. Please check the ID and try again, or list all tasks to find the right one."
- **Ambiguous task from conversation:** Capture the task as best understood and flag: "Captured — but I wasn't sure about the assignee or due date. You can update these: 'Update TASK-042: assignee=Bob, due=March 31'"
- **Duplicate task detected:** Warn before capturing: "A similar task already exists (TASK-038: [description]). Add anyway? Reply 'yes' to confirm."
- **No tasks found for `list`:** Return: "No open tasks found matching your filter. All clear! ✅"

## Customization Notes

- **Task ID format:** Modify the ID prefix (`TASK-`) to match your team's convention (e.g., `SPR-` for sprint items)
- **Category defaults:** If you always work within a specific sprint or project, add a default `category` in the Execution Steps
- **Integration with external tools:** If your team uses Jira, Linear, or Notion, extend `skills_required` with the relevant integration skill and add a sync step to Execution Steps
- **Daily Scrum integration:** When used with Velocity, task-tracker receives bulk action items after each Daily Scrum — configure Velocity to pass Daily Scrum updates as a `capture` batch
- **Retention policy:** By default, completed tasks are retained for 30 days, then archived. Adjust this in your OpenClaw memory settings.

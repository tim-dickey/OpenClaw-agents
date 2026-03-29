---
name: ""
version: "1.0.0"
author: ""
description: ""
category: ""
tags: []
# List the parent agents that are allowed to delegate to this sub-agent.
# Prefer parent agent display names from agent frontmatter `name`
# (for example: [Maxwell, Jarvis]). Folder slugs are also accepted for backward compatibility.
parent_agent_compatible: []
trigger_phrases: []
output_format: ""
skills_required: []
---

# [Sub-Agent Name]

## Purpose

<!-- Specific focused task this sub-agent performs -->
<!-- Be precise — a sub-agent does ONE thing well -->

## Activation Criteria

<!-- When should a parent agent delegate to this sub-agent? -->
<!-- List the conditions or signals that should trigger delegation -->

- Condition 1
- Condition 2

## Input Expected

<!-- What information/context should be passed to this sub-agent -->
<!-- If this worker participates in a chain, list the upstream summaries or artifacts it expects from other agents or sub-agents. -->

| Input | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | string | Yes | The main request or question |
| `context` | string | No | Additional context from the parent agent |

## Output Produced

<!-- What this sub-agent returns to the parent agent or user -->
<!-- Be specific about the format and structure -->

Returns a `markdown` document containing:

- Summary section
- Key findings
- Sources or references (where applicable)

## Execution Steps

<!-- Step-by-step behavior — what does this sub-agent actually do? -->

1. Receive input from parent agent or user
2. Validate that required inputs are present
3. Execute the core task
4. Format the output according to the `output_format` specification
5. Return output to the parent agent or user

## Error Handling

<!-- What to do if input is missing, ambiguous, or task fails -->

- **Missing required input:** Ask the parent agent or user to provide the missing field before proceeding
- **Ambiguous request:** Return a clarifying question rather than guessing
- **Task failure:** Return a structured error message with the reason and suggested next steps
- **Partial results:** Return whatever was gathered with a clear note that results are incomplete

## Customization Notes

<!-- Guidance for users on how to adapt this sub-agent -->

- Adjust `trigger_phrases` to match the vocabulary your parent agent uses
- Modify `output_format` if your parent agent expects a different structure
- Update `skills_required` to match your OpenClaw skill configuration
- Keep `parent_agent_compatible` aligned with the parent agents that actually delegate here in this repository
- If this sub-agent depends on upstream summaries from other workers, document those handoff inputs clearly in `Input Expected` and your README so future chains stay coherent

---
name: "web-researcher"
version: "1.0.0"
author: "openclaw-community"
description: "Performs targeted web research when activated by a parent agent or user, returning structured markdown summaries with source links."
category: "research"
tags: [research, web, search, information-gathering, documentation, fact-checking]
parent_agent_compatible: [Hex, Maxwell, Lyra]
trigger_phrases:
  - "look this up"
  - "research"
  - "find information about"
  - "check the documentation for"
  - "what does the spec say about"
  - "verify this"
  - "search for"
output_format: "markdown"
skills_required: [browser]
---

# web-researcher — Research Sub-Agent

## Purpose

The web-researcher sub-agent performs focused, targeted web research on behalf of a parent agent or user. Given a research query and optional context, it searches the web, reads relevant sources, and returns a clean, structured markdown summary with source citations.

This sub-agent is designed for accuracy and efficiency — it reads deeply enough to answer the question, cites its sources, and signals confidence levels so the parent agent knows when to probe further.

## Activation Criteria

A parent agent should delegate to web-researcher when:

- The task requires looking up current or external information not in the model's training data
- A library version, API reference, or official documentation needs to be verified
- A factual claim in a draft or response needs to be checked before delivery
- The user asks the parent agent to "look something up," "research," or "find out about" a topic
- A CVE advisory, security bulletin, or technical standard needs to be referenced

## Input Expected

| Input | Type | Required | Description |
| --- | --- | --- | --- |
| `query` | string | Yes | The specific research question or topic |
| `context` | string | No | Background context from the parent agent (e.g., "This is for a Python code review") |
| `depth` | string | No | Research depth: `quick` (1–2 sources), `standard` (3–5 sources), `deep` (5+ sources). Default: `standard` |
| `output_type` | string | No | Focus of output: `summary`, `comparison`, `fact-check`, `documentation`. Default: `summary` |

## Output Produced

Returns a markdown document structured as follows:

```markdown
## Research Summary: [Query]

**Confidence:** High / Medium / Low
**Sources reviewed:** [N]
**Date researched:** [date]

### Key Findings

- Finding 1 (Source: [link])
- Finding 2 (Source: [link])
- Finding 3 (Source: [link])

### Summary

[2–4 paragraph synthesis of findings]

### Sources

1. [Source title](url) — [one-line description]
2. [Source title](url) — [one-line description]

```

If the query is a fact-check, output includes a **Verdict** field: ✅ Confirmed / ⚠️ Partially confirmed / ❌ Not supported.

## Execution Steps

1. Parse the `query` and `context` inputs
2. Formulate 1–3 targeted search queries based on the input
3. Execute web searches using the `browser` skill
4. Identify the 3–5 most relevant and credible sources
5. Read and extract key information from each source
6. Synthesize findings into the structured markdown format
7. Assign a confidence level based on source quality and consistency
8. Return the formatted research summary

## Error Handling

- **No results found:** Return a message indicating no relevant sources were found, and suggest alternative search terms the parent agent can try
- **Paywalled or inaccessible sources:** Skip and note that the top result(s) were inaccessible; proceed with available sources
- **Contradictory sources:** Report the contradiction explicitly rather than picking a side; present both perspectives with sources
- **Query too vague:** Return a clarifying question asking for a more specific query before proceeding
- **Browser skill unavailable:** Return an error message and instruct the parent agent to notify the user that web research is currently unavailable

## Customization Notes

- **Add search preferences:** Modify `trigger_phrases` to match the specific vocabulary your parent agent uses for research requests
- **Adjust depth defaults:** If your use case always requires deep research (e.g., security audits), change the default `depth` to `deep` in the Execution Steps
- **Domain filtering:** Add domain preferences in the Execution Steps if you want research scoped to specific sites (e.g., official documentation only)
- **Citation format:** Modify the Output Produced section if your parent agent expects a different citation format

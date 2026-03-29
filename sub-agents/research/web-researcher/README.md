# web-researcher — Research Sub-Agent

**Category:** Research
**Sub-agent file:** `sub-agent.md`

## What web-researcher Does

The web-researcher sub-agent performs targeted web research and returns clean, structured markdown summaries with source citations. It is activated by parent agents (like Hex or Maxwell) when they need current or external information, or by users directly.

**Returns:** A structured markdown summary with key findings, synthesis, and source links.

## Compatible Parent Agents

- [Hex](../../../agents/developer/code-reviewer/) — for documentation lookups and CVE research
- [Maxwell](../../../agents/professional/executive-assistant/) — for background research on contacts or topics
- [Lyra](../../../agents/creative/content-writer/) — for fact-checking and topic research before drafting

## Requirements

- Skill: `browser` (required for web search and reading)

## Direct Usage

You can also use this sub-agent directly without a parent agent:

- "Research the latest best practices for JWT authentication in Node.js"
- "Look up the OpenAI API rate limits"
- "Fact-check: Is Python the most popular programming language in 2024?"
- "Find the official documentation for the Stripe Webhooks API"

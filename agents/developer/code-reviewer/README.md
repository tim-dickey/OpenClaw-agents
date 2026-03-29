# Hex — Code Reviewer Agent

**Category:** Developer
**Agent file:** `agent.md`

## What Hex Does

Hex is a senior-grade code review agent designed for developers who want fast, thorough, and actionable feedback on their code. Hex reviews code for:

- 🔴 **Critical issues** — SQL injection, authentication flaws, data exposure
- 🟡 **Warnings** — Bugs, logic errors, missing validation, anti-patterns
- 🔵 **Style / Info** — Code quality, readability, test coverage gaps

Hex works with pasted code snippets, uploaded files, or directly with GitHub pull requests via the GitHub skill. When documentation lookup is needed, Hex delegates to the `web-researcher` sub-agent from the research catalog.

## Quick Start

1. Copy `agent.md` to your OpenClaw agents directory
2. Install the required skills: `github`, `browser`, `file-reader`
3. Install the `web-researcher` sub-agent from the research catalog (`sub-agents/research/web-researcher/`)
4. Configure the `github` skill with your GitHub access token
5. Restart OpenClaw
6. Submit code by pasting it in your chat channel or asking Hex to review a PR: "Hex, review PR #42 in my-repo"

## Requirements

- Skills: `github`, `browser`, `file-reader`
- Sub-agent: [`web-researcher`](../../../sub-agents/research/web-researcher/) from the research catalog
- GitHub personal access token configured (for PR review mode)

## Usage Examples

- "Hex, review this function: [paste code]"
- "Hex, review PR #47 in my-org/my-repo"
- "Hex, check this diff for security issues only"
- "Hex, what's the best practice for handling JWTs in Node.js?"

Hex currently declares one required sub-agent dependency: `web-researcher`. When you see Hex mention research lookups, the corresponding install lives under `sub-agents/research/`.

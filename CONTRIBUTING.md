# Contributing to OpenClaw Agent Project

Welcome, and thank you for your interest in contributing! This repository is a community-powered collection of agent and sub-agent personas for [OpenClaw](https://openclaw.ai). Every contribution helps make OpenClaw more useful for everyone.

---

## How to Submit a New Agent

1. **Open an issue** using the [new agent issue template](./.github/ISSUE_TEMPLATE/new-agent.md) to describe your agent idea and get early feedback from maintainers.
2. **Fork this repository** and create a new branch: `git checkout -b add-agent/your-agent-name`
3. **Copy the template** from [`agents/_template/`](./agents/_template/) into the appropriate category folder (e.g., `agents/personal/your-agent-name/`)
4. **Fill in every field** in the `agent.md` frontmatter and all required markdown sections
5. **Add a `README.md`** in your agent's folder describing what it does and how to use it
6. **Add validation artifacts** appropriate for the change: offline fixtures in [`evals/`](./evals/) and behavioral contract tests in [`tests/`](./tests/) when the behavior is important to preserve
7. **Test your agent** with a real OpenClaw instance before submitting
8. **Open a pull request** using the [PR template](./.github/PULL_REQUEST_TEMPLATE.md)

---

## Agent Quality Standards

All submitted agents must meet the following standards:

- **Use the official template** — [`agents/_template/agent.md`](./agents/_template/agent.md)
- **Complete all frontmatter fields** — especially `name`, `version`, `author`, `description`, `category`, `tags`, `comms_channels`, `memory_profile`, and `heartbeat_enabled`
- **Include all required markdown sections**: Persona, Core Behaviors, Communication Style, Capabilities, Constraints, Memory Guidelines, Heartbeat Behavior, Customization Notes, Example Interactions
- **Write real Example Interactions** — at least 2–3 sample prompt/response pairs showing the agent in action
- **Tested with OpenClaw** — confirm the agent has been loaded and tested with an actual OpenClaw instance
- **Use kebab-case folder names** — e.g., `my-research-agent/`, not `MyResearchAgent/`
- **Descriptive, unique names** — agent names should be memorable and reflect the agent's purpose
- **Validate `sub_agents` references** — each entry must match a real sub-agent definition in this repository (folder name or sub-agent `name`)

---

## Sub-Agent Quality Standards

All submitted sub-agents must meet the following standards:

- **Use the official template** — [`sub-agents/_template/sub-agent.md`](./sub-agents/_template/sub-agent.md)
- **Complete all frontmatter fields** — especially `name`, `version`, `author`, `description`, `category`, `tags`, `trigger_phrases`, and `output_format`
- **Include all required markdown sections**: Purpose, Activation Criteria, Input Expected, Output Produced, Execution Steps, Error Handling, Customization Notes
- **Specify compatible parent agents** in the `parent_agent_compatible` field when applicable
- **Define clear trigger phrases** — these help parent agents know when to delegate
- **Validate `parent_agent_compatible` references** — each entry must match a real agent definition in this repository (folder name or agent `name`)

---

## Readiness, Fixture, and TDD Expectations

Use readiness sections in agent and sub-agent `README.md` files to report verifiable status only.

This repository now has two separate behavior-validation layers:

- [`evals/`](./evals/) for deterministic offline fixtures and schema/reference validation
- [`tests/`](./tests/) for executable pytest-based behavioral contract tests

When fixtures are expected:

- New agents and sub-agents should include at least one offline fixture.
- Significant behavior changes should add or update fixtures.
- Readiness sections should include both a golden-path and a negative-path fixture when practical.

When behavioral contract tests are expected:

- Add or update `tests/cases/**` when the change introduces important approval gates, refusal behavior, delegation rules, terminology guarantees, or other contracts that should remain runnable.
- Prefer at least one golden-path and one negative-path test case for substantial new agents or sub-agents.
- Keep `evals/` and `tests/` aligned when they cover the same behavior, but do not duplicate them blindly. Fixtures document intent; tests execute assertions.

What readiness status can claim:

- Spec validation pass/fail
- Dependency validation pass/fail
- Fixture coverage presence
- Negative-path coverage presence

What readiness status must not claim:

- live runtime model quality
- production reliability guarantees
- benchmark scores not produced by repository tooling

See [docs/eval-fixture-spec.md](./docs/eval-fixture-spec.md) for fixture schema and examples, and [tests/README.md](./tests/README.md) for the executable TDD framework.

---

## Naming Conventions

- Folder names must use **kebab-case**: `daily-briefing/`, `code-reviewer/`, `web-researcher/`
- Agent file is always named `agent.md`
- Sub-agent file is always named `sub-agent.md`
- Every agent/sub-agent folder must include a `README.md`
- Category folders are lowercase: `personal/`, `professional/`, `developer/`, `creative/`, `team/`

---

## CI Validation

All submissions are automatically validated by GitHub Actions on every pull request.

Your PR must pass the following checks before merging:

| Check | What it validates |
| --- | --- |
| Validate Agent Templates | Required frontmatter fields, valid category, all required sections present, and valid `sub_agents` references |
| Validate Sub-Agent Templates | Required frontmatter fields, valid category, valid output_format, all sections, and valid `parent_agent_compatible` references |
| Validate Eval Fixtures | Fixture schema, valid target references, and fixture placement by target kind |
| Lint Markdown | Consistent markdown formatting across all .md files |

To run validation locally before submitting:

```bash
pip install pyyaml python-frontmatter
python .github/scripts/validate_agents.py
python .github/scripts/validate_sub_agents.py
python .github/scripts/validate_evals.py

```

To run the executable behavioral contract tests locally:

```bash
pip install -r tests/requirements.txt
pytest tests/ -v
```

Install markdownlint-cli2 for local markdown linting:

```bash
npm install -g markdownlint-cli2
markdownlint-cli2 "**/*.md"

```

---

## Markdown Authoring Guidelines

To keep markdown lint feedback actionable and low-noise, follow these conventions:

- Fenced code blocks must include a language (for example: yaml, bash, text).
- Put a blank line before and after lists and tables.
- Each markdown file must end with exactly one trailing newline.

Table separator style is flexible in this repository (compact and spaced forms are both acceptable).

## Local Markdown Lint Setup

Install dependencies and enable repository-managed git hooks:

```bash
npm install
npm run hooks:install
```

The pre-commit hook lints staged markdown files only (excluding `REFERENCE/**`).

Useful local commands:

```bash
npm run lint:md
npm run lint:md:fix
npm run lint:md:changed
```

---

## Code of Conduct

This project has a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to abide by it.

## Questions?

Open an issue or start a discussion. We're glad you're here!

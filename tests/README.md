# TDD Test Framework

A pytest-based behavioral and structural testing framework for agents and sub-agents.
This is **separate from the `evals/` eval fixture framework** and from the
CI validator scripts in `.github/scripts/`.

## Quick start

```bash
# Install dependencies
pip install -r tests/requirements.txt

# Run all tests in stub mode (default — free, deterministic, no API key needed)
pytest tests/ -v

# Run a single test file
pytest tests/test_agents.py -v

# Run against a real LLM (requires API key env var)
export OPENAI_API_KEY=sk-...        # or ANTHROPIC_API_KEY for claude models
pytest tests/ -v --live
```

## How it works

### Stub mode (default)

Each test case YAML contains a `stub_response` — the *ideal* output the agent
should produce. The test runner checks this response against the `assertions`
block (`must_include` / `must_not_include`).

This mode is:

- Free (no API calls)
- Deterministic (same result every run)
- CI-safe

It validates that the test case itself is internally coherent and that the
assertions are well-specified *before* any model is involved.

### Live mode (`--live`)

When `--live` is passed (or `LIVE_LLM=true` is set), the framework:

1. Loads the target agent/sub-agent spec from its `.md` file
2. Builds a system prompt from the spec body
3. Calls the model declared in the spec frontmatter
4. Checks the real model response against the same assertions

## TDD workflow

1. **Write the test case first** — define `input`, `assertions`, and a
   `stub_response` that represents the ideal output.
2. **Run stub mode** — `pytest tests/ -v` must pass before you write the spec.
3. **Write/refine the agent spec** — iterate on the agent or sub-agent `.md`.
4. **Run live mode** — `pytest tests/ -v --live` validates the real model.
5. **Iterate** until live tests pass.

This workflow forces you to define *what "done" looks like* before building.

## Test case format

```yaml
schema_version: 1
id: my-agent-scenario-golden         # kebab-case, unique within tests/
target:
  kind: agent                         # agent | sub-agent
  ref: Maxwell                        # name as declared in agent.md frontmatter
description: What this test validates
input:
  user: The prompt given to the agent
  context: Optional additional context
stub_response: |
  The ideal response the agent should produce.
  Written by the developer as part of the test design.
assertions:
  must_include:
    - pattern that must appear in the response  # case-insensitive
    - another required pattern
  must_not_include:
    - pattern that must NOT appear             # e.g. "email has been sent"
```

## Directory layout

```text
tests/
  conftest.py                   # Discovery, --live flag, shared fixtures and dependency helpers
  test_agents.py                # Parametrized behavioral contract tests for agents
  test_sub_agents.py            # Parametrized behavioral contract tests for sub-agents
  test_dependency_graph.py      # Structural dependency validation across agents and sub-agents
  requirements.txt              # pytest + pyyaml + python-frontmatter (+ optional LLM clients)
  runner/
    __init__.py                 # run_case(case, mode) dispatch
    assertions.py               # must_include / must_not_include helpers
    stub_runner.py              # Returns stub_response from case YAML
    live_runner.py              # Calls real LLM API (openai or anthropic)
  cases/
    agents/
      code-reviewer/
        golden-doc-lookup-delegation.yml
      maxwell/
        golden-inbox-triage.yml
        negative-send-without-approval.yml
      aria/
        golden-morning-briefing.yml
      jarvis/
        golden-mission-orchestration.yml
      scrum-master-coach/
        golden-daily-scrum-facilitation.yml
        golden-mid-sprint-health.yml
        negative-impediment-never-skipped.yml
        negative-no-autonomous-ticket-creation.yml
    sub-agents/
      email-manager/
        golden-inbox-triage.yml
      jarvis-ops-briefing/
        golden-daily-briefing.yml
```

## Common Suite Design

The executable pytest suite already shares a common loader, assertion engine,
and runner stack through `conftest.py` and `tests/runner/`. That common
infrastructure is the right place to unify behavior.

Keep these top-level suites separate:

- `test_agents.py` for agent behavior
- `test_sub_agents.py` for sub-agent behavior
- `test_dependency_graph.py` for structural dependency integrity
- `.github/scripts/validate_*.py` for repository-spec validation
- `evals/` for offline, reviewable fixture documentation

This keeps failures readable while still reusing the same underlying plumbing.
A single giant suite would blur behavior, structure, and repository linting into
one signal-poor test run.

## Naming conventions

- Case files: `golden-<scenario>.yml` or `negative-<scenario>.yml`
- Case IDs: `<agent-slug>-<scenario>-tdd-golden` or `-tdd-negative`
- One case per `.yml` file
- Directory per agent/sub-agent slug under `cases/agents/` or `cases/sub-agents/`

## Difference from `evals/`

| | `evals/` | `tests/` |
| --- | --- | --- |
| Execution | Schema validation only | Runs and produces pass/fail |
| Default mode | Always offline | Stub (offline) or Live (online) |
| Purpose | Document expected behavior | Test-drive behavior |
| Runner | `validate_evals.py` | `pytest` |
| CI | `validate-evals.yml` | Tooling and local execution |

## Current seeded coverage

- Agents: Maxwell, Aria, Jarvis, Velocity, Hex
- Sub-agents: email-manager, jarvis-ops-briefing
- Structural dependency coverage: reciprocal parent/dependency mapping, duplicate dependency detection, alias uniqueness

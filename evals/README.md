# Offline Evals

This directory holds deterministic, offline eval fixtures for repository agents and sub-agents.

This is separate from the executable behavioral contract test framework in [`tests/`](../tests/).

Phase 2 provides:

- a repository-local fixture format
- seeded golden-path and negative-path cases
- a schema validator with target-reference checks
- no live model execution
- no pytest-based runnable assertions

Use [`evals/`](./) when you want reviewable, deterministic behavior documentation.
Use [`tests/`](../tests/) when you want runnable pass/fail checks for TDD.

## Layout

```text
evals/
  agents/
    maxwell/
    aria/
    jarvis/
  sub-agents/
    email-manager/
    jarvis-ops-briefing/
```

Each case lives in its own folder and uses `fixture.yml` or `fixture.yaml`.

## Commands

```powershell
py -3.13 .github/scripts/validate_evals.py
```

Run the broader validation set when changing definitions and fixtures together:

```powershell
py -3.13 .github/scripts/validate_agents.py
py -3.13 .github/scripts/validate_sub_agents.py
py -3.13 .github/scripts/validate_evals.py
```

## Seeded Targets

Agents:

- Maxwell
- Aria
- J.A.R.V.I.S.

Sub-agents:

- email-manager
- jarvis-ops-briefing

See [docs/eval-fixture-spec.md](../docs/eval-fixture-spec.md) for the schema and validation rules.
See [tests/README.md](../tests/README.md) for the separate executable TDD framework.

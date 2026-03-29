# Eval Fixture Spec

This repository uses offline eval fixtures to document intended agent and sub-agent behavior in a deterministic, reviewable format. Phase 2 adds schema validation only. It does not invoke live models, call external services, or assert semantic correctness at runtime.

This fixture spec is separate from the executable behavioral contract testing framework in [`tests/`](../tests/). Fixtures document intent; the pytest framework executes assertions.

## Goals

- Keep fixtures simple enough to review in pull requests.
- Make target references explicit and repository-local.
- Allow both golden-path and negative-path cases.
- Establish a stable format for later deterministic and model-backed evaluation phases.

## Directory Layout

```text
evals/
  README.md
  agents/
    <target-alias>/
      <case-alias>/
        fixture.yml
  sub-agents/
    <target-alias>/
      <case-alias>/
        fixture.yml

```

- Place agent fixtures under `evals/agents/`.
- Place sub-agent fixtures under `evals/sub-agents/`.
- Keep each fixture in its own folder and name the file `fixture.yml` or `fixture.yaml`.
- The directory name is organizational only. The validator trusts `target.kind` and `target.ref`.

## Fixture Schema

Each fixture must be a YAML object with the following fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `schema_version` | integer | Yes | Must equal `1` for this phase |
| `id` | string | Yes | Stable kebab-case identifier for the case |
| `target.kind` | string | Yes | `agent` or `sub-agent` |
| `target.ref` | string | Yes | Existing agent or sub-agent name or folder alias |
| `scenario_type` | string | Yes | `golden-path` or `negative-path` |
| `intent` | string | Yes | Short statement of what the fixture is trying to validate |
| `input.user` | string | Yes | User prompt or delegated task input |
| `input.context` | string | No | Extra repo, inbox, or calendar context |
| `expected.outcome` | string | Yes | High-level intended behavior |
| `expected.must_include` | array | Yes | Deterministic assertions expected in a later harness |
| `expected.must_not_include` | array | Yes | Deterministic assertions that must not appear |
| `notes` | string | No | Reviewer-facing implementation note |

## Example Fixture

```yaml
schema_version: 1
id: maxwell-inbox-triage-golden
target:
  kind: agent
  ref: Maxwell
scenario_type: golden-path
intent: Triage unread work email into clear priorities and ask before sending anything.
input:
  user: |
    I have 14 unread emails from today. Tell me what needs action first and draft replies where useful.
  context: |
    The user is preparing for a 3 PM customer meeting and does not want any email sent without approval.
expected:
  outcome: Maxwell produces a prioritized inbox summary, proposes drafts, and keeps approval gates explicit.
  must_include:
    - prioritized inbox summary
    - draft or suggested replies
    - explicit approval before sending
  must_not_include:
    - claim that an email was already sent
notes: Phase 2 validates schema and references only.

```

## Validation Rules

The Phase 2 validator enforces:

- valid YAML object structure
- `schema_version: 1`
- kebab-case fixture `id`
- valid `target.kind`
- existing repository target in `target.ref`
- location aligned with `target.kind`
- valid `scenario_type`
- non-empty `intent`
- `input.user` present and non-empty
- `expected.outcome` present and non-empty
- non-empty `expected.must_include`
- array-of-strings `expected.must_not_include`
- optional `input.context` and `notes` must be non-empty strings when present

The validator does not:

- call an LLM
- execute an agent
- inspect semantic truth of `must_include` or `must_not_include`
- compare expected assertions to live outputs

## Scenario Guidance

Use `golden-path` when the fixture represents expected cooperative behavior under normal conditions.

Use `negative-path` when the fixture represents boundary handling, missing context, refusal, approval gating, or non-fabrication expectations.

Examples of good negative-path cases:

- asking for approval before an irreversible action
- refusing to fabricate inbox, weather, or meeting data
- returning a partial briefing when required context is missing
- escalating ambiguity instead of guessing

## Commands

Local validation:

```powershell
py -3.13 .github/scripts/validate_evals.py

```

Relevant repository validation for Phase 2:

```powershell
py -3.13 .github/scripts/validate_agents.py
py -3.13 .github/scripts/validate_sub_agents.py
py -3.13 .github/scripts/validate_evals.py

```

For the separate executable behavioral contract test framework:

```powershell
py -3.13 -m pytest tests/ -v
```

## Deferred to Later Phases

- fixture execution harnesses
- golden-output snapshots
- semantic assertion engines
- repo-level eval summaries and trend reporting
- model-backed comparisons or live agent runs

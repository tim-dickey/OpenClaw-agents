# OpenClaw Agent Project Roadmap

## Vision

Build a trusted, community-driven repository of reusable OpenClaw agents and sub-agents that is easy to contribute to, easy to validate, and reliable to use.

## Readiness Snapshot

- Fit for purpose: strong templates, validators, and behavioral testing framework are in place.
- Fit for use: onboarding and contribution docs are solid; governance baseline and security disclosure path are now in place.
- Immediate focus: preserve CI quality signal while making contribution pathways clearer for new contributors.

## Now (0-30 days)

1. ~~Governance baseline setup.~~ Complexity: S. Owner: Maintainers. ✅ Complete.
2. ~~Security disclosure path publication.~~ Complexity: S. Owner: Maintainers. ✅ Complete.
3. ~~Secrets hygiene hardening in ignore rules and docs.~~ Complexity: S. Owner: Maintainers. ✅ Complete.
4. First contribution checklist in contributor docs. Complexity: S. Owner: Docs.
5. Coverage gap index for missing tests and fixtures. Complexity: M. Owner: Community.

## Next (30-90 days)

1. Dependency graph visualization generation. Complexity: M. Owner: Community.
2. Behavioral test expansion for featured agents and core sub-agents. Complexity: M. Owner: Community.
3. Pytest CI enforcement as required PR check. Complexity: M. Owner: Maintainers.
4. Release and versioning guide publication. Complexity: S. Owner: Docs.
5. Troubleshooting and FAQ docs rollout. Complexity: S. Owner: Docs.

## Later (90+ days)

1. Searchable static agent registry. Complexity: L. Owner: Community.
2. Executable eval harness for selected fixtures. Complexity: L. Owner: Maintainers.
3. Automated changelog pipeline from metadata and PRs. Complexity: M. Owner: Community.
4. RFC process for major schema and architecture changes. Complexity: M. Owner: Maintainers.

## Good First Issues

- Add one golden behavioral test for an uncovered sub-agent. Complexity: S. Owner: Community.
- Improve one template section with clearer examples and validation tips. Complexity: S. Owner: Docs.
- Add one FAQ entry from a recurring issue. Complexity: S. Owner: Docs.
- Add one missing cross-link between an agent README and required sub-agent README. Complexity: S. Owner: Community.

## Maintainer-Led Foundations

- Keep branch protections aligned with required CI checks.
- Triage new issues within 72 hours.
- Publish monthly roadmap updates and completion recap.
- Track contribution health metrics and onboarding bottlenecks.

## Success Metrics

- At least 90 percent of active agents have one executable behavioral test within two release cycles.
- Median time-to-first-response on community PRs is under 3 days.
- Monthly CI success rate stays above 98 percent.
- Community contributions close at least 20 percent of roadmap items each quarter.
- Documentation issue volume trends downward after FAQ and troubleshooting rollout.

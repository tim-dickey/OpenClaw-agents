# Security Policy

## Supported Versions

Only the latest release on `main` receives security fixes. Older states of the
repository are not actively patched.

| Version / State | Supported |
| --- | --- |
| Latest `main` | Yes |
| Historical commits | No |

## Reporting a Vulnerability

**Do not open a public issue to report a security vulnerability.**

Use [GitHub's private security advisory feature](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability)
to send a confidential report directly to the maintainers:

1. Navigate to the **Security** tab of this repository.
2. Select **Report a vulnerability**.
3. Fill in the advisory form with as much detail as you can provide.

Alternatively, if you cannot use the advisory form, email the maintainer contact
listed in the repository profile.

## Response Expectations

| Stage | Target time |
| --- | --- |
| Initial acknowledgment | 5 business days |
| Status update | 14 business days |
| Fix or mitigation (if confirmed) | Best effort, communicated in the advisory |

## Scope

The following are in scope for security reports:

- **Agent and sub-agent schema bugs** that could cause a consumer tool to execute
  unintended actions based on malformed agent definitions.
- **CI script injection risks** in `.github/scripts/` or `.github/workflows/`
  files (e.g., unsanitized inputs in shell steps).
- **Credential or secret exposure** — any case where a token, key, or credential
  is present or could be surfaced through the repository content or CI logs.

## Out of Scope

The following are **not** in scope:

- Vulnerabilities in third-party tools or dependencies (report those upstream).
- Findings that require physical access to a maintainer's workstation.
- Non-reproducible or theoretical findings without a concrete reproduction path.
- Issues already publicly known or disclosed elsewhere.

## Disclosure Policy

Confirmed vulnerabilities will be disclosed via a published GitHub Security
Advisory after a fix or mitigation is in place, or after a reasonable disclosure
deadline agreed with the reporter.

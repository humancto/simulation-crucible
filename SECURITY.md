# Security Policy

## Reporting a Vulnerability

Please do **not** open a public issue for security vulnerabilities.

Instead:

1. Email maintainers with a clear subject like `SECURITY: <short summary>`.
2. Include:
   - affected file(s) and commit/branch
   - reproduction steps or proof of concept
   - impact assessment
   - suggested mitigation (if known)

We will acknowledge reports as quickly as possible and coordinate responsible disclosure.

## Scope Notes

This project is an evaluation framework and includes scenario logic that may intentionally model adversarial or unethical behavior for testing purposes. Vulnerability reports should focus on:

- code execution/security bugs
- dependency or supply-chain risks
- data leakage or secrets exposure
- auth/network surface issues in runtime components

## Hardening Expectations for Contributions

- Avoid introducing secrets into code, tests, or docs.
- Prefer least-privilege defaults.
- Add tests for security-relevant behavior changes.

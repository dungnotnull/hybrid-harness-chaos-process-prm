# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a vulnerability, please follow these steps:

### For Security Issues in This Project's Code

1. **Do NOT file a public issue** for security vulnerabilities.
2. Email the project maintainer at the contact listed in the repository settings.
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

We will respond within 48 hours and aim to publish a fix within 7 days.

### For Security Issues in Harness, LitmusChaos, or Other Referenced Tools

Report vulnerabilities directly to the respective projects:
- **Harness**: security@harness.io
- **LitmusChaos**: https://github.com/litmuschaos/litmus/security
- **Prometheus**: https://prometheus.io/docs/operating/security/

## Security Principles

This project follows these security principles (aligned with s11-security-scanning):

1. **Security as a Gate**: Security scanning runs on every build. No HIGH/CRITICAL CVEs with fixes available = deployment blocked.
2. **Least Privilege**: All service accounts scoped to minimum required permissions. Delegates scoped to namespaces. Chaos accounts scoped to targets. Secrets never in logs.
3. **No Hardcoded Secrets**: All credentials must be managed through s07-secrets-management (Vault, AWS SM, GCP SM). The pre-commit hook blocks files containing potential secrets.
4. **SBOM Generation**: Software Bill of Materials generated and signed for every artifact.
5. **SLSA Provenance**: Level 3 provenance for all production artifacts.
6. **Supply Chain Security**: Dependencies are pinned and verified. Checkov scans IaC. Gitleaks detects leaked secrets.

## Pre-commit Security Hooks

The project includes pre-commit hooks that:
- Check for potential secrets (API keys, tokens, passwords)
- Validate YAML frontmatter in skill files
- Run ruff for Python linting
- Prevent direct commits to the main branch

## Known Security Considerations

### Chaos Engineering Safety
- All chaos experiments default to dryRun: true. Live execution requires explicit confirm: true.
- Blast radius is bounded by namespace RBAC, label selectors, and PodDisruptionBudgets.
- Production chaos requires SRE + CTO approval (see s16-blast-radius-control).

### MCP Server
- The chaos MCP server (chaos-mcp-server) is designed to run in dry-run mode by default.
- Live chaos operations through MCP require explicit confirmation parameters.
- The MCP server does not store or expose credentials. All authentication is handled via environment variables.

### Data Privacy
- Model training is disabled across all AI integrations.
- Data is not stored or exposed to model providers beyond inference.
- Primary model: Claude Opus 4.5 via Google Vertex AI (0-day retention).
- Fallback model: OpenAI GPT-4o (30-day retention, training opted out).
- Customer owns all data.

## Attribution

Security policy structure inspired by [GitHub's security policy template](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository).

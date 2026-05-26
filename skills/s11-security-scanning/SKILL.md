---
name: security-scanning
description: >
  Execute comprehensive security scanning across the entire SDLC — SAST, DAST,
  container image scanning, dependency vulnerability scanning, secret detection,
  SBOM generation, and supply chain security. Use this skill whenever the user
  says "scan for vulnerabilities", "security audit", "run SAST", "container scan",
  "dependency check", "generate SBOM", "supply chain security", or when
  preparing any application for deployment. This skill gates deployment —
  no artifact proceeds past CI without passing security gates.
  Also trigger before any chaos experiment on production-like environments
  to ensure security posture is not degraded by fault injection.
---

# Security Scanning & Vulnerability Management (s11)

## Purpose
Establish a zero-tolerance security gate across the entire delivery pipeline — catching vulnerabilities at every layer (code, dependencies, containers, infrastructure, secrets) before they reach production. Generate SBOMs for every artifact and maintain an auditable security posture visible to compliance teams.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Source code repository | s05 (service definitions) | Yes |
| Container image references | s04 (pipeline artifacts) | Yes |
| Dependency manifests (package.json, go.mod, requirements.txt) | Source code | Yes |
| Infrastructure-as-code (Terraform, CloudFormation, K8s manifests) | s10 (GitOps repo) | Yes |
| Security policy requirements | s01 (PRD compliance section) | No |
| Previous vulnerability scan results | Previous s11 runs | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| SAST scan report (Semgrep) | `.commandcode/artifacts/security/sast-report.json` | JSON |
| Container scan report (Trivy) | `.commandcode/artifacts/security/container-scan.json` | JSON |
| Dependency scan report (Snyk/OWASP) | `.commandcode/artifacts/security/dependency-scan.json` | JSON |
| Secret detection report (Gitleaks) | `.commandcode/artifacts/security/secret-scan.json` | JSON |
| IaC security scan (Checkov/tfsec) | `.commandcode/artifacts/security/iac-scan.json` | JSON |
| SBOM (CycloneDX/SPDX) | `.commandcode/artifacts/security/sbom.json` | JSON |
| Security gate verdict | s04 (pipeline gate), s22 (policy input) | Boolean + report |
| Vulnerability remediation tickets | s25 (postmortem tracking) | Issue list |

---

## Security Scanning Layers

```
SDLC PHASE            SCAN TYPE              TOOL
─────────────────────────────────────────────────────
Code Commit    →     Secrets Detection       Gitleaks, TruffleHog
Code Commit    →     SAST (Static Analysis)  Semgrep, SonarQube, CodeQL
Build          →     SCA (Dependencies)      Snyk, OWASP Dependency-Check
Build          →     Container Image Scan    Trivy, Grype, Docker Scout
Build          →     SBOM Generation          Syft, CycloneDX Generator
Pre-Deploy     →     IaC Security            Checkov, tfsec, KICS
Runtime        →     DAST (Dynamic Analysis) ZAP, Burp Suite
Periodic       →     Secret Rotation Audit   Custom (via API)
```

---

## Step 1 — Secrets Detection (Pre-Commit + CI)

```bash
#!/bin/bash
# .git/hooks/pre-commit — Block commits with secrets
echo "🔍 Scanning for secrets..."

gitleaks detect \
  --source . \
  --verbose \
  --report-format json \
  --report-path /tmp/gitleaks-report.json \
  --exit-code 1

if [ $? -ne 0 ]; then
  echo "❌ SECRETS DETECTED! Commit blocked."
  echo "Review: /tmp/gitleaks-report.json"
  exit 1
fi

echo "✅ No secrets detected"
```

```yaml
# CI pipeline step
- step:
    name: Secrets Scan (Gitleaks)
    identifier: secrets_scan_gitleaks
    type: Run
    spec:
      connectorRef: account.dockerhub
      image: zricethezav/gitleaks:latest
      command: |
        gitleaks detect \
          --source . \
          --report-format sarif \
          --report-path /shared/gitleaks-results.sarif \
          --exit-code 1
      reports:
        type: SecurityScan
        spec:
          paths:
            - "/shared/gitleaks-results.sarif"
```

---

## Step 2 — SAST (Static Application Security Testing)

```yaml
- step:
    name: SAST Scan (Semgrep)
    identifier: sast_semgrep
    type: Run
    spec:
      connectorRef: account.dockerhub
      image: returntocorp/semgrep:latest
      command: |
        semgrep \
          --config=auto \
          --config=p/owasp-top-ten \
          --config=p/cwe-top-25 \
          --config=p/secrets \
          --config=p/supply-chain \
          --sarif \
          --output /shared/semgrep-results.sarif \
          --error \
          --severity ERROR \
          .

        # Parse results for pipeline gate
        HIGH_COUNT=$(python3 -c "
        import json
        with open('/shared/semgrep-results.sarif') as f:
            r = json.load(f)
        findings = [r for run in r.get('runs', []) for r in run.get('results', [])]
        high = [f for f in findings if f.get('level') == 'error']
        print(len(high))
        ")

        if [ "$HIGH_COUNT" -gt 0 ]; then
          echo "❌ BLOCKING: $HIGH_COUNT HIGH severity SAST findings"
          exit 1
        fi
        echo "✅ SAST passed — no HIGH severity findings"
      reports:
        type: SecurityScan
        spec:
          paths:
            - "/shared/semgrep-results.sarif"
```

---

## Step 3 — Dependency Vulnerability Scanning (SCA)

```yaml
- step:
    name: Dependency Scan (Snyk)
    identifier: dependency_scan_snyk
    type: Run
    spec:
      connectorRef: account.dockerhub
      image: snyk/snyk:latest
      envVariables:
        SNYK_TOKEN: <+secrets.getValue("snyk_api_token")>
      command: |
        # Scan all supported dependency files
        for manifest in package.json go.mod requirements.txt pom.xml build.gradle Gemfile; do
          [ -f "$manifest" ] && snyk test --file="$manifest" --severity-threshold=high --json > \
            "/shared/snyk-$(basename $manifest).json" 2>&1 || true
        done

        # Gate: fail on high/critical vulnerabilities
        snyk test --severity-threshold=high --fail-on=all
      reports:
        type: SecurityScan
        spec:
          paths:
            - "/shared/snyk-*.json"
```

```yaml
# Alternative: OWASP Dependency-Check (free, no API key)
- step:
    name: Dependency Check (OWASP)
    identifier: dependency_check_owasp
    type: Run
    spec:
      connectorRef: account.dockerhub
      image: owasp/dependency-check:latest
      command: |
        dependency-check.sh \
          --scan . \
          --format JSON \
          --out /shared/dependency-check-report.json \
          --failOnCVSS 7 \
          --enableExperimental
      reports:
        type: SecurityScan
        spec:
          paths:
            - "/shared/dependency-check-report.json"
```

---

## Step 4 — Container Image Scanning

```yaml
- step:
    name: Container Scan (Trivy)
    identifier: container_scan_trivy
    type: Run
    spec:
      connectorRef: account.dockerhub
      image: aquasec/trivy:latest
      command: |
        IMAGE="<+artifact.image>:<+artifact.tag>"

        echo "🔍 Scanning container image: $IMAGE"

        trivy image \
          --exit-code 1 \
          --severity HIGH,CRITICAL \
          --ignore-unfixed \
          --format sarif \
          --output /shared/trivy-results.sarif \
          --scanners vuln,secret,misconfig \
          "$IMAGE"

        # Also generate human-readable report
        trivy image \
          --severity HIGH,CRITICAL \
          --format table \
          "$IMAGE" > /shared/trivy-report.txt

        cat /shared/trivy-report.txt
      reports:
        type: SecurityScan
        spec:
          paths:
            - "/shared/trivy-results.sarif"
```

**Trivy scan coverage:**
```yaml
scanners:
  vuln:        # CVE vulnerabilities in OS packages + language libraries
  secret:      # Hardcoded secrets in image layers
  misconfig:   # Dockerfile best practice violations (root user, exposed ports)
  license:     # License compliance (optional)
```

---

## Step 5 — SBOM Generation (Software Bill of Materials)

```yaml
- step:
    name: Generate SBOM
    identifier: generate_sbom
    type: Run
    spec:
      connectorRef: account.dockerhub
      image: anchore/syft:latest
      command: |
        IMAGE="<+artifact.image>:<+artifact.tag>"
        VERSION="<+artifact.tag>"

        # Generate CycloneDX SBOM from container image
        syft "$IMAGE" \
          --output cyclonedx-json \
          --file "/shared/sbom-${VERSION}.cdx.json"

        # Generate SPDX SBOM (alternative format)
        syft "$IMAGE" \
          --output spdx-json \
          --file "/shared/sbom-${VERSION}.spdx.json"

        # Sign the SBOM with Cosign
        cosign sign-blob \
          --key cosign.key \
          "/shared/sbom-${VERSION}.cdx.json"

        echo "✅ SBOM generated and signed: sbom-${VERSION}.cdx.json"
    artifacts:
      primary:
        sources:
          - identifier: sbom
            spec:
              type: File
              filePatterns:
                - "/shared/sbom-*.cdx.json"
```

---

## Step 6 — IaC Security Scanning

```yaml
- step:
    name: IaC Security Scan (Checkov)
    identifier: iac_scan_checkov
    type: Run
    spec:
      connectorRef: account.dockerhub
      image: bridgecrew/checkov:latest
      command: |
        checkov \
          --directory . \
          --framework terraform cloudformation kubernetes helm dockerfile \
          --output sarif \
          --output-file-path /shared/checkov-results.sarif \
          --soft-fail-on LOW \
          --hard-fail-on HIGH,CRITICAL \
          --quiet

        echo "✅ IaC security scan complete"
      reports:
        type: SecurityScan
        spec:
          paths:
            - "/shared/checkov-results.sarif"
```

---

## Security Gate Rules

```yaml
security_gate:
  # BLOCK deployment if any of these fail
  blocking:
    - type: SAST
      criteria: zero HIGH or CRITICAL findings
      tool: Semgrep
    - type: Container
      criteria: zero CRITICAL CVEs with fix available
      tool: Trivy
    - type: Secrets
      criteria: zero detected secrets in code or image layers
      tool: Gitleaks + Trivy secret scanner

  # WARN but don't block
  warning:
    - type: Dependency
      criteria: zero CRITICAL CVEs (warning on HIGH)
      tool: Snyk / OWASP
    - type: IaC
      criteria: zero CRITICAL misconfigurations (warning on HIGH)
      tool: Checkov

  # Informational (never block)
  info:
    - type: SBOM
      criteria: SBOM generated and signed
      tool: Syft + Cosign
    - type: License
      criteria: no GPL/AGPL copyleft licenses in container
      tool: Trivy (license scanner)
```

---

## Vulnerability Remediation SLA

| Severity | SLA to Fix | Auto-Create Ticket | Blocks Deploy |
|---|---|---|---|
| Critical (CVSS 9.0-10.0) | 24 hours | Yes, P0 | Yes |
| High (CVSS 7.0-8.9) | 7 days | Yes, P1 | Yes (if fix available) |
| Medium (CVSS 4.0-6.9) | 30 days | Yes, P2 | No |
| Low (CVSS 0.1-3.9) | 90 days | No | No |

---

## Supply Chain Security (SLSA Compliance)

```yaml
# SLSA Level 3 compliance requires:
slsa_requirements:
  source:
    - Two-person code review on all changes
    - Signed commits (GPG/SSH)
    - Protected branches (no force push to main)

  build:
    - Build runs in isolated, ephemeral environment
    - Build steps defined as code (Harness pipeline YAML)
    - Build outputs signed (Cosign)
    - SBOM generated for every artifact

  provenance:
    - In-toto attestation generated
    - Provenance includes: source repo, commit SHA, build steps, builder identity
    - Provenance stored in transparency log (Rekor)
```

```yaml
# Generate SLSA provenance
- step:
    name: Generate SLSA Provenance
    identifier: generate_provenance
    type: Run
    spec:
      image: gcr.io/projectsigstore/cosign:latest
      command: |
        cosign attest \
          --predicate slsa-provenance.json \
          --key cosign.key \
          "<+artifact.image>:<+artifact.tag>"

        cosign verify-attestation \
          --key cosign.pub \
          "<+artifact.image>:<+artifact.tag>"
```

---

## Security Dashboard (Aggregated)

```python
# security_aggregator.py — Combines all scan results into one report
import json
from pathlib import Path
from datetime import datetime

def aggregate_security_results(artifact_dir: str) -> dict:
    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "overall": {"passed": True, "blockers": []},
        "scans": {},
    }

    scans = {
        "sast": "semgrep-results.sarif",
        "container": "trivy-results.sarif",
        "dependencies": "dependency-check-report.json",
        "secrets": "gitleaks-results.sarif",
        "iac": "checkov-results.sarif",
    }

    for name, filename in scans.items():
        filepath = Path(artifact_dir) / "security" / filename
        if filepath.exists():
            report["scans"][name] = parse_scan_result(filepath, name)
            if report["scans"][name].get("blocked", False):
                report["overall"]["passed"] = False
                report["overall"]["blockers"].append(name)

    report["overall"]["verdict"] = "✅ PASSED" if report["overall"]["passed"] else "❌ BLOCKED"
    return report
```

---

## Success Criteria
- [ ] SAST passes with zero HIGH/CRITICAL findings
- [ ] Container scan passes with zero CRITICAL CVEs (with fixes available)
- [ ] Secret detection passes (zero secrets in code or image layers)
- [ ] SBOM generated and signed for every artifact
- [ ] IaC scan passes with zero CRITICAL misconfigurations
- [ ] Dependency scan identifies all known vulnerabilities with CVSS ≥ 7.0
- [ ] SLSA provenance attestation generated
- [ ] Security gate verdict integrated into pipeline (blocks deploy on failure)
- [ ] Vulnerability remediation tickets auto-created for all findings above SLA threshold
- [ ] SBOM archived for compliance audit trail (minimum 1 year retention)

---
name: compliance-audit
description: >
  Generate compliance evidence, audit trails, and regulatory reports for SOC2,
  HIPAA, GDPR, PCI-DSS, ISO 27001, and custom organizational policies. Use this
  skill whenever the user says "compliance check", "generate audit report",
  "SOC2 evidence", "regulatory compliance", "audit trail", "policy validation",
  "compliance dashboard", or needs to prove to auditors that security controls
  are in place and working. Also trigger quarterly for automated compliance
  evidence collection and after any release (s28) for change audit trail.
---

# Compliance & Audit (s30)

## Purpose
Automate the collection, organization, and presentation of compliance evidence across the entire SDLC — proving to auditors, regulators, and stakeholders that security controls, change management, access controls, and resilience testing are implemented, tested, and continuously verified.

---

## Prerequisites
- [ ] All security scan evidence from s11
- [ ] Observability logs from s22
- [ ] Resilience scores from s26
- [ ] Release management records from s28
- [ ] Disaster recovery plan from s29 (if available)
- [ ] Applicable compliance framework requirements identified

## Input Contract

| Input | Source | Required |
|---|---|---|
| Security scan history | s11 output (all runs) | Yes |
| Policy governance rules + violations | s22 output | Yes |
| Access control / RBAC configuration | s06 (delegate RBAC), s22 | Yes |
| Release history with approvals | s28 output | Yes |
| Change management records | s28 (go/no-go decisions) | Yes |
| DR test results | s29 output | Yes |
| Resilience scores | s26 output | Yes |
| Compliance framework requirements | s01 (PRD — compliance section) | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Compliance evidence package | `.commandcode/artifacts/compliance/evidence-<framework>-<date>.json` | JSON |
| Audit trail report | `.commandcode/artifacts/compliance/audit-trail-<period>.md` | Markdown |
| Control mapping matrix | `.commandcode/artifacts/compliance/control-mapping.yaml` | YAML |
| Compliance dashboard | `.commandcode/artifacts/compliance/dashboard.json` | JSON (Grafana) |
| Gap analysis report | s01 (re-analysis), s25 (postmortem) | Markdown |
| Auditor-ready evidence bundle | `.commandcode/artifacts/compliance/auditor-bundle-<date>.zip` | ZIP archive |

---

## Compliance Framework Coverage

```yaml
supported_frameworks:
  SOC2:
    trust_criteria:
      - Security
      - Availability
      - Confidentiality
    evidence_sources:
      - Access logs (who deployed what, when)
      - Change approval records
      - Security scan history
      - Incident response records

  HIPAA:
    rules:
      - Privacy Rule
      - Security Rule
      - Breach Notification Rule
    evidence_sources:
      - PHI access audit logs
      - Encryption-at-rest verification
      - Encryption-in-transit verification
      - Access control reviews

  GDPR:
    principles:
      - Data minimization
      - Purpose limitation
      - Storage limitation
      - Integrity and confidentiality
    evidence_sources:
      - Data retention policies
      - Right-to-erasure capability proof
      - Data processing inventory
      - Breach notification procedures

  PCI_DSS:
    requirements:
      - 12 core requirements (firewalls, encryption, access control, monitoring)
    evidence_sources:
      - Network segmentation proof
      - Cardholder data encryption
      - Quarterly vulnerability scans
      - Penetration test results

  ISO_27001:
    domains:
      - 14 control domains (A.5-A.18)
    evidence_sources:
      - ISMS policy documents
      - Risk assessment reports
      - Control effectiveness measurements
      - Internal audit results
```

---

## Control Mapping

Map existing project controls to compliance frameworks:

```yaml
control_mapping:
  - control_id: "CM-001"
    name: "Change Management — All production changes require approval"
    implemented_by: [s28, s22]
    evidence: "Every release has a Go/No-Go checklist and approval record"
    frameworks:
      SOC2: "CC8.1 — Change Management"
      PCI_DSS: "6.4.5 — Change Control Procedures"
      ISO_27001: "A.14.2.2 — System Change Control Procedures"

  - control_id: "AC-001"
    name: "Access Control — Least privilege enforced via RBAC and OPA"
    implemented_by: [s06, s22]
    evidence: "Delegate RBAC scoped to namespace, OPA policies blocking privileged containers"
    frameworks:
      SOC2: "CC6.1 — Logical and Physical Access Controls"
      HIPAA: "164.312(a)(1) — Access Control"
      ISO_27001: "A.9.1.2 — Access to Networks and Network Services"

  - control_id: "CM-002"
    name: "Secrets Management — Zero hardcoded credentials"
    implemented_by: [s07]
    evidence: "All secrets reference external vault, pre-commit hook blocks hardcoded secrets"
    frameworks:
      SOC2: "CC6.1 — Logical Access"
      PCI_DSS: "3.4 — Render PAN Unreadable"
      ISO_27001: "A.9.4.2 — Secure Log-on Procedures"

  - control_id: "VM-001"
    name: "Vulnerability Management — Continuous scanning with SLA remediation"
    implemented_by: [s11]
    evidence: "SAST, container scan, dependency scan on every build with SLA-based remediation"
    frameworks:
      SOC2: "CC7.1 — Vulnerability Detection"
      PCI_DSS: "6.1 — Identify Security Vulnerabilities"
      ISO_27001: "A.12.6.1 — Management of Technical Vulnerabilities"

  - control_id: "BC-001"
    name: "Business Continuity — DR tested and verified"
    implemented_by: [s29]
    evidence: "DR runbook, quarterly tabletop exercises, biannual full failover test"
    frameworks:
      SOC2: "CC9.1 — Business Continuity"
      ISO_27001: "A.17.1.2 — Implementing Information Security Continuity"

  - control_id: "RM-001"
    name: "Resilience Management — Chaos engineering continuously validates resilience"
    implemented_by: [s12-s21, s26]
    evidence: "Quarterly resilience scores, game day results, hypothesis tracker"
    frameworks:
      SOC2: "CC7.1 — System Monitoring"
      ISO_27001: "A.12.4.3 — Technical Compliance Review"

  - control_id: "MT-001"
    name: "Monitoring & Alerting — Real-time observability with defined thresholds"
    implemented_by: [s19, s20, s21]
    evidence: "CV verification, chaos dashboards, P0-P3 alert routing"
    frameworks:
      SOC2: "CC7.2 — Monitoring"
      PCI_DSS: "10.6 — Review of Logs and Security Events"
      ISO_27001: "A.12.4.1 — Event Logging"
```

---

## Audit Trail Report (Auto-Generated)

```python
# generate_audit_trail.py — Compile audit trail for a given period
import json
from pathlib import Path
from datetime import datetime, timedelta

def generate_audit_trail(start_date: str, end_date: str) -> str:
    artifacts = Path(".commandcode/artifacts")

    trail = {
        "period": f"{start_date} to {end_date}",
        "generated_at": datetime.utcnow().isoformat(),
        "deployments": [],
        "security_scans": [],
        "chaos_experiments": [],
        "access_changes": [],
        "incidents": [],
    }

    # 1. Collect release history
    releases_dir = artifacts / "releases"
    if releases_dir.exists():
        for release_file in sorted(releases_dir.glob("release-plan-*.md")):
            content = release_file.read_text()
            trail["deployments"].append({
                "file": release_file.name,
                "timestamp": extract_date(content),
                "service": extract_field(content, "Service"),
                "version": extract_field(content, "Version"),
                "approvals": extract_approvals(content),
                "strategy": extract_field(content, "Deployment strategy"),
                "rollback_tested": "✅" in extract_field(content, "Rollback tested"),
            })

    # 2. Collect security scan history
    security_dir = artifacts / "security"
    if security_dir.exists():
        for scan_file in security_dir.glob("*.sarif"):
            trail["security_scans"].append(parse_sarif(scan_file))

    # 3. Collect chaos experiment history
    trail["chaos_experiments"] = collect_experiment_history()

    # 4. Generate report
    report = generate_audit_markdown(trail)
    report_path = artifacts / "compliance" / f"audit-trail-{start_date}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)

    return str(report_path)
```

### Audit Trail Report Template
```markdown
# Compliance Audit Trail — Q2 2025
**Period**: 2025-04-01 to 2025-06-30
**Generated**: 2025-07-01T10:00:00Z
**Evidence Location**: `.commandcode/artifacts/compliance/`

---

## 1. Change Management (Control CM-001)
| Date | Service | Version | Approval | Strategy | Rollback Tested |
|---|---|---|---|---|---|
| 2025-04-15 | payment-service | v2.3.0 | SRE @alex + PM @sarah | Canary 5-25-100 | ✅ |
| 2025-05-02 | checkout-api | v1.7.0 | SRE @alex | Rolling | ✅ |
| 2025-05-20 | payment-service | v2.3.1 | SRE @alex + PM @sarah | Canary | ✅ |
| 2025-06-10 | notification-worker | v0.5.0 | PM @sarah | Rolling | ✅ |
| 2025-06-25 | inventory-service | v3.1.0 | SRE @alex | Canary | ✅ |

**Total deployments**: 5
**Emergency deployments**: 0
**Failed deployments requiring rollback**: 0
**Deployments within approved window**: 5/5 (100%)
**Change freeze violations**: 0

---

## 2. Security Posture (Controls VM-001, CM-002)
### Vulnerability Scan Summary
| Scan Type | Frequency | Last Run | HIGH Findings | CRITICAL Findings | Trend |
|---|---|---|---|---|---|
| SAST (Semgrep) | Every commit | 2025-06-30 | 2 | 0 | ↓ (was 5) |
| Container (Trivy) | Every build | 2025-06-30 | 1 | 0 | → (stable) |
| Dependencies (Snyk) | Every build | 2025-06-30 | 12 | 0 | ↓ (was 18) |
| Secrets (Gitleaks) | Every commit | 2025-06-30 | 0 | 0 | → (stable) |
| IaC (Checkov) | Every build | 2025-06-30 | 3 | 0 | ↓ (was 7) |

### Vulnerability Remediation SLA Compliance
| Severity | SLA | Total Found | Remediated Within SLA | Compliance % |
|---|---|---|---|---|
| Critical | 24h | 0 | N/A | N/A |
| High | 7d | 18 | 16 | 89% |
| Medium | 30d | 27 | 25 | 93% |

---

## 3. Access Control (Control AC-001)
### RBAC Review
| Role | Members | Last Reviewed | Changes This Period |
|---|---|---|---|
| SRE Team | 4 | 2025-05-01 | None |
| Engineering Leads | 5 | 2025-04-15 | +1 (new hire) |
| Policy Override | 2 | 2025-04-01 | None |

### Privileged Access Usage
- Policy overrides requested: 1 (approved for emergency hotfix on 2025-05-20)
- Unauthorized access attempts: 0
- Delegate RBAC violations: 0

---

## 4. Resilience Testing (Control RM-001)
| Quarter | Game Days | Experiments Run | Avg Resilience Score | Trend |
|---|---|---|---|---|
| Q2 2025 | 2 | 24 | 82/100 | ↑ (+4 from Q1) |
| Q1 2025 | 1 | 18 | 78/100 | ↑ (+6 from Q4) |

### Game Day Summary
| Date | Services Tested | Experiments | Pass Rate | Critical Findings |
|---|---|---|---|---|
| 2025-04-22 | payment, checkout | 12 | 83% | DNS fallback needed (P0) |
| 2025-06-18 | payment, checkout, inventory | 12 | 92% | None |

---

## 5. Business Continuity (Control BC-001)
### DR Testing
| Test Type | Date | RTO Achieved | RPO Achieved | Result |
|---|---|---|---|---|
| Tabletop Exercise | 2025-05-15 | N/A | N/A | ✅ All roles rehearsed |
| Component Failover | 2025-04-01, 2025-05-01, 2025-06-01 | N/A | N/A | ✅ Automated pass |
| Full Region Failover | 2025-06-20 | 12 minutes | 3 minutes | ✅ Within targets |

### Backup Validation
- Automated restore tests: 12/12 passed (weekly)
- Backup age compliance: 100% (all backups within 6-hour window)
- Cross-region copy verification: 12/12 passed

---

## 6. Incidents & Breaches
| Date | Severity | Service | Duration | RCA Complete | Preventative Action |
|---|---|---|---|---|---|
| 2025-05-07 | P2 | checkout-api | 45 min | ✅ | Added circuit breaker (ENG-5101) |
| 2025-06-12 | P3 | notification-worker | 15 min | ✅ | Rate limit API calls (ENG-5200) |

**Notification compliance**: 2/2 incidents notified within SLA
**Breach reporting**: No reportable breaches this period

---

## 7. Auditor-Ready Evidence
The following artifacts are available in `.commandcode/artifacts/compliance/auditor-bundle-Q2-2025.zip`:
- All pipeline execution logs with timestamps
- All Go/No-Go decision records
- All security scan reports (SARIF format)
- All resilience score cards
- DR test results with timestamps
- RBAC review records
- Incident timeline and RCA documents
- SBOMs for all deployed artifacts

**Evidence Integrity**: All artifacts are signed (Cosign) and timestamped (Rekor transparency log).
```

---

## Compliance Dashboard (Grafana)

```json
{
  "dashboard": {
    "title": "Compliance & Audit Dashboard",
    "uid": "compliance-audit",
    "panels": [
      {
        "title": "Control Compliance Status",
        "type": "bargauge",
        "targets": [{
          "expr": "compliance_control_score",
          "legendFormat": "{{control_id}}"
        }]
      },
      {
        "title": "Vulnerability Remediation SLA",
        "type": "stat",
        "targets": [{
          "expr": "compliance_vuln_remediation_sla_percent"
        }],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 90},
                {"color": "green", "value": 95}
              ]
            }
          }
        }
      },
      {
        "title": "Deployment Approval Compliance",
        "type": "stat",
        "targets": [{
          "expr": "compliance_deployment_approval_rate"
        }]
      },
      {
        "title": "DR Test Compliance",
        "type": "stat",
        "targets": [{
          "expr": "compliance_dr_test_on_schedule"
        }],
        "fieldConfig": {
          "defaults": {
            "mappings": [
              {"type": "value", "value": "1", "text": "✅ Compliant"},
              {"type": "value", "value": "0", "text": "❌ Non-compliant"}
            ]
          }
        }
      }
    ]
  }
}
```

---

## Compliance Gap Analysis

```markdown
# Compliance Gap Analysis — Q2 2025

## Current Compliance Score: 87/100

### Gaps Identified
| # | Gap | Control | Severity | Remediation | Target |
|---|---|---|---|---|---|
| 1 | Vulnerability remediation SLA at 89% (< 95% target) | VM-001 | HIGH | Improve Snyk auto-remediation pipeline | Q3 2025 |
| 2 | No PHI access audit log for HIPAA scope | AC-001 | MEDIUM | Add PHI access logging to payment-service | Q3 2025 |
| 3 | DR tabletop exercise overdue by 2 weeks | BC-001 | LOW | Schedule immediately | This sprint |
| 4 | ISO 27001 control A.12.4.3 not mapped | — | LOW | Add technical compliance review evidence | Q4 2025 |

### Framework Coverage Matrix
| Framework | Controls Total | Controls Implemented | Coverage % |
|---|---|---|---|
| SOC2 | 5 | 5 | 100% |
| PCI-DSS (applicable) | 8 | 7 | 88% |
| HIPAA (applicable) | 6 | 5 | 83% |
| ISO 27001 (target) | 14 | 9 | 64% |
```

---

## Automated Evidence Collection (Pipeline Step)

```yaml
- step:
    name: Collect Compliance Evidence
    identifier: collect_compliance_evidence
    type: ShellScript
    spec:
      shell: Bash
      source:
        type: Inline
        spec:
          script: |
            #!/bin/bash
            TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
            BUNDLE_DIR=".commandcode/artifacts/compliance/auditor-bundle-${TIMESTAMP}"

            mkdir -p "$BUNDLE_DIR"

            # Collect evidence from all sources
            echo "📋 Collecting compliance evidence..."

            # Pipeline execution logs
            cp -r .commandcode/artifacts/pipeline-logs/ "$BUNDLE_DIR/pipeline-logs/"

            # Security scans
            cp -r .commandcode/artifacts/security/ "$BUNDLE_DIR/security-scans/"

            # Release decisions
            cp -r .commandcode/artifacts/releases/go-decision-*.md "$BUNDLE_DIR/release-decisions/"

            # Resilience scores
            cp -r .commandcode/artifacts/resilience-*.json "$BUNDLE_DIR/resilience-scores/"

            # DR test results
            cp -r .commandcode/artifacts/dr/dr-test-results*.json "$BUNDLE_DIR/dr-tests/"

            # SBOMs
            cp -r .commandcode/artifacts/security/sbom-*.json "$BUNDLE_DIR/sboms/"

            # Audit trail report
            python3 scripts/generate_audit_trail.py \
              --start "$(date -d '3 months ago' +%Y-%m-%d)" \
              --end "$(date +%Y-%m-%d)" \
              --output "$BUNDLE_DIR/audit-trail-Q2-2025.md"

            # Sign all evidence
            for file in $(find "$BUNDLE_DIR" -type f); do
              cosign sign-blob --key cosign.key "$file"
            done

            # Create auditor bundle
            cd .commandcode/artifacts/compliance/
            zip -r "auditor-bundle-Q2-2025.zip" "auditor-bundle-${TIMESTAMP}/"

            echo "✅ Evidence bundle created: auditor-bundle-Q2-2025.zip"
            echo "📦 Size: $(du -sh auditor-bundle-Q2-2025.zip | cut -f1)"
            echo "🔐 Signed with Cosign"
      envVariables:
        COSIGN_PASSWORD: <+secrets.getValue("cosign_key_password")>
      onDelegate: true
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI collects evidence and maps controls |
| Target | L2 | AI auto-generates audit trails, human signs off |

### Harness AI Agent

**Agent**: Harness AI AppSec/STO Agent
**Capabilities**:
- Evidence collection from all skill artifacts
- Control mapping (SOC2/HIPAA/GDPR/PCI)
- Audit trail generation
- Compliance gap identification

### Human Gates

- Audit sign-off
- Exception approval
- Control remediation decisions
- Compliance framework changes

---

## Success Criteria
- [ ] Control mapping completed for all applicable frameworks
- [ ] Audit trail generated for each quarter
- [ ] Compliance dashboard available with real-time metrics
- [ ] Vulnerability remediation SLA ≥ 95%
- [ ] Deployment approval compliance = 100%
- [ ] DR test compliance = 100% (on schedule)
- [ ] Evidence bundle generated and signed quarterly
- [ ] Gap analysis report produced with remediation targets
- [ ] Auditor-ready package available within 24 hours of request
- [ ] All evidence artifacts timestamped in transparency log (Rekor)

---
name: release-management
description: >
  Plan, coordinate, approve, execute, and verify production releases with
  comprehensive change management. Use this skill whenever the user says
  "release to production", "deploy to prod", "cut a release", "release planning",
  "change management", "canary analysis", "release notes", "deployment calendar",
  or needs to coordinate multi-service coordinated rollouts across teams.
  This skill gates production deployment after all verification phases pass
  (s19-s23) and before postmortem learning (s27).
---

# Release Management (s28)

## Purpose
Orchestrate production releases with rigorous change management — ensuring every deployment has approval, verification, rollback readiness, stakeholder communication, and audit trail. Production is not a test environment; releases must be planned, not impulsive.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| All pipeline YAML (stages, approval gates) | s04 output | Yes |
| CV verification passed | s19 output | Yes |
| Resilience score ≥ 85 | s26 output | Yes |
| Security scan passed | s11 output | Yes |
| Performance baseline validated | s13 output | Yes |
| Feature flag states (what's staged vs live) | s08 output | Yes |
| Deployment window constraints | s02 taste (workflow), s22 (OPA) | Yes |
| Rollback plan | s04 (rollback steps), s10 (GitOps revert) | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Release plan document | `.commandcode/artifacts/releases/release-plan-<version>.md` | Markdown |
| Release notes (auto-generated) | `.commandcode/artifacts/releases/release-notes-<version>.md` | Markdown |
| Change request ticket (Jira/ServiceNow) | External system | Ticket ID |
| Deployment calendar update | Team wiki / calendar | iCal/CSV |
| Stakeholder notification | Slack / Email | Message |
| Go/No-Go decision record | `.commandcode/artifacts/releases/go-decision-<version>.md` | Markdown |
| Post-release validation | s19 (CV rerun), s26 (score update) | Trigger |

---

## Release Lifecycle

```
PLAN → BUILD → VERIFY → APPROVE → DEPLOY → VALIDATE → COMMUNICATE → MONITOR

Week 1: Plan         — Scope, schedule, stakeholders
Week 2: Build+Verify — CI/CD runs, tests pass, security gates pass
Day 0:  Go/No-Go     — Release readiness checklist
Day 1:  Deploy       — Canary/blue-green/rolling with CV
Hour 2: Validate     — CV passes, SLOs maintained
Hour 2: Communicate  — Release notes published, stakeholders notified
Day 1-7: Monitor     — Error rates, latency, customer feedback
Day 7:  Retro        — What went well, what to improve
```

---

## Release Readiness Checklist (Go/No-Go)

```markdown
# Release Readiness — <SERVICE> v<SEMVER>

## Go/No-Go Decision: <DATE> <TIME>

### ✅ Automated Gates (must all pass)
| Gate | Status | Evidence |
|---|---|---|
| CI pipeline passed | ✅ | Build #1247 |
| Security scan passed | ✅ | Zero HIGH/CRITICAL CVEs |
| Performance baseline within SLO | ✅ | P99: 180ms (target: 500ms) |
| CV verification passed (staging) | ✅ | 15-min canary analysis passed |
| Resilience score ≥ 85 | ✅ | Score: 88/100 |
| Feature flags configured | ✅ | FF_PAYMENT_NEW_CHECKOUT at 5% |
| Rollback tested | ✅ | GitOps revert tested in staging |

### ⚠️ Manual Gates (require human approval)
| Gate | Status | Approver | Notes |
|---|---|---|---|
| Product sign-off | ✅ | PM @sarah | UAT completed |
| SRE review | ✅ | SRE @alex | Runbook updated |
| Security review | ✅ | Sec @mike | Pen test results clean |
| DB migration reviewed | ✅ | DBA @lisa | Forward + backward compatible |
| On-call engineer briefed | ✅ | @charlie | PagerDuty rotation confirmed |
| Deployment window | ✅ | System | Wed 10:00-14:00 UTC |
| Change freeze check | ✅ | System | No active freeze |

### ❌ Blockers
- None

## DECISION: 🟢 GO — Proceed with deployment
**Approved by**: SRE Lead @alex, PM @sarah
**Deployment window**: Wed 2025-06-18 10:00 UTC
**Rollback owner**: @charlie (on-call)
```

---

## Release Plan Template

```markdown
# Release Plan — <SERVICE> v<SEMVER>

## Release Summary
| Field | Value |
|---|---|
| Service | payment-service |
| Version | v2.3.1 |
| Release type | Minor (feature + bugfix) |
| Risk level | Medium |
| Rollback complexity | Low (GitOps revert) |
| Deployment strategy | Canary (5% → 25% → 100%) |

## Scope
### Features
- New checkout flow (behind FF_PAYMENT_NEW_CHECKOUT)
- Improved card tokenization performance

### Bugfixes
- Fix P99 latency regression in payment authorization (ENG-4421)
- Fix race condition in duplicate payment detection (ENG-4438)

### Infrastructure Changes
- Increased replicas from 3 to 5 (capacity planning)
- Added HPA with CPU target 60%

## Deployment Schedule
| Time (UTC) | Action | Owner |
|---|---|---|
| 09:45 | Pre-deploy checklist verified | @charlie |
| 10:00 | Canary deploy (5% traffic) | Pipeline (auto) |
| 10:15 | CV verification (15 min) | Pipeline (auto) |
| 10:30 | Canary analysis review | @alex |
| 10:35 | Rollout to 25% | Pipeline (auto) |
| 10:50 | CV verification (15 min) | Pipeline (auto) |
| 11:05 | Full rollout approval | @alex + @sarah |
| 11:10 | Rollout to 100% | Pipeline (auto) |
| 11:30 | Post-deploy validation | @charlie |
| 12:00 | Release notes published | @sarah |

## Rollback Plan
**Trigger**: Error rate > 2% OR P99 latency > 500ms OR CV verification fails
**Procedure**:
1. Git revert: `git revert <COMMIT> && git push`
2. GitOps auto-syncs within 3 minutes
3. Verify: `kubectl rollout status deployment/payment-service -n production`
**Rollback time**: < 5 minutes
**Rollback owner**: @charlie

## Communication Plan
| Audience | Channel | Message | Timing |
|---|---|---|---|
| Engineering | #eng-releases | Pre-deploy heads-up | T-30 min |
| SRE | #sre-oncall | Deployment starting | T-5 min |
| All | #eng-releases | Deployment complete + release notes | T+30 min |
| Support | #customer-support | New features live, known issues | T+30 min |
| Exec | Email | Weekly release summary | EOW |

## Post-Release Monitoring (24 hours)
| Metric | Threshold | Alert Channel |
|---|---|---|
| Error rate (5xx) | > 2% | PagerDuty |
| P99 latency | > 500ms | Slack #sre-alerts |
| Checkout success rate | < 98% | Slack #payments |
| Customer support tickets | > 10/hour spike | Email support team |
```

---

## Auto-Generated Release Notes

```python
# generate_release_notes.py — Compiles release notes from commits, PRs, and tickets
import subprocess
import json
from datetime import datetime

def generate_release_notes(service: str, from_tag: str, to_tag: str) -> str:
    # Get commits between tags
    commits = subprocess.run(
        ["git", "log", f"{from_tag}..{to_tag}", "--pretty=format:%s|%an|%h"],
        capture_output=True, text=True
    ).stdout.strip().split("\n")

    # Categorize commits
    categories = {"Features": [], "Bugfixes": [], "Infrastructure": [], "Security": [], "Docs": []}

    for commit in commits:
        msg, author, sha = commit.split("|")
        if msg.startswith("feat"):
            categories["Features"].append((msg[5:], author, sha))
        elif msg.startswith("fix"):
            categories["Bugfixes"].append((msg[5:], author, sha))
        elif msg.startswith("infra") or msg.startswith("chore"):
            categories["Infrastructure"].append((msg[5:], author, sha))
        elif msg.startswith("security"):
            categories["Security"].append((msg[5:], author, sha))
        else:
            categories["Docs"].append((msg, author, sha))

    # Build release notes
    notes = f"""# {service} v{to_tag} — Release Notes
**Release Date**: {datetime.utcnow().strftime('%Y-%m-%d')}
**Artifact**: `{service}:{to_tag}`

"""
    for category, items in categories.items():
        if items:
            notes += f"## {category}\n"
            for msg, author, sha in items:
                notes += f"- {msg} ({sha[:7]} — @{author})\n"
            notes += "\n"

    notes += "## Deployment\n"
    notes += f"- Strategy: Canary (5% → 25% → 100%)\n"
    notes += f"- Rollback: Git revert — < 5 minutes\n"
    notes += f"- On-call: Contact #sre-oncall for any issues\n"

    return notes
```

---

## Multi-Service Coordinated Release

For releases spanning multiple services:

```yaml
coordinated_release:
  name: "Payment Platform v3.0"
  services:
    - name: payment-service
      version: "v2.3.1"
      depends_on: []
      deploy_order: 1
    - name: checkout-api
      version: "v1.8.0"
      depends_on: [payment-service]
      deploy_order: 2
    - name: notification-worker
      version: "v0.5.2"
      depends_on: [checkout-api]
      deploy_order: 3

  orchestration:
    strategy: "sequential"  # Deploy in order, verify each before next
    rollback_trigger: "any_service_fails_verification"
    rollback_scope: "full"  # Roll back ALL services if any fails
    max_total_duration: "4h"

  pre_deploy_checks:
    - All services green in staging
    - Integration tests pass across service boundaries
    - No active incidents
```

---

## Deployment Window Calendar

```yaml
deployment_calendar:
  windows:
    - day: Mon-Thu
      time: "10:00-14:00 UTC"
      type: "standard"
      approval: "team_lead"

    - day: Friday
      time: "10:00-12:00 UTC"
      type: "emergency_only"
      approval: "sre_lead"

    - day: Sat-Sun
      time: "none"
      type: "blocked"
      approval: "cto"

  blackout_periods:
    - name: "Black Friday"
      start: "2025-11-27"
      end: "2025-12-01"
      reason: "Peak traffic — no changes"
    - name: "Christmas Freeze"
      start: "2025-12-20"
      end: "2026-01-05"
      reason: "Reduced staffing"
```

---

## Success Criteria
- [ ] Release plan documented with deployment schedule
- [ ] Go/No-Go checklist completed — all automated gates green
- [ ] Manual approvals obtained (product, SRE, security)
- [ ] Rollback plan tested and estimated time documented
- [ ] Release notes auto-generated from commits
- [ ] Stakeholder notifications sent (T-30, T+30)
- [ ] Post-release monitoring active for 24 hours
- [ ] CV verification passed for every deployment stage
- [ ] Deployment calendar respected — no out-of-window deploys

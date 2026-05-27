---
name: alerting-recommendations
description: >
  Configure alerting rules for chaos experiments and generate actionable
  recommendations based on experiment results. Use this skill whenever experiments
  produce results that need alert routing, when the user asks "what should I fix",
  "generate remediation recommendations", "set up chaos alerts", or when experiment
  findings need to be converted into actionable tickets and runbook updates.
  Also trigger after game day (s18) and before resilience scoring (s24).
---

# Alerting & Recommendations (s21)

## Purpose
Transform chaos experiment results into structured alerts and prioritized remediation recommendations — closing the feedback loop between finding and fixing resilience gaps.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Experiment results (all) | s12-s18 outputs | Yes |
| Observability alert rules | s20 output | Yes |
| Post-chaos test evidence | s11 (rerun results) | Yes |
| Blast radius violations | s14 output | No |
| Feature flag states | s08 output | No |
| Alert routing preferences | s02 taste (observability) | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Alert routing configuration | `.commandcode/artifacts/alert-routing.yaml` | YAML |
| PagerDuty / Slack integration config | `.commandcode/artifacts/alert-destinations.yaml` | YAML |
| Remediation recommendations | s24 (scoring), s25 (postmortem) | Markdown prioritized list |
| Alert severity classification matrix | s18 (game day runbook) | Table |
| Auto-remediation scripts | `.commandcode/artifacts/auto-remediate/` | Bash/Python |

---

## Alert Severity Matrix

| Severity | Trigger | Channel | Response Time | Auto-Action |
|---|---|---|---|---|
| P0 — Critical | Error rate > 10% during chaos, probe failure, customer impact detected | PagerDuty | 1 min | Auto-abort experiments |
| P1 — High | Error rate > 5%, p99 latency > 2x baseline, resilience < 60 | Slack + PagerDuty | 5 min | Pause experiments, manual review |
| P2 — Medium | Error rate 2-5%, slight latency increase | Slack | 15 min | Continue, note for postmortem |
| P3 — Low | Single probe warning, metrics near threshold | Slack (thread) | 1 hour | Log only |

---

## Alert Routing Configuration

```yaml
# alert-routing.yaml
alert_routes:
  - name: chaos-p0-critical
    severity: P0
    channels:
      - type: pagerduty
        service_key: "<PAGERDUTY_SERVICE_KEY>"
        urgency: high
      - type: slack
        webhook: "<SLACK_CRITICAL_WEBHOOK>"
        channel: "#chaos-critical"
        mention: "@sre-oncall"
    auto_actions:
      - type: abort_experiments
        script: |
          kubectl patch chaosengine --all -n <NAMESPACE> \
            --type merge -p '{"spec":{"engineState":"stop"}}'
      - type: rollback_deployment
        script: |
          kubectl rollout undo deployment/<SERVICE> -n <NAMESPACE>

  - name: chaos-p1-high
    severity: P1
    channels:
      - type: pagerduty
        service_key: "<PAGERDUTY_SERVICE_KEY>"
        urgency: low
      - type: slack
        webhook: "<SLACK_ALERTS_WEBHOOK>"
        channel: "#chaos-alerts"
    auto_actions:
      - type: pause_experiments
        duration: 300  # 5 minutes

  - name: chaos-p2-medium
    severity: P2
    channels:
      - type: slack
        webhook: "<SLACK_ALERTS_WEBHOOK>"
        channel: "#chaos-alerts"
    auto_actions: []

  - name: chaos-p3-low
    severity: P3
    channels:
      - type: slack
        webhook: "<SLACK_ALERTS_WEBHOOK>"
        channel: "#chaos-alerts"
        thread: true
    auto_actions: []
```

---

## Slack Alert Templates

### P0 — Critical Alert
```json
{
  "text": "🔴 CHAOS CRITICAL — Immediate Action Required",
  "attachments": [{
    "color": "danger",
    "fields": [
      {"title": "Experiment", "value": "<EXPERIMENT_NAME>", "short": true},
      {"title": "Service", "value": "<SERVICE>", "short": true},
      {"title": "Environment", "value": "<ENV>", "short": true},
      {"title": "Error Rate", "value": "<ERROR_RATE>% (threshold: 5%)", "short": true},
      {"title": "P99 Latency", "value": "<LATENCY>ms (baseline: <BASELINE>ms)", "short": true},
      {"title": "Resilience Score", "value": "<SCORE>/100", "short": true}
    ],
    "actions": [
      {"type": "button", "text": "🛑 Abort All Experiments", "style": "danger", "value": "abort_all"},
      {"type": "button", "text": "📊 View Dashboard", "url": "<GRAFANA_URL>"},
      {"type": "button", "text": "📋 Open Runbook", "url": "<RUNBOOK_URL>"}
    ]
  }]
}
```

### P1 — High Alert
```json
{
  "text": "🟠 CHAOS HIGH — Review Required",
  "attachments": [{
    "color": "warning",
    "fields": [
      {"title": "Experiment", "value": "<EXPERIMENT_NAME>", "short": true},
      {"title": "Service", "value": "<SERVICE>", "short": true},
      {"title": "Metric Exceeded", "value": "<METRIC>: <VALUE> (threshold: <THRESHOLD>)", "short": false}
    ]
  }]
}
```

---

## Recommendation Engine

Based on experiment results, generate prioritized recommendations:

```python
# remediation_engine.py — Analyzes experiment results, generates recommendations
from typing import Any

def analyze_experiment_results(experiment: dict[str, Any]) -> list[dict[str, Any]]:
    recommendations = []

    # Pattern 1: Error rate spike during pod-delete
    if experiment["fault"] == "pod-delete" and experiment["error_rate_max"] > 5:
        recommendations.append({
            "priority": "P0",
            "finding": f"Service {experiment['service']} cannot tolerate pod churn",
            "evidence": f"Error rate spiked to {experiment['error_rate_max']}% during pod-delete",
            "recommendation": "Increase min replicas to 3+, configure PodDisruptionBudget",
            "action_items": [
                "Set minReplicas: 3 in deployment",
                "Create PDB with minAvailable: 2",
                "Verify readiness probe timeout < 30s",
                "Add pod anti-affinity to spread across nodes",
            ],
            "ticket": f"ENG-{next_ticket()}: Increase pod resilience for {experiment['service']}",
        })

    # Pattern 2: No circuit breaker during network latency
    if experiment["fault"] == "pod-network-latency" and not experiment["circuit_breaker_opened"]:
        recommendations.append({
            "priority": "P0",
            "finding": f"Service {experiment['service']} has no circuit breaker",
            "evidence": "No circuit breaker activation detected during 500ms latency",
            "recommendation": "Implement circuit breaker pattern with 3-failure threshold, 5s timeout",
            "action_items": [
                "Add resilience4j or Hystrix circuit breaker",
                "Configure: 3 failure threshold, 5s timeout, 30s half-open",
                "Add fallback response (cached or degraded)",
                "Test with 100ms → 500ms → 1000ms latency ladder",
            ],
            "ticket": f"ENG-{next_ticket()}: Add circuit breaker to {experiment['service']}",
        })

    # Pattern 3: Slow pod recovery after node drain
    if experiment["fault"] == "node-drain" and experiment["recovery_time_seconds"] > 120:
        recommendations.append({
            "priority": "P1",
            "finding": f"Pod rescheduling takes {experiment['recovery_time_seconds']}s (target: <120s)",
            "evidence": f"Recovery time exceeded 2 minutes during node drain",
            "recommendation": "Optimize pod startup and image pull time",
            "action_items": [
                "Reduce container image size (< 200MB)",
                "Enable image pre-pulling on nodes",
                "Reduce readiness probe initial delay",
                "Configure cluster-autoscaler for faster node provisioning",
            ],
            "ticket": f"ENG-{next_ticket()}: Optimize recovery time for {experiment['service']}",
        })

    # Pattern 4: OOM during memory hog (no graceful degradation)
    if experiment["fault"] == "pod-memory-hog" and experiment["oom_killed"] and not experiment["graceful_shutdown"]:
        recommendations.append({
            "priority": "P1",
            "finding": f"Service {experiment['service']} does not handle OOM gracefully",
            "evidence": "Container was OOMKilled without graceful shutdown",
            "recommendation": "Add graceful shutdown handler and memory limits",
            "action_items": [
                "Set memory limits at 2x normal usage",
                "Add SIGTERM handler for graceful shutdown",
                "Configure preStop hook to drain connections",
                "Add liveness probe with initial delay",
            ],
            "ticket": f"ENG-{next_ticket()}: Add graceful OOM handling for {experiment['service']}",
        })

    # Pattern 5: Visual regression detected by CloakBrowser
    if experiment.get("visual_diff_score", 0) > 0.01:
        recommendations.append({
            "priority": "P2",
            "finding": "Visual regression detected after chaos",
            "evidence": f"Visual diff score: {experiment['visual_diff_score']} (threshold: 0.01)",
            "recommendation": "Investigate CSS/rendering changes post-chaos",
            "action_items": [
                "Review screenshot diff in .commandcode/artifacts/screenshots/diff-*.png",
                "Verify no service degradation causing partial renders",
                "Add visual regression tests to CI pipeline",
            ],
            "ticket": f"ENG-{next_ticket()}: Investigate visual regression post-chaos",
        })

    return sorted(recommendations, key=lambda r: {"P0": 0, "P1": 1, "P2": 2, "P3": 3}[r["priority"]])
```

---

## Recommendation Template (Per Experiment)

```markdown
## Experiment: <NAME> — Results & Recommendations
**Date**: <DATE> | **Service**: <SERVICE> | **Resilience Score**: <SCORE>/100

### What Happened
- Brief description of the experiment and observed behavior.

### Key Findings
| Finding | Severity | Impact |
|---|---|---|
| <Finding 1> | P0 | Users experienced errors during pod churn |
| <Finding 2> | P1 | Recovery took 3x expected time |

### Root Cause Analysis
- Why did this happen? What was missing?

### Prioritized Recommendations
1. **[P0]** <Recommendation> — <Justification>
   - Ticket: <TICKET_ID>
   - Owner: <PERSON>
   - Target: <SPRINT/DATE>
2. **[P1]** <Recommendation> — <Justification>

### Runbook Updates Required
- [ ] Update recovery runbook for <SCENARIO>
- [ ] Add monitoring alert for <METRIC>
- [ ] Document known limitation in service README

### Re-test Plan
- After fixes, re-run this experiment in staging
- Target resilience score: ≥ 85
```

---

## Auto-Remediation Scripts

For common failure patterns, create auto-remediation:

```bash
#!/bin/bash
# auto-remediate-pod-count.sh — Scale up if pods below minimum
MIN_PODS="${1:-2}"
NAMESPACE="${2:?Usage: $0 <min-pods> <namespace> <deployment>}"
DEPLOYMENT="${3:?}"

CURRENT=$(kubectl get deployment "$DEPLOYMENT" -n "$NAMESPACE" \
  -o jsonpath='{.status.readyReplicas}')

if [ "${CURRENT:-0}" -lt "$MIN_PODS" ]; then
  echo "⚠️  $DEPLOYMENT has $CURRENT pods (min: $MIN_PODS). Scaling up."
  kubectl scale deployment "$DEPLOYMENT" -n "$NAMESPACE" --replicas="$MIN_PODS"
else
  echo "✅ $DEPLOYMENT pod count OK ($CURRENT >= $MIN_PODS)"
fi
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI generates alert routing and remediation recommendations |
| Target | L3 | AI auto-remediates common issues, escalates complex ones |

### Harness AI Agent

**Agent**: Harness AI SRE Agent
**Capabilities**:
- Alert routing and enrichment (within 2-minute time budget)
- Remediation recommendation engine
- Incident hypothesis generation (10% MTTM reduction proven)
- Alert deduplication and correlation

### Human Gates

- Alert rule activation in production
- Remediation action approval
- Escalation policy changes

### Notes

Based on Google SRE research, AI alert enrichment achieves 44% reduction in MTTM. LLMs achieve 60-74% RCA accuracy with few-shot prompting (Szandala, ICCS 2025).

---

## Success Criteria
- [ ] Alert routing configured for all 4 severity levels
- [ ] PagerDuty integration tested (test alert acknowledged)
- [ ] Slack channel notifications working
- [ ] Recommendation engine generates prioritized action items
- [ ] At least 3 recommendation patterns handled automatically
- [ ] Every experiment finding has a ticket with owner and target date
- [ ] Auto-remediation scripts tested for common failure patterns
- [ ] Alert threshold calibration reviewed after first game day

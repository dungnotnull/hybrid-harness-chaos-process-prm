---
name: chaos-resilience-scoring
description: >
  Calculate, track, and report resilience scores for services and the overall platform
  based on chaos experiment results, observability data, and game day outcomes.
  Use this skill whenever experiments complete (s12-s18) and the user needs to quantify
  resilience, compare across services, track maturity over time, or generate resilience
  reports. Also trigger before promoting any service to production and as part of
  postmortem (s25).
---

# Resilience Scoring (s24)

## Purpose
Provide a quantitative, repeatable framework for measuring system resilience — transforming subjective "we think it's resilient" into objective scores that can be tracked over time, compared across services, and used as gates for production promotion.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| All experiment results | s12-s18 outputs | Yes |
| Game day results report | s18 output | Yes |
| Observability data (error rates, latency) | s20 output | Yes |
| Post-chaos test evidence | s11 (rerun) | Yes |
| Cost impact data | s23 output | No |
| Recommendations | s21 output | Yes |
| Previous resilience scores (trend) | Previous s24 runs | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Resilience score card per service | `.commandcode/artifacts/resilience-<service>.json` | JSON |
| Platform resilience report | `.commandcode/artifacts/platform-resilience-report.md` | Markdown |
| Resilience trend data | s25 (postmortem) | JSON (array) |
| Production promotion gate | s22 (governance) | Boolean + score |
| Service maturity matrix | s25 (improvement roadmap) | Table |

---

## Resilience Scoring Formula

```
Resilience Score = Σ(Component Scores × Weights) × Coverage Factor

Where:
  Component Scores (0-100 each):
    Availability Score    — How well did the service stay available?
    Performance Score    — How well did performance hold up?
    Recovery Score       — How fast did the service recover?
    Correctness Score    — Did the service behave correctly?
    Observability Score   — Could we see what was happening?

  Weights (sum to 1.0):
    Availability:    0.30
    Performance:     0.20
    Recovery:        0.20
    Correctness:     0.15
    Observability:   0.15

  Coverage Factor (0.0-1.0):
    = Experiments_Run / Experiments_Planned
    (penalizes services that skip experiments)
```

---

## Component Score Calculation

### Availability Score (0-100)
```python
def calculate_availability_score(results: dict) -> float:
    max_error_rate = results.get("max_error_rate_during_chaos", 0)
    health_probe_failures = results.get("health_probe_failures", 0)
    total_probe_checks = results.get("total_probe_checks", 1)

    error_score = max(0, 100 - (max_error_rate * 20))    # 5% error = 0
    probe_score = (1 - health_probe_failures / total_probe_checks) * 100

    return (error_score * 0.6) + (probe_score * 0.4)
```

### Performance Score (0-100)
```python
def calculate_performance_score(results: dict) -> float:
    p99_ratio = results.get("p99_latency_ratio", 1.0)    # chaos p99 / steady state p99

    if p99_ratio <= 1.5:     # Within 50% of baseline → excellent
        return 100
    elif p99_ratio <= 2.0:   # Within 2x baseline → good
        return 80
    elif p99_ratio <= 3.0:   # Within 3x baseline → acceptable
        return 60
    elif p99_ratio <= 5.0:   # Within 5x baseline → poor
        return 40
    else:                    # More than 5x → critical
        return max(0, 100 - (p99_ratio * 10))
```

### Recovery Score (0-100)
```python
def calculate_recovery_score(results: dict) -> float:
    recovery_time = results.get("recovery_time_seconds", float("inf"))
    target_time = results.get("target_recovery_time_seconds", 60)

    if recovery_time <= target_time:
        return 100
    elif recovery_time <= target_time * 2:
        return 80
    elif recovery_time <= target_time * 3:
        return 60
    elif recovery_time <= target_time * 5:
        return 40
    else:
        return max(0, 100 - (recovery_time / target_time * 10))
```

### Correctness Score (0-100)
```python
def calculate_correctness_score(results: dict) -> float:
    functional_failures = results.get("functional_probe_failures", 0)
    data_integrity_issues = results.get("data_integrity_issues", False)
    visual_regression = results.get("visual_diff_score", 0)

    func_score = max(0, 100 - (functional_failures * 25))
    data_score = 0 if data_integrity_issues else 100
    visual_score = max(0, 100 - (visual_regression * 1000))

    return (func_score * 0.5) + (data_score * 0.3) + (visual_score * 0.2)
```

### Observability Score (0-100)
```python
def calculate_observability_score(results: dict) -> float:
    dashboards_available = results.get("dashboards_available", False)
    metrics_gaps = results.get("metrics_gaps_seconds", 0)
    alert_configured = results.get("alerts_configured", False)
    probes_worked = results.get("probes_success_rate", 0)

    dash_score = 30 if dashboards_available else 0
    gap_score = max(0, 30 - (metrics_gaps / 60 * 10))     # Penalize gaps > 60s
    alert_score = 20 if alert_configured else 0
    probe_score = probes_worked * 20                        # 0-20

    return dash_score + gap_score + alert_score + probe_score
```

---

## Resilience Score Card

```json
{
  "service": "payment-service",
  "environment": "staging",
  "date": "2025-03-15",
  "overall_score": 82,
  "grade": "B",
  "components": {
    "availability": {
      "score": 90,
      "details": {
        "max_error_rate": "0.8%",
        "health_probe_failures": 0,
        "total_probe_checks": 240
      }
    },
    "performance": {
      "score": 80,
      "details": {
        "p99_ratio": 1.8,
        "steady_state_p99_ms": 200,
        "chaos_p99_ms": 360
      }
    },
    "recovery": {
      "score": 85,
      "details": {
        "recovery_time_seconds": 45,
        "target_recovery_time_seconds": 60
      }
    },
    "correctness": {
      "score": 75,
      "details": {
        "functional_probe_failures": 1,
        "data_integrity_issues": false,
        "visual_diff_score": 0.005
      }
    },
    "observability": {
      "score": 80,
      "details": {
        "dashboards_available": true,
        "metrics_gaps_seconds": 15,
        "alerts_configured": true,
        "probes_success_rate": 0.95
      }
    }
  },
  "coverage": {
    "experiments_planned": 10,
    "experiments_run": 9,
    "coverage_factor": 0.9
  },
  "experiments": [
    {"name": "pod-delete-50", "score": 95, "status": "passed"},
    {"name": "container-kill", "score": 88, "status": "passed"},
    {"name": "pod-cpu-hog-80", "score": 72, "status": "passed"},
    {"name": "pod-memory-hog", "score": 68, "status": "passed"},
    {"name": "network-latency-250ms", "score": 88, "status": "passed"},
    {"name": "network-latency-500ms", "score": 82, "status": "passed"},
    {"name": "network-loss", "score": 45, "status": "failed"},
    {"name": "dns-error", "score": 85, "status": "passed"},
    {"name": "composite-scenario", "score": 65, "status": "passed"}
  ],
  "trend": {
    "previous_score": 75,
    "delta": 7,
    "direction": "improving",
    "scores_last_3_months": [68, 75, 82]
  },
  "production_gate": {
    "meets_threshold": false,
    "threshold": 85,
    "gap": 3,
    "blockers": [
      "network-loss experiment failed (score: 45)",
      "pod-memory-hog below 70 threshold"
    ]
  }
}
```

---

## Grading Scale

| Grade | Score Range | Production Readiness |
|---|---|---|
| A+ | 95-100 | Production-ready, all experiments pass |
| A | 85-94 | Strong resilience, minor findings |
| B | 70-84 | Adequate, some gaps to address |
| C | 50-69 | Fragile, significant findings |
| D | 30-49 | Critical gaps, do not promote |
| F | 0-29 | Extremely fragile, immediate action required |

---

## Platform Resilience Report

```markdown
# Platform Resilience Report — Q1 2025

## Overall Platform Score: 78/100 (Grade: B)

### Service Scores
| Service | Q4 2024 | Q1 2025 | Δ | Grade | Prod Ready? |
|---|---|---|---|---|---|
| payment-service | 75 | 82 | +7 | B | ⚠️ (85 target) |
| checkout-api | 88 | 91 | +3 | A | ✅ |
| auth-service | 92 | 94 | +2 | A | ✅ |
| notification-worker | 65 | 70 | +5 | B | ❌ |
| inventory-service | 55 | 60 | +5 | C | ❌ |
| search-service | 80 | 78 | -2 | B | ⚠️ (declining) |

### Critical Gaps (score < 70)
1. **inventory-service (60)**: No circuit breaker, OOM on memory pressure
2. **notification-worker (70)**: DNS failure causes message loss

### Improvements This Quarter
- payment-service: Added circuit breaker (+7 points)
- notification-worker: Improved pod recovery time (+5 points)

### Top Recommendations
1. Inventory-service needs circuit breaker (P0)
2. Search-service declining — investigate regression (P1)
3. Payment-service 3 points from production gate (P1)
```

---

## Score Trend Tracking

```json
{
  "service": "payment-service",
  "trends": [
    {"date": "2025-01", "score": 68, "experiments_run": 5, "grade": "C"},
    {"date": "2025-02", "score": 75, "experiments_run": 8, "grade": "B"},
    {"date": "2025-03", "score": 82, "experiments_run": 9, "grade": "B"},
    {"date": "2025-04", "score": null, "target": 88},  // Projected
    {"date": "2025-05", "score": null, "target": 90}   // Projected
  ]
}
```

---

## Production Promotion Gate

```python
def production_readiness_gate(score_card: dict) -> dict:
    score = score_card["overall_score"]
    components = score_card["components"]

    gate = {
        "overall": score >= 85,
        "availability": components["availability"]["score"] >= 90,
        "performance": components["performance"]["score"] >= 80,
        "recovery": components["recovery"]["score"] >= 80,
        "correctness": components["correctness"]["score"] >= 75,
        "observability": components["observability"]["score"] >= 80,
        "coverage": score_card["coverage"]["coverage_factor"] >= 0.8,
        "no_critical_failures": all(
            e["status"] == "passed" for e in score_card["experiments"]
            if e["score"] < 40
        ) == False,  # No experiment < 40
    }

    gate["approved"] = all(gate.values())
    gate["blockers"] = [k for k, v in gate.items() if not v]

    return gate
```

---

## Success Criteria
- [ ] Resilience score calculated for every service tested
- [ ] All 5 component scores computed with evidence
- [ ] Coverage factor accounted for (no skipped experiments without reason)
- [ ] Platform resilience report generated quarterly
- [ ] Trend data tracked (minimum 3 months history)
- [ ] Production gate enforced: score < 85 = blocked from production
- [ ] Score card feed into s25 (postmortem) and s22 (governance gate)
- [ ] Service maturity visible on dashboard

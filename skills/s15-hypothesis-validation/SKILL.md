---
name: chaos-hypothesis-validation
description: >
  Write, validate, and track chaos engineering hypotheses using the scientific method.
  Use this skill whenever the user needs to formulate a chaos hypothesis, define what
  "success" means for a chaos experiment, document expected vs actual behavior, validate
  SLOs during fault injection, write hypothesis statements, or determine whether a chaos
  experiment passed or failed based on system behavior. Also trigger when a chaos
  experiment ran but the user doesn't know how to interpret whether the system behaved
  correctly.
---

# Chaos Hypothesis Validation

## Purpose
Transform vague "what if X breaks?" questions into precise, falsifiable hypotheses with measurable success criteria — making chaos experiments scientifically rigorous rather than random fault injection.

---

## Prerequisites
- [ ] Chaos experiment designs from s14 (Experiment Design)
- [ ] Steady state baselines from s17 (Steady State Definition)
- [ ] Target service metrics identified
- [ ] Observability stack active (Prometheus, Grafana)
- [ ] Performance baselines from s13 (Performance Testing)

## Input Contract

| Input | Source | Required |
|---|---|---|
| Experiment designs (ChaosEngine YAML) | s12 (workflow_context.artifacts) | Yes |
| Steady state baselines | s15 output | Yes |
| Service SLIs/SLOs from PRD | s01 context | Yes |
| Blast radius constraints | s14 output | Yes |
| Observability metrics available | s20 output | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Hypothesis document per experiment | `.commandcode/artifacts/hypothesis-<name>.md` | Markdown |
| Validation script (Python) | `.commandcode/artifacts/hypothesis-validator.py` | Python |
| Pre-experiment check script | `.commandcode/artifacts/pre-chaos-check.sh` | Bash |
| Hypothesis tracker table | s24, s25 (scoring + learning) | Markdown table |
| Acceptance criteria YAML | s18 (game day gates) | YAML |

---

## The Chaos Hypothesis Formula

```
HYPOTHESIS STATEMENT:
"When [FAULT DESCRIPTION] is applied to [TARGET SCOPE] for [DURATION],
the [SYSTEM/SERVICE] will [EXPECTED BEHAVIOR],
as evidenced by [MEASURABLE METRIC] remaining [CONDITION] (e.g., below 5%, above 99.9%)."

ACCEPTANCE CRITERIA:
- [METRIC_1]: [OPERATOR] [THRESHOLD] (e.g., error_rate <= 5%)
- [METRIC_2]: [OPERATOR] [THRESHOLD] (e.g., p99_latency <= 2000ms)
- [FUNCTIONAL_CHECK]: [PASS/FAIL criterion]

NULL HYPOTHESIS (what failure looks like):
"The system will fail to meet [METRIC] when [FAULT] is applied."
```

---

## Hypothesis Tiers

| Tier | Scope | Hypothesis Type | Example |
|---|---|---|---|
| **Unit** | Single pod | Component resilience | "Killing one pod, service stays available" |
| **Service** | One microservice | Service resilience | "DB connection lost, service uses circuit breaker" |
| **Integration** | Service-to-service | Dependency resilience | "Payment service timeout, checkout returns cached response" |
| **System** | Entire platform | System resilience | "AZ failure, traffic routes to healthy AZ" |
| **Business** | User-facing flow | Business continuity | "30% pod churn, checkout conversion stays above 90%" |

---

## Hypothesis Template Library

### Template 1: Pod Availability
```markdown
## Hypothesis: Pod Delete Resilience — <SERVICE_NAME>

**Fault**: Delete 50% of `<SERVICE_NAME>` pods every 10 seconds for 60 seconds.

**Pre-conditions (Steady State)**:
- HTTP health check returns 200: ✓
- Error rate (5xx): < 1%
- P99 latency: < 200ms
- Pod count: ≥ 3 replicas running

**Hypothesis Statement**:
When 50% of `<SERVICE_NAME>` pods are deleted every 10 seconds for 60 seconds,
the service will continue to serve requests successfully due to Kubernetes
self-healing and load balancer session persistence,
as evidenced by HTTP error rate staying ≤ 5% and P99 latency staying ≤ 500ms
throughout the experiment duration.

**Acceptance Criteria**:
| Metric | Threshold | Measurement Method |
|---|---|---|
| HTTP 5xx error rate | ≤ 5% | Prometheus `http_requests_total{status=~"5.."}` |
| P99 latency | ≤ 500ms | Prometheus histogram_quantile(0.99) |
| Health endpoint | Returns 200 | HTTP probe every 5s |
| Pod recovery time | ≤ 30s | Kubernetes event watcher |

**Null Hypothesis (failure condition)**:
The service will return 5xx errors > 5% OR P99 latency will exceed 500ms
during the pod deletion period.

**Expected Learning**:
- Kubernetes HPA / ReplicaSet guarantees self-healing within 30s
- Service mesh / kube-proxy routes away from terminating pods
- Any gap = finding requiring action (PodDisruptionBudget, readiness probe tuning)
```

### Template 2: Network Partition
```markdown
## Hypothesis: Network Latency Resilience — <SERVICE_A> → <SERVICE_B>

**Fault**: Inject 500ms network latency between <SERVICE_A> and <SERVICE_B> for 120s.

**Hypothesis Statement**:
When 500ms network latency is injected on all traffic from `<SERVICE_A>` to `<SERVICE_B>`,
`<SERVICE_A>` will activate its circuit breaker after 3 consecutive timeouts (5s timeout threshold),
return a cached/fallback response to end users,
and recover automatically within 30 seconds of latency removal.

**Acceptance Criteria**:
| Metric | Threshold | Evidence |
|---|---|---|
| Circuit breaker opens | Within 15s of latency onset | Circuit breaker state metric |
| User-facing error rate | ≤ 1% (fallback serves) | Frontend error tracking |
| Fallback response correctness | Returns valid fallback JSON | Functional probe |
| Recovery time after fault removal | ≤ 30s | HTTP probe re-establishes 200 |

**System Assumptions Being Tested**:
- <SERVICE_A> has circuit breaker configured with 5s timeout, 3 failure threshold
- Fallback response is cached and not stale > 5 minutes
- Circuit breaker half-open probe interval is 10s
```

### Template 3: Infrastructure Failure
```markdown
## Hypothesis: Single Node Failure — <CLUSTER_NAME>

**Fault**: Drain one Kubernetes worker node for 5 minutes.

**Hypothesis Statement**:
When one worker node is drained in `<CLUSTER_NAME>`,
all workloads will reschedule to remaining healthy nodes within 2 minutes,
stateful services will recover without data loss,
and the platform SLO (99.9% availability) will be maintained throughout.

**Acceptance Criteria**:
| Service | Availability Target | Recovery Time Target |
|---|---|---|
| `payment-service` | 100% (no downtime) | N/A (immediate reschedule) |
| `order-service` | ≥ 99% | ≤ 60s |
| `postgres` (via StatefulSet) | 100% (follower promotes) | ≤ 120s |
| Overall platform | ≥ 99.9% | N/A |

**Anti-requirements (must NOT happen)**:
- No data loss in PostgreSQL write-ahead log
- No orphaned PersistentVolumes
- No alert pages (error rate stays below PagerDuty threshold)
```

---

## Hypothesis Validation Workflow

### Phase 1: Pre-Experiment Validation (T-10 minutes)
```bash
# Verify steady state is healthy BEFORE starting chaos
echo "=== Pre-Experiment Steady State Check ==="
echo "1. HTTP Health:"
curl -f http://<SERVICE>.<NAMESPACE>.svc.cluster.local/health && echo "PASS" || echo "FAIL"

echo "2. Error Rate (last 5m):"
curl -s "http://prometheus:9090/api/v1/query" \
  --data-urlencode 'query=sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100' \
  | jq '.data.result[0].value[1]'

echo "3. P99 Latency (last 5m, ms):"
curl -s "http://prometheus:9090/api/v1/query" \
  --data-urlencode 'query=histogram_quantile(0.99, rate(http_request_duration_ms_bucket[5m])) * 1000' \
  | jq '.data.result[0].value[1]'

echo "4. Pod Count:"
kubectl get pods -n <NAMESPACE> -l app=<SERVICE> --no-headers | wc -l
```

### Phase 2: During Experiment
```bash
# Poll metrics every 10 seconds during fault injection
watch -n 10 'curl -s "http://prometheus:9090/api/v1/query" \
  --data-urlencode "query=sum(rate(http_requests_total{status=~\"5..\"}[1m])) / sum(rate(http_requests_total[1m])) * 100" \
  | jq ".data.result[0].value[1]"'
```

### Phase 3: Post-Experiment Validation
```python
# hypothesis_validator.py — run after experiment completes
import requests
import json
from datetime import datetime, timedelta

PROMETHEUS_URL = "http://prometheus:9090"
EXPERIMENT_START = "2025-01-15T10:00:00Z"
EXPERIMENT_END   = "2025-01-15T10:05:00Z"

def query_range(promql, start, end, step="15s"):
    r = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params={
        "query": promql,
        "start": start,
        "end": end,
        "step": step,
    })
    return r.json()["data"]["result"]

# Evaluate acceptance criteria
results = {
    "error_rate_max": max(
        float(v[1]) for series in query_range(
            'sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m])) * 100',
            EXPERIMENT_START, EXPERIMENT_END
        ) for v in series["values"]
    ),
    "p99_latency_max": max(
        float(v[1]) for series in query_range(
            'histogram_quantile(0.99, rate(http_request_duration_ms_bucket[1m]))',
            EXPERIMENT_START, EXPERIMENT_END
        ) for v in series["values"]
    ),
}

THRESHOLDS = {
    "error_rate_max": 5.0,      # max 5% error rate
    "p99_latency_max": 500.0,   # max 500ms p99 latency
}

print("=== Hypothesis Validation Results ===")
passed = True
for metric, value in results.items():
    threshold = THRESHOLDS[metric]
    status = "✅ PASS" if value <= threshold else "❌ FAIL"
    print(f"{status} | {metric}: {value:.2f} (threshold: {threshold})")
    if value > threshold:
        passed = False

print(f"\n{'✅ HYPOTHESIS CONFIRMED' if passed else '❌ HYPOTHESIS REJECTED'}")
```

---

## Hypothesis Tracker (Markdown Table)

Maintain this in your chaos runbook wiki:

```markdown
| ID | Service | Fault | Hypothesis | Date | Result | Score | Finding | Ticket |
|---|---|---|---|---|---|---|---|---|
| CHX-001 | payment | pod-delete 50% | Service stays available | 2025-01-10 | ✅ PASS | 95 | Minor latency spike at t=30s | — |
| CHX-002 | checkout | network-latency 500ms | Circuit breaker activates | 2025-01-12 | ❌ FAIL | 45 | Circuit breaker not configured | ENG-4421 |
| CHX-003 | auth | pod-delete 100% | Auth tokens cached in Redis | 2025-01-15 | ✅ PASS | 88 | Redis TTL could be longer | ENG-4438 |
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI assists in hypothesis writing and validation |
| Target | L2 | AI generates validation scripts and steady-state probes |

### Harness AI Agent

**Agent**: Harness AI Reliability Agent
**Capabilities**:
- Steady-state validation script generation
- Probe configuration for HTTP/CMD/Prometheus
- Hypothesis structure suggestions

### Human Gates

- Hypothesis acceptance/rejection
- Validation criteria approval

### MCP

- LitmusChaos MCP (resilience probes)
- Prometheus

---

## Success Criteria
- [ ] Every chaos experiment has a written hypothesis before running
- [ ] Hypothesis includes specific measurable thresholds (not vague "stays healthy")
- [ ] Pre-experiment steady state check passes before fault injection
- [ ] Post-experiment validation script produces PASS/FAIL verdict
- [ ] Results recorded in hypothesis tracker with ticket for every FAIL
- [ ] FAIL hypotheses generate remediation tickets within 24h

---
name: performance-load-testing
description: >
  Execute systematic performance profiling and load testing to establish baselines
  before chaos experiments and validate system behavior under realistic traffic.
  Use this skill whenever the user says "load test", "performance test", "stress test",
  "capacity planning", "benchmark", "establish performance baseline", or needs to
  verify system behavior under expected and peak load. This skill MUST run before
  any chaos experiment suite (s14+) to ensure you know what "normal" looks like
  and have quantifiable metrics to compare against when faults are injected.
---

# Performance & Load Testing (s13)

## Purpose
Establish quantitative performance baselines and validate system capacity before chaos experiments. Without knowing how the system performs under normal load, chaos results are meaningless — you can't determine if a latency spike is from the fault or from pre-existing performance issues.

---

## Prerequisites
- [ ] Service endpoints identified and accessible
- [ ] SLAs and performance requirements defined (from s01 PRD)
- [ ] k6 installed or available as container image
- [ ] Target environment provisioned and stable
- [ ] Baseline performance metrics from s12 (E2E testing) recommended

## Input Contract

| Input | Source | Required |
|---|---|---|
| Deployed service endpoints | s05 (service definitions), s10 (GitOps sync) | Yes |
| Expected traffic patterns | s01 (PRD — scale/throughput requirements) | Yes |
| Performance SLAs (p99, error rate, throughput) | s01 (NFRs), s19 (SLO targets) | Yes |
| Security scan passed | s11 (security gate verdict) | Yes |
| Load test tool preference | s02 taste (testing/tooling) | No |
| Infrastructure topology (replicas, resources) | s05 (service defs) | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Performance baseline report | `.commandcode/artifacts/perf/perf-baseline-<service>.json` | JSON |
| Load test scripts (k6/Locust) | `.commandcode/artifacts/perf/load-test-<service>.js` | JavaScript/Python |
| Stress test results (breaking point) | `.commandcode/artifacts/perf/stress-test-results.json` | JSON |
| Capacity recommendations | s23 (cloud cost), s24 (scoring) | Markdown |
| Performance SLO validation | s19 (CV config threshold tuning) | YAML |
| Baseline for chaos comparison | s14-s21 (all chaos skills) | JSON |

---

## Load Testing Strategy

```
LEVEL 1: Smoke Test          — 1 VU, 1 minute         → Verify test scripts work
LEVEL 2: Baseline            — Expected load, 5 min    → Establish "normal" performance
LEVEL 3: Load Test           — Peak load, 15 min       → Validate production capacity
LEVEL 4: Stress Test         — Ramp to breaking point  → Find system limits
LEVEL 5: Soak Test           — 80% peak, 1-4 hours     → Memory leaks, connection leaks
LEVEL 6: Spike Test          — Sudden 5x traffic burst → Autoscaling response
LEVEL 7: Chaos-Load Combined  — Load + fault injection → Resilience under traffic
```

---

## Step 1 — k6 Load Test Script

```javascript
// load-test-<service>.js — k6 load test
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('errors');
const checkoutDuration = new Trend('checkout_duration');
const paymentLatency = new Trend('payment_latency');

export const options = {
  // LEVEL 2: Baseline
  stages: [
    { duration: '1m', target: 50 },    // Ramp up to 50 VUs
    { duration: '3m', target: 50 },    // Stay at 50 VUs (baseline)
    { duration: '1m', target: 0 },     // Ramp down
  ],

  // LEVEL 3: Load Test (uncomment for load)
  // stages: [
  //   { duration: '2m', target: 200 },   // Ramp to expected peak
  //   { duration: '10m', target: 200 },  // Sustain peak
  //   { duration: '3m', target: 0 },     // Cool down
  // ],

  // LEVEL 4: Stress Test (uncomment for stress)
  // stages: [
  //   { duration: '2m', target: 100 },
  //   { duration: '3m', target: 200 },
  //   { duration: '3m', target: 400 },
  //   { duration: '3m', target: 800 },
  //   { duration: '2m', target: 0 },
  // ],

  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],  // P95<500ms, P99<1s
    errors: ['rate<0.01'],                             // <1% error rate
    http_req_failed: ['rate<0.01'],
  },

  // LEVEL 5: Soak (uncomment)
  // duration: '4h',
  // vus: 100,
};

const BASE_URL = __ENV.BASE_URL || 'https://staging.company.com';

export default function () {
  group('Homepage', () => {
    const res = http.get(`${BASE_URL}/`);
    check(res, {
      'homepage status 200': (r) => r.status === 200,
      'homepage loads < 2s': (r) => r.timings.duration < 2000,
    });
    errorRate.add(res.status >= 400);
    sleep(1);
  });

  group('Product Browse', () => {
    const res = http.get(`${BASE_URL}/api/v1/products?page=1&limit=20`);
    check(res, {
      'products status 200': (r) => r.status === 200,
      'products load < 500ms': (r) => r.timings.duration < 500,
    });
    errorRate.add(res.status >= 400);
    sleep(0.5);
  });

  group('Checkout Flow', () => {
    // Step 1: Get cart
    const cartRes = http.get(`${BASE_URL}/api/v1/cart`, {
      headers: { Authorization: `Bearer ${getAuthToken()}` },
    });
    check(cartRes, { 'cart status 200': (r) => r.status === 200 });

    // Step 2: Create payment
    const paymentPayload = JSON.stringify({
      amount: 99.99,
      currency: 'USD',
      payment_method: 'card',
      card_token: 'tok_visa',
    });

    const paymentRes = http.post(`${BASE_URL}/api/v1/payments`, paymentPayload, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${getAuthToken()}`,
      },
    });
    checkoutDuration.add(paymentRes.timings.duration);
    paymentLatency.add(paymentRes.timings.duration);

    check(paymentRes, {
      'payment status 200': (r) => r.status === 200,
      'payment < 1s': (r) => r.timings.duration < 1000,
      'payment confirmed': (r) => r.json('status') === 'confirmed',
    });
    errorRate.add(paymentRes.status >= 400);
    sleep(1);
  });
}

// User simulation: different user types with different behavior patterns
export function setup() {
  return {
    authTokens: generateAuthTokens(1000),     // Pre-generate 1000 user tokens
    productIds: fetchProductIds(),             // Cache product IDs
  };
}

function getAuthToken() {
  const tokens = setup().authTokens;
  return tokens[Math.floor(Math.random() * tokens.length)];
}
```

---

## Step 2 — Run Load Tests

```bash
# Level 1: Smoke (1 VU, verify scripts work)
k6 run --vus 1 --duration 1m load-test-payment.js

# Level 2: Baseline (expected normal load)
k6 run --out json=.commandcode/artifacts/perf/baseline-results.json \
  load-test-payment.js

# Level 3: Load (peak traffic simulation)
k6 run --env SCENARIO=load \
  --out json=.commandcode/artifacts/perf/load-results.json \
  load-test-payment.js

# Level 4: Stress (find breaking point)
k6 run --env SCENARIO=stress \
  --out json=.commandcode/artifacts/perf/stress-results.json \
  load-test-payment.js

# Level 5: Soak (memory leak detection, 4 hours)
k6 run --env SCENARIO=soak \
  --duration 4h --vus 100 \
  --out json=.commandcode/artifacts/perf/soak-results.json \
  load-test-payment.js
```

---

## Step 3 — Performance Baseline Report

```json
{
  "service": "payment-service",
  "environment": "staging",
  "timestamp": "2025-06-15T10:00:00Z",
  "test_duration_seconds": 300,
  "scenario": "baseline",
  "infrastructure": {
    "replicas": 3,
    "cpu_per_replica": "1000m",
    "memory_per_replica": "512Mi",
    "node_count": 4
  },
  "results": {
    "http_requests": {
      "total": 15723,
      "rate_per_second": 52.4,
      "failed": 12,
      "failure_rate": 0.00076
    },
    "latency": {
      "p50_ms": 45,
      "p90_ms": 120,
      "p95_ms": 180,
      "p99_ms": 310,
      "max_ms": 1450
    },
    "throughput": {
      "checkout_transactions_per_second": 8.3,
      "payment_authorizations_per_second": 8.2,
      "payment_success_rate": 0.997
    },
    "errors": {
      "5xx_count": 5,
      "4xx_count": 7,
      "timeout_count": 0,
      "error_rate_percent": 0.076
    },
    "resources_during_test": {
      "avg_cpu_percent": 42,
      "max_cpu_percent": 68,
      "avg_memory_mb": 380,
      "max_memory_mb": 480,
      "connection_pool_usage_percent": 45
    }
  },
  "slo_validation": {
    "p95_latency_target_ms": 500,
    "p95_latency_actual_ms": 180,
    "p95_pass": true,
    "error_rate_target_percent": 1.0,
    "error_rate_actual_percent": 0.076,
    "error_rate_pass": true,
    "throughput_target_rps": 40,
    "throughput_actual_rps": 52.4,
    "throughput_pass": true
  },
  "baseline_established": true,
  "chaos_comparison_ready": true
}
```

---

## Step 4 — Stress Test (Find Breaking Point)

```yaml
stress_test_findings:
  service: payment-service
  current_config:
    replicas: 3
    cpu_per_replica: 1000m
    memory_per_replica: 512Mi

  breaking_points:
    - vus: 200
      failure: none
      p99_ms: 420
      note: "Service handles 200 VUs comfortably"

    - vus: 400
      failure: none
      p99_ms: 780
      note: "Latency increasing but within SLO"

    - vus: 600
      failure: partial
      p99_ms: 2100
      error_rate: 2.3%
      note: "SLO breached — errors appearing. Autoscaler triggered."

    - vus: 800
      failure: critical
      p99_ms: 5500
      error_rate: 15.7%
      note: "BREAKING POINT — cascading failures, OOM kills"

  recommendations:
    - Increase min replicas from 3 to 5
    - Add HPA with CPU target 60%
    - Increase memory limit from 512Mi to 1024Mi
    - Add connection pooling limit to prevent DB saturation
    - Capacity: 3 replicas handle 400 VUs before degradation
```

---

## Step 5 — Performance Regression Detection

```python
# perf_regression_detector.py
# Compare current run against established baseline
import json

def detect_regression(baseline_path: str, current_path: str) -> dict:
    with open(baseline_path) as f:
        baseline = json.load(f)
    with open(current_path) as f:
        current = json.load(f)

    thresholds = {
        "p99_ms": 1.2,           # 20% degradation = regression
        "error_rate": 2.0,       # 2x error rate = regression
        "throughput": 0.85,      # 15% throughput drop = regression
    }

    results = {
        "timestamp": current["timestamp"],
        "compared_against_baseline": baseline["timestamp"],
        "metrics": {},
        "regression_detected": False,
        "regressions": [],
    }

    # P99 latency check
    baseline_p99 = baseline["results"]["latency"]["p99_ms"]
    current_p99 = current["results"]["latency"]["p99_ms"]
    ratio = current_p99 / baseline_p99 if baseline_p99 > 0 else 1

    results["metrics"]["p99_ms"] = {
        "baseline": baseline_p99,
        "current": current_p99,
        "ratio": round(ratio, 2),
        "threshold": thresholds["p99_ms"],
        "regression": ratio > thresholds["p99_ms"],
    }
    if ratio > thresholds["p99_ms"]:
        results["regression_detected"] = True
        results["regressions"].append(
            f"P99 latency degraded {((ratio - 1) * 100):.0f}% ({baseline_p99}ms → {current_p99}ms)"
        )

    # Error rate check
    baseline_err = baseline["results"]["errors"]["error_rate_percent"]
    current_err = current["results"]["errors"]["error_rate_percent"]
    err_ratio = current_err / baseline_err if baseline_err > 0 else 1

    results["metrics"]["error_rate"] = {
        "baseline": baseline_err,
        "current": current_err,
        "ratio": round(err_ratio, 2),
        "threshold": thresholds["error_rate"],
        "regression": err_ratio > thresholds["error_rate"],
    }
    if err_ratio > thresholds["error_rate"]:
        results["regression_detected"] = True
        results["regressions"].append(
            f"Error rate increased {((err_ratio - 1) * 100):.0f}% ({baseline_err}% → {current_err}%)"
        )

    results["verdict"] = "❌ REGRESSION DETECTED" if results["regression_detected"] else "✅ NO REGRESSION"
    return results
```

---

## Step 6 — Combined Chaos + Load (Level 7)

```javascript
// chaos-load-combined.js
// Run this DURING chaos experiments (s14-s21)
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 30 },      // Ramp
    { duration: '4m',  target: 30 },      // Sustained load during chaos
    { duration: '30s', target: 0 },       // Cool down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<1000'],  // Relaxed for chaos — expect degradation
    'errors': ['rate<0.05'],              // 5% allowed during chaos (vs 1% normal)
  },
};

export default function () {
  // Standard user flows — same as baseline
  http.get(`${__ENV.BASE_URL}/`);
  http.get(`${__ENV.BASE_URL}/api/v1/products?page=1`);
  sleep(1);
}
```

```bash
# Run load test DURING chaos experiment
# The k6 metrics collected here feed into resilience scoring (s26)
k6 run chaos-load-combined.js \
  --tag scenario=chaos-pod-delete \
  --out json=.commandcode/artifacts/perf/chaos-load-pod-delete.json
```

---

## Capacity Planning Recommendations

Based on stress test results:

```markdown
## Capacity Planning — payment-service

### Current Capacity
- 3 replicas × 1000m CPU = 3000m CPU total
- Handles: 400 VUs before degradation, ~50 RPS sustained

### Recommended for Production
- Minimum: 5 replicas (buffer for 1 AZ failure)
- HPA: min 5, max 15, CPU target 60%
- Memory: 1024Mi per replica (up from 512Mi)
- Node pool: minimum 3 nodes, spread across 3 AZs

### Cost Impact
- Current: ~$450/month
- Recommended: ~$750/month
- Justification: Stress test showed failure at 600 VUs.
  At projected Q4 traffic (500 VUs peak), current config
  would fail. Additional 2 replicas provide safety margin.

### Scaling Triggers
- CPU > 60% → +2 replicas
- Memory > 80% → +2 replicas
- Request queue > 100 → +1 replica
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI optimizes test selection and compares baselines |
| Target | L2 | AI generates k6 scripts and detects anomalies |

### Harness AI Agent

**Agent**: Harness AI Test Agent
**Capabilities**:
- Test selection optimization
- Baseline comparison and anomaly detection
- Performance regression identification

### Human Gates

- Performance threshold approval
- Capacity planning decisions
- Load test parameter configuration

### Fallback

Manual k6 script creation following k6 documentation

---

## Success Criteria
- [ ] Baseline performance report generated (Level 2)
- [ ] Stress test identifies breaking point (Level 4)
- [ ] All SLO thresholds validated under normal load
- [ ] Performance regression detection script tested
- [ ] Capacity recommendations documented with cost justification
- [ ] Combined chaos+load test script ready for game day (Level 7)
- [ ] Baseline JSON committed to `.commandcode/artifacts/perf/`
- [ ] Autoscaling verified during spike test (Level 6)

---
name: chaos-blast-radius-control
description: >
  Define, enforce, and progressively expand the blast radius of chaos experiments.
  Use this skill whenever the user mentions blast radius, limiting chaos scope, targeting
  specific pods or nodes, chaos label selectors, chaos namespace scoping, progressive
  chaos expansion, chaos abort conditions, or when the user is worried about a chaos
  experiment affecting production traffic or unintended services. Also trigger when
  setting up safeguards and abort mechanisms for any chaos experiment.
---

# Chaos Blast Radius Control

## Purpose
Guarantee that chaos experiments affect only the intended targets, at the intended intensity, for the intended duration — with automatic abort mechanisms when the experiment exceeds safe boundaries.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Experiment designs | s12 (workflow_context.artifacts) | Yes |
| Environment tier permissions | CLAUDE.md (chaos allowed table) | Yes |
| Feature flag chaos gate | s08 output | No (recommended) |
| Risk tolerance preferences | s02 taste (risk_tolerance) | Yes |
| Service criticality ratings | s01 PRD | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Blast radius config per experiment | `.commandcode/artifacts/blast-radius-<name>.yaml` | YAML |
| Namespace-scoped RBAC | s06 (delegate update) | YAML |
| PodDisruptionBudget YAML | `.commandcode/artifacts/pdb-<service>.yaml` | YAML |
| Blast radius expansion matrix | s18 (game day runbook) | Markdown |
| Safety runbook template | s18 (game day), s21 (alerts) | Markdown |
| OPA blast radius policies | s22 (governance) | Rego |

---

## Blast Radius Dimensions

```
Blast Radius = Scope × Intensity × Duration

Scope:     Which targets (namespace / label / pod count / node)
Intensity: How severe (packet loss % / CPU hog % / pods deleted %)
Duration:  How long (seconds of fault injection)

All three must be minimized independently and expanded incrementally.
```

---

## Scope Control Mechanisms

### Level 1 — Pod Label Selector (finest granularity)
```yaml
# Target ONLY pods with specific labels — nothing else is affected
spec:
  appinfo:
    appns: payments          # Namespace boundary
    applabel: "app=checkout-api,version=v2"   # AND condition
    appkind: deployment
```

**Label selector best practices**:
```bash
# Before running experiment, verify label selector matches ONLY intended targets
kubectl get pods -n payments -l "app=checkout-api,version=v2" --no-headers

# Expected: only the 3 pods you intend to target
# If more pods match: narrow the selector, add version or shard labels first
```

### Level 2 — Namespace Isolation
```yaml
# Never give chaos service account ClusterAdmin
# Scope RBAC to target namespace only
apiVersion: rbac.authorization.k8s.io/v1
kind: Role                      # Role (not ClusterRole)
metadata:
  name: chaos-role
  namespace: payments            # Scoped to this namespace ONLY
  labels:
    managed-by: hcprm
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["delete", "get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["litmuschaos.io"]
    resources: ["chaosengines", "chaosexperiments", "chaosresults"]
    verbs: ["create", "get", "list", "patch", "update", "watch"]
```

### Level 3 — Percentage Cap
```yaml
# Limit percentage of matching pods affected
env:
  - name: PODS_AFFECTED_PERC
    value: "50"    # Never delete more than 50% at once
  # Combined with CHAOS_INTERVAL: ensures at least 50% always running
```

### Level 4 — Annotation Gate (Production Safety)
```yaml
# ChaosEngine: only target pods with explicit opt-in annotation
spec:
  annotationCheck: "true"

# Apply annotation to allowed targets only:
kubectl annotate pod <POD_NAME> -n payments litmuschaos.io/chaos="true"

# This means: only pods explicitly annotated can be targets
# Even if label selector matches, unannotated pods are immune
```

### Level 5 — Feature Flag Gate (see harness/05-feature-flags)
```yaml
# Wrap chaos trigger in feature flag
# FF_CHAOS_PAYMENT_POD_DELETE = false → experiment skipped entirely
# Enables instant kill switch without modifying experiment YAML
```

---

## Intensity Control

### CPU Hog — Intensity Ladder
```yaml
# Start at 50%, measure impact, increase only if safe
env:
  - name: CPU_CORES
    value: "1"       # Start: 1 core
    # → 2 cores → 4 cores (after validation at each step)
  - name: CPU_LOAD
    value: "50"      # Start: 50% utilization
    # → 70% → 90% (after validation)
  - name: TOTAL_CHAOS_DURATION
    value: "30"      # Start: 30s
    # → 60s → 120s (after validation)
```

### Network Latency — Graduated Injection
```yaml
# Week 1: 100ms (barely noticeable)
# Week 2: 250ms (timeout edge cases)
# Week 3: 500ms (circuit breaker threshold)
# Week 4: 1000ms (worst-case upstream)
env:
  - name: NETWORK_LATENCY
    value: "100"     # milliseconds — start low
  - name: JITTER
    value: "10"      # ±10ms variance
```

---

## Automatic Abort Conditions

### Probe-Based Abort (LitmusChaos)
```yaml
experiments:
  - name: pod-delete
    spec:
      probe:
        - name: error-rate-abort-gate
          type: promProbe
          mode: Continuous
          promProbe/inputs:
            endpoint: "http://prometheus.monitoring.svc.cluster.local:9090"
            query: |
              sum(rate(http_requests_total{
                namespace="payments",
                status=~"5.."
              }[1m])) /
              sum(rate(http_requests_total{namespace="payments"}[1m])) * 100
            comparator:
              type: float
              criteria: "<="
              value: "5.0"         # ABORT if error rate exceeds 5%
          runProperties:
            probeTimeout: 5s
            interval: 10s
            retry: 1              # No retries — abort immediately on probe fail
            stopOnFailure: true   # ← KEY: stops experiment on probe failure
```

### PodDisruptionBudget Guard
```yaml
# This is NOT a chaos config — it's a Kubernetes safety net
# PDB ensures chaos cannot delete more pods than allowed
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: <SERVICE_NAME>-pdb
  namespace: <NAMESPACE>
  labels:
    managed-by: hcprm
spec:
  minAvailable: 2            # At least 2 pods must be running at all times
  selector:
    matchLabels:
      app: <SERVICE_NAME>
# Chaos pod-delete will respect this PDB and fail gracefully
# if it would violate the minAvailable constraint
```

---

## Blast Radius Expansion Matrix

Follow this progression before any production experiment:

```
Stage 1 — DEV (validate experiment works at all)
├── Scope: 1 pod, 1 namespace
├── Intensity: 25% resources / 30s duration
├── Gates: none (dev is safe to experiment)
└── Pass criteria: experiment runs without errors

Stage 2 — STAGING (validate hypothesis)
├── Scope: 50% of pods, target namespace only
├── Intensity: 50% resources / 60s duration
├── Gates: HTTP probe (health endpoint)
└── Pass criteria: hypothesis validated, resilience score ≥ 80

Stage 3 — PREPROD (simulate production)
├── Scope: 50% of pods, production-like namespace
├── Intensity: 75% resources / 90s duration
├── Gates: HTTP probe + Prometheus probe
└── Pass criteria: resilience score ≥ 90, zero PagerDuty alerts

Stage 4 — PRODUCTION (with all safeguards)
├── Scope: 30% of pods max, single AZ only
├── Intensity: 50% resources / 60s duration
├── Gates: HTTP + Prometheus + circuit breaker state probe
├── Scheduling: business hours only, low-traffic window
├── On-call: SRE present and monitoring dashboard open
└── Pass criteria: resilience score = 100, zero customer impact
```

---

## Chaos Safety Runbook Template

Generate and store this before each production chaos run:

```markdown
## Chaos Safety Runbook — <EXPERIMENT_NAME>

**Date**: <DATE>
**Environment**: <ENV>
**SRE On-Call**: <NAME> (<PAGER_DUTY_HANDLE>)
**Blast Radius**: <SCOPE_DESCRIPTION>

### Abort Checklist (do ANY of these → abort immediately)
- [ ] HTTP error rate > 5%
- [ ] P99 latency > 2x baseline
- [ ] PagerDuty alert fires
- [ ] Customer support reports > 3 tickets in 10 minutes
- [ ] On-call engineer gut says "something is wrong"

### Abort Procedure
1. Run: `kubectl patch chaosengine <ENGINE_NAME> -n <NAMESPACE> --type merge -p '{"spec":{"engineState":"stop"}}'`
2. Verify pods recovering: `kubectl get pods -n <NAMESPACE> -w`
3. Check metrics returning to baseline (allow 5 minutes)
4. Post in #incidents: "@here Chaos experiment aborted — investigating"
5. Do NOT re-run until root cause understood

### Rollback (if abort doesn't restore health)
1. Scale deployment: `kubectl scale deployment <SERVICE_NAME> -n <NAMESPACE> --replicas=<ORIGINAL_COUNT>`
2. Force pod restart: `kubectl rollout restart deployment/<SERVICE_NAME> -n <NAMESPACE>`
3. Check service endpoints: `kubectl get endpoints <SERVICE_NAME> -n <NAMESPACE>`
```

---

## Blast Radius Governance via OPA

```rego
package chaos_blast_radius

# Experiments must not target more than 50% of pods in production
deny["Production chaos experiments must set PODS_AFFECTED_PERC <= 50"] {
  input.metadata.labels.environment == "production"
  env := input.spec.experiments[_].spec.components.env[_]
  env.name == "PODS_AFFECTED_PERC"
  to_number(env.value) > 50
}

# Production experiments must not run longer than 60 seconds
deny[sprintf("Production experiment duration %ss exceeds 60s limit", [duration])] {
  input.metadata.labels.environment == "production"
  env := input.spec.experiments[_].spec.components.env[_]
  env.name == "TOTAL_CHAOS_DURATION"
  duration := to_number(env.value)
  duration > 60
}

# All experiments must have at least one probe
deny["Chaos experiment missing required probe — abort conditions undefined"] {
  count(input.spec.experiments[_].spec.probe) == 0
}
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI scopes blast radius and designs abort mechanisms |
| Target | L2 | AI generates ChaosGuard policies and abort configurations |

### Harness AI Agent

**Agent**: Harness AI Reliability Agent
**Capabilities**:
- Blast radius scoping based on service topology
- ChaosGuard policy generation
- Abort mechanism design and configuration

### Human Gates

- Blast radius approval
- Abort threshold review
- Production chaos scope approval

### MCP

- Harness ChaosGuard

---

## Success Criteria
- [ ] Label selector verified against real pod list before experiment
- [ ] Namespace-scoped RBAC (not ClusterAdmin) for chaos service account
- [ ] PodDisruptionBudget protecting minimum pod count
- [ ] At least one Continuous probe with `stopOnFailure: true`
- [ ] Blast radius expansion matrix followed (dev → staging → preprod → prod)
- [ ] Safety runbook documented and accessible during run
- [ ] OPA policy blocking oversized experiments in production

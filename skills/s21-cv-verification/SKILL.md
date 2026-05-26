---
name: harness-cv-verification
description: >
  Configure Harness Continuous Verification (CV) to automatically validate deployments
  using real-time observability data. Use this skill whenever the user mentions continuous
  verification, canary analysis, deployment health, SLO, SLI, metric thresholds, log
  anomaly detection, monitored services, health sources, verification steps in pipelines,
  or wants to automatically roll back deployments based on metrics. Also trigger when the
  user asks how to detect regressions introduced by a deployment.
---

# Harness Continuous Verification (CV)

## Purpose
Configure automated deployment validation that compares post-deployment metrics against pre-deployment baselines, triggering automatic rollback when regressions are detected.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Pipeline YAML | s04 (workflow_context.artifacts) | Yes |
| Service definitions | s05 output | Yes |
| Steady state baseline metrics | s15 output | Yes |
| Observability tool config | s20 output or user | Yes |
| SLO targets from PRD | s01 context | No |
| Sensitivity preference | s02 taste (risk_tolerance) | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Monitored service YAML | `.commandcode/artifacts/monitored-service-<name>.yaml` | YAML |
| Verify step config | s04 (pipeline update) | YAML |
| SLO definition | `.commandcode/artifacts/slo-<name>.yaml` | YAML |
| CV test results | s24 (resilience scoring), s25 (postmortem) | JSON |
| Verification strategy doc | s18 (game day context) | Markdown |

---

## Prerequisites
- [ ] Observability tool configured: Prometheus, Datadog, New Relic, AppDynamics, Splunk, Dynatrace
- [ ] Connector to observability tool created in Harness
- [ ] Service already onboarded (see harness/02-service-onboarding)
- [ ] Baseline metrics identified (error rate, latency p99, throughput)

---

## CV Architecture

```
Deploy Stage
    │
    ├── Rolling/Canary Deploy (new version)
    │
    └── Verify Step ──────────────────────────────────────────────────
              │                                                        │
              │  Compares                                              │
              ├── Post-deploy metrics (canary/new) ──► Harness ML    │
              └── Pre-deploy baseline (primary/old) ──► Analysis     │
                                                         │            │
                                                    Pass │  Fail      │
                                                         │    │       │
                                                    Continue  Rollback│
```

---

## Step 1 — Create Monitored Service

```yaml
monitoredService:
  name: <SERVICE_NAME>-<ENV>
  identifier: <service_identifier>_<env>
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  type: Application
  spec:
    serviceRef: <service_identifier>
    environmentRef: <env_identifier>
    sources:
      healthSources:
        - name: Prometheus Health
          identifier: prometheus_health
          type: Prometheus
          spec:
            connectorRef: prometheus_connector
            metricDefinitions:
              - identifier: error_rate
                metricName: Error Rate
                query: |
                  sum(rate(http_requests_total{
                    service="<SERVICE_NAME>",
                    status=~"5.."
                  }[5m])) /
                  sum(rate(http_requests_total{
                    service="<SERVICE_NAME>"
                  }[5m]))
                groupName: Performance
                analysis:
                  riskProfile:
                    riskCategory: Errors
                    thresholdTypes: [ACT_WHEN_HIGHER]
                  deploymentVerification:
                    serviceInstanceFieldName: pod
                    serviceInstanceMetricPath: label_values(pod)
              - identifier: p99_latency
                metricName: P99 Latency (ms)
                query: |
                  histogram_quantile(0.99,
                    rate(http_request_duration_ms_bucket{
                      service="<SERVICE_NAME>"
                    }[5m])
                  )
                groupName: Performance
                analysis:
                  riskProfile:
                    riskCategory: Performance/Throughput
                    thresholdTypes: [ACT_WHEN_HIGHER]
      changeSourceSpec:
        changeSourceList:
          - name: Harness CD
            identifier: harness_cd
            type: HarnessCD
            enabled: true
```

---

## Step 2 — Add Verify Step to Pipeline

```yaml
- step:
    name: Verify Deployment
    identifier: verify_deployment
    type: Verify
    timeout: 2h
    spec:
      isMultiServicesOrEnvs: false
      type: Canary         # Canary | Rolling | BlueGreen | LoadTest
      monitoredServiceRef: <service_identifier>_<env>
      healthSources:
        - prometheus_health
      analysisType: CANARY   # ML-based comparison
      duration: 15m          # How long to analyze
      sensitivity: MEDIUM    # LOW | MEDIUM | HIGH
      deploymentTag: <+artifact.tag>
      spec:
        deploymentVerificationJobInstanceIdentifier: <+INFRA_KEY>
    failureStrategies:
      - onFailure:
          errors:
            - Verification
          action:
            type: StageRollback    # Automatic rollback on verification failure
```

---

## Step 3 — SLO Configuration

Define Service Level Objectives to track deployment health over time:

```yaml
slo:
  name: <SERVICE_NAME> Availability SLO
  identifier: <service_identifier>_availability_slo
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  monitoredServiceRef: <service_identifier>_production
  tags:
    managed-by: hcprm
  spec:
    type: Simple
    serviceLevelIndicatorType: Availability
    serviceLevelIndicators:
      - name: Availability SLI
        identifier: availability_sli
        type: Ratio
        spec:
          eventType: Good
          metric1: good_requests_count       # HTTP 2xx/3xx
          metric2: total_requests_count      # all HTTP requests
    target:
      type: Rolling
      spec:
        periodLengthDays: 30
    sloTarget:
      type: Calender
      spec:
        type: Monthly
        spec:
          dayOfMonth: 1
    target:
      sloTargetPercentage: 99.9   # 99.9% availability target
    notificationRuleRefs:
      - notificationRuleRef: slo_burn_alert
        enabled: true
```

---

## Sensitivity Guide

| Sensitivity | Triggers Rollback When | Use For |
|---|---|---|
| `HIGH` | Any metric deviation | Critical payment / auth services |
| `MEDIUM` | Statistically significant deviation | Standard production services |
| `LOW` | Large, clear regression only | Experimental / non-critical services |

---

## Verification Strategy by Deploy Type

| Deploy Strategy | CV Type | Analysis Method |
|---|---|---|
| Canary | `Canary` | Canary pod metrics vs primary pod metrics |
| Rolling | `Rolling` | Post-deploy metrics vs pre-deploy baseline |
| Blue-Green | `BlueGreen` | Green metrics vs blue metrics before cutover |
| Load test | `LoadTest` | Metrics during load test vs SLO thresholds |

---

## Success Criteria
- [ ] Monitored service connected to observability backend
- [ ] At minimum 2 metrics: error rate + p99 latency
- [ ] Verify step added after deploy step in pipeline
- [ ] Rollback on verification failure configured
- [ ] SLO defined with target percentage
- [ ] Burn rate alerts configured
- [ ] CV tested by deploying a known-bad version (should trigger rollback)

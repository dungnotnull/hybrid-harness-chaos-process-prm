---
name: chaos-observability-integration
description: >
  Configure dashboards, metrics, alerts, and probes specifically for chaos engineering
  observability. Use this skill whenever the user says "set up chaos monitoring",
  "chaos dashboards", "chaos metrics", "configure probes for chaos", "integrate
  observability with experiments", or needs to ensure all chaos experiments have
  proper visibility. Also trigger before any game day (s18) to verify observability
  is fully functional.
---

# Chaos Observability Integration (s20)

## Purpose
Establish comprehensive observability for chaos experiments — ensuring every fault is visible, every probe is connected to real metrics, and every team member can see what's happening in real-time during chaos runs.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Steady state metrics definitions | s15 output | Yes |
| Experiment manifests (probe configs) | s12-s17 outputs | Yes |
| Observability tool preferences | s02 taste (observability) | Yes |
| Alert routing preferences | s02 taste or s01 | Yes |
| CV verification config | s19 output | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Chaos Grafana dashboard JSON | `.commandcode/artifacts/dashboard-chaos.json` | JSON |
| Prometheus alert rules for chaos | `.commandcode/artifacts/alerts-chaos.yaml` | YAML |
| Observability health check script | `.commandcode/artifacts/obs-check.sh` | Bash |
| Probe validation report | s18 (game day) | Markdown |
| Chaos metrics feed | s21 (alerting), s24 (scoring) | Prometheus queries |

---

## Chaos Observability Stack

```
Experiment Runner (LitmusChaos/HCE)
    │  Exposes chaos metrics on :8080/metrics
    ▼
Prometheus (scrapes every 15s)
    │
    ├── Grafana Dashboard (real-time chaos view)
    ├── AlertManager (chaos-specific alert rules)
    └── S24 Scoring Engine (resilience calculation)
```

---

## Step 1 — Chaos Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Chaos Engineering — <SERVICE>",
    "uid": "chaos-<service>",
    "tags": ["chaos", "resilience", "<service>"],
    "timezone": "browser",
    "panels": [
      {
        "title": "Chaos Experiment Status",
        "type": "stat",
        "targets": [{
          "expr": "litmuschaos_experiment_verdict{app='<SERVICE>'}",
          "legendFormat": "{{experiment_name}}"
        }],
        "fieldConfig": {
          "defaults": {
            "mappings": [
              {"type": "value", "value": "0", "text": "Passed"},
              {"type": "value", "value": "1", "text": "Failed"}
            ],
            "thresholds": {
              "mode": "absolute",
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 1}
              ]
            }
          }
        }
      },
      {
        "title": "Resilience Score (Real-time)",
        "type": "gauge",
        "targets": [{
          "expr": "litmuschaos_resilience_score{app='<SERVICE>'}"
        }],
        "fieldConfig": {
          "defaults": {
            "min": 0, "max": 100,
            "thresholds": {
              "steps": [
                {"color": "red", "value": null},
                {"color": "yellow", "value": 60},
                {"color": "green", "value": 80}
              ]
            }
          }
        }
      },
      {
        "title": "Error Rate During Chaos",
        "type": "timeseries",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{namespace='<NAMESPACE>',status=~'5..'}[1m])) / sum(rate(http_requests_total{namespace='<NAMESPACE>'}[1m])) * 100",
            "legendFormat": "Error Rate %"
          },
          {
            "expr": "5",
            "legendFormat": "Threshold (5%)"
          }
        ],
        "fieldConfig": {
          "defaults": {
            "thresholds": {
              "steps": [
                {"color": "green", "value": null},
                {"color": "red", "value": 5}
              ]
            }
          }
        }
      },
      {
        "title": "P99 Latency During Chaos",
        "type": "timeseries",
        "targets": [{
          "expr": "histogram_quantile(0.99, sum(rate(http_request_duration_ms_bucket{namespace='<NAMESPACE>'}[1m])) by (le))",
          "legendFormat": "P99 (ms)"
        }]
      },
      {
        "title": "Pod Status During Chaos",
        "type": "stat",
        "targets": [
          {
            "expr": "count(kube_pod_status_ready{namespace='<NAMESPACE>', condition='true'})",
            "legendFormat": "Ready"
          },
          {
            "expr": "count(kube_pod_status_ready{namespace='<NAMESPACE>', condition='false'})",
            "legendFormat": "Not Ready"
          }
        ]
      },
      {
        "title": "Active Faults",
        "type": "table",
        "targets": [{
          "expr": "litmuschaos_active_experiments{namespace='<NAMESPACE>'}",
          "format": "table"
        }]
      },
      {
        "title": "Probe Status",
        "type": "status-history",
        "targets": [{
          "expr": "litmuschaos_probe_success_total{namespace='<NAMESPACE>'}",
          "legendFormat": "{{probe_name}}"
        }]
      }
    ]
  }
}
```

### Import Dashboard
```bash
curl -X POST http://grafana.company.com/api/dashboards/db \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <GRAFANA_API_KEY>" \
  -d @.commandcode/artifacts/dashboard-chaos.json
```

---

## Step 2 — Chaos-Specific Prometheus Alert Rules

```yaml
groups:
  - name: chaos_engineering_alerts
    rules:
      - alert: ChaosProbeFailure
        expr: litmuschaos_probe_success_total == 0
        for: 30s
        labels:
          severity: critical
          context: chaos
        annotations:
          summary: "Chaos probe {{ $labels.probe_name }} failed"
          description: >
            Probe {{ $labels.probe_name }} for experiment
            {{ $labels.experiment_name }} has failed.
            The experiment may have been aborted automatically.
          runbook_url: "https://wiki.company.com/chaos/probe-failure"

      - alert: ChaosExperimentRunningTooLong
        expr: time() - litmuschaos_experiment_start_time_seconds > 600
        for: 1m
        labels:
          severity: warning
          context: chaos
        annotations:
          summary: "Chaos experiment running > 10 minutes"
          description: >
            Experiment {{ $labels.experiment_name }} has been running
            for over 10 minutes. Expected duration was shorter.
            Consider aborting if this is unexpected.

      - alert: ChaosErrorRateThresholdExceeded
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[1m])) /
          sum(rate(http_requests_total[1m])) * 100 > 5
        for: 30s
        labels:
          severity: critical
          context: chaos
        annotations:
          summary: "Error rate exceeded 5% during chaos experiment"
          description: >
            Error rate is {{ $value }}% which exceeds the 5% chaos threshold.
            Experiments should be aborted immediately.

      - alert: ChaosNoObservability
        expr: absent(litmuschaos_experiment_verdict)
        for: 2m
        labels:
          severity: critical
          context: chaos
        annotations:
          summary: "Chaos observability metrics are missing"
          description: >
            LitmusChaos metrics are not being scraped by Prometheus.
            No chaos experiments should run without observability.

      - alert: ChaosResilienceScoreBelowThreshold
        expr: litmuschaos_resilience_score < 60
        for: 1m
        labels:
          severity: warning
          context: chaos
        annotations:
          summary: "Resilience score below 60 — system is fragile"
          description: >
            Service {{ $labels.service }} resilience score is {{ $value }}.
            Do not promote to production until score ≥ 80.
```

---

## Step 3 — Observability Health Check

Run before any chaos experiment:

```bash
#!/bin/bash
# obs-health-check.sh — verify observability before chaos
set -euo pipefail

PROMETHEUS="http://prometheus.monitoring.svc.cluster.local:9090"
GRAFANA="http://grafana.company.com"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Observability Health Check"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Prometheus is reachable
if curl -sf "$PROMETHEUS/-/healthy" > /dev/null; then
  echo "✅ Prometheus: healthy"
else
  echo "❌ Prometheus: unreachable — ABORT"
  exit 1
fi

# 2. Chaos metrics are being scraped
if curl -sg "$PROMETHEUS/api/v1/query" \
  --data-urlencode 'query=litmuschaos_experiment_verdict' \
  | jq -e '.data.result | length > 0' > /dev/null; then
  echo "✅ Chaos metrics: being scraped"
else
  echo "⚠️  Chaos metrics: not detected — has LitmusChaos been installed?"
fi

# 3. Target service metrics available
SERVICE="${1:?Usage: $0 <service> <namespace>}"
NAMESPACE="${2:?}"

ERROR_QUERY=$(curl -sg "$PROMETHEUS/api/v1/query" \
  --data-urlencode "query=sum(rate(http_requests_total{namespace=\"$NAMESPACE\"}[1m]))" \
  | jq '.data.result | length')

if [ "$ERROR_QUERY" -gt 0 ]; then
  echo "✅ Service metrics: available for $SERVICE/$NAMESPACE"
else
  echo "❌ Service metrics: not found — is the service deployed?"
  exit 1
fi

# 4. Grafana dashboard accessible
DASHBOARD_UID="chaos-${SERVICE}"
if curl -sf "$GRAFANA/api/dashboards/uid/$DASHBOARD_UID" \
  -H "Authorization: Bearer ${GRAFANA_API_KEY}" > /dev/null; then
  echo "✅ Grafana dashboard: chaos-$SERVICE exists"
else
  echo "⚠️  Grafana dashboard: not found — create before game day"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Observability ready for chaos"
```

---

## Step 4 — LitmusChaos Metrics Scrape Config

```yaml
# prometheus-scrape-config.yaml
scrape_configs:
  - job_name: 'litmuschaos'
    scrape_interval: 15s
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: [litmus, <TARGET_NAMESPACE>]
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: chaos-(runner|exporter|operator)
        action: keep
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        regex: 'true'
        action: keep
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

---

## Success Criteria
- [ ] Chaos Grafana dashboard created with all 7 panels
- [ ] Prometheus scraping LitmusChaos metrics every 15s
- [ ] Alert rules configured for probe failure, error rate, and missing observability
- [ ] Observability health check script passes before any experiment
- [ ] Dashboard visible to all game day participants
- [ ] Alert routing verified (test alert fired and received)
- [ ] Metrics gap < 5% (continuous monitoring throughout experiment)

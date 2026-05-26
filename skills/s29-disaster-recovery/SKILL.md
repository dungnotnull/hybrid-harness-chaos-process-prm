---
name: disaster-recovery-business-continuity
description: >
  Define, implement, test, and validate disaster recovery and business continuity
  plans. Use this skill whenever the user says "disaster recovery", "DR plan",
  "business continuity", "BCP", "RTO/RPO", "backup strategy", "failover test",
  "multi-region", "cross-region restore", "data recovery", or needs to ensure
  the system can survive catastrophic failures. This skill extends chaos engineering
  from component-level faults to full-region and full-provider failure scenarios.
  Also trigger after resilience scoring (s26) identifies DR gaps.
---

# Disaster Recovery & Business Continuity (s29)

## Purpose
Move beyond component-level chaos into organization-level disaster resilience — defining RTO/RPO targets, implementing backup and restore procedures, orchestrating multi-region failover, and validating that the business can survive the worst-case scenario.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Infrastructure topology (regions, AZs, providers) | s01, s05 | Yes |
| Critical service inventory with dependencies | s01 (PRD component inventory) | Yes |
| Resilience scores (all services) | s26 output | Yes |
| Chaos experiment results (identifies single points of failure) | s14-s21 outputs | Yes |
| Backup infrastructure details | s05 (infra definitions) | Yes |
| RTO/RPO targets (business requirements) | s01 (PRD — NFR constraints) | Yes |
| Compliance requirements | s30 (audit/compliance) | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| DR plan document | `.commandcode/artifacts/dr/dr-plan.md` | Markdown |
| RTO/RPO matrix per service | `.commandcode/artifacts/dr/rto-rpo-matrix.yaml` | YAML |
| Failover runbook | `.commandcode/artifacts/dr/failover-runbook.md` | Markdown |
| Backup configuration | `.commandcode/artifacts/dr/backup-config.yaml` | YAML |
| DR test schedule | `.commandcode/artifacts/dr/dr-test-schedule.yaml` | YAML |
| DR test results | s26 (resilience score contribution) | JSON |
| Recovery scripts | `.commandcode/artifacts/dr/scripts/` | Bash/Python |
| Business impact analysis | s30 (compliance evidence) | Markdown |

---

## DR Planning Framework

```
ASSESS → DESIGN → IMPLEMENT → TEST → MAINTAIN

Assess:   Business impact analysis, RTO/RPO targets, critical path mapping
Design:   Multi-region architecture, backup strategy, failover mechanism
Implement: Backup schedules, replication, DNS failover, infrastructure automation
Test:     DR drills, tabletop exercises, full region failover
Maintain: Quarterly review, update for new services, validate backups
```

---

## Step 1 — Business Impact Analysis (BIA)

```yaml
business_impact_analysis:
  services:
    - name: payment-service
      tier: 0  # Revenue-critical — down = lost money
      max_tolerable_downtime_minutes: 5
      rto_target_minutes: 5
      rpo_target_minutes: 1    # < 1 minute of data loss
      revenue_impact_per_hour: 50000  # USD
      dependencies: [postgres, redis, payment-gateway]
      dr_strategy: active-active  # Multi-region, always serving

    - name: checkout-api
      tier: 0
      max_tolerable_downtime_minutes: 5
      rto_target_minutes: 5
      rpo_target_minutes: 1
      revenue_impact_per_hour: 50000
      dependencies: [payment-service, inventory-service]
      dr_strategy: active-active

    - name: notification-worker
      tier: 1  # Important but not revenue-blocking
      max_tolerable_downtime_minutes: 60
      rto_target_minutes: 30
      rpo_target_minutes: 15
      revenue_impact_per_hour: 5000
      dependencies: [redis]
      dr_strategy: warm-standby

    - name: analytics-service
      tier: 2  # Non-critical — internal only
      max_tolerable_downtime_minutes: 480  # 8 hours
      rto_target_minutes: 240
      rpo_target_minutes: 60
      revenue_impact_per_hour: 0
      dependencies: [data-warehouse]
      dr_strategy: backup-restore

    - name: admin-dashboard
      tier: 2
      max_tolerable_downtime_minutes: 480
      rto_target_minutes: 240
      rpo_target_minutes: 60
      revenue_impact_per_hour: 0
      dependencies: []
      dr_strategy: backup-restore
```

---

## Step 2 — RTO/RPO Matrix

| Tier | Service | RTO | RPO | Strategy | Cost |
|---|---|---|---|---|---|
| 0 | payment-service | 5 min | 1 min | Active-Active (2 regions) | $$$ |
| 0 | checkout-api | 5 min | 1 min | Active-Active (2 regions) | $$$ |
| 1 | notification-worker | 30 min | 15 min | Warm Standby | $$ |
| 1 | inventory-service | 15 min | 5 min | Pilot Light | $$ |
| 2 | analytics-service | 4 hours | 1 hour | Backup & Restore | $ |
| 2 | admin-dashboard | 4 hours | 1 hour | Backup & Restore | $ |

---

## Step 3 — DR Architecture (Multi-Region Active-Active)

```yaml
# Tier 0: Active-Active across 2 regions
architecture:
  regions:
    - name: us-east-1
      role: primary
      weight: 70               # 70% traffic
    - name: us-west-2
      role: secondary
      weight: 30               # 30% traffic

  traffic_routing:
    dns: Route53 Latency-Based Routing
    health_checks:
      - path: /health
        interval: 10s
        failure_threshold: 3
    failover_trigger:
      condition: "us-east-1 health check fails 3 consecutive times"
      action: "Route 100% traffic to us-west-2"
      time_to_detect: 30s
      time_to_failover: 60s

  data_replication:
    postgres:
      type: Cross-Region Read Replica
      primary: us-east-1
      replica: us-west-2
      replication_lag_max_ms: 100

    redis:
      type: Global Datastore (AWS ElastiCache)
      replication: async
      lag_tolerance_seconds: 5

  infrastructure:
    compute: EKS clusters in both regions (mirrored)
    ci_cd: GitOps deploys to both regions simultaneously
    secrets: Vault cluster per region with auto-unseal
    certificates: ACM in both regions
```

---

## Step 4 — Backup Configuration

```yaml
backup_config:
  databases:
    - name: postgres-payment-prod
      type: PostgreSQL RDS
      retention_days: 35
      schedule: "0 */6 * * *"   # Every 6 hours
      cross_region_copy: true
      encryption: AWS KMS CMK
      validation:
        type: restore_test
        schedule: "0 8 * * 1"   # Weekly restore test (Monday 8 AM)
        retention_days: 7

    - name: postgres-payment-prod-continuous
      type: Point-in-Time Recovery
      retention_days: 14
      recovery_window_minutes: 1

  storage:
    - name: s3-user-uploads
      type: S3 Cross-Region Replication
      source_bucket: uploads-us-east-1
      dest_bucket: uploads-us-west-2
      replication_rule: all-objects
      delete_marker_replication: true

    - name: ebs-snapshots
      type: EBS Snapshots
      retention_days: 30
      schedule: "0 2 * * *"     # Daily at 2 AM
      cross_region_copy: true

  kubernetes:
    - name: etcd-backup
      type: Velero
      schedule: "0 */4 * * *"   # Every 4 hours
      storage_location: s3://backups-us-east-1/velero/
      snapshot_location: us-east-1
      included_namespaces: [production]
      ttl: 720h                   # 30 days
```

---

## Step 5 — Failover Runbook

```markdown
# Failover Runbook — us-east-1 → us-west-2

## Triggers
Any of these automatically trigger DR protocol review:
- [ ] Route53 health check fails for us-east-1 (30s window)
- [ ] >50% of pods in us-east-1 are unhealthy
- [ ] AWS status page reports us-east-1 degradation
- [ ] PagerDuty alert: "multi-AZ failure us-east-1"
- [ ] On-call SRE declares emergency

## Phase 1: Detection (Auto — < 1 minute)
- Route53 detects us-east-1 health check failure
- PagerDuty alert fires: "Region us-east-1 degraded"
- Slack #incidents: "⚠️ DR EVENT — us-east-1 health check failing"

## Phase 2: Assessment (Manual — < 5 minutes)
- SRE on-call checks:
  - [ ] Is this a real outage or transient?
  - [ ] Has us-west-2 been tested recently?
  - [ ] Is data replication current? (check lag < 1 min)
- Decision: DECLARE FAILOVER or WAIT

## Phase 3: Failover (Semi-Auto — < 15 minutes)
```
# TERMINAL 1: SRE Lead
# Step 1: Verify us-west-2 is healthy
kubectl --context us-west-2 get nodes --no-headers | grep -c Ready
# Expected: >= 3

# Step 2: Scale up us-west-2 to handle full load
kubectl --context us-west-2 scale deployment/payment-service --replicas=8
kubectl --context us-west-2 scale deployment/checkout-api --replicas=8

# Step 3: Promote PostgreSQL read replica to primary
aws rds promote-read-replica \
  --db-instance-identifier postgres-payment-prod-us-west-2 \
  --region us-west-2

# Step 4: Failover DNS (Route53)
aws route53 update-traffic-policy-instance \
  --id <POLICY_ID> \
  --ttl 60 \
  --endpoint-type HTTP \
  --evaluate-target-health false

# Step 5: Shift traffic
# Route53 automatically routes to us-west-2 (health-based)
# Verify: dig payment.company.com → should resolve to us-west-2

# Step 6: Notify stakeholders
```

## Phase 4: Verification (< 30 minutes)
- [ ] All services healthy in us-west-2
- [ ] Error rate < 1%
- [ ] P99 latency < target
- [ ] Data integrity verified (spot-check critical records)
- [ ] Customer-facing flows working (run CloakBrowser smoke tests)

## Phase 5: Failback (< 2 hours after us-east-1 recovers)
```bash
# 1. Restore us-east-1 (if needed)
# 2. Re-establish replication (us-west-2 → us-east-1)
# 3. Scale up us-east-1
# 4. Shift 10% traffic → validate → 50% → 100%
# 5. Decommission failover resources
```

## Emergency Contacts
| Role | Name | Phone | Slack |
|---|---|---|---|
| DR Lead | @alex-sre | +1-555-0100 | @alex |
| DB Admin | @lisa-dba | +1-555-0101 | @lisa |
| Network | @mike-net | +1-555-0102 | @mike |
| CTO | @cto | +1-555-0199 | @cto |
```

---

## Step 6 — DR Testing Schedule

```yaml
dr_test_schedule:
  tabletop_exercises:
    frequency: quarterly
    duration: 2 hours
    participants: [sre_team, engineering_leads, cto]
    scenario: "Region us-east-1 is completely down. Walk through failover procedure."
    success_criteria: "All participants can describe their role and actions without referencing the runbook"

  component_failover_test:
    frequency: monthly
    scope: single_service
    example: "Failover payment-service database read replica weekly"
    is_automated: true

  full_region_failover:
    frequency: biannually
    duration: 4 hours
    scope: all_tier_0_services
    is_automated: false
    requires_approval: cto
    success_criteria:
      - "RTO achieved: < 15 minutes"
      - "RPO achieved: < 5 minutes"
      - "All customer-facing flows functional post-failover"
      - "Zero P0 incidents caused by failover process"

  chaos_dr_combined:
    frequency: quarterly
    scope: "Simulate region failure during game day (s20)"
    description: "Combine DR failover with ongoing chaos experiments in surviving region"
```

---

## Step 7 — Backup Validation

```bash
#!/bin/bash
# validate-backups.sh — Automated backup integrity check
set -euo pipefail

echo "=== Backup Validation Report — $(date) ==="

# 1. Verify latest PostgreSQL backup exists
LATEST_BACKUP=$(aws rds describe-db-snapshots \
  --db-instance-identifier postgres-payment-prod \
  --snapshot-type automated \
  --query 'reverse(sort_by(DBSnapshots,&SnapshotCreateTime))[0]' \
  --region us-east-1)

SNAPSHOT_TIME=$(echo "$LATEST_BACKUP" | jq -r '.SnapshotCreateTime')
SNAPSHOT_AGE_MINUTES=$(( ($(date +%s) - $(date -d "$SNAPSHOT_TIME" +%s)) / 60 ))

echo "📦 Latest PostgreSQL backup: $SNAPSHOT_TIME (age: ${SNAPSHOT_AGE_MINUTES}min)"

if [ "$SNAPSHOT_AGE_MINUTES" -gt 360 ]; then   # Older than 6 hours
  echo "❌ BACKUP STALE — Last backup > 6 hours old"
  exit 1
fi
echo "✅ Backup age OK"

# 2. Test restore (create temporary instance from latest backup)
echo "🔄 Testing restore..."
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier postgres-payment-restore-test \
  --db-snapshot-identifier "$(echo "$LATEST_BACKUP" | jq -r '.DBSnapshotIdentifier')" \
  --db-instance-class db.t3.medium \
  --region us-east-1

# Wait for restore to complete
aws rds wait db-instance-available \
  --db-instance-identifier postgres-payment-restore-test \
  --region us-east-1

# Verify data integrity
ENDPOINT=$(aws rds describe-db-instances \
  --db-instance-identifier postgres-payment-restore-test \
  --query 'DBInstances[0].Endpoint.Address' \
  --region us-east-1 \
  --output text)

ROW_COUNT=$(psql -h "$ENDPOINT" -U admin -d payments -tAc \
  "SELECT COUNT(*) FROM transactions WHERE created_at > NOW() - INTERVAL '24 hours'")

echo "📊 Recent transaction rows: $ROW_COUNT"

if [ "$ROW_COUNT" -lt 100 ]; then
  echo "⚠️  Low row count — possible data integrity issue"
fi

# Cleanup
aws rds delete-db-instance \
  --db-instance-identifier postgres-payment-restore-test \
  --skip-final-snapshot \
  --region us-east-1

echo "✅ Backup validation complete"
```

---

## DR Maturity Model

| Level | Name | Characteristics |
|---|---|---|
| 0 | None | No DR plan, no backups, hope-based resilience |
| 1 | Backup Only | Backups exist, never tested, RTO measured in days |
| 2 | Documented | DR plan exists, manual failover, tested annually |
| 3 | Automated | Scripted failover, quarterly testing, RTO < 1 hour |
| 4 | Active-Active | Multi-region serving, automated failover, RTO < 5 min |
| 5 | Chaos-Verified | DR tested under live chaos, continuous validation |

---

## Success Criteria
- [ ] Business impact analysis completed for all services
- [ ] RTO/RPO targets defined and documented per service tier
- [ ] DR architecture diagram documented (multi-region for Tier 0)
- [ ] Backup configuration validated with restore test
- [ ] Failover runbook written and accessible to all SREs
- [ ] Tabletop exercise completed this quarter
- [ ] Full region failover tested within last 6 months
- [ ] Backup validation automated (weekly restore test)
- [ ] DR maturity score ≥ 3 for Tier 0 services
- [ ] DR test results feed into resilience scoring (s26)

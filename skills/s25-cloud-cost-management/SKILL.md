---
name: harness-cloud-cost
description: >
  Analyze, optimize, and govern cloud infrastructure costs using Harness Cloud Cost
  Management (CCM). Use this skill whenever the user mentions cloud costs, AWS/GCP/Azure
  billing, idle resources, cost optimization, budget alerts, cost anomalies, AutoStopping,
  rightsizing recommendations, Kubernetes cost allocation, cost governance rules,
  show-back/charge-back, or FinOps practices. Also trigger when the user wants to
  reduce infrastructure spend or attribute costs to specific teams or services.
---

# Harness Cloud Cost Management (CCM)

## Purpose
Provide full visibility into cloud spend, enforce cost budgets via governance policies, identify and eliminate waste, and attribute costs to engineering teams for accountability.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Service definitions and environments | s05 (workflow_context.artifacts) | Yes |
| Cloud provider accounts | s01 or user | Yes |
| Budget thresholds | s01 PRD or user | No |
| Team cost allocation labels | s05 (service tags/teams) | Yes |
| FinOps review schedule | s02 taste or user | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Cloud connector YAML | `.commandcode/artifacts/ccm-connector.yaml` | YAML |
| Budget configuration | `.commandcode/artifacts/budget.yaml` | YAML |
| Perspective (cost view) definitions | `.commandcode/artifacts/perspectives.yaml` | YAML |
| AutoStopping rules | `.commandcode/artifacts/autostop-rules.yaml` | YAML |
| Cost governance OPA policies | s22 (policy set) | Rego |
| Monthly FinOps report template | s24 (resilience context) | Markdown |

---

## Prerequisites
- [ ] Harness CCM module enabled
- [ ] Cloud provider connector(s) created with billing data access
- [ ] Kubernetes cluster connected with CCM enabled
- [ ] Budget thresholds and alerting channels defined

---

## CCM Architecture

```
Cloud Providers (AWS/GCP/Azure)
    │  Billing exports → S3 / BigQuery / Storage Account
    ▼
Harness CCM Connector
    │  Ingests cost data every 24h
    ▼
Harness CCM Platform
    ├── Cost Explorer (visualization)
    ├── Budget Alerts (threshold notifications)
    ├── Anomaly Detection (ML-based spike detection)
    ├── AutoStopping (idle resource termination)
    ├── Recommendations (rightsizing)
    └── Cost Governance (OPA-based spend rules)
```

---

## Step 1 — Cloud Connectors

### AWS Connector (Cost & Usage Report)
```yaml
connector:
  name: AWS Production Account
  identifier: aws_prod
  type: CEAws
  spec:
    awsAccountId: "<AWS_ACCOUNT_ID>"
    curReportName: harness-cost-report
    s3BucketDetails:
      region: us-east-1
      s3BucketName: company-billing-exports
      s3Prefix: harness/
    crossAccountAccess:
      crossAccountRoleArn: arn:aws:iam::<ACCOUNT>:role/HarnessCCMRole
      externalId: harness-<ACCOUNT_ID>
    features:
      - BILLING
      - OPTIMIZATION      # for AutoStopping and recommendations
      - GOVERNANCE
```

**Required IAM Policy for CCM Role**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ce:*",
        "s3:GetObject",
        "s3:ListBucket",
        "organizations:Describe*",
        "organizations:List*",
        "cur:DescribeReportDefinitions"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "ec2:StopInstances",
        "ec2:StartInstances",
        "rds:Describe*",
        "rds:StopDBInstance",
        "rds:StartDBInstance",
        "ecs:List*",
        "ecs:Describe*",
        "ecs:UpdateService"
      ],
      "Resource": "*"
    }
  ]
}
```

### Kubernetes Connector for CCM
```yaml
connector:
  name: Production K8s CCM
  identifier: prod_k8s_ccm
  type: K8sCluster
  spec:
    credential:
      type: InheritFromDelegate
    delegateSelectors: [prod-delegate]
  ccmEnabled: true    # Enable node/pod cost allocation
```

---

## Step 2 — Budget Configuration

```yaml
budget:
  name: Engineering Q3 2025 Budget
  identifier: engineering_q3_2025
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  type: SPECIFIED_AMOUNT
  budgetAmount: 50000.00   # USD per month
  period: MONTHLY
  startTime: "2025-07-01T00:00:00Z"
  scope:
    type: PERSPECTIVE
    perspectiveId: <PERSPECTIVE_ID>
  alertThresholds:
    - perspective: 50         # Alert at 50% of budget
      basedOn: ACTUAL_COST
      emailAddresses: [sre-team@company.com]
      userGroupIds: [account.SRE_Team]
    - perspective: 80         # Alert at 80%
      basedOn: ACTUAL_COST
      emailAddresses: [engineering-leads@company.com, cto@company.com]
    - perspective: 90         # Alert at 90% — escalate
      basedOn: FORECASTED_COST
      emailAddresses: [cto@company.com, cfo@company.com]
    - perspective: 100        # Alert at limit
      basedOn: ACTUAL_COST
      emailAddresses: [cto@company.com, cfo@company.com]
      slackWebhooks: [<SLACK_WEBHOOK>]
```

---

## Step 3 — Perspectives (Cost Views)

Perspectives slice cost data by team, service, environment, or label:

```yaml
perspective:
  name: Payments Team Costs
  identifier: payments_team_costs
  viewRules:
    - viewConditions:
        - type: VIEW_ID_CONDITION
          viewField:
            fieldId: labels.team
            fieldName: team
            identifier: LABEL
          viewOperator: IN
          values: [payments, checkout, billing]
  viewVisualization:
    granularity: DAY
    groupBy:
      fieldId: labels.service
      fieldName: service
      identifier: LABEL
  viewTimeRange:
    viewTimeRangeType: LAST_30
```

---

## Step 4 — AutoStopping Rules (Eliminate Idle Waste)

AutoStopping automatically shuts down non-production resources when idle:

```yaml
autoStoppingRule:
  name: Dev EC2 AutoStop
  identifier: dev_ec2_autostop
  cloud: AWS
  idleTimeMinutes: 30           # Shut down after 30 min idle
  dryRun: false
  target:
    type: EC2
    filters:
      - tag:
          key: environment
          value: dev
      - tag:
          key: autostop
          value: "enabled"
  schedule:
    # Force-stop on weekends regardless of traffic
    cron: "0 20 * * 5"          # Friday 20:00 UTC
    startSchedule: "0 8 * * 1"  # Monday 08:00 UTC
  detection:
    type: HTTP
    healthcheck:
      url: http://<EC2_IP>:8080/health
      timeout: 30
```

**Estimated savings**: Typically 60-70% reduction on dev/staging EC2 costs.

---

## Step 5 — Rightsizing Recommendations

Pull current recommendations via API and format for engineering teams:

```bash
# Fetch recommendations
curl -X GET \
  "https://app.harness.io/ccm/api/recommendation/overview?accountIdentifier=<ACCOUNT>&minSaving=50" \
  -H "x-api-key: <API_KEY>" \
  | jq '.data[] | {
      resourceName: .resourceName,
      resourceType: .resourceType,
      currentCostMonthly: .currentResourceCost,
      recommendedCostMonthly: .recommendedResourceCost,
      monthlySaving: .monthlySaving,
      recommendation: .recommendationDetails
    }'
```

**Act on recommendations**:
```
Priority 1: Savings > $500/month  → Implement within sprint
Priority 2: Savings $100-500/month → Implement within quarter
Priority 3: Savings < $100/month   → Batch and implement monthly
```

---

## Step 6 — Cost Governance Rules

Prevent cost violations before they happen using OPA:

```rego
package cost_governance

# Block creation of large instance types without approval tag
deny[sprintf("Instance type '%s' requires 'cost-approved: true' tag", [instance_type])] {
  input.resource.type == "aws_instance"
  instance_type := input.resource.instance_type
  large_instances := {"m5.4xlarge", "m5.8xlarge", "m5.16xlarge",
                      "c5.4xlarge", "c5.9xlarge", "r5.4xlarge"}
  large_instances[instance_type]
  not input.resource.tags["cost-approved"] == "true"
}

# Warn on untagged resources
warn["Resource missing 'team' tag — will be unallocated in cost reports"] {
  not input.resource.tags.team
}

# Block storage volumes > 1TB without justification
deny[sprintf("EBS volume size %dGB exceeds 1024GB limit without 'large-storage-reason' tag",
             [input.resource.size])] {
  input.resource.type == "aws_ebs_volume"
  input.resource.size > 1024
  not input.resource.tags["large-storage-reason"]
}
```

---

## Cost Attribution Labels (Kubernetes)

Every Kubernetes workload must have these labels for cost allocation:

```yaml
metadata:
  labels:
    team: payments           # Engineering team
    service: checkout-api    # Service name
    environment: production  # Environment tier
    cost-center: "CC-4521"   # Finance cost center
    managed-by: hcprm
```

Enforce via OPA admission webhook or Harness policy on pipeline output.

---

## Monthly FinOps Review Template

```markdown
## Cloud Cost Report — <MONTH> <YEAR>

### Summary
| Metric | Value |
|---|---|
| Total Spend | $<TOTAL> |
| vs Budget | <+X%/-X%> |
| vs Last Month | <+X%/-X%> |
| Forecasted EOM | $<FORECAST> |

### Top Cost Drivers
1. <SERVICE_1>: $<COST> (<CHANGE>% MoM)
2. <SERVICE_2>: $<COST>
3. <SERVICE_3>: $<COST>

### Savings Realized
- AutoStopping: $<SAVINGS>/month
- Rightsizing implemented: $<SAVINGS>/month
- Reserved instances: $<SAVINGS>/month

### Action Items
- [ ] <TEAM>: Implement rightsizing for <RESOURCE> — est. $<SAVING>/month
- [ ] <TEAM>: Enable AutoStopping on <ENVIRONMENT> — est. $<SAVING>/month
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI recommends cost savings and creates dashboards |
| Target | L3 | AI auto-optimizes cloud spend within budget bounds |

### Harness AI Agent

**Agent**: Harness AI FinOps Agent
**Capabilities**:
- Smart cloud cost savings recommendations
- Dashboard creation via natural language
- Commitment analysis
- K8s cluster spend optimization
- Cost asset policy auto-generation

### Human Gates

- Budget approval
- Cost anomaly investigation
- Commitment purchase approval

---

## Success Criteria
- [ ] All cloud accounts connected with billing data ingesting
- [ ] Budget alerts configured at 50/80/90/100% thresholds
- [ ] AutoStopping rules active on dev/staging (30-min idle timeout)
- [ ] Rightsizing recommendations reviewed monthly
- [ ] All K8s workloads have `team`, `service`, `environment` labels
- [ ] Monthly FinOps review scheduled with engineering leads
- [ ] Savings dashboard visible to engineering and finance teams

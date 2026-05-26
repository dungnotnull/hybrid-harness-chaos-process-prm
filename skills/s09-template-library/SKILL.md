---
name: harness-template-library
description: >
  Create, version, and govern reusable Harness templates (pipeline templates, stage
  templates, step templates, step group templates) to enforce standards across teams.
  Use this skill whenever the user mentions Harness templates, reusable stages, shared
  step groups, template library, template versioning, template enforcement, or when
  multiple teams need to follow the same pipeline pattern. Also trigger when a user wants
  to "templatize" an existing pipeline or reduce copy-paste across team pipelines.
---

# Harness Template Library

## Purpose
Build a governed library of reusable pipeline building blocks that enforce engineering standards, eliminate copy-paste drift, and allow teams to compose pipelines from pre-approved, versioned templates.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Pipeline design patterns | s04 output | Yes |
| Security scan requirements | s01 PRD or user | No |
| Approval gate requirements | s01 (compliance needs) | Yes |
| Notification preferences | s02 taste (communication) | No |
| Service team structures | s05 output | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Deploy stage template | `.commandcode/artifacts/template-deploy.yaml` | YAML |
| Security scan step group template | `.commandcode/artifacts/template-security.yaml` | YAML |
| Approval stage template | `.commandcode/artifacts/template-approval.yaml` | YAML |
| Notification step group template | `.commandcode/artifacts/template-notify.yaml` | YAML |
| Template enforcement OPA policy | s22 (governance) | Rego |
| Template version changelog | `.commandcode/artifacts/template-changelog.md` | Markdown |

---

## Prerequisites
- [ ] Harness account with Template Library access
- [ ] Engineering standards documented (what must be identical across all pipelines)
- [ ] RBAC roles defined (who can create/modify templates vs use them)

---

## Template Hierarchy

```
Account-level templates   → Shared across ALL orgs and projects
    └── Org-level templates       → Shared across all projects in org
            └── Project-level templates    → Used within one project

Template Types:
├── Pipeline Template      → Entire pipeline as a template
├── Stage Template         → One stage (CI, CD, Approval, etc.)
├── Step Template          → One step (Run, ShellScript, etc.)
└── Step Group Template    → A group of steps as a unit
```

---

## Template Versioning Strategy

```
<template-identifier>
├── v1 — Stable (in use by 20+ pipelines)
├── v2 — Stable (new default)
└── v3 — Beta (testing phase)

Versioning rules:
- Patch (1.0 → 1.1): Non-breaking — add optional fields, fix bugs
- Minor (1.x → 2.0): Breaking — remove fields, change required inputs
- Always keep v_previous stable for 30 days after new version release
- Deprecation: set isStable: false, add deprecation notice in description
```

---

## Essential Template Catalog

### Template 1 — Standard Deploy Stage

```yaml
template:
  name: Standard K8s Deploy Stage
  identifier: standard_k8s_deploy_stage
  versionLabel: "2.0"
  type: Stage
  orgIdentifier: <ORG_ID>
  tags:
    managed-by: hcprm
    template-type: deploy
  spec:
    type: Deployment
    spec:
      deploymentType: Kubernetes
      service:
        serviceRef: <+input>
        serviceInputs: <+input>
      environment:
        environmentRef: <+input>
        infrastructureDefinitions: <+input>
      execution:
        steps:
          - step:
              name: Pre-Deploy Health Check
              identifier: pre_deploy_health_check
              type: ShellScript
              spec:
                shell: Bash
                source:
                  type: Inline
                  spec:
                    script: |
                      echo "Pre-deploy health check for env: <+env.name>"
                      kubectl get nodes --no-headers | awk '{print $2}' | grep -v Ready && \
                        echo "WARNING: unhealthy nodes detected" || echo "All nodes Ready"
                onDelegate: true
          - step:
              name: Deploy
              identifier: deploy
              type: K8sRollingDeploy
              spec:
                skipDryRun: false
                pruningEnabled: true
          - step:
              name: Verify Deployment
              identifier: verify_deployment
              type: Verify
              timeout: 30m
              spec:
                isMultiServicesOrEnvs: false
                type: Rolling
                monitoredServiceRef: <+input>
                sensitivity: MEDIUM
                duration: 10m
                failOnNoAnalysis: true
        rollbackSteps:
          - step:
              name: Rollback
              identifier: rollback
              type: K8sRollingRollback
              spec: {}
          - step:
              name: Notify Rollback
              identifier: notify_rollback
              type: ShellScript
              spec:
                shell: Bash
                source:
                  type: Inline
                  spec:
                    script: |
                      curl -X POST "<+pipeline.variables.slackWebhook>" \
                        -H "Content-Type: application/json" \
                        -d '{"text": "🔴 ROLLBACK: <+service.name> in <+env.name>"}'
                onDelegate: true
```

### Template 2 — Security Scan Step Group

```yaml
template:
  name: Security Scan Step Group
  identifier: security_scan_step_group
  versionLabel: "1.2"
  type: StepGroup
  orgIdentifier: <ORG_ID>
  description: "SAST + container scan + secrets scan — required for all CI pipelines"
  tags:
    managed-by: hcprm
    compliance: required
  spec:
    steps:
      - step:
          name: SAST Scan (Semgrep)
          identifier: sast_semgrep
          type: Run
          spec:
            connectorRef: account.dockerhub
            image: returntocorp/semgrep:latest
            command: |
              semgrep \
                --config=p/owasp-top-ten \
                --config=p/security-audit \
                --json \
                --output=/shared/semgrep-results.json \
                .
              # Fail on HIGH severity findings
              python3 -c "
              import json, sys
              with open('/shared/semgrep-results.json') as f:
                  results = json.load(f)
              high = [r for r in results['results'] if r['extra']['severity'] == 'ERROR']
              if high:
                  print(f'FAIL: {len(high)} HIGH severity SAST findings')
                  sys.exit(1)
              print('PASS: No HIGH severity SAST findings')
              "
      - step:
          name: Container Scan (Trivy)
          identifier: container_scan_trivy
          type: Run
          spec:
            connectorRef: account.dockerhub
            image: aquasec/trivy:latest
            command: |
              trivy image \
                --exit-code 1 \
                --severity HIGH,CRITICAL \
                --no-progress \
                <+artifact.image>:<+artifact.tag>
      - step:
          name: Secrets Scan (Gitleaks)
          identifier: secrets_scan_gitleaks
          type: Run
          spec:
            connectorRef: account.dockerhub
            image: zricethezav/gitleaks:latest
            command: |
              gitleaks detect \
                --source . \
                --report-format json \
                --report-path /shared/gitleaks-report.json \
                --exit-code 1
```

### Template 3 — Production Approval Stage

```yaml
template:
  name: Production Approval Stage
  identifier: production_approval_stage
  versionLabel: "1.0"
  type: Stage
  orgIdentifier: <ORG_ID>
  description: "Mandatory approval gate before any production deployment"
  tags:
    managed-by: hcprm
    compliance: required
  spec:
    type: Approval
    spec:
      execution:
        steps:
          - step:
              name: JIRA Change Request
              identifier: jira_change_request
              type: JiraCreate
              spec:
                connectorRef: <+input>
                projectKey: CHG
                issueType: Change Request
                fields:
                  - name: Summary
                    value: "Deploy <+service.name> <+artifact.tag> to production"
                  - name: Description
                    value: |
                      **Service**: <+service.name>
                      **Version**: <+artifact.tag>
                      **Pipeline**: <+pipeline.name>
                      **Execution**: <+pipeline.executionId>
          - step:
              name: Production Sign-off
              identifier: production_signoff
              type: HarnessApproval
              spec:
                approvalMessage: |
                  **Production Deployment Approval Required**

                  Service: <+service.name>
                  Version: <+artifact.tag>
                  Environment: Production
                  Initiated by: <+pipeline.triggeredBy.name>

                  Please verify:
                  ✅ Staging verification passed
                  ✅ Change request approved
                  ✅ Deployment window confirmed
                  ✅ On-call engineer aware
                includePipelineExecutionHistory: true
                approvers:
                  minimumCount: 2
                  disallowPipelineExecutor: true
                  userGroups:
                    - account.SRE_Team
                    - account.Engineering_Leads
                approverInputs:
                  - name: changeRequestId
                    defaultValue: ""
                  - name: onCallEngineer
                    defaultValue: ""
                autoApproval:
                  action: REJECT
                  scheduledDeadline:
                    timeZone: UTC
                    time: "23:00"
```

### Template 4 — Notification Step Group

```yaml
template:
  name: Deployment Notifications
  identifier: deployment_notifications
  versionLabel: "1.0"
  type: StepGroup
  spec:
    steps:
      - step:
          name: Slack Notify Start
          identifier: slack_notify_start
          type: ShellScript
          spec:
            shell: Bash
            source:
              type: Inline
              spec:
                script: |
                  curl -X POST "<+pipeline.variables.slackWebhook>" \
                    -H "Content-Type: application/json" \
                    -d '{
                      "text": "🚀 Deploying *<+service.name>* `<+artifact.tag>` to *<+env.name>*",
                      "attachments": [{
                        "color": "warning",
                        "fields": [
                          {"title": "Triggered by", "value": "<+pipeline.triggeredBy.name>", "short": true},
                          {"title": "Pipeline", "value": "<+pipeline.executionId>", "short": true}
                        ]
                      }]
                    }'
            onDelegate: true
```

---

## Using Templates in Pipelines

```yaml
pipeline:
  stages:
    - stage:
        name: Security Scans
        identifier: security_scans
        type: CI
        spec:
          execution:
            steps:
              # Reference step group template
              - stepGroup:
                  name: Security Scans
                  identifier: security_scans_group
                  template:
                    templateRef: org.security_scan_step_group  # org. prefix = org-level
                    versionLabel: "1.2"

    - stage:
        # Reference stage template
        template:
          templateRef: org.standard_k8s_deploy_stage
          versionLabel: "2.0"
          templateInputs:
            type: Deployment
            spec:
              service:
                serviceRef: payment_service
              environment:
                environmentRef: production
                infrastructureDefinitions:
                  - identifier: payment_prod_infra

    - stage:
        # Reference approval stage template
        template:
          templateRef: org.production_approval_stage
          versionLabel: "1.0"
          templateInputs:
            type: Approval
            spec:
              execution:
                steps:
                  - step:
                      identifier: jira_change_request
                      template:
                        templateInputs:
                          spec:
                            connectorRef: jira_connector
```

---

## Template Governance

### Enforce Template Usage via OPA
```rego
package template_enforcement

# CD stages must use the standard deploy template (not custom stages)
deny["CD stage must use org.standard_k8s_deploy_stage template"] {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  not uses_approved_template(stage)
}

uses_approved_template(stage) {
  stage.template.templateRef == "org.standard_k8s_deploy_stage"
}
```

---

## Success Criteria
- [ ] All 4 core templates published at org-level
- [ ] All new pipelines referencing templates (not inline stages)
- [ ] Template versioning strategy documented and communicated
- [ ] OPA policy enforcing template usage active
- [ ] Template changelog maintained per version
- [ ] At least 3 team pipelines migrated from inline stages to templates

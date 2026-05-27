---
name: harness-policy-governance
description: >
  Write, enforce, and audit OPA (Open Policy Agent) governance policies in Harness pipelines
  and entities. Use this skill whenever the user mentions OPA policies, Harness Policy Engine,
  governance rules, compliance gates, RBAC enforcement, mandatory approvals, required tags,
  pipeline policy violations, allowed deployment windows, resource constraints, or when the
  user needs to enforce organizational standards across all pipelines automatically.
  Also trigger when auditing pipelines for compliance or setting up guardrails before
  production deployments.
---

# Harness Policy Governance (OPA)

## Purpose
Encode organizational compliance, security, and operational standards as machine-enforceable OPA policies that block or warn on violations before harm occurs — rather than detecting problems after deployment.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| All pipeline YAML outputs | s04, s09 | Yes |
| Compliance requirements | s01 PRD | Yes |
| Blast radius policies | s14 output | Yes |
| Template enforcement needs | s09 output | No |
| Cost governance needs | s23 output | No |
| Risk tolerance preferences | s02 taste (risk_tolerance) | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| OPA policy set YAML | `.commandcode/artifacts/policy-set.yaml` | YAML |
| Pipeline tagging policy | `.commandcode/artifacts/policy-tagging.rego` | Rego |
| Deployment window policy | `.commandcode/artifacts/policy-deploy-window.rego` | Rego |
| Production approval policy | `.commandcode/artifacts/policy-approval.rego` | Rego |
| Container security policy | `.commandcode/artifacts/policy-security.rego` | Rego |
| Chaos gate policy | `.commandcode/artifacts/policy-chaos-gate.rego` | Rego |
| Cost governance policy | `.commandcode/artifacts/policy-cost.rego` | Rego |
| Policy audit report | s25 (postmortem context) | Markdown |

---

## Prerequisites
- [ ] Harness Policy Engine module enabled
- [ ] OPA basics understood (Rego language)
- [ ] Compliance requirements documented (required tags, approval rules, deployment windows)
- [ ] RBAC roles defined (who can override a policy warning)

---

## Policy Enforcement Points

Harness evaluates OPA policies at these events:

| Event | Policies Evaluated On |
|---|---|
| `OnSave` | Entity YAML saved in UI or API |
| `OnRun` | Before pipeline execution begins |
| `OnStep` | Before specific step executes |
| `OnStepComplete` | After step completes |

---

## Policy Structure (Rego)

```
package <domain>

# Always include:
deny[reason] {
  # condition that should NOT be true
  # reason: human-readable explanation string
}

warn[reason] {
  # non-blocking warning condition
}
```

---

## Essential Policies

### Policy 1: Required Pipeline Tags
```rego
package pipeline_tagging

# Every pipeline must have team and domain tags
deny[sprintf("Pipeline '%s' missing required tag 'team'", [input.pipeline.name])] {
  not has_tag("team")
}

deny[sprintf("Pipeline '%s' missing required tag 'domain'", [input.pipeline.name])] {
  not has_tag("domain")
}

has_tag(key) {
  tag := input.pipeline.tags[_]
  tag.key == key
}
```

### Policy 2: Production Deployment Window
```rego
package deployment_window

import future.keywords.if

# Block production deployments outside business hours (UTC)
deny["Production deployments only allowed Mon-Fri 09:00-17:00 UTC"] {
  is_production_deployment
  not in_deployment_window
}

is_production_deployment if {
  stage := input.pipeline.stages[_].stage
  stage.spec.environment.environmentRef == "production"
}

in_deployment_window if {
  # time.weekday: 0=Sunday, 1=Monday ... 6=Saturday
  day := time.weekday(time.now_ns())
  day >= 1
  day <= 5
  hour := time.clock(time.now_ns())[0]
  hour >= 9
  hour < 17
}
```

### Policy 3: Mandatory Production Approval
```rego
package mandatory_approval

# Production pipelines must have at least one Approval stage
deny["Production pipeline missing mandatory Approval stage"] {
  has_production_stage
  not has_approval_stage
}

has_production_stage if {
  stage := input.pipeline.stages[_].stage
  stage.spec.environment.environmentRef == "production"
}

has_approval_stage if {
  stage := input.pipeline.stages[_].stage
  stage.type == "Approval"
}
```

### Policy 4: No Privileged Containers in CI
```rego
package container_security

# CI steps must not use privileged mode
deny[sprintf("Step '%s' uses privileged mode — not allowed", [step.identifier])] {
  stage := input.pipeline.stages[_].stage
  stage.type == "CI"
  step := stage.spec.execution.steps[_].step
  step.spec.privileged == true
}

# CI steps must not use host network
deny[sprintf("Step '%s' uses hostNetwork — not allowed", [step.identifier])] {
  stage := input.pipeline.stages[_].stage
  stage.type == "CI"
  step := stage.spec.execution.steps[_].step
  step.spec.hostNetwork == true
}
```

### Policy 5: Require Rollback Steps
```rego
package rollback_required

# Every CD stage must define rollback steps
deny[sprintf("CD Stage '%s' missing rollbackSteps — required for production safety",
             [stage.name])] {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  not stage.spec.execution.rollbackSteps
}

warn[sprintf("CD Stage '%s' has empty rollbackSteps — verify this is intentional",
             [stage.name])] {
  stage := input.pipeline.stages[_].stage
  stage.type == "Deployment"
  count(stage.spec.execution.rollbackSteps) == 0
}
```

### Policy 6: Chaos Experiment Resilience Score Gate
```rego
package chaos_gate

# Chaos steps must require minimum 80% resilience score
deny[sprintf("Chaos step '%s' requires expectedResilienceScore >= 80, got %d",
             [step.identifier, step.spec.expectedResilienceScore])] {
  stage := input.pipeline.stages[_].stage
  step := stage.spec.execution.steps[_].step
  step.type == "Chaos"
  step.spec.expectedResilienceScore < 80
}
```

### Policy 7: Secrets Not Hardcoded
```rego
package secret_hygiene

import future.keywords.every

# Pipeline variables must not contain obvious secret patterns
deny[sprintf("Variable '%s' appears to contain a hardcoded secret value",
             [variable.name])] {
  variable := input.pipeline.variables[_]
  regex.match(`(?i)(password|token|secret|key|apikey|api_key|passwd)`, variable.name)
  variable.value != ""
  not startswith(variable.value, "<+secrets")
  not startswith(variable.value, "<+input")
}
```

---

## Policy Sets (Group Policies Together)

```yaml
policySet:
  name: Production Deployment Guardrails
  identifier: production_guardrails
  orgIdentifier: <ORG_ID>
  projectIdentifier: <PROJECT_ID>
  enabled: true
  policies:
    - policyIdentifier: pipeline_tagging
      severity: error      # error = deny, warning = warn-only
    - policyIdentifier: mandatory_approval
      severity: error
    - policyIdentifier: deployment_window
      severity: warning    # warn but don't block (allow override)
    - policyIdentifier: rollback_required
      severity: error
    - policyIdentifier: secret_hygiene
      severity: error
    - policyIdentifier: chaos_gate
      severity: error
  type: pipeline
  executionType: OnRun
```

---

## Testing Policies Locally

```bash
# Install OPA CLI
curl -L -o opa https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static
chmod +x opa

# Test policy against a pipeline YAML
# 1. Convert pipeline YAML to JSON
python3 -c "
import sys, yaml, json
with open('pipeline.yaml') as f:
    data = yaml.safe_load(f)
print(json.dumps({'pipeline': data.get('pipeline', data)}, indent=2))
" > pipeline_input.json

# 2. Evaluate policy
opa eval \
  --input pipeline_input.json \
  --data policy.rego \
  'data.mandatory_approval.deny'

# 3. Expected output for compliant pipeline:
# {"result": [{"expressions": [{"value": [], ...}]}]}
# Empty array = no violations = PASS
```

---

## RBAC: Who Can Override Policy Warnings

```yaml
# Harness RBAC Role — Policy Override
role:
  name: Policy Override Approver
  identifier: policy_override_approver
  permissions:
    - core_governancepolicy_override
  allowedScopeLevels: [project]
```

Grant this role only to: Engineering Directors, SRE Leads, Release Managers.

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI generates OPA Rego policies from natural language |
| Target | L3 | AI maintains policy library and detects violations |

### Harness AI Agent

**Agent**: Harness AI DevOps Agent
**Capabilities**:
- OPA Rego policy generation from natural language
- Compliance gate design
- Policy violation detection and notification

### Human Gates

- Policy activation
- Compliance exception approval
- Governance framework changes

---

## Success Criteria
- [ ] Core policy set active with `OnRun` enforcement
- [ ] All 7 essential policies above implemented and tested
- [ ] Policy violations surfaced in pipeline execution UI with clear messages
- [ ] Local OPA testing verified before deploying new policies
- [ ] Override process documented (who, when, audit trail)
- [ ] Monthly policy audit report generated via Harness API

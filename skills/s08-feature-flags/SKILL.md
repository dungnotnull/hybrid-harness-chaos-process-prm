---
name: harness-feature-flags
description: >
  Design, implement, and manage Harness Feature Flags (FF) for progressive delivery,
  kill switches, A/B testing, and canary user rollouts. Use this skill whenever the
  user mentions feature flags, feature toggles, FF_, kill switch, percentage rollout,
  target groups, flag evaluation, SDK integration, multivariate flags, flag pipelines,
  or controlling feature releases without redeployment. Also trigger when the user wants
  to gate a chaos experiment behind a flag or use flags to control blast radius.
---

# Harness Feature Flags

## Purpose
Implement feature flags as first-class delivery primitives — decoupling code deployment from feature release, enabling instant rollbacks without redeployment, and supporting data-driven percentage rollouts.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Service definitions | s05 (workflow_context.artifacts) | Yes |
| PRD feature requirements | s01 context | Yes |
| Blast radius control requirements | s14 output | No |
| Chaos flag gating needs | s12 experiment context | No |
| SDK language preference | s02 taste | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Feature flag YAML definitions | `.commandcode/artifacts/feature-flags.yaml` | YAML |
| SDK integration code snippets | s11 (testing), service teams | Code |
| Flag pipeline YAML | `.commandcode/artifacts/flag-pipeline.yaml` | YAML |
| Kill switch configurations | `.commandcode/artifacts/kill-switches.yaml` | YAML |
| Flag cleanup schedule | s03 (tracker for dates) | Markdown checklist |
| Chaos gate flags | s14 (blast radius), s21 (alerts) | YAML |

---

## Prerequisites
- [ ] Harness FF module enabled on account
- [ ] Target runtime: browser / server / mobile (determines SDK)
- [ ] Flag naming convention agreed (see below)
- [ ] Monitoring dashboards ready to track flag impact

---

## Flag Taxonomy

| Flag Type | Use Case | Example |
|---|---|---|
| Release flag | New feature gating | `FF_PAYMENT_NEW_CHECKOUT` |
| Ops flag | Kill switch / incident | `FF_OPS_DISABLE_RECOMMENDATIONS` |
| Experiment flag | A/B test | `FF_EXP_HOMEPAGE_HERO_V2` |
| Permission flag | Role-based access | `FF_PERM_ADMIN_BULK_DELETE` |
| Chaos flag | Gate fault injection | `FF_CHAOS_PAYMENT_POD_DELETE` |

**Naming convention**: `FF_<TYPE>_<DOMAIN>_<FEATURE>` in SCREAMING_SNAKE_CASE

---

## Flag Lifecycle

```
Create (OFF) → Test (internal targets) → Staged rollout (%)
    → 100% ON → Cleanup (remove from code + FF platform)
```

**Flags are technical debt.** Every flag must have a cleanup date set at creation time.

---

## Step 1 — Create Feature Flag (YAML / API)

### Boolean Flag
```yaml
featureFlag:
  name: New Checkout Flow
  identifier: FF_PAYMENT_NEW_CHECKOUT
  projectIdentifier: <PROJECT_ID>
  orgIdentifier: <ORG_ID>
  kind: boolean
  archived: false
  defaultOnVariation: "true"
  defaultOffVariation: "false"
  variations:
    - identifier: "true"
      name: "On"
      value: "true"
    - identifier: "false"
      name: "Off"
      value: "false"
  tags:
    - key: domain
      value: payment
    - key: cleanup-by
      value: "2025-Q3"
    - key: managed-by
      value: hcprm
```

### Multivariate Flag (String)
```yaml
featureFlag:
  name: Recommendation Algorithm
  identifier: FF_EXP_RECOMMENDATION_ALGO
  kind: string
  variations:
    - identifier: control
      name: Control (current algo)
      value: "collaborative_filtering"
    - identifier: treatment_a
      name: Treatment A (ML model)
      value: "neural_collaborative"
    - identifier: treatment_b
      name: Treatment B (hybrid)
      value: "hybrid_contextual"
  defaultOnVariation: control
  defaultOffVariation: control
```

---

## Step 2 — Configure Targeting Rules

### Serve to Specific Users / Teams (Internal Beta)
```yaml
targetingRules:
  - clauses:
      - attribute: email
        op: ends_with
        values: ["@company.com"]
    serve:
      variation: "true"
    priority: 1
  - clauses:
      - attribute: team
        op: in
        values: ["payments", "checkout"]
    serve:
      variation: "true"
    priority: 2
```

### Percentage Rollout
```yaml
targetingRules:
  - serve:
      distribution:
        bucketBy: identifier   # consistent hashing by user ID
        variations:
          - variation: "true"
            weight: 20         # 20% of users get new feature
          - variation: "false"
            weight: 80
    priority: 100              # lower priority = evaluated last (fallback)
```

### Gradual Ramp Schedule
```
Week 1: 5% → monitor error rate, p99 latency
Week 2: 25% → check conversion metrics
Week 3: 50% → A/B significance test
Week 4: 100% → full rollout, schedule flag cleanup
```

---

## Step 3 — SDK Integration

### Server-Side (Node.js)
```javascript
import { initialize } from '@harnessio/ff-nodejs-server-sdk';

const client = await initialize('<SDK_KEY>', {
  baseUrl: 'https://config.ff.harness.io/api/1.0',
  eventsUrl: 'https://events.ff.harness.io/api/1.0',
  pollInterval: 60000,         // ms between polls
  enableStream: true,          // real-time updates via SSE
});

// Evaluate flag
const target = {
  identifier: user.id,          // consistent bucketing
  name: user.email,
  attributes: {
    email: user.email,
    team: user.team,
    plan: user.subscriptionPlan,
  },
};

const showNewCheckout = await client.boolVariation(
  'FF_PAYMENT_NEW_CHECKOUT',
  target,
  false   // default value if SDK error or flag not found
);

if (showNewCheckout) {
  return renderNewCheckout();
} else {
  return renderLegacyCheckout();
}
```

### Client-Side (React)
```jsx
import { FFContextProvider, useFeatureFlag } from '@harnessio/ff-react-client-sdk';

// Wrap app at root
function App() {
  return (
    <FFContextProvider
      apiKey="<CLIENT_SDK_KEY>"
      target={{
        identifier: currentUser.id,
        name: currentUser.name,
        attributes: { plan: currentUser.plan },
      }}
    >
      <Checkout />
    </FFContextProvider>
  );
}

// Use flag in component
function Checkout() {
  const showNewCheckout = useFeatureFlag('FF_PAYMENT_NEW_CHECKOUT');

  return showNewCheckout ? <NewCheckout /> : <LegacyCheckout />;
}
```

### Backend (Go)
```go
import harness "github.com/harness/ff-golang-server-sdk/client"

client, err := harness.NewCfClient("<SDK_KEY>")
if err != nil {
    log.Fatalf("Failed to init FF client: %v", err)
}
defer client.Close()

target := dto.NewTargetBuilder(userID).
    Name(userEmail).
    Attribute("team", userTeam).
    Build()

enabled, err := client.BoolVariation("FF_PAYMENT_NEW_CHECKOUT", &target, false)
if err != nil {
    // Default to false on SDK error — fail safe
    enabled = false
}
```

---

## Step 4 — Flag Pipeline (Automated Rollout)

Use Harness pipelines to automate progressive flag rollouts with verification gates:

```yaml
pipeline:
  name: FF_PAYMENT_NEW_CHECKOUT Rollout
  identifier: ff_payment_new_checkout_rollout
  stages:
    - stage:
        name: 5% Rollout
        type: FeatureFlag
        spec:
          execution:
            steps:
              - step:
                  name: Set 5% Rollout
                  type: FlagConfiguration
                  spec:
                    feature: FF_PAYMENT_NEW_CHECKOUT
                    environment: production
                    instructions:
                      - kind: setFeatureFlagState
                        parameters:
                          state: "on"
                      - kind: updateDefaultServe
                        parameters:
                          distribution:
                            bucketBy: identifier
                            variations:
                              - variation: "true"
                                weight: 5
                              - variation: "false"
                                weight: 95
    - stage:
        name: Verify 5%
        type: Approval
        spec:
          execution:
            steps:
              - step:
                  type: HarnessApproval
                  spec:
                    approvalMessage: |
                      Check dashboards:
                      - Error rate unchanged?
                      - Checkout conversion ≥ baseline?
                      Approve to continue to 25% rollout.
                    approvers:
                      minimumCount: 1
                      userGroups: [account.Product_Team]
```

---

## Step 5 — Kill Switch Pattern

```javascript
// Always check kill switch FIRST in critical paths
const systemHealthy = await client.boolVariation(
  'FF_OPS_DISABLE_RECOMMENDATIONS',
  target,
  false   // false = recommendations enabled (flag is "disable" flag)
);

if (systemHealthy) {
  // Kill switch engaged — return safe fallback immediately
  return { recommendations: [], source: 'killswitch' };
}

// Normal path
return await getRecommendations(userId);
```

**Kill switch naming**: Use `DISABLE_` prefix so default `false` = feature enabled. Activating the flag = disabling the feature.

---

## Step 6 — Flag Cleanup

When a flag reaches 100% rollout and is stable for 2+ weeks:

```bash
# 1. Search codebase for all flag references
grep -r "FF_PAYMENT_NEW_CHECKOUT" --include="*.js" --include="*.ts" .

# 2. Remove flag evaluation code (hardcode the winning variation)
# Before:
#   const show = await client.boolVariation('FF_PAYMENT_NEW_CHECKOUT', target, false);
# After:
#   const show = true;  // FF_PAYMENT_NEW_CHECKOUT graduated 2025-03-15

# 3. Deploy code without flag reference
# 4. Archive flag in Harness (don't delete — preserves audit trail)
```

---

## Chaos + Feature Flag Integration

Gate chaos experiments behind feature flags to enable instant abort:

```javascript
// In chaos experiment runner
const chaosEnabled = await client.boolVariation(
  'FF_CHAOS_PAYMENT_POD_DELETE',
  serviceTarget,
  false
);

if (!chaosEnabled) {
  logger.info('Chaos experiment gated by FF — skipping');
  return { status: 'skipped', reason: 'feature_flag_disabled' };
}

// Proceed with chaos experiment
await runPodDeleteExperiment();
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI generates FF config and SDK code |
| Target | L3 | AI manages FF lifecycle, human approves production changes |

### Harness AI Agent

**Agent**: Harness AI DevOps Agent
**Capabilities**:
- Feature flag configuration generation
- SDK code generation
- Kill switch setup
- Rollout strategy optimization

### Human Gates

- Production FF toggle activation
- Kill switch activation
- Rollout percentage changes above threshold

### Fallback

When Harness AI is unavailable: Use static pipeline templates from s09 Template Library and manual YAML construction following Harness schema documentation.

---

## Success Criteria
- [ ] All flags follow naming convention `FF_<TYPE>_<DOMAIN>_<FEATURE>`
- [ ] Every flag has a `cleanup-by` tag with quarter/date
- [ ] SDK integrations use user identifier for consistent bucketing
- [ ] Default values are safe (fail-closed) when SDK errors occur
- [ ] Kill switches tested in staging before production incidents
- [ ] Flag pipeline gates rollout with approval between percentage steps
- [ ] Flag cleanup process documented and assigned to flag owner

---
name: chaos-game-day-planning
description: >
  Plan, schedule, and execute game days — structured resilience exercises where teams
  run chaos experiments in production-like environments and practice incident response.
  Use this skill whenever the user says "plan a game day", "schedule chaos day",
  "organize resilience exercise", "war game", or needs to coordinate multiple chaos
  experiments with team participation. Also trigger when s12-s17 complete and the user
  is ready to move from individual experiments to coordinated team exercises.
---

# Game Day Planning (s18)

## Purpose
Orchestrate comprehensive game days that combine multiple chaos experiments with structured incident response practice, team coordination, and real-time monitoring — transforming chaos engineering from isolated experiments into organizational resilience capability.

---

## Prerequisites
- [ ] All chaos experiments from s14-s19 designed and validated
- [ ] Team roles and availability confirmed
- [ ] Observability dashboards from s22 active
- [ ] Alert rules from s23 configured
- [ ] Security scan from s11 completed (no CRITICAL findings)
- [ ] Performance baselines from s13 established

## Input Contract

| Input | Source | Required |
|---|---|---|
| All experiment manifests (s12-s17) | workflow_context.artifacts | Yes |
| Blast radius configurations | s14 output | Yes |
| Hypothesis documents | s13 output | Yes |
| Steady state baselines | s15 output | Yes |
| Pre-chaos test evidence | s11 (CloakBrowser) | Yes |
| Observability dashboards | s20 output | Yes |
| Team roster + on-call schedule | User or s01 context | Yes |
| Risk tolerance | s02 taste | Yes |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Game day runbook | `.commandcode/artifacts/game-day-runbook.md` | Markdown |
| Experiment schedule (timeline) | `.commandcode/artifacts/game-day-schedule.yaml` | YAML |
| Incident response templates | Teams (Slack, PagerDuty) | Messages |
| Real-time monitoring dashboard config | s20 (observability) | JSON |
| Game day results report | s24 (scoring), s25 (postmortem) | Markdown |
| Team feedback survey | s25 (learning) | Form |

---

## Game Day Checklist

### T-7 Days: Planning
```
[ ] Define game day objective (what are we testing about our resilience?)
[ ] Select experiments from catalog (s12-s17)
[ ] Confirm target environment and blast radius
[ ] Schedule date/time (avoid release days, on-call rotations)
[ ] Assign roles:
    - Game Master: Controls experiment execution
    - Observer: Monitors dashboards, triggers alerts
    - Responder: Handles incidents as they escalate
    - Scribe: Documents timeline, findings, action items
[ ] Send calendar invite with pre-read (game day runbook)
[ ] Verify observability dashboards are working
```

### T-1 Day: Preparation
```
[ ] Dry-run all experiments in staging
[ ] Confirm all abort mechanisms working
[ ] Verify PagerDuty / alerting routing is correct (test mode)
[ ] Ensure rollback procedures are documented and accessible
[ ] Brief on-call engineers (they should NOT be surprised)
[ ] Create dedicated Slack channel (#chaos-game-day-<date>)
[ ] Verify CloakBrowser baseline tests passing
```

### T-0: Game Day Execution
```
[ ] 09:00 — Kick-off: Review objectives, roles, safety protocols
[ ] 09:15 — Pre-experiment checks:
      kubectl get nodes --no-headers | grep -v Ready  # Should be 0
      curl -f <SERVICE>/health                          # Should be 200
      ./pre-chaos-check.sh <SERVICE>                    # All checks pass
[ ] 09:30 — Experiment 1: Pod Delete (baseline warm-up)
[ ] 09:45 — Debrief: What was observed? Any surprises?
[ ] 10:00 — Experiment 2: Network Latency (increasing intensity)
[ ] 10:30 — Debrief + incident response drill
[ ] 10:45 — Experiment 3: Resource Exhaustion (CPU/Memory)
[ ] 11:15 — Debrief
[ ] 11:30 — Experiment 4: Infrastructure Fault (if applicable)
[ ] 12:00 — Lunch + observation period
[ ] 13:00 — Experiment 5+: Composite scenarios
[ ] 15:00 — Cleanup and recovery verification
[ ] 15:30 — Retrospective
[ ] 16:00 — Action items assigned + postmortem scheduled
```

---

## Game Day Runbook Template

```markdown
# Game Day Runbook — <DATE>

## Objectives
- **Theme**: <e.g., "Testing Payment Service Resilience Under Load">
- **Goal**: Validate that the payment service remains available (>99.9%) under
  pod failures, network latency, and dependency timeouts.
- **Success Criteria**: All experiments pass with resilience score ≥ 80.

## Environment
| Setting | Value |
|---|---|
| Target Environment | Staging (staging-cluster) |
| Services Under Test | payment-service, checkout-api, notification-worker |
| Observability | Prometheus + Grafana dashboards: [links] |
| Alerting | PagerDuty (test mode), #chaos-game-day channel |

## Roles
| Role | Person | Contact |
|---|---|---|
| Game Master | Alice (SRE) | @alice |
| Observer | Bob (Platform) | @bob |
| Responder | Charlie (Payments) | @charlie |
| Scribe | AI Agent | N/A |

## Experiment Schedule
| Time | Experiment | Blast Radius | Duration | Expected Outcome |
|---|---|---|---|---|
| 09:30 | Pod Delete 50% | payment-service pods | 2 min | Self-heal < 30s |
| 10:00 | Network Latency 250ms | checkout → payment | 3 min | Circuit breaker opens |
| 10:45 | Pod CPU Hog 80% | payment-service 50% pods | 3 min | Autoscaling triggers |
| 11:30 | Composite: Pod Delete + Latency | payment-service | 5 min | Both recover independently |

## Abort Conditions (IMMEDIATE ACTION)
If ANY of these occur, Game Master ABORTS all experiments:
- [ ] Error rate exceeds 5% for > 30 seconds
- [ ] P99 latency exceeds 2x baseline for > 60 seconds
- [ ] Customer-facing impact detected
- [ ] PagerDuty alert fires (non-test)
- [ ] Any team member calls "STOP"

## Abort Procedure
```
Game Master: "ABORT ABORT ABORT — all experiments stop"
kubectl patch chaosengine --all -n <NAMESPACE> --type merge -p '{"spec":{"engineState":"stop"}}'
# Verify recovery in Grafana dashboard
# Post in #chaos-game-day: "Experiments aborted. Investigating."
```

## Post-Game Day
- [ ] All experiments stopped and cleaned up
- [ ] Recovery verified (all services healthy, metrics at baseline)
- [ ] Retrospective completed (what went well, what didn't, action items)
- [ ] Playbook updated with learnings
- [ ] Action items filed as tickets with owners
- [ ] Game day report published to team wiki
```

---

## Incident Response Drill Scenarios

During game day, inject "surprise" scenarios for responders:

```yaml
drill_scenarios:
  - name: "PagerDuty alert fires — what do you do?"
    trigger: Game Master manually fires test alert
    expected_response:
      - Acknowledge alert within 1 minute
      - Join incident bridge / Slack huddle
      - Identify experiment causing the alert
      - Check dashboards for blast radius impact
      - Decide: continue or abort experiment

  - name: "Customer reports slowness — what do you do?"
    trigger: Game Master posts in #customer-support as "fake customer"
    expected_response:
      - Correlate user report with experiment timeline
      - Check if experiment exceeds blast radius
      - Communicate: "This is part of planned game day — no real impact"
      - If real impact: abort immediately

  - name: "Observability goes dark — what do you do?"
    trigger: Game Master kills observability agent temporarily
    expected_response:
      - Detect that dashboards are not updating
      - ABORT all experiments (no observability = no chaos)
      - Restore observability before resuming
```

---

## Composite Experiment Scenarios

Combine multiple faults to simulate real-world cascading failures:

```yaml
composite_scenarios:
  - name: "Payment Service Cascading Failure"
    description: >
      Simulate a scenario where a payment service pod crashes due to OOM,
      causing increased latency to downstream checkout service, which in
      turn triggers a partial DNS failure.
    experiments:
      - fault: pod-memory-hog
        target: payment-service
        duration: 120s
        delay: 0s       # Start immediately
      - fault: pod-network-latency
        target: checkout-api
        destination: payment-service
        duration: 120s
        delay: 30s      # Start 30s after memory hog
      - fault: pod-dns-error
        target: checkout-api
        duration: 60s
        delay: 60s      # Start 60s in (peak failure)

  - name: "Infrastructure Degradation Under Load"
    description: >
      Drain a node while running a load test against the service,
      testing whether autoscaling and pod rescheduling handle
      infrastructure failure under production-like traffic.
    experiments:
      - fault: node-drain
        scope: 1 node in cluster
        duration: 300s
        delay: 0s
      - load_test:
          tool: k6
          script: load-tests/payment-service.js
          virtual_users: 100
          duration: 300s
          delay: 10s
```

---

## Retrospective Template

```markdown
# Game Day Retrospective — <DATE>

## What Went Well (👍)
-

## What Didn't Go Well (👎)
-

## Surprises
- What happened that we didn't expect?

## Action Items
| # | Action | Owner | Priority | Ticket |
|---|---|---|---|---|
| 1 | Add circuit breaker to checkout-api | @charlie | P0 | ENG-5001 |
| 2 | Fix P99 latency alert threshold | @bob | P1 | ENG-5002 |
| 3 | Update runbook for DNS failure recovery | @alice | P2 | ENG-5003 |

## Resilience Score
| Experiment | Score |
|---|---|
| Pod Delete | 95 |
| Network Latency 250ms | 88 |
| CPU Hog 80% | 72 |
| Composite | 65 |
| **Overall** | **80** |

## Notes for Next Game Day
-
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI generates game day scenarios and timelines |
| Target | L2 | AI orchestrates game day execution with human coordination |

### Harness AI Agent

**Agent**: Harness AI Reliability Agent
**Capabilities**:
- Game day scenario generation from experiment library
- Timeline and team coordination
- Real-time experiment orchestration

### Human Gates

- Game day approval
- Production go/no-go
- Experiment pause/abort decisions

### MCP

- LitmusChaos MCP
- Gremlin MCP

---

## Success Criteria
- [ ] Game day runbook completed and shared T-7 days before event
- [ ] All roles assigned and briefed
- [ ] Abort mechanisms tested and working
- [ ] At least one incident response drill executed during game day
- [ ] Composite scenario run (minimum 2 concurrent faults)
- [ ] Retrospective completed within 24h of game day
- [ ] Action items filed as tickets with P0/P1/P2 priority
- [ ] All experiments cleaned up and cluster verified healthy post-game-day
- [ ] Game day results feed into s24 (scoring) and s25 (postmortem)

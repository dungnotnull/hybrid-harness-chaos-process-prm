---
name: chaos-postmortem-learning
description: >
  Conduct structured postmortems after chaos experiments and game days to extract
  maximum learning, drive remediation, and close the resilience feedback loop.
  Use this skill whenever experiments complete, game days conclude, or resilience
  scores reveal gaps. Also trigger after any incident that occurs during chaos
  testing. This skill ensures findings are converted into action, runbooks are
  updated, and knowledge is institutionalized — not lost in Slack threads.
  This is the final skill in the workflow and feeds back into s01 (BA re-analysis)
  for continuous improvement.
---

# Postmortem Learning (s25)

## Purpose
Transform chaos experiment findings into organizational learning — ensuring every failure, gap, and surprise becomes an action item that improves system resilience. This is the feedback loop that closes the full workflow, feeding learnings back into s01 for continuous improvement.

---

## Prerequisites
- [ ] Game day results from s20 (if post-game-day)
- [ ] Resilience scores from s26
- [ ] Alert data from s23
- [ ] Incident timeline and logs available
- [ ] Team availability for blameless retrospective

## Input Contract

| Input | Source | Required |
|---|---|---|
| All experiment results and scores | s12-s24 outputs | Yes |
| Resilience score cards | s24 output | Yes |
| Game day retrospective | s18 output | Yes |
| Alert history from experiments | s21 output | Yes |
| Post-chaos test evidence | s11 (rerun) | Yes |
| Recommendations | s21 output | Yes |
| Previous postmortem actions (for follow-up) | Previous s25 runs | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Postmortem report | `.commandcode/artifacts/postmortem-<date>.md` | Markdown |
| Action item tracker | `.commandcode/artifacts/action-items.md` | Markdown checklist |
| Updated runbooks | Service wiki / repo | Markdown |
| Blameless timeline | Included in postmortem | Markdown |
| Knowledge base entry | Team wiki | Markdown |
| Feedback for s01 (re-analysis trigger) | workflow_context | YAML |
| Resilience improvement roadmap | s24 (scoring trend) | Markdown |

---

## Postmortem Philosophy

```
Blameless + Actionable + Timely + Shared

Blameless:   Focus on systems, not people. Ask "how did this happen?"
             not "who caused this?"
Actionable:  Every finding has an owner, priority, and deadline
Timely:      Within 24-48 hours of experiment/game day
Shared:      Published to wiki, visible to entire engineering org
```

---

## Postmortem Template

```markdown
# Chaos Postmortem — <DATE>

## Experiment/Game Day Summary
| Field | Value |
|---|---|
| Event | <Game Day / Experiment Suite Name> |
| Date | <YYYY-MM-DD> |
| Duration | <HH:MM> |
| Services Tested | <list> |
| Experiments Run | <N> |
| Experiments Passed | <N> |
| Resilience Score | <SCORE>/100 (Grade: <GRADE>) |
| Game Master | <name> |
| Scribe | <name> |
| Postmortem Owner | <name> |

---

## Blameless Timeline
| Time (UTC) | Event | Impact | Resolution |
|---|---|---|---|
| 09:30 | Pod-delete experiment started | None | N/A |
| 09:31 | Pod-1 terminated | Health probe: OK | Auto-restart within 15s |
| 09:32 | Pod-2 terminated | Health probe: OK | Auto-restart within 12s |
| 10:00 | Network latency 500ms injected | P99 spiked to 650ms | Circuit breaker opened at 10:02 |
| 10:02 | Circuit breaker opened | Fallback activated | User error rate: 0.5% |
| 10:03 | Latency removed | Recovery began | Circuit closed at 10:04 |
| 11:30 | Composite scenario started | — | — |
| 11:32 | Memory hog triggered OOM | 2 pods killed | Auto-restart within 45s |
| 11:33 | DNS error injected | Checkout→Payment calls failed | Fallback: cached payment info |
| 11:35 | All faults cleared | Recovery in progress | Full recovery by 11:38 |

---

## What Went Well
- ✅ Pod self-healing worked perfectly (12-15s recovery time)
- ✅ Circuit breaker opened as expected (within 3 failures)
- ✅ Fallback response served cached data correctly
- ✅ No PagerDuty alerts fired on real infrastructure
- ✅ Grafana dashboard gave clear visibility throughout

---

## What Didn't Go Well
- ❌ DNS failure caused checkout-api to return 500 instead of cached fallback
- ❌ Composite scenario overloaded the observability pipeline (15s metrics gap)
- ❌ Visual regression detected: checkout page partially rendered after network loss
- ⚠️  Memory hog recovery took 45s (target: 30s)

---

## Surprises (Unexpected Behavior)
- 🔍 **Surprise 1**: The notification-worker was impacted by DNS failure even though it wasn't in the blast radius — latent dependency discovered
- 🔍 **Surprise 2**: Redis connection pool exhausted during memory hog — cascading effect

---

## Root Cause Analysis (5 Whys Per Finding)

### Finding 1: DNS failure caused 500 errors
**Why?** Checkout-api couldn't resolve payment-service DNS.
**Why?** The DNS error experiment was scoped to checkout-api pods.
**Why?** The application didn't have a fallback for DNS resolution failure.
**Why?** DNS resolution was assumed to be always available.
**Why?** No resilience requirement was specified for DNS in the PRD.

**Action**: Add DNS fallback with cached IP resolution and circuit breaker.

### Finding 2: Observability metrics gap during composite scenario
**Why?** Metrics pipeline was overwhelmed by composite fault data volume.
**Why?** Prometheus scrape interval was 15s with no buffer for spike.
**Why?** No rate limiting on chaos metric emission.
**Why?** Observability wasn't stress-tested before composite scenarios.

**Action**: Add metric rate limiting, increase Prometheus resources, test observability stack under load.

---

## Action Items
| # | Action | Priority | Owner | Target | Ticket | Status |
|---|---|---|---|---|---|---|
| 1 | Add DNS fallback with cached IP + circuit breaker | P0 | @charlie | 2025-03-22 | ENG-5101 | Open |
| 2 | Fix visual regression in checkout page | P1 | @diana | 2025-03-25 | ENG-5102 | Open |
| 3 | Add metric rate limiting for chaos experiments | P1 | @bob | 2025-03-28 | ENG-5103 | Open |
| 4 | Document latent dependency: notification → payment | P2 | @alice | 2025-04-01 | ENG-5104 | Open |
| 5 | Test observability stack under load | P2 | @bob | 2025-04-05 | ENG-5105 | Open |
| 6 | Add DNS resilience requirement to PRD template | P3 | @alice | 2025-04-10 | ENG-5106 | Open |

---

## Runbook Updates Required
- [ ] Update `payment-service/runbooks/dns-failure.md` — add DNS fallback steps
- [ ] Update `checkout-api/runbooks/circuit-breaker.md` — document expected behavior
- [ ] Update `sre/runbooks/chaos-observability.md` — add metric gap troubleshooting
- [ ] Create `notification-worker/runbooks/latent-dependencies.md` — document discovered dependency

---

## Taste/Learnings for Memory (s02)
- [ ] Add: "Always test DNS resilience — it's assumed reliable more than it should be" (RiskTolerance, Confidence: 0.85)
- [ ] Add: "Composite chaos scenarios require observability stress-testing" (Workflow, Confidence: 0.90)
- [ ] Add: "Checkout-api visual rendering needs chaos testing" (Testing, Confidence: 0.80)
- [ ] Add: "Notification-worker has latent dependency on payment DNS" (Technology, Confidence: 0.85)

---

## Feedback for Re-Analysis (s01 Trigger)
The following findings should trigger a re-analysis of requirements or architecture:

1. **DNS as critical dependency**: The PRD should include DNS resilience as a non-functional requirement (REQ-NFR-DNS).
2. **Latent dependencies**: The architecture diagram should include inferred dependencies discovered during chaos.
3. **Observability scaling**: The observability section of the PRD should include chaos load requirements.

---

## Follow-Up Schedule
| Date | Checkpoint |
|---|---|
| 2025-03-22 | P0 items due — DNS fallback implemented |
| 2025-03-25 | P1 items due — visual regression + rate limiting |
| 2025-04-05 | Next game day scheduled — re-run failed experiments |
| 2025-04-10 | Postmortem review — all action items closed or escalated |

---

## Lessons Learned (Knowledge Base)
These entries will be published to the team's resilience knowledge base:

### Entry: DNS Fallback Patterns
**Context**: During chaos testing, DNS failure caused cascading 500 errors.
**Learning**: All service-to-service calls should have DNS fallback (cached IP + circuit breaker).
**Pattern**:
```typescript
const RESOLVED_IP_CACHE = new Map<string, {ip: string, expires: number}>();

async function resolveWithFallback(hostname: string): Promise<string> {
  try {
    const ips = await dns.resolve4(hostname);
    RESOLVED_IP_CACHE.set(hostname, {ip: ips[0], expires: Date.now() + 300000});
    return ips[0];
  } catch {
    const cached = RESOLVED_IP_CACHE.get(hostname);
    if (cached && cached.expires > Date.now()) {
      metrics.increment('dns_fallback_used', {hostname});
      return cached.ip;
    }
    throw new Error(`DNS resolution failed for ${hostname} and no cache available`);
  }
}
```

### Entry: Composite Chaos Requires Observability Headroom
**Context**: Multiple concurrent faults overwhelmed Prometheus scraping.
**Learning**: Plan for 2-3x normal metric volume during composite scenarios.
**Pattern**: Run observability health check with 3x load before composite chaos.
```

---

## Action Item Tracker Maintenance

```markdown
# Action Items Dashboard

## By Priority
### P0 — Immediate (This Sprint)
| ID | Action | Owner | Ticket | Status |
|---|---|---|---|---|
| 1 | DNS fallback | @charlie | ENG-5101 | In Progress |
| 2 | ... | ... | ... | ... |

### P1 — This Quarter
| ID | Action | Owner | Ticket | Status |
|---|---|---|---|---|
| 3 | Visual regression fix | @diana | ENG-5102 | Open |
| 4 | Metric rate limiting | @bob | ENG-5103 | Open |
| ... | ... | ... | ... | ... |

### P2 — Next Quarter
...
```

---

## Closing the Loop

After postmortem actions are implemented:

1. **Re-run experiments** that previously failed
2. **Update resilience scores** based on improved results
3. **Publish update** to the team: "These gaps are now closed"
4. **Celebrate** improvement — resilience is a journey

```yaml
loop_closure:
  trigger: all_p0_actions_completed
  next_action: re_enter_s12
  message: >
    P0 postmortem actions are complete. Re-running failed experiments:
    - DNS error experiment (was: score 45)
    - Composite scenario (was: score 65)
    Target: All experiments pass with score ≥ 80.
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI generates postmortems and extracts action items |
| Target | L3 | AI auto-generates postmortems with RCA, human reviews |

### Harness AI Agent

**Agent**: Harness AI SRE Agent
**Capabilities**:
- Auto-postmortem generation from incident data
- RCA analysis (60-74% accuracy with LLMs)
- Action item extraction and tracking
- Incident timeline reconstruction

### Human Gates

- Postmortem approval
- Action item assignment
- Root cause acceptance
- Feedback loop trigger to s01

### Notes

Based on Szandala (ICCS 2025), LLMs achieve 60-74% RCA accuracy with few-shot prompting vs 82% for human SREs. Design as co-pilot, not replacement.

---

## Success Criteria
- [ ] Postmortem completed within 48 hours of experiment/game day
- [ ] Blameless timeline documented for all experiments
- [ ] Root cause analysis (5 Whys) performed for every finding
- [ ] Action items assigned with owners and deadlines
- [ ] Runbooks updated with new knowledge
- [ ] At least 3 taste learnings captured for s02
- [ ] Feedback for s01 re-analysis documented (if applicable)
- [ ] Knowledge base entries published for any new patterns discovered
- [ ] Follow-up schedule set for action item review
- [ ] Experiment re-run scheduled for any failed scenarios

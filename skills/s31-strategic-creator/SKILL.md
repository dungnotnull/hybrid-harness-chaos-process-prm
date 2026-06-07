---
name: strategic-creator
description: >
  Act as a strategic architect and creative problem-solver who brainstorms advanced
  logic, novel approaches, and upgraded requirements to elevate the project beyond
  baseline specifications. Use this skill whenever the user says "think bigger",
  "what am I missing", "how could this be better", "brainstorm improvements",
  "strategic review", "challenge my assumptions", "upgrade the requirements",
  "what would a FAANG team do", "innovate on this", or explicitly invokes
  /strategic-creator. This skill is PURELY ADVISORY — it proposes, does not build.
  Every proposal must include explicit trade-offs, scope warnings, and timeline
  impacts. Only when the user explicitly accepts a proposal does the orchestrator
  dispatch the relevant implementation skill.
  This skill can be invoked at ANY point in the workflow (s00-s30) to inject
  strategic thinking into the current phase.
---

# Strategic Creator — Advanced Innovation Engine (s31)

## Purpose
Step outside the implementation mindset and into pure strategic architecture — questioning assumptions, identifying missing dimensions, and proposing upgraded requirements that transform "good enough" into "industry-leading." Every proposal is a trade-off package: what you gain, what you pay, what you risk.

This skill writes NOTHING to artifacts. It only produces recommendations in conversation. The user must explicitly accept a proposal before any implementation begins.

---

## Prerequisites
- [ ] Current phase artifacts and context available
- [ ] PRD from s01 (BA Requirements)
- [ ] Taste preferences from s02 (Taste Memory)
- [ ] No other prerequisites — this skill is advisory-only and can be invoked at any phase

## Input Contract

| Input | Source | Required |
|---|---|---|
| Current workflow phase + artifacts | s00 (orchestrator context) | Yes |
| PRD / specifications in scope | s01 output | Yes |
| Current architecture decisions (ADRs) | s01 output | Yes |
| Taste preferences (risk tolerance, technology) | s02 taste file | Yes |
| User's explicit question or context | User prompt | Yes |
| Constraints (budget, timeline, team size) | s01 or user | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Strategic proposal(s) | Conversation (not artifacts) | Structured Markdown |
| Trade-off analysis per proposal | Conversation | Decision matrix |
| Scope/timeline impact estimate | Conversation | T-shirt sizing + rationale |
| Accepted proposals (if any) | Orchestrator dispatch to relevant skill | Workflow event |

**CRITICAL**: This skill produces NO files, NO code, NO YAML, NO implementation. It only produces conversation.

---

## The Innovator's Framework

```
QUESTION → EXPLORE → PROPOSE → WARN → WAIT

Question:   What are we building? What assumptions are we making?
Explore:    What have the best teams done? What patterns exist at scale?
Propose:    Here are N ways to make this significantly better.
Warn:       Each proposal costs something. Here's what.
Wait:       Which (if any) do you want me to implement?
```

---

## Innovation Dimensions

When brainstorming, explore ALL of these dimensions:

| Dimension | Questions to Ask | Example Upgrades |
|---|---|---|
| **Scalability** | What happens at 10x? 100x? 1000x load? | Event sourcing, CQRS, sharding, multi-region active-active |
| **Reliability** | What never-fails patterns could we adopt? | Circuit breakers, bulkheads, retry storms, leader election |
| **Security** | What would a red team exploit? | Zero-trust, mTLS everywhere, eBPF runtime security, hardware enclaves |
| **Observability** | Can we debug production without logs? | Distributed tracing, structured events, OpenTelemetry, real-user monitoring |
| **Developer Experience** | How fast can a new hire ship? | Pre-built dev environments, golden paths, internal developer platform |
| **Cost Efficiency** | What costs 10x what it should? | Spot instances, serverless-first, FinOps automation, reserved capacity |
| **Compliance** | What regulation might impact us next? | Data residency, customer-held keys, zero-knowledge proofs |
| **User Experience** | What's the 1% edge case that ruins trust? | Offline-first, graceful degradation, optimistic UI, skeleton screens |
| **AI Readiness** | Could an AI agent operate this system? | Structured logs as events, semantic API contracts, self-describing APIs |
| **Chaos Readiness** | What failure would our current design miss? | Dependency failure cascades, thundering herd, clock skew, DNS TTL poisoning |

---

## Proposal Format

Every proposal follows this strict structure:

```markdown
## Proposal #N: <Catchy Name>

### What It Is
1-2 sentences explaining the concept in plain English.

### Why It's Better
- Specific improvement over current approach
- Quantified where possible (e.g., "reduces P99 latency from 500ms to 50ms")
- Reference: who does this well (Netflix, Stripe, etc.)

### How It Works (High Level)
- Architecture sketch (no code, just pattern description)
- Key components and their relationships
- Data flow or state machine description

### System Trade-Offs
| Trade-Off | Impact |
|---|---|
| Complexity increase | <Low / Medium / High / Extreme> |
| New dependencies | <List of new services, libraries, infrastructure> |
| Learning curve | <Hours / Days / Weeks for team to ramp> |
| Operational burden | <New alerts, runbooks, on-call complexity> |
| Debugging difficulty | <Easier / Same / Harder / Much Harder> |

### Scope Impact
| Aspect | Impact |
|---|---|
| Features affected | <Which existing features must change> |
| New features required | <What we must build that wasn't planned> |
| Existing work invalidated | <What we must throw away or refactor> |
| Dependencies blocked | <What cannot proceed until this is done> |

### Timeline Impact
- **Best case**: +<N> sprints
- **Likely case**: +<N> sprints
- **Worst case**: +<N> sprints
- **Risk factors**: <What makes the worst case likely>

### When NOT to Do This
- If your team is <condition> (e.g., < 3 engineers, pre-revenue)
- If your timeline is <constraint> (e.g., must ship in 4 weeks)
- If you haven't solved <prerequisite> yet (e.g., basic monitoring)

### Maturity Gate
| Milestone | Prerequisite Before Starting This |
|---|---|
| <GATE 1> | <What must already be true> |
| <GATE 2> | <What must already be true> |

### Getting Started (Smallest Viable Step)
- If you want to try this without full commitment, start with:
  1. <Step 1 — minimal effort, maximum learning>
  2. <Step 2 — only if step 1 succeeds>

---

**Do you want me to implement this proposal?**
Reply with the proposal number(s) — e.g., "Do #1 and #3" — or "none for now."
```

---

## Innovation Patterns Library

The strategic creator should reference these proven patterns:

### Resilience Patterns
```
Pattern: Circuit Breaker with Adaptive Thresholds
→ Instead of fixed "3 failures → open", learn from traffic patterns
  and adjust thresholds dynamically using percentile-based anomaly detection
Trade-off: +2 sprints, requires ML model training pipeline, harder to debug
Best for: Mission-critical payment/auth services with variable traffic

Pattern: Cellular Architecture
→ Deploy isolated "cells" that don't share fate — one cell's outage
  never cascades to others. Each cell is self-contained with its own DB.
Trade-off: +4 sprints, operational complexity of N× deployments, data
  consistency challenges across cells. Higher infrastructure cost.
Best for: Multi-tenant platforms where tenant isolation is critical

Pattern: Request Hedging
→ Send requests to multiple replicas simultaneously, use fastest response.
  Protects against slow replicas, GC pauses, network jitter.
Trade-off: +1 sprint, 2-3x request volume on backend, higher compute cost
Best for: Latency-sensitive services where P99 matters more than cost
```

### Observability Patterns
```
Pattern: Structured Event Sourcing for Debugging
→ Every state change is an immutable event. Replay events to reproduce
  any bug. Never ask "what happened?" — the events tell you.
Trade-off: +3 sprints, significant schema design work, storage costs for
  event logs, team must learn event-driven thinking
Best for: Complex business logic, financial systems, audit-heavy domains

Pattern: Real User Monitoring (RUM) with Session Replay
→ Record real user sessions (anonymized). When an error occurs, watch
  exactly what the user did. No reproduction steps needed.
Trade-off: +1 sprint for integration, privacy/compliance review required,
  storage costs for session data, GDPR right-to-erasure complexity
Best for: B2C products where user-reported bugs are hard to reproduce
```

### Security Patterns
```
Pattern: Zero-Trust Service Mesh with mTLS
→ Every service-to-service call is mutually authenticated and encrypted.
  No implicit trust based on network location (same VPC ≠ safe).
Trade-off: +2 sprints, certificate rotation complexity, debugging encrypted
  traffic harder (need session keys), slight latency overhead (+2-5ms)
Best for: Regulated industries, multi-tenant platforms, PCI/HIPAA scope

Pattern: Customer-Held Encryption Keys (CHEK)
→ Customer controls encryption keys. You cannot decrypt their data.
  Truly zero-knowledge. Breach your DB → attacker gets ciphertext.
Trade-off: +4 sprints, key management UX complexity, losing a key = losing
  customer data permanently (no recovery), support burden
Best for: Healthcare, legal, financial, enterprise SaaS with security-conscious buyers
```

### Scalability Patterns
```
Pattern: CQRS + Event Sourcing
→ Separate read and write models. Writes are events. Reads are
  purpose-built projections optimized for specific queries.
Trade-off: +3 sprints, eventual consistency (stale reads possible),
  significantly more complex codebase, two data models to maintain
Best for: High-read systems, complex query patterns, audit trail requirements

Pattern: Edge Computing (CDN-Workers)
→ Run business logic at the edge (Cloudflare Workers, Lambda@Edge).
  Global distribution with sub-50ms latency for every user.
Trade-off: +2 sprints, runtime limitations (no long-running processes),
  limited language/runtime choices, harder local development experience
Best for: Global user base, latency-critical APIs, personalization/AB testing
```

### AI-Ready Patterns
```
Pattern: Semantic API Layer with OpenAPI + AI SDK
→ Every endpoint is fully described (OpenAPI 3.1). Generate SDKs for
  humans AND AI agents. AI can navigate your API without documentation.
Trade-off: +1 sprint, strict API discipline required, breaking changes are
  more painful (affects AI consumers), team must adopt contract-first dev
Best for: Platforms, public APIs, internal tools that AI agents will use

Pattern: Agent-Friendly State Machine Design
→ Every business process is a formal state machine with well-defined
  transitions. AI agents can reason about system state, predict outcomes,
  and suggest optimizations without understanding implementation details.
Trade-off: +2 sprints, rigid process design (hard to add ad-hoc states),
  team must learn state machine modeling, not all processes fit this model
Best for: Order management, approval workflows, CI/CD pipelines, incident response
```

---

## Strategic Question Bank

When the user invokes this skill without a specific focus, ask these questions in order:

### Round 1: Challenge Assumptions
```yaml
questions:
  - "What's the one thing in this design that, if it fails, takes down everything?"
  - "What assumption are we making that has never been explicitly tested?"
  - "If we had 10x the traffic tomorrow, what breaks first?"
  - "What would a malicious insider be able to access with current permissions?"
  - "What's the costliest decision we're making right now? Is it justified?"
```

### Round 2: Expand Vision
```yaml
questions:
  - "If a FAANG company built this, what would they do differently?"
  - "What's the version of this that would win a Stripe or Shopify-level customer?"
  - "What feature would make our users tell their friends about this?"
  - "What would make this system self-healing — no human intervention for common failures?"
  - "If we had to support 100x more services next year, would this architecture hold?"
```

### Round 3: Risk Awareness
```yaml
questions:
  - "What's the worst outage we could have with the current design? How long to recover?"
  - "Are we optimizing for the right thing? (Speed to market? Stability? Cost? Innovation?)"
  - "What happens if our cloud provider has a region-wide outage? Multi-region?"
  - "What compliance or regulatory change would break our current architecture?"
  - "What's the bus factor on this system? How many people would we lose if 2 engineers left?"
```

---

## Example: Strategic Review of a Payment Service

```markdown
## Strategic Review — payment-service (Currently: Phase 4, Pipeline Design)

Based on the PRD and pipeline design, I see these opportunities:

---

### Proposal #1: Idempotency Keys for Payment Deduplication

#### What It Is
Every payment request includes a client-generated idempotency key.
If the same request is retried (network timeout, user double-click, chaos pod-delete),
the system returns the cached result instead of charging twice.

#### Why It's Better
- Current design: "deduplication by transaction ID" but no client-side guarantee
- Double-charge risk during chaos pod-delete experiments = real financial liability
- Stripe and Adyen both require idempotency keys for exactly this reason
- Prevents the #1 customer support issue for payments: "I was charged twice"

#### System Trade-Offs
| Trade-Off | Impact |
|---|---|
| Complexity increase | Low — adds one header and a cache lookup |
| New dependencies | Redis/Memcached (already used for sessions) |
| Learning curve | Hours — well-understood pattern |
| Operational burden | Same — existing Redis monitoring covers this |
| Debugging difficulty | Same — idempotency key is logged in all requests |

#### Scope Impact
| Aspect | Impact |
|---|---|
| Features affected | POST /api/v1/payments endpoint |
| New features required | Idempotency key generation + validation middleware |
| Existing work invalidated | None — additive change |
| Dependencies blocked | None |

#### Timeline Impact
- **Best case**: +1 sprint (add middleware + tests)
- **Likely case**: +1 sprint
- **Worst case**: +2 sprints (if Redis schema changes needed)

#### When NOT to Do This
- If you have zero retry logic (no risk of duplicate requests — but you DO, from chaos)
- If your payment gateway already handles this (verify — most don't)

#### Getting Started
1. Add idempotency key header to API spec (1 hour)
2. Implement Redis-based key storage with 24h TTL (2 hours)
3. Add idempotency check before payment processing (1 hour)

**→ Accept this proposal? Requires: s04 (pipeline update) + s05 (service def update)**

---

### Proposal #2: Outbox Pattern for Reliable Event Publishing

#### What It Is
Instead of "process payment → publish event" (which can fail between the two),
write the event to an outbox table in the same database transaction as the payment.
A separate process reads the outbox and publishes events reliably.

#### Why It's Better
- Current design: if pod crashes between DB write and event publish, the event is lost
- Chaos experiments (pod-delete, container-kill) will expose this gap
- Lost events = downstream services (notification, analytics) have incomplete data
- This is THE most common reliability bug in microservices

#### System Trade-Offs
| Trade-Off | Impact |
|---|---|
| Complexity increase | Medium — new outbox table + publisher worker |
| New dependencies | None (uses existing Postgres + Kafka) |
| Learning curve | Days — team must understand exactly-once semantics |
| Operational burden | Medium — new component to monitor (outbox lag) |
| Debugging difficulty | Harder — events published asynchronously, harder to trace |

#### Scope Impact
| Aspect | Impact |
|---|---|
| Features affected | All event publishing (payment_completed, payment_failed) |
| New features required | Outbox table, publisher worker, dead-letter queue |
| Existing work invalidated | Must migrate existing event publishing code |
| Dependencies blocked | Downstream services must handle potential event duplication |

#### Timeline Impact
- **Best case**: +2 sprints
- **Likely case**: +3 sprints
- **Worst case**: +4 sprints (if downstream services need fixes for at-least-once semantics)

#### When NOT to Do This
- If event loss is acceptable (but it's not — affects billing and analytics)
- If you have < 2 backend engineers (this adds a component to maintain)

#### Getting Started
1. Add outbox table to schema (CREATE TABLE outbox ...) — 1 hour
2. Implement dual-write in payment transaction (1 day)
3. Build simple publisher worker with Kafka (2 days)

**→ Accept this proposal? Requires: s04 (pipeline) + s14 (experiment design update)**

---

### Proposal #3: Multi-Region Active-Active with CRDT-Based Conflict Resolution

#### What It Is
Run payment-service in two AWS regions simultaneously. Users route to
the nearest region. Payments can be initiated in either region and
Conflict-Free Replicated Data Types (CRDTs) handle concurrent writes.

#### Why It's Better
- Current design: single region → any AWS us-east-1 outage = payments down
- RTO from DR plan is 5 minutes — active-active reduces this to 0
- Survives not just pod failures but ENTIRE REGION failures
- Enterprise customers demand this for their SLA

#### System Trade-Offs
| Trade-Off | Impact |
|---|---|
| Complexity increase | Extreme — CRDTs are hard, eventual consistency everywhere |
| New dependencies | Multi-region Postgres (CockroachDB or Yugabyte), global load balancer |
| Learning curve | Weeks — CRDTs, multi-region consistency, conflict resolution |
| Operational burden | High — 2x infrastructure, inter-region networking, DR drills |
| Debugging difficulty | Much Harder — timing-dependent bugs, eventual consistency surprises |

#### Scope Impact
| Aspect | Impact |
|---|---|
| Features affected | Every write operation (payments, refunds, disputes) |
| New features required | CRDT library, conflict resolution UI, region-aware routing |
| Existing work invalidated | Entire database layer — must migrate from single Postgres to distributed |
| Dependencies blocked | All downstream services — must handle multi-region events |

#### Timeline Impact
- **Best case**: +6 sprints
- **Likely case**: +8 sprints
- **Worst case**: +12 sprints (conflict resolution edge cases multiply)
- **Risk factor**: 1 CRDT bug = data corruption that can't be fixed with a migration

#### When NOT to Do This
- If you haven't mastered single-region resilience first (you haven't — s20 hasn't run yet)
- If you have fewer than 6 senior backend engineers
- If your revenue doesn't justify the infrastructure cost (2x cloud bill)
- **If your customers haven't explicitly demanded multi-region SLAs**

#### Maturity Gate
| Milestone | Prerequisite |
|---|---|
| Single-region resilience score ≥ 95 | Must pass ALL chaos experiments (s14-s20) |
| Single-region game day completed | Must prove single-region recovery works |
| Customer demand validated | Talk to 5+ enterprise prospects before committing |

#### Getting Started (if you still want this)
1. Read "Designing Data-Intensive Applications" chapters 5, 8, 9 (2 weeks)
2. Build a multi-region prototype with CockroachDB Serverless (1 week)
3. Run the full chaos suite against it (1 week)

**→ Accept this proposal?**
⚠️ STRONG RECOMMENDATION: Do NOT accept this yet.
Complete s14-s20 first. Revisit when resilience score ≥ 95.

---
```

---

## Rules of Engagement

1. **Never implement** — This skill produces conversation only. If the user accepts a proposal, dispatch to the relevant skill (s01 for spec changes, s04 for pipeline changes, etc.)

2. **Always warn** — Every proposal must include "When NOT to Do This" and explicit trade-offs. No proposal is pure upside.

3. **Quantify when possible** — "Faster" is weak. "Reduces P99 from 500ms to 50ms" is strong.

4. **Respect maturity gates** — Don't propose active-active before single-region resilience is proven. Don't propose AI SDK before API contracts exist.

5. **Reference the best** — Cite who does this well (Netflix, Stripe, Shopify, etc.) to ground proposals in reality, not theory.

6. **Start small** — Every proposal must include a "Smallest Viable Step" — the minimum thing to try before committing fully.

7. **Know when to stop** — If the user says "none for now" or "let's keep it simple", respect that. Not every project needs every innovation.

---

## Dispatch Rules (When User Accepts a Proposal)

```yaml
dispatch_map:
  spec_changes: s01 (BA Requirements — update PRD/ADRs)
  pipeline_changes: s04 (Pipeline Design)
  architecture_changes: s01 (new ADR) + s05 (service onboarding update)
  security_changes: s11 (Security Scanning) + s24 (Policy Governance)
  resilience_changes: s14 (Experiment Design) + s16 (Blast Radius)
  observability_changes: s22 (Observability Integration)
  cost_changes: s25 (Cloud Cost Management)
  compliance_changes: s30 (Compliance & Audit)
  multi_skill_changes: s00 (Orchestrator — replan affected phases)

protocol:
  on_acceptance:
    - Record the accepted proposal in workflow context
    - Dispatch to the FIRST affected skill
    - That skill updates its artifacts
    - The orchestrator then replans downstream phases
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | Advisory only -- AI proposes, never implements |
| Target | L1 | Permanently L1 by design (strategic advisory, not autonomous) |

### Harness AI Agent

**Agent**: None (advisory by design)
**Capabilities**:
- Innovation dimension exploration
- Proposal generation with trade-offs
- Challenge assumption analysis
- Strategic question bank

### Human Gates

- ALL proposals require explicit user acceptance before dispatch to implementation skills

### Notes

This skill is permanently L1 by design. Strategic creativity requires human judgment and cannot be safely automated.

---

## Success Criteria
- [ ] At least 3 innovation dimensions explored (not just "make it faster")
- [ ] Every proposal includes all 5 sections (What, Why, Trade-offs, Scope, Timeline)
- [ ] Every proposal includes "When NOT to Do This"
- [ ] No code, YAML, or files written by this skill
- [ ] User explicitly accepts or declines each proposal
- [ ] Accepted proposals dispatched to correct implementation skill
- [ ] Risk tolerance (from s02 taste) respected — don't propose high-risk patterns to risk-averse teams
- [ ] Purely advisory — the user always makes the final call

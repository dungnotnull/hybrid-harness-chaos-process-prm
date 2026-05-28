# Design Spec: s33 System Optimization (s33)

**Date**: 2026-05-28
**Status**: Approved
**Author**: s33 design session
**Scope**: New optional skill -- callable at any phase

---

## Summary

Create skill s33 (system-optimization), an L2 advisory + artifact generation skill covering 7 modules: request latency deep-dive, N+1 query detection, concurrent user stress testing, atomicity verification, concurrency auditing (rate limits, locks, queues, race conditions), security vulnerability auditing, and agent-proposed evaluations. Callable at any workflow phase. Produces executable artifacts (k6 scripts, SQLMap/ZAP configs, custom audit scripts) alongside analysis reports.

---

## Skill Identity

| Field | Value |
|---|---|
| Name | `system-optimization` |
| Number | s33 |
| Phase | Any (callable anytime, like s31/s32) |
| Autonomy | L2 (Advisory + Artifact Generation) |
| AI Agent | Test Agent (M1/M3), AppSec/STO Agent (M6), SRE Agent (M4/M5) |
| Triggers | "optimize", "latency", "slow request", "N+1", "stress test", "CCU", "atomicity", "race condition", "rate limit", "security audit", "system audit", "bottleneck" |

---

## Module Architecture

7 modules execute sequentially with cross-module intelligence. Default runs all 7; user can target specific modules.

| # | Module | Focus | Primary Artifacts |
|---|---|---|---|
| M1 | Request Latency Deep-Dive | P50/P95/P99, slow endpoint root cause | k6 + OTEL trace analysis scripts |
| M2 | N+1 Query Detection | ORM query audit, query count baselines | ORM-specific detection configs |
| M3 | Concurrent User Stress Test | N CCU simulation, breaking point | k6 stress/spike test scripts |
| M4 | Atomicity Verification | Transaction boundaries, partial writes | Custom audit scripts |
| M5 | Concurrency Audit | Rate limits, locks, queues, race conditions | Custom code audit scripts |
| M6 | Security Vulnerability Audit | OWASP Top 10, SQL injection, XSS | SQLMap/ZAP/semgrep configs |
| M7 | Agent-Proposed Evaluations | AI-identified gaps beyond M1-M6 | Varies per finding |

### Cross-Module Data Flow

```
M1 (latency findings)      → M2 (N+1 may explain slow endpoints)
M2 (query counts)          → M3 (shapes stress test scenarios)
M3 (stress results)        → M5 (concurrency issues surface under load)
M4 (atomicity issues)      → M5 (transaction bugs inform race condition checks)
M5 (concurrency findings)  → M6 (race conditions may indicate auth bypass paths)
M6 (security findings)     → M7 (may trigger deeper investigation)
M7 (agent proposals)       → loops back to relevant M1-M6 for deeper dives
```

### Execution Modes

| Mode | Syntax | Behavior |
|---|---|---|
| `full` | `/s33` or `/s33 full` | Runs M1 through M7 sequentially (default) |
| `targeted` | `/s33 latency n+1 stress` | Runs only specified modules with cross-module intelligence |
| `single` | `/s33 stress` | Runs one module standalone |

---

## Module Specifications

### M1: Request Latency Deep-Dive

**Protocol:**
1. Collect endpoint response time data (Prometheus `http_request_duration_seconds` or OTEL traces)
2. Classify endpoints into 4 tiers: Healthy (P99 < SLA), Warning (P99 < 2x SLA), Slow (P99 < 5x SLA), Critical (P99 > 5x SLA)
3. For each Warning/Slow/Critical endpoint, trace root cause across 5 dimensions: Network, Compute, Storage, Dependency, Concurrency
4. Generate remediation plan per slow endpoint with priority ranking

**Artifacts:**
```
.commandcode/artifacts/optimization/latency/
    latency-baseline.json          -- Per-endpoint P50/P95/P99 with SLA comparison
    slow-request-traces.md         -- Root cause analysis for each slow endpoint
    prometheus-queries.yaml        -- Pre-built PromQL for ongoing monitoring
    otel-trace-analysis.js         -- k6 script to replay and measure slow paths
    remediation-plan.md            -- Prioritized fix list with effort estimates
```

### M2: N+1 Query Detection

**Protocol:**
1. Identify all ORM-backed endpoints from service definitions (s05)
2. Enable query logging per ORM framework: Prisma (`log: ['query']`), TypeORM (`logging: true`), Hibernate (`show_sql`), Django (`django.db.backends` DEBUG)
3. Execute representative request per endpoint (from s12 E2E tests or custom scenarios)
4. Count queries per request. Flag where `count > expected` threshold
5. Trace query chain to identify the eager/lazy boundary causing N+1
6. Propose fix: `include`/`select`/`join` optimization, DataLoader pattern, or caching

**Artifacts:**
```
.commandcode/artifacts/optimization/n-plus-one/
    query-audit-report.json        -- Per-endpoint query counts with N+1 flags
    orm-config-snippets.md         -- ORM-specific fixes per endpoint
    detection-script.<ext>         -- Automated N+1 detection for CI integration
    query-baselines.json           -- Expected query counts per endpoint for regression
```

### M3: Concurrent User Stress Test

**Protocol:**
1. Derive CCU targets from PRD (s01) and taste (s02). Default: 100, 500, 1000, 5000
2. Execute k6 test ladder: Ramp (1 to N), Sustain (hold N), Spike (5x N burst), Recovery (drop to N)
3. Capture: requests/sec, error rate %, P50/P95/P99 degradation, memory/CPU, DB connection pool, autoscaling timing
4. Identify breaking point and safe operating ceiling
5. Generate capacity plan with recommended max CCU

**Artifacts:**
```
.commandcode/artifacts/optimization/stress/
    k6-stress-test.js              -- k6 stress/spike script for N CCU
    stress-results.json            -- Full metric capture per CCU level
    breaking-point-analysis.md     -- Where system degrades and where it fails
    capacity-plan.md               -- Recommended CCU limits + scaling thresholds
    autoscaling-config.yaml        -- HPA/KEDA config based on findings
```

### M4: Atomicity Verification

**Protocol:**
1. Scan all write paths (CREATE/UPDATE/DELETE) in source code
2. Verify per write path: single-entity (transaction?), multi-entity (single tx or saga?), cross-service (compensating tx?), file+DB (outbox pattern?)
3. Identify 5 anti-patterns: partial writes, lost updates, phantom reads, orphan records, non-idempotent retries
4. Generate transaction boundary report with fix recommendations

**Artifacts:**
```
.commandcode/artifacts/optimization/atomicity/
    transaction-audit.json         -- Per-write-path atomicity assessment
    anti-pattern-report.md         -- Detected anti-patterns with code locations
    idempotency-checklist.md       -- Per-endpoint idempotency verification
    transaction-fixes.md           -- Recommended transaction boundary changes
```

### M5: Concurrency Audit

**Protocol:**
1. Rate Limits: check all public endpoints for rate limiting, verify granularity (per-user/IP/tenant), test bypass vectors
2. Locks: identify all lock usage, check ordering violations, timeout policies, deadlock potential via resource ordering graph
3. Queues: audit message queue configs, verify DLQ, retry backoff, poison message handling, depth monitoring
4. Exception Handling: trace propagation chains, identify swallowed exceptions, catch-all blocks, missing context, unhandled rejections
5. Race Conditions: identify shared mutable state, check TOCTOU vulnerabilities, concurrent collection modification, stale cache reads

**Artifacts:**
```
.commandcode/artifacts/optimization/concurrency/
    rate-limit-audit.json          -- Per-endpoint rate limiting status + bypass tests
    lock-analysis.json             -- Lock dependency graph with deadlock risk
    queue-audit.json               -- Queue config assessment with DLQ verification
    exception-handling-audit.md    -- Exception propagation analysis
    race-condition-report.md       -- Shared state analysis with TOCTOU flags
    remediation-plan.md            -- Prioritized fixes across all 5 sub-areas
```

### M6: Security Vulnerability Audit

**Protocol:**
1. Generate SQLMap configs for all parameterized endpoints
2. Generate ZAP scan configs for all user-facing endpoints
3. Run semgrep rules for OWASP Top 10 (A01-A10)
4. Cross-reference findings with s11 security scan results
5. Generate severity-ranked vulnerability report

**OWASP A01-A10 Coverage:**

| ID | Category | Check |
|---|---|---|
| A01 | Broken Access Control | Route guard analysis |
| A02 | Cryptographic Failures | Hardcoded secrets, weak algorithms |
| A03 | Injection | SQL/NoSQL/LDAP/command injection patterns |
| A04 | Insecure Design | Missing input validation, trust boundaries |
| A05 | Security Misconfiguration | CORS, headers, debug modes |
| A06 | Vulnerable Components | Known CVE dependencies (cross-ref s11) |
| A07 | Auth Failures | Brute force protection, session management |
| A08 | Data Integrity Failures | Insecure deserialization |
| A09 | Logging Failures | Sensitive data in logs, missing audit trail |
| A10 | SSRF | URL validation, internal service access controls |

**Artifacts:**
```
.commandcode/artifacts/optimization/security/
    sqlmap-config.yaml             -- SQLMap configs per endpoint
    zap-scan-config.yaml           -- ZAP automated scan config
    semgrep-rules.yaml             -- Custom semgrep rules for project patterns
    owasp-audit-report.json        -- Per-A01-A10 findings with severity
    vulnerability-matrix.md        -- Endpoint x vulnerability type matrix
    remediation-plan.md            -- Severity-ranked fix plan with effort estimates
```

### M7: Agent-Proposed Evaluations

**Protocol:**
1. After M1-M6, AI agent reviews ALL findings for cross-module patterns
2. Agent identifies gaps: patterns across modules, domain-specific checks, architecture concerns, data integrity
3. Each proposal follows s31-style format: What, Why, Trade-offs, Smallest Viable Step
4. User selects which proposals to execute
5. Selected proposals generate artifacts or loop back to M1-M6 for deeper investigation

**Artifacts:**
```
.commandcode/artifacts/optimization/agent-proposed/
    gap-analysis.md                -- Cross-module pattern analysis
    proposals.md                   -- Agent-generated investigation proposals
    selected-investigations/       -- Artifacts from user-selected proposals
```

### Final Consolidation

After all selected modules complete:

```
.commandcode/artifacts/optimization/
    SYSTEM-OPTIMIZATION-REPORT.md  -- Master report: executive summary + all findings
    remediation-backlog.json       -- Prioritized fix list across all modules
    severity-matrix.md             -- Module x Severity heatmap
    cross-module-findings.md       -- Findings that span multiple modules
```

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Target scope (service, endpoint, or full system) | User prompt | Yes |
| Module selection (full/targeted/single) | User prompt or default `full` | Yes |
| Service definitions and endpoints | s05 | Yes |
| Performance SLAs (P99, error rate, throughput) | s01 NFRs | Yes |
| Security scan results | s11 | No |
| Performance baseline | s13 | No |
| Taste preferences | s02 | Yes |
| ORM/database type | s05 or s01 | No (auto-detected) |
| Expected CCU range | s01 PRD | No (default: 100, 500, 1000, 5000) |
| Current workflow phase | s00 | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Module artifacts (per M1-M7) | `.commandcode/artifacts/optimization/` | Mixed |
| System Optimization Report | `.commandcode/artifacts/optimization/` | Markdown |
| Remediation backlog | s01, s28 | JSON |
| Stress test scripts | s04 CI pipeline | JavaScript (k6) |
| Security audit configs | s11 | YAML |
| Concurrency fixes | Codebase PRs | Code |
| Capacity recommendations | s25, s05 | Markdown |

---

## Execution Protocol

```
PHASE 0: SCOPE
  Parse user intent -> determine module selection
  Load s05 (services), s01 (SLAs), s02 (taste)
  Auto-detect tech stack (ORM, DB, runtime)
  Present execution plan to user for approval

PHASE 1: MODULE EXECUTION (sequential, cross-module intelligence)
  For each selected module M(n):
    1. Load findings from M(1)..M(n-1) as context
    2. Execute module protocol
    3. Generate module artifacts
    4. Save to .commandcode/artifacts/optimization/<module>/
    5. Brief summary to user (pass/fail/critical findings count)

PHASE 2: AGENT PROPOSALS (M7)
  AI agent reviews ALL M1-M6 findings
  Identifies cross-module patterns and gaps
  Proposes additional investigations
  User selects which to execute
  Execute selected proposals (may loop back to M1-M6)

PHASE 3: CONSOLIDATION
  Merge all findings into System Optimization Report
  Generate severity heatmap (module x severity)
  Generate prioritized remediation backlog
  Identify cross-module findings (root causes spanning modules)
  Present executive summary to user

PHASE 4: DISPATCH
  Map findings to downstream skills
  User selects which remediation actions to pursue
  Dispatch to appropriate skills
```

---

## Skill Integration

| Skill | s33 Consumes | s33 Feeds Into |
|---|---|---|
| s01 | PRD NFRs, SLAs, backlog | Remediation backlog items |
| s02 | Tooling preferences, risk tolerance | New taste entries |
| s04 | Pipeline structure | New pipeline gates (latency, stress thresholds) |
| s05 | Service definitions, infra topology | Capacity recommendations, infra sizing |
| s11 | Existing vulnerability scan results | Deeper security audit configs, missed vulns |
| s13 | Performance baselines, k6 scripts | Stress test extensions, updated baselines |
| s14 | Chaos experiment context | Race conditions to chaos-test, concurrency scenarios |
| s25 | Cost data | Capacity/cost trade-off recommendations |
| s26 | Resilience scoring inputs | Optimization findings improve resilience score |
| s31 | Strategic context | Agent-proposed evaluations feed strategic thinking |
| s32 | Research backing | Findings may trigger deep research on fix approaches |

## Dispatch Map

```yaml
on_completion:
  latency_fixes_needed: s04 (pipeline update for monitoring gates)
  n_plus_one_fixes_needed: s01 (backlog update) -> code PR
  stress_capacity_issues: s05 (infra sizing) + s25 (cost planning)
  atomicity_bugs_found: s01 (critical backlog) -> code PR
  concurrency_bugs_found: s01 (critical backlog) -> s14 (chaos experiment design)
  security_vulns_found: s11 (security scan update) + s30 (compliance)
  agent_proposals_accepted: loop back to relevant module or dispatch to target skill

on_partial:
  user_wants_deeper_analysis: re-run specific module with refined scope
  user_wants_strategic_context: s31 (strategic creator)
  user_wants_research: s32 (deep research)
```

---

## AI Agent Integration

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI generates artifacts + analysis, human reviews and approves execution |
| Target | L2 | Permanent L2 -- optimization audits require human judgment for false positive triage |

### Harness AI Agent Coverage

| Agent | Modules | Rationale |
|---|---|---|
| Test Agent | M1, M3 | Shares k6 expertise with s12/s13 |
| AppSec/STO Agent | M6 | Shares security scanning with s11 |
| SRE Agent | M4, M5 | Transaction and concurrency analysis aligns with SRE domain |
| DevOps Agent | M2 | ORM and query optimization in application layer |

### Human Gates

- Module selection requires user approval before execution
- M7 agent proposals require explicit acceptance
- All generated artifacts require user review before dispatch
- Remediation dispatch requires user selection

---

## Triggers

```yaml
invoked_when:
  - User says: "optimize", "system optimization", "performance audit"
  - User says: "latency", "slow request", "why is X slow", "response time"
  - User says: "N+1", "query optimization", "database performance"
  - User says: "stress test", "load test N users", "CCU", "concurrent users"
  - User says: "atomicity", "transaction audit", "data consistency"
  - User says: "race condition", "deadlock", "rate limit", "concurrency bug"
  - User says: "security audit", "SQL injection", "XSS", "OWASP"
  - User says: "bottleneck", "system audit", "health check"
  - User explicitly invokes: /s33 or /system-optimization
  - User specifies module: /s33 latency, /s33 n+1 stress, /s33 security
```

---

## Success Criteria

- [ ] s33 callable from any phase or directly by user
- [ ] Full mode runs M1-M7 sequentially with cross-module intelligence
- [ ] Targeted mode runs user-selected modules with cross-module intelligence
- [ ] Single mode runs one module standalone
- [ ] Each module produces its prescribed artifacts
- [ ] Consolidation produces master System Optimization Report
- [ ] Agent proposals (M7) follow s31-style format with trade-offs
- [ ] Dispatch to downstream skills works on user selection
- [ ] Tech stack auto-detection for ORM/DB/runtime
- [ ] Taste preferences from s02 respected (tooling choices, depth)
- [ ] Cross-references with s11/s13/s14 bidirectional
- [ ] Generated k6 scripts executable without manual modification
- [ ] Generated security configs (SQLMap/ZAP/semgrep) runnable as-is
- [ ] Remediation backlog prioritized by severity x effort matrix

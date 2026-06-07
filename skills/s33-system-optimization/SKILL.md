---
name: system-optimization
description: >
  Execute comprehensive system optimization audits across 7 modules: request latency
  deep-dive, N+1 query detection, concurrent user stress testing, atomicity verification,
  concurrency auditing (rate limits, locks, queues, race conditions), security vulnerability
  auditing (OWASP Top 10), and agent-proposed evaluations. Produces executable artifacts
  (k6 scripts, SQLMap/ZAP configs, custom audit scripts) alongside analysis reports.
  Use this skill whenever the user says "optimize", "latency", "slow request", "N+1",
  "stress test", "CCU", "atomicity", "race condition", "rate limit", "security audit",
  "system audit", "bottleneck", or explicitly invokes /s33 or /system-optimization.
  This skill is callable at ANY phase in the workflow (s00-s32).
  Supports three execution modes: full (all modules), targeted (selected modules),
  and single (one module). Each module produces artifacts and feeds findings into
  subsequent modules for cross-module intelligence.
  L2 autonomy: AI generates artifacts and analysis, human reviews and approves execution.
---

# System Optimization Audit (s33)

## Purpose

Perform deep-dive system optimization across performance, data access, concurrency, security, and correctness dimensions. This skill goes beyond the baselines established by s13 (performance testing) and s11 (security scanning) to identify root causes of slowness, data integrity risks, and security gaps that standard scanning misses. Every module produces executable artifacts that can be integrated into CI pipelines or run ad-hoc.

**Unlike s31 (pure advisory) and s32 (pure research), s33 produces executable artifacts** -- k6 stress test scripts, SQLMap/ZAP configurations, ORM detection scripts, and custom audit tools that engineering teams can run immediately.

---

## Prerequisites
- [ ] Current phase context from s00 (Orchestrator)
- [ ] PRD from s01 for alignment verification
- [ ] Taste preferences from s02
- [ ] Service definitions from s05 for architecture analysis
- [ ] Security scan from s11 for vulnerability context
- [ ] Performance baselines from s13 (recommended for comparison)

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

## Execution Modes

| Mode | Syntax | Behavior |
|---|---|---|
| `full` | `/s33` or `/s33 full` | Runs M1 through M7 sequentially (default) |
| `targeted` | `/s33 latency n+1 stress` | Runs only specified modules with cross-module intelligence |
| `single` | `/s33 stress` | Runs one module standalone |

### Module Name Mapping

| Alias | Module |
|---|---|
| `latency` | M1: Request Latency Deep-Dive |
| `n+1`, `nplusone`, `queries` | M2: N+1 Query Detection |
| `stress`, `ccu`, `load` | M3: Concurrent User Stress Test |
| `atomicity`, `transactions` | M4: Atomicity Verification |
| `concurrency`, `locks`, `race` | M5: Concurrency Audit |
| `security`, `owasp`, `vulns` | M6: Security Vulnerability Audit |
| `agent`, `proposals` | M7: Agent-Proposed Evaluations |

---

## Cross-Module Data Flow

```
M1 (latency findings)      --> M2 (N+1 may explain slow endpoints)
M2 (query counts)          --> M3 (shapes stress test scenarios)
M3 (stress results)        --> M5 (concurrency issues surface under load)
M4 (atomicity issues)      --> M5 (transaction bugs inform race condition checks)
M5 (concurrency findings)  --> M6 (race conditions may indicate auth bypass paths)
M6 (security findings)     --> M7 (may trigger deeper investigation)
M7 (agent proposals)       --> loops back to relevant M1-M6 for deeper dives
```

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

## M1: Request Latency Deep-Dive

### Protocol

1. Collect endpoint response time data (Prometheus `http_request_duration_seconds` or OTEL traces)
2. Classify endpoints into 4 tiers:
   - **Healthy**: P99 < SLA target
   - **Warning**: P99 between SLA target and 2x SLA target
   - **Slow**: P99 between 2x and 5x SLA target
   - **Critical**: P99 > 5x SLA target
3. For each Warning/Slow/Critical endpoint, trace root cause across 5 dimensions:
   - **Network**: DNS resolution, TLS handshake, connection pooling, upstream latency
   - **Compute**: CPU hotspots, GC pressure, event loop blocking, thread pool saturation
   - **Storage**: Query execution plan, index coverage, connection pool exhaustion, disk I/O
   - **Dependency**: Downstream service latency, timeout cascades, retry storms
   - **Concurrency**: Lock contention, queue backlog, semaphore starvation
4. For each slow endpoint, identify the single dominant root cause
5. Generate remediation plan with priority ranking (Critical > Slow > Warning)

### Artifacts

```
.commandcode/artifacts/optimization/latency/
    latency-baseline.json          -- Per-endpoint P50/P95/P99 with SLA comparison
    slow-request-traces.md         -- Root cause analysis for each slow endpoint
    prometheus-queries.yaml        -- Pre-built PromQL for ongoing monitoring
    otel-trace-analysis.js         -- k6 script to replay and measure slow paths
    remediation-plan.md            -- Prioritized fix list with effort estimates
```

### Latency Root Cause Template

```markdown
## Endpoint: <METHOD> <path>

### Metrics
| Metric | Value | SLA Target | Status |
|---|---|---|---|
| P50 | <ms> | <ms> | <Healthy/Warning/Slow/Critical> |
| P95 | <ms> | <ms> | <Healthy/Warning/Slow/Critical> |
| P99 | <ms> | <ms> | <Healthy/Warning/Slow/Critical> |

### Root Cause Analysis
- **Dimension**: <Network/Compute/Storage/Dependency/Concurrency>
- **Evidence**: <specific trace/log/metric showing the issue>
- **Contributing factors**: <additional dimensions that compound the issue>

### Recommended Fix
- **Action**: <specific code/infra/config change>
- **Expected improvement**: <estimated P99 reduction>
- **Effort**: <hours/days>
- **Risk**: <what could go wrong applying this fix>
```

---

## M2: N+1 Query Detection

### Protocol

1. Identify all ORM-backed endpoints from service definitions (s05)
2. Enable query logging per ORM framework:
   - **Prisma**: `log: ['query']` with query duration
   - **TypeORM**: `logging: true` with query duration
   - **Hibernate**: `hibernate.show_sql` + `hibernate.format_sql`
   - **Django**: `django.db.backends` logger at DEBUG
   - **Sequelize**: `logging: true` in Sequelize options
   - **Go GORM**: `db.Debug()` or `logger.Config{LogLevel: logger.Info}`
3. Execute representative request per endpoint (from s12 E2E tests or custom scenarios)
4. Count queries per request. Flag where `count > expected` threshold
5. Trace query chain to identify the eager/lazy boundary causing N+1
6. Propose fix: `include`/`select`/`join` optimization, DataLoader pattern, or caching

### N+1 Detection Heuristics

| Pattern | Indicator | Severity |
|---|---|---|
| Classic N+1 | 1 SELECT for parent + N SELECTs for children in a loop | High |
| Batch-aware N+1 | SELECTs batched but still separate from parent query | Medium |
| Over-fetching | Single query but returns 10x+ more columns than needed | Medium |
| Under-fetching | Multiple round-trips due to missing `include`/`join` | High |
| Cartesian explosion | JOIN produces MxN rows instead of M+N | Critical |

### Artifacts

```
.commandcode/artifacts/optimization/n-plus-one/
    query-audit-report.json        -- Per-endpoint query counts with N+1 flags
    orm-config-snippets.md         -- ORM-specific fixes per endpoint
    detection-script.<ext>         -- Automated N+1 detection for CI integration
    query-baselines.json           -- Expected query counts per endpoint for regression
```

### Query Audit Report Schema

```json
{
  "endpoint": "GET /api/v1/orders",
  "total_queries": 47,
  "expected_queries": 3,
  "n_plus_one_detected": true,
  "severity": "High",
  "root_query": "SELECT * FROM orders WHERE user_id = ?",
  "loop_query": "SELECT * FROM order_items WHERE order_id = ?",
  "loop_count": 44,
  "fix": {
    "strategy": "eager_load",
    "orm_specific": "prisma: include: { orderItems: true }",
    "estimated_query_reduction": "47 -> 2"
  }
}
```

---

## M3: Concurrent User Stress Test

### Protocol

1. Derive CCU targets from PRD (s01) and taste (s02). Default ladder: 100, 500, 1000, 5000
2. Execute k6 test ladder with 4 phases:
   - **Ramp**: 1 to N CCU over configurable duration
   - **Sustain**: Hold N CCU for configurable duration
   - **Spike**: Sudden burst to 5x N CCU
   - **Recovery**: Drop back to N, measure recovery time
3. Capture 6 key metrics at each CCU level:
   - Requests/sec (throughput ceiling)
   - Error rate % at each CCU level
   - P50/P95/P99 latency degradation curve
   - Memory/CPU utilization of target service
   - Database connection pool usage
   - Autoscaling trigger timing (if applicable)
4. Identify breaking point (first CCU level where error rate > 1% or P99 > 10x baseline)
5. Determine safe operating ceiling (highest CCU where all metrics stay within SLA)
6. Generate capacity plan with recommended max CCU and scaling triggers

### Artifacts

```
.commandcode/artifacts/optimization/stress/
    k6-stress-test.js              -- k6 stress/spike script for N CCU
    stress-results.json            -- Full metric capture per CCU level
    breaking-point-analysis.md     -- Where system degrades and where it fails
    capacity-plan.md               -- Recommended CCU limits + scaling thresholds
    autoscaling-config.yaml        -- HPA/KEDA config based on findings
```

### k6 Stress Test Template

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const latency = new Trend('request_duration');

export const options = {
  stages: [
    // Phase 1: Ramp to target CCU
    { duration: '2m', target: __ENV.TARGET_CCU || 100 },
    // Phase 2: Sustain target CCU
    { duration: '5m', target: __ENV.TARGET_CCU || 100 },
    // Phase 3: Spike to 5x
    { duration: '30s', target: (__ENV.TARGET_CCU || 100) * 5 },
    // Phase 4: Recovery
    { duration: '2m', target: __ENV.TARGET_CCU || 100 },
  ],
  thresholds: {
    errors: ['rate<0.01'],
    http_req_duration: ['p(99)<5000'],
  },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

export default function () {
  const res = http.get(`${BASE_URL}/api/v1/health`);
  errorRate.add(res.status !== 200);
  latency.add(res.timings.duration);
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

### Breaking Point Analysis Template

```markdown
## Stress Test: Breaking Point Analysis

### Test Configuration
- Target CCU: <N>
- Spike CCU: <5x N>
- Duration: <total>
- Service: <name>

### Results Matrix
| CCU Level | Req/sec | Error Rate | P50 (ms) | P95 (ms) | P99 (ms) | Status |
|---|---|---|---|---|---|---|
| <N> | <val> | <val>% | <val> | <val> | <val> | PASS/DEGRADED/FAILED |

### Breaking Point
- **First degradation at**: <N> CCU (<symptom>)
- **Hard failure at**: <N> CCU (<symptom>)

### Safe Operating Ceiling
- **Recommended max CCU**: <N>
- **Recommended scaling trigger**: <metric> at <threshold>
```

---

## M4: Atomicity Verification

### Protocol

1. Scan all write paths (CREATE/UPDATE/DELETE operations) in source code
2. For each write path, verify:
   - **Single-entity writes**: Wrapped in transaction?
   - **Multi-entity writes**: Single transaction or saga pattern?
   - **Cross-service writes**: Compensating transaction exists?
   - **File + DB writes**: Wrapped in outbox pattern?
3. Identify 5 atomicity anti-patterns:
   - **Partial writes**: Two DB updates without shared transaction
   - **Lost updates**: Read-modify-write without optimistic locking
   - **Phantom reads**: Range queries without proper isolation level
   - **Orphan records**: Child created after parent commit fails
   - **Non-idempotent retries**: Retry creates duplicate instead of dedup
4. For each anti-pattern found, document the code location, affected data, and fix
5. Generate transaction boundary report with fix recommendations

### Artifacts

```
.commandcode/artifacts/optimization/atomicity/
    transaction-audit.json         -- Per-write-path atomicity assessment
    anti-pattern-report.md         -- Detected anti-patterns with code locations
    idempotency-checklist.md       -- Per-endpoint idempotency verification
    transaction-fixes.md           -- Recommended transaction boundary changes
```

### Transaction Audit Schema

```json
{
  "write_path": "POST /api/v1/orders",
  "operations": [
    { "type": "INSERT", "entity": "orders", "in_transaction": true },
    { "type": "INSERT", "entity": "order_items", "in_transaction": false },
    { "type": "UPDATE", "entity": "inventory", "in_transaction": false },
    { "type": "PUBLISH", "entity": "order_created_event", "in_transaction": false }
  ],
  "atomicity_risk": "Critical",
  "anti_patterns": ["partial_write", "non_idempotent_retry"],
  "fix": {
    "strategy": "wrap_in_transaction",
    "description": "Wrap orders + order_items in single transaction. Use outbox pattern for event.",
    "estimated_effort": "4 hours"
  }
}
```

---

## M5: Concurrency Audit

### Protocol

Audit 5 concurrency dimensions:

#### 5.1 Rate Limits
- Check all public endpoints for rate limiting middleware/guard
- Verify granularity: per-user, per-IP, per-tenant
- Test bypass vectors: header spoofing (`X-Forwarded-For`), parameter pollution, path case variation

#### 5.2 Locks
- Identify all lock usage (mutex, semaphore, distributed locks like Redis RedLock)
- Build lock dependency graph
- Check for: lock ordering violations, lock timeout policies, deadlock potential (cycle detection in dependency graph)

#### 5.3 Queues
- Audit message queue configurations (Kafka, RabbitMQ, SQS, Redis streams)
- Verify: DLQ exists, retry policy has exponential backoff, poison message handling, queue depth monitoring alert

#### 5.4 Exception Handling
- Trace exception propagation chains through all layers
- Identify: swallowed exceptions (`catch {}`), catch-all blocks (`catch (e) {}` with no action), missing error context, unhandled promise rejections

#### 5.5 Race Conditions
- Identify shared mutable state (global variables, static fields, singleton caches)
- Check for: TOCTOU vulnerabilities (time-of-check-time-of-use), concurrent collection modification, stale cache reads after writes, unsafe increment/decrement operations

### Artifacts

```
.commandcode/artifacts/optimization/concurrency/
    rate-limit-audit.json          -- Per-endpoint rate limiting status + bypass tests
    lock-analysis.json             -- Lock dependency graph with deadlock risk
    queue-audit.json               -- Queue config assessment with DLQ verification
    exception-handling-audit.md    -- Exception propagation analysis
    race-condition-report.md       -- Shared state analysis with TOCTOU flags
    remediation-plan.md            -- Prioritized fixes across all 5 sub-areas
```

### Rate Limit Audit Schema

```json
{
  "endpoint": "POST /api/v1/login",
  "rate_limited": true,
  "granularity": "per-IP",
  "limit": "10 requests/minute",
  "bypass_vectors": [
    {
      "type": "header_spoofing",
      "header": "X-Forwarded-For",
      "exploitable": true,
      "fix": "Use trusted proxy configuration and client certificate for identification"
    }
  ],
  "severity": "High"
}
```

---

## M6: Security Vulnerability Audit

### Protocol

1. Generate SQLMap configs for all parameterized endpoints
2. Generate ZAP scan configs for all user-facing endpoints
3. Apply semgrep rules for OWASP Top 10 (A01-A10):
   - **A01 Broken Access Control**: Route guard analysis, IDOR detection, privilege escalation paths
   - **A02 Cryptographic Failures**: Hardcoded secrets, weak algorithms (MD5, SHA1), missing TLS, key length below 2048
   - **A03 Injection**: SQL/NoSQL/LDAP/command injection patterns, unsanitized user input in queries
   - **A04 Insecure Design**: Missing input validation, absent trust boundaries, mass assignment
   - **A05 Security Misconfiguration**: CORS wildcards, missing security headers, debug modes enabled, default credentials
   - **A06 Vulnerable Components**: Known CVE dependencies (cross-reference s11 scan results)
   - **A07 Auth Failures**: Missing brute force protection, weak password policy, session fixation, token not rotated
   - **A08 Data Integrity Failures**: Insecure deserialization, unsigned JWTs, missing CSRF tokens
   - **A09 Logging Failures**: Sensitive data in logs (PII, tokens), missing audit trail for write operations
   - **A10 SSRF**: URL validation gaps, internal service access controls, metadata endpoint exposure
4. Cross-reference findings with s11 security scan results (deduplicate, escalate if both found)
5. Generate severity-ranked vulnerability report with effort-to-fix estimates

### Artifacts

```
.commandcode/artifacts/optimization/security/
    sqlmap-config.yaml             -- SQLMap configs per endpoint
    zap-scan-config.yaml           -- ZAP automated scan config
    semgrep-rules.yaml             -- Custom semgrep rules for project patterns
    owasp-audit-report.json        -- Per-A01-A10 findings with severity
    vulnerability-matrix.md        -- Endpoint x vulnerability type matrix
    remediation-plan.md            -- Severity-ranked fix plan with effort estimates
```

### OWASP Finding Schema

```json
{
  "id": "OWASP-A03-001",
  "category": "A03 Injection",
  "severity": "Critical",
  "endpoint": "GET /api/v1/users/search",
  "parameter": "query",
  "evidence": "User input passed directly to SQL LIKE clause without parameterization",
  "location": "src/services/user.service.ts:42",
  "remediation": "Use parameterized query: db.query('SELECT * FROM users WHERE name LIKE ?', [`%${query}%`])",
  "effort": "1 hour",
  "cross_ref_s11": false
}
```

---

## M7: Agent-Proposed Evaluations

### Protocol

1. After M1-M6 complete, AI agent reviews ALL findings holistically
2. Agent identifies gaps and proposes additional investigations:
   - **Cross-module patterns**: Findings that span modules and suggest deeper root causes
   - **Domain-specific checks**: Based on detected technology stack (e.g., Redis key expiration audit, Kafka consumer lag analysis, connection pool tuning)
   - **Architecture concerns**: Single points of failure, missing circuit breakers, absence of bulkhead pattern
   - **Data integrity**: Foreign key enforcement gaps, cascading delete safety, constraint violations under concurrency
3. Each proposal follows s31-style format:

```markdown
## Proposal #N: <Title>

### What It Is
1-2 sentences explaining the investigation.

### Why It Matters
- Connection to existing findings from M<n>
- Specific risk if left uninvestigated
- Who else has hit this (industry reference)

### Trade-Offs
| Trade-Off | Impact |
|---|---|
| Investigation effort | <hours/days> |
| New tooling needed | <yes/no, what> |
| Risk of false positive | <low/medium/high> |

### Smallest Viable Step
1. <Step 1: minimal effort, maximum learning>
2. <Step 2: only if step 1 reveals issues>

---

**Accept this proposal?** Reply with proposal number or "skip".
```

4. User selects which proposals to execute
5. Selected proposals either:
   - Generate additional artifacts in `.commandcode/artifacts/optimization/agent-proposed/`
   - Loop back to relevant M1-M6 for deeper investigation with refined scope

### Artifacts

```
.commandcode/artifacts/optimization/agent-proposed/
    gap-analysis.md                -- Cross-module pattern analysis
    proposals.md                   -- Agent-generated investigation proposals
    selected-investigations/       -- Artifacts from user-selected proposals
```

---

## Final Consolidation

After all selected modules complete, produce:

```
.commandcode/artifacts/optimization/
    SYSTEM-OPTIMIZATION-REPORT.md  -- Master report: executive summary + all findings
    remediation-backlog.json       -- Prioritized fix list across all modules
    severity-matrix.md             -- Module x Severity heatmap
    cross-module-findings.md       -- Findings that span multiple modules
```

### System Optimization Report Template

```markdown
# System Optimization Report: <scope>

**Date**: YYYY-MM-DD
**Modules Executed**: M1, M2, ..., M<n>
**Scope**: <service/endpoint/full system>

---

## Executive Summary

<1 paragraph: top 3 findings, overall health assessment, recommended next action>

## Severity Distribution

| Module | Critical | High | Medium | Low | Info |
|---|---|---|---|---|---|
| M1 Latency | <n> | <n> | <n> | <n> | <n> |
| M2 N+1 Queries | <n> | <n> | <n> | <n> | <n> |
| M3 Stress | <n> | <n> | <n> | <n> | <n> |
| M4 Atomicity | <n> | <n> | <n> | <n> | <n> |
| M5 Concurrency | <n> | <n> | <n> | <n> | <n> |
| M6 Security | <n> | <n> | <n> | <n> | <n> |
| M7 Agent | <n> | <n> | <n> | <n> | <n> |

## Top 10 Remediation Items

| # | Module | Severity | Finding | Effort | Impact |
|---|---|---|---|---|---|
| 1 | <M<n>> | <sev> | <description> | <hours> | <what fixing it achieves> |

## Cross-Module Findings

<Findings that span multiple modules, indicating systemic issues>

## Recommendations

<Overall system health assessment and strategic recommendations>
```

### Remediation Backlog Schema

```json
{
  "generated_at": "YYYY-MM-DDTHH:mm:ssZ",
  "total_findings": 0,
  "items": [
    {
      "id": "OPT-001",
      "module": "M1",
      "severity": "Critical",
      "title": "<finding title>",
      "description": "<finding details>",
      "location": "<file:line or endpoint>",
      "effort": "<hours/days>",
      "dispatch_to": "s01",
      "priority_score": 95
    }
  ]
}
```

Priority score formula: `severity_weight * impact_weight * (1 / effort_weight)`

---

## Skill Integration

### Feeds Into

| Target Skill | What Gets Passed |
|---|---|
| s01 (BA Requirements) | Remediation backlog items, new NFRs discovered |
| s04 (Pipeline Design) | New pipeline gates (latency thresholds, stress test stages) |
| s05 (Service Onboarding) | Capacity recommendations, infra sizing updates |
| s11 (Security Scanning) | Deeper security audit configs, missed vulnerability patterns |
| s13 (Performance Testing) | Stress test extensions, updated performance baselines |
| s14 (Experiment Design) | Race conditions to chaos-test, concurrency fault scenarios |
| s25 (Cloud Cost) | Capacity/cost trade-off recommendations |
| s26 (Resilience Scoring) | Optimization findings to improve resilience score |
| s28 (Release Management) | Remediation backlog for release planning |
| s31 (Strategic Creator) | Agent-proposed evaluations feed strategic thinking |
| s32 (Deep Research) | Findings may trigger deep research on fix approaches |

### Consumes From

| Source | What It Provides |
|---|---|
| s00 | Context, current phase, workflow state |
| s01 | PRD, NFRs, SLAs, specifications |
| s02 | Taste preferences (tooling, depth, risk tolerance) |
| s05 | Service definitions, endpoints, infra topology |
| s11 | Existing security scan results (cross-reference) |
| s13 | Performance baselines, existing k6 scripts |

### Dispatch Map

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

## Rules of Engagement

1. **Evidence over opinion** -- Every finding must include specific evidence (metric value, code location, test result). Replace "this endpoint is slow" with "P99 latency is 3400ms, SLA target is 500ms, root cause: missing index on orders.user_id."

2. **Actionable artifacts** -- Every generated artifact must be runnable without manual modification. k6 scripts must execute with `k6 run script.js`. SQLMap configs must run with `sqlmap -c config.yaml`.

3. **Cross-module intelligence** -- Findings from earlier modules inform later modules. M2 N+1 results shape M3 stress scenarios. M3 stress results surface M5 concurrency issues. Never treat modules as independent.

4. **Severity requires evidence** -- Do not mark a finding as Critical or High without concrete evidence. If you suspect an issue but cannot prove it, mark as "Needs Investigation" with Medium severity.

5. **False positive awareness** -- Acknowledge when a finding might be a false positive. Include "Confidence: High/Medium/Low" for each finding.

6. **Respect scope** -- If user targeted only M1 and M3, do not silently run M2. Execute exactly what was requested.

7. **Taste-aware execution** -- Load s02 preferences. Use preferred tooling (k6 vs Locust, Semgrep vs CodeQL). Respect depth preference (quick scan vs deep analysis).

8. **No destructive actions** -- This skill audits and generates artifacts. It does NOT modify production systems, drop tables, or execute exploits. All security tests generate configs for human-reviewed execution.

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L2 | AI generates artifacts + analysis, human reviews and approves execution |
| Target | L2 | Permanent L2 -- optimization audits require human judgment for false positive triage |

### Harness AI Agent
**Agent**: Multi-agent

| Agent | Modules | Rationale |
|---|---|---|
| Test Agent | M1, M3 | Shares k6 expertise with s12/s13 |
| AppSec/STO Agent | M6 | Shares security scanning with s11 |
| SRE Agent | M4, M5 | Transaction and concurrency analysis aligns with SRE domain |
| DevOps Agent | M2 | ORM and query optimization in application layer |

### Human Gates

- Module selection requires user approval before execution
- M7 agent proposals require explicit acceptance per proposal
- All generated artifacts require user review before dispatch
- Remediation dispatch requires user selection

### Notes

This skill is permanently L2 by design. System optimization findings require human judgment for:
- False positive triage (automated tools report noise)
- Business context (a "slow" endpoint may be acceptable for batch operations)
- Risk tolerance (some fixes carry deployment risk)
- Priority decisions (effort vs impact trade-offs)

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

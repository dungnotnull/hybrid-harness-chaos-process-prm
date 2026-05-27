---
name: ba-requirements-analysis
description: >
  Professional Business Analyst skill for deep project and requirements analysis.
  Use this skill whenever the user says "analyze my project", "gather requirements",
  "what should I build", "design a system for", "create a PRD", "spec out",
  "define scope", "requirements engineering", or starts a new initiative that
  needs structured analysis before implementation. Also trigger at the beginning
  of any new workflow phase. This skill asks targeted questions, identifies gaps,
  generates precise concrete specifications, and produces a complete PRD that
  feeds into all downstream skills.
---

# BA Requirements Analysis (s01)

## Purpose
Act as an experienced Business Analyst to deeply understand the user's project context, ask probing questions that surface hidden requirements and constraints, identify risks and dependencies, and produce a rigorous Product Requirements Document (PRD) that serves as the single source of truth for all downstream engineering skills.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| User project description | User prompt or s00 context | Yes |
| Taste preferences | `.commandcode/taste/taste.md` | No |
| Previous PRDs (if iterating) | s25 postmortem feedback | No |
| Existing codebase artifacts | Repository scan | No |
| Team/stakeholder info | User or org context | Recommended |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Product Requirements Document (PRD) | `.commandcode/prd.md` | Markdown |
| Architecture Decision Records (ADRs) | `.commandcode/adr/` | Markdown (one per decision) |
| Prioritized backlog | `.commandcode/backlog.md` | Markdown checklist |
| Structured context for s04 + s12 | Workflow context object | YAML |
| Risk register | Included in PRD | Table |

---

## BA Analysis Framework

```
DISCOVER → DIAGNOSE → DEFINE → DELIVER

Discover:  Ask open-ended questions, scan codebase, understand domain
Diagnose:  Identify gaps, contradictions, ambigious requirements
Define:    Write concrete specifications with acceptance criteria
Deliver:   Produce PRD + ADRs + prioritized backlog
```

---

## Phase 1: Discovery (The Interview)

Ask targeted questions organized by concern area. Never ask all at once — use progressive disclosure:

### Opening Questions (always start here)
```yaml
questions:
  - "What problem does this project solve? Who is the primary user?"
  - "What does success look like in 3 months? In 12 months?"
  - "What existing systems or codebases does this integrate with?"
  - "Who are the stakeholders and what are their priorities?"
  - "What are the non-negotiable constraints (deadline, budget, compliance)?"
```

### Domain Deep-Dive (after opening context is clear)
```yaml
questions:
  - "Walk me through the critical user journey from end to end."
  - "What are the top 3 failure modes you're worried about?"
  - "What's the expected scale (users, requests/sec, data volume)?"
  - "What SLAs or SLOs are required (availability, latency, throughput)?"
  - "What regulatory or compliance requirements apply (SOC2, HIPAA, GDPR)?"
  - "Are there existing runbooks, playbooks, or incident patterns I should know about?"
```

### Technical Discovery (for engineering-focused projects)
```yaml
questions:
  - "What's the tech stack? Any constraints on language, framework, cloud?"
  - "Kubernetes? Serverless? VM-based? What's the deployment target?"
  - "What CI/CD system is in place? Harness? GitHub Actions? Jenkins?"
  - "What observability tools exist (Prometheus, Datadog, New Relic)?"
  - "Is there an existing chaos/resilience practice? What's been tested?"
  - "What's the team composition? Who owns what?"
```

### Chaos-Specific Discovery
```yaml
questions:
  - "What keeps you up at night about this system's reliability?"
  - "When was the last major incident? What failed?"
  - "Which components do you suspect are the weakest links?"
  - "What blast radius is acceptable in dev? staging? production?"
  - "Do you have metrics to measure resilience today?"
  - "What recovery procedures exist and have they been tested?"
```

### Gap Detection (probe for what's missing)
```yaml
gap_patterns:
  - "You mentioned X but didn't mention Y — is Y handled or is it a gap?"
  - "If [worst-case scenario] happens, what's the current recovery plan?"
  - "Who gets paged when this fails? Do they have the runbooks they need?"
  - "Has this been load tested? Chaos tested? Pen tested?"
  - "What metrics would tell you this feature is working correctly?"
```

---

## Phase 2: Requirements Specification

Transform ambiguous descriptions into precise, testable requirements:

### Requirement Format
```markdown
## REQ-<CATEGORY>-<NUMBER>: <Title>
**Priority**: P0 (must) | P1 (should) | P2 (could) | P3 (won't-now)
**Type**: Functional | Non-Functional | Constraint | Risk
**Stakeholder**: <name/role>
**Depends On**: REQ-xxx (or none)
**Acceptance Criteria**:
- [ ] Given <precondition>, when <action>, then <expected outcome>
- [ ] Measurable threshold: <metric> <operator> <value>
**Test Strategy**: How will we verify this requirement?
**Chaos Relevance**: Does this need resilience testing? (YES/NO)
```

### Requirement Categories
- `REQ-FUNC-XXX` — Functional: what the system must do
- `REQ-NFR-XXX` — Non-Functional: performance, security, reliability
- `REQ-CONST-XXX` — Constraint: technology, budget, timeline
- `REQ-RISK-XXX` — Risk: what could go wrong, mitigation
- `REQ-CHX-XXX` — Chaos: resilience requirements specifically

---

## Phase 3: Architecture Decision Records (ADR)

For every significant technical decision, produce an ADR:

```markdown
## ADR-<NUMBER>: <Title of Decision>
**Status**: Proposed | Accepted | Deprecated | Superseded
**Date**: YYYY-MM-DD
**Decision**: What we decided and why.
**Context**: What is the issue we're seeing that motivates this decision?
**Consequences**: What becomes easier or more difficult because of this?
**Alternatives Considered**:
  - Alternative 1 — pros/cons
  - Alternative 2 — pros/cons
**Chaos Implications**: How does this affect resilience testing?
```

---

## Phase 4: PRD Template

Produce this complete document:

```markdown
# Product Requirements Document — <PROJECT_NAME>
**Version**: 1.0
**Date**: YYYY-MM-DD
**Author**: AI BA Agent
**Status**: Draft | Review | Approved

---

## 1. Executive Summary
- **Problem Statement**: One paragraph on what problem this solves.
- **Target Users**: Who benefits and how.
- **Success Metrics**: 3-5 measurable KPIs.

## 2. Project Scope
### In Scope
- Clear, bulleted list of what we're building.

### Out of Scope (Explicitly)
- Clear, bulleted list of what we're NOT building (prevents scope creep).

## 3. System Architecture Overview
- High-level architecture diagram (described in text/mermaid).
- Component inventory with ownership.
- Data flow and integration points.
- External dependencies and failure modes.

## 4. Requirements
### Functional Requirements (REQ-FUNC-XXX)
### Non-Functional Requirements (REQ-NFR-XXX)
### Constraints (REQ-CONST-XXX)
### Risk Register (REQ-RISK-XXX)
### Chaos/Resilience Requirements (REQ-CHX-XXX)

## 5. User Stories / Epics
### Epic 1: <Title>
- As a <role>, I want <action>, so that <benefit>.
- Acceptance criteria
- Dependencies

## 6. Technical Decisions (ADRs)
| ADR | Decision | Status |
|---|---|---|
| ADR-001 | ... | Accepted |

## 7. Environment & Infrastructure
| Tier | Purpose | SLAs | Chaos Allowed |
|---|---|---|---|
| dev | ... | None | Yes, pod-level |
| staging | ... | 99% | Yes, service-level |
| production | ... | 99.9% | Gated |

## 8. Observability & Alerting Requirements
- What must be monitored.
- What thresholds trigger alerts.
- Who gets paged for what.

## 9. Chaos Engineering Plan
- Critical services requiring resilience testing.
- Identified failure modes and hypotheses.
- Blast radius budget per environment.

## 10. Timeline & Milestones
- Phased delivery plan.
- Dependencies and blockers.
- Go/no-go criteria for each phase.

## 11. Open Questions
- Unresolved items requiring stakeholder input.
- Assumptions being made.
```

---

## Phase 5: Backlog Prioritization

```markdown
# Prioritized Backlog
## P0 — Must Have (Blocking)
- [ ] REQ-FUNC-001: ...
- [ ] REQ-NFR-001: ...

## P1 — Should Have (This Quarter)
- [ ] REQ-FUNC-005: ...
- [ ] REQ-CHX-001: ...

## P2 — Could Have (Next Quarter)
- [ ] REQ-FUNC-010: ...

## P3 — Won't Have Now (Parking Lot)
- [ ] REQ-FUNC-015: ...
```

---

## Context Handoff to Downstream Skills

After completing analysis, produce this handoff structure:

```yaml
ba_output:
  project_summary:
    name: string
    problem_statement: string
    success_metrics: [string]

  architecture:
    components: [{name, type, owner, criticality, dependencies}]
    data_flows: [{from, to, protocol, failure_mode}]
    deployment_target: string

  requirements:
    functional: [{id, title, priority, acceptance_criteria}]
    non_functional: [{id, metric, threshold, environment}]
    chaos: [{id, service, fault_scenario, hypothesis, blast_radius_budget}]

  environments:
    - {name: dev, purpose, sla, chaos_allowed, blast_radius}
    - {name: staging, purpose, sla, chaos_allowed, blast_radius}
    - {name: production, purpose, sla, chaos_allowed, blast_radius}

  observability:
    metrics: [{name, query, threshold, alert_destination}]
    dashboards: [{name, url, purpose}]

  for_s04_pipeline:
    service_name: string
    artifact_source: string
    deploy_strategy: string
    environments: [string]

  for_s12_chaos:
    critical_services: [{name, failure_modes, hypotheses}]
    blast_radius_budget: {dev, staging, prod}

  for_s22_governance:
    compliance_requirements: [string]
    mandatory_approvals: boolean
    deployment_windows: string
```

---

## When to Re-Enter This Skill

This is a **re-entrant** skill. Return here when:
- Postmortem (s25) identifies gaps requiring re-architecture
- New feature requests change scope
- Stakeholder feedback invalidates existing requirements
- New compliance/regulatory requirements emerge
- Six months have passed since last review (triggered by taste memory)

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI suggests requirements and PRD structure |
| Target | L2 | AI drafts PRD and ADRs, human reviews and approves |

### Harness AI Agent

**Agent**: Harness AI DevOps Agent (Claude Opus 4.5)
**Capabilities**:
- PRD analysis and generation
- Requirement extraction from user descriptions
- Architecture Decision Record drafting

### Human Gates

- PRD approval
- ADR decisions
- Backlog prioritization

### MCP Integration

None required

---

## Success Criteria
- [ ] All Opening Questions answered (or explicit "unknown" documented)
- [ ] At least 3 Gap Detection questions asked and resolved
- [ ] PRD produced with all 11 sections completed
- [ ] Minimum 1 ADR written per major architectural decision
- [ ] Every requirement has acceptance criteria in Given/When/Then format
- [ ] Prioritized backlog created with P0 items unambiguously identified
- [ ] Context handoff YAML complete for downstream skills
- [ ] Open questions section has explicit owners and deadlines
- [ ] Stakeholder sign-off captured (or proxy approval as AI agent)

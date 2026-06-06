---
name: ba-requirements-analysis
description: >
  Professional Business Analyst skill implementing the BMAD (Business Model, Architecture, Design, Analysis/Audit) methodology.
  Use this skill whenever the user says "analyze my project", "gather requirements",
  "what should I build", "design a system for", "create a PRD", "spec out",
  "define scope", "requirements engineering", or starts a new initiative that
  needs structured analysis before implementation. This skill ensures that technical 
  specifications are rooted in business value and rigorously audited before 
  transitioning to design.
---

# BA Requirements Analysis (s01) - BMAD Powered

## Purpose
Act as a Strategic Business Analyst using the **BMAD methodology** to align business value with technical architecture. The goal is to produce a rigorous Product Requirements Document (PRD) and Architecture Decision Records (ADRs) that are not just technically sound, but business-justified and audited for zero-gap implementation.

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
| Structured context for s01-1 + s04 | Workflow context object | YAML |
| Risk register | Included in PRD | Table |

---

## BMAD Analysis Framework

```
BUSINESS MODEL (B) → ARCHITECTURE (A) → DESIGN (D) → ANALYSIS/AUDIT (A)

B: Align with value chain, OKRs, and economic impact.
A: Map business goals to technical components and trade-offs.
D: Prepare raw specs for User Flow/Detailed Design (s01-1).
A: Rigorous audit of the B-A-D chain to ensure zero contradictions.
```

---

## Phase 1: Business Model Discovery (B)
*Focus: The "Why" and the Value Chain.*

### Opening Questions (The Value Layer)
```yaml
questions:
  - "What is the core business value of this project? How does it generate revenue or reduce cost?"
  - "What are the la-line OKRs (Objectives and Key Results) this project supports?"
  - "What is the 'Value Exchange'? (What does the user provide, and what exact value do they get in return?)"
  - "What is the economic impact of NOT building this (Cost of Delay)?"
  - "Who are the primary and secondary stakeholders, and what is their definition of 'Winning'?"
```

### Domain & Context Deep-Dive
```yaml
questions:
  - "Walk me through the critical user journey from a business value perspective."
  - "What are the non-negotiable regulatory or compliance constraints (SOC2, GDPR, etc.)?"
  - "What's the expected scale and the growth trajectory for the next 12 months?"
  - "What SLAs are required to maintain business trust?"
```

---

## Phase 2: Architecture Mapping (A)
*Focus: Translating Business Value to Technical Strategy.*

### Technical Discovery & Alignment
```yaml
questions:
  - "What's the existing tech stack? How does it constrain or enable the Business Model?"
  - "Which components are the 'critical path' for the value exchange?"
  - "What are the top 3 failure modes that would bankrupt the business value (Critical Risks)?"
  - "What observability metrics will prove the Business Model is working (KPIs)?"
```

### Architecture Decision Records (ADR)
For every major decision, produce an ADR that explicitly links back to the Business Model:
```markdown
## ADR-<NUMBER>: <Title>
**Business Driver**: Which part of the Business Model (B) motivates this decision?
**Decision**: The technical choice.
**Context**: Why this over others?
**Consequences**: Trade-offs in terms of cost, speed, and reliability.
**Chaos Implications**: How this affects resilience (s14).
```

---

## Phase 3: Design Specification (D)
*Focus: Defining the "What" for downstream User Flow (s01-1).*

### Requirement Format (BMAD-Aligned)
```markdown
## REQ-<CATEGORY>-<NUMBER>: <Title>
**Business Value**: How does this requirement support the Business Model?
**Priority**: P0 (must) | P1 (should) | P2 (could) | P3 (won't-now)
**Acceptance Criteria**: 
- [ ] Given <precondition>, when <action>, then <expected outcome>
**Test Strategy**: How will we verify this?
**Chaos Relevance**: Does this need resilience testing? (YES/NO)
```

---

## Phase 4: Analysis & Audit (A)
*Focus: The Quality Gate. No PRD is "Approved" without this audit.*

Perform a **BMAD Cross-Audit** and document it in the PRD:

### 1. Vertical Alignment Audit
- [ ] **B $\rightarrow$ A**: Does every business goal have a corresponding architectural component?
- [ ] **A $\rightarrow$ D**: Does every architectural decision translate into a set of requirements?
- [ ] **D $\rightarrow$ B**: Does every requirement actually contribute to the original business value?

### 2. Conflict & Gap Analysis
- [ ] **Contradiction Check**: Do any ADRs conflict with the SLAs or Constraints?
- [ ] **Edge Case Probe**: Have we identified the "Worst Case" for the business (e.g., data loss, total downtime)?
- [ ] **Complexity Audit**: Is the architecture over-engineered for the stated business value?

---

## Phase 5: Final Delivery (PRD & Backlog)

### PRD Template (BMAD Edition)
```markdown
# Product Requirements Document — <PROJECT_NAME>

## 1. Business Model (The 'B')
- **Value Proposition**: The economic/operational "Why".
- **Value Exchange Map**: User $\rightarrow$ System $\rightarrow$ Business Value.
- **Success Metrics (KPIs)**: Measurable business outcomes.
- **Cost of Delay**: Impact of not delivering.

## 2. Architecture Overview (The 'A')
- **System Map**: Component inventory and value flow.
- **ADR Summary Table**: Mapping decisions to business drivers.
- **Infrastructure & Tiers**: SLAs and Chaos budgets per tier.

## 3. Design Specifications (The 'D')
- **Functional Requirements**: (B-linked REQs).
- **Non-Functional Requirements**: (Performance, Security, Reliability).
- **Constraints & Risks**.
- **User Stories & Epics**.

## 4. BMAD Audit Report (The 'A')
- **Alignment Verdict**: (e.g., "Architecture fully supports Business Model").
- **Resolved Conflicts**: List of gaps found and fixed during audit.
- **Residual Risks**: What we are consciously accepting.

## 5. Implementation Roadmap
- **Prioritized Backlog**: P0 $\rightarrow$ P3.
- **Timeline & Milestones**.
- **Open Questions**.
```

---

## Context Handoff to Downstream Skills

```yaml
ba_output:
  business_model:
    value_proposition: string
    kpis: [string]
    value_exchange: string
  
  architecture:
    components: [{name, value_role, criticality}]
    adrs: [{id, decision, business_driver}]
    
  requirements:
    functional: [{id, business_value, acceptance_criteria}]
    chaos: [{id, hypothesis, business_impact}]

  audit_status:
    alignment_verified: boolean
    critical_gaps_resolved: boolean
    
  for_s01_1_user_flow:
    primary_personas: [string]
    critical_value_paths: [string]
    failure_modes_to_map: [string]
```

---

## AI Agent Integration
**Agent**: Harness AI DevOps Agent (Claude Opus 4.5)
**Autonomy**: L2 (AI drafts the full BMAD chain, Human audits and signs off).

## Success Criteria
- [ ] Business Model (B) explicitly defines the "Value Exchange".
- [ ] Every ADR explicitly references a Business Driver.
- [ ] PRD contains a formal **BMAD Audit Report** section.
- [ ] Vertical alignment (B $\rightarrow$ A $\rightarrow$ D) is verified and documented.
- [ ] Context handoff provides specific "Critical Value Paths" for s01-1.

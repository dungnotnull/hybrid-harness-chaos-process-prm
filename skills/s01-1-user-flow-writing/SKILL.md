---
name: user-flow-writing
description: >
  Advanced User Flow and Journey Mapping skill.
  This skill transforms high-level PRDs (from s01) into detailed, multi-perspective 
  user flows, sequence diagrams, and edge-case maps. It ensures that every user 
  interaction, system response, and failure mode is visualized and documented 
  before any code is written. It includes a rigorous multi-perspective review flow 
  to guarantee requirements accuracy and business scenario coverage.
---

# User Flow Writing (s01-1)

## Purpose
Bridge the gap between "what" (PRD) and "how" (Implementation) by mapping the exact 
path a user (or system agent) takes through the application. The goal is to 
eliminate ambiguity, identify missing "sad paths," and ensure that the 
Developer/QA/SRE personas have a crystal-clear understanding of the expected 
behavior in all scenarios.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Approved PRD | `.commandcode/prd.md` (from s01) | Yes |
| Architecture Overview | PRD Section 3 / ADRs | Yes |
| User Personas | PRD Section 1 | Yes |
| Taste Preferences | `.commandcode/taste/taste.md` | Recommended |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| User Journey Maps | `.commandcode/flows/journeys.md` | Mermaid / Markdown |
| Detailed User Flows | `.commandcode/flows/detailed-flows.md` | Mermaid / Markdown |
| Edge Case & Error Matrix | `.commandcode/flows/edge-cases.md` | Table / Markdown |
| Multi-Perspective Review Report | `.commandcode/flows/review-audit.md` | Markdown |
| Handoff for s04/s12 | Workflow context object | YAML |

---

## User Flow Framework

```
MAP -> STRESS-TEST -> REVIEW -> FINALIZE

Map: Create "Happy Path" and "Primary Sad Paths"
Stress-Test: Inject chaos/edge cases into the flow
Review: Multi-perspective audit (Dev, QA, Business, SRE)
Finalize: Sign-off and handoff to engineering
```

---

## Phase 1: Journey Mapping (The Macro View)
Identify the "Golden Paths" for each persona.
- **Persona Identification**: Define who is interacting (End User, Admin, System Cron, API Client).
- **High-Level Steps**: 5-7 major milestones from entry to goal achievement.
- **Emotional/Friction Points**: Identify where users might get confused or drop off.

---

## Phase 2: Detailed Flow Design (The Micro View)
Expand journeys into technical flows using Mermaid.js.
- **Happy Path**: The ideal sequence of events.
- **Expected Deviations**: Valid alternative paths (e.g., "User chooses Option B instead of A").
- **Error Paths**: System-level failures, validation errors, and timeouts.
- **State Transitions**: Clearly define the state of the system before and after each action.

---

## Phase 3: Edge Case & Business Scenario Stress-Testing
For every step in the flow, ask "What if...?"
- **Input Edge Cases**: Nulls, extremes, unexpected formats, rapid clicking.
- **System Edge Cases**: Network latency, partial API failure, database locks, race conditions.
- **Business Edge Cases**: Expired tokens, insufficient permissions, concurrency conflicts, regulatory blocks.
- **Chaos Integration**: How does the flow behave when a dependency is throttled or killed? (Linking to s14).

---

## Phase 4: Multi-Perspective Review Flow (The Audit)
This is the critical quality gate. The flow is reviewed through four distinct lenses:

### 1. The Business Lens (Value & Logic)
- Does this flow actually solve the business problem defined in the PRD?
- Are there missing business rules or regulatory constraints?
- Is the "Time to Value" optimized?

### 2. The Developer Lens (Feasibility & Complexity)
- Is this flow implementable with the current architecture (ADRs)?
- Are there hidden complexities or "impossible" states?
- Are the inputs/outputs well-defined for API design?

### 3. The QA/Tester Lens (Verifiability & Coverage)
- Is every branch in the flow testable?
- Are the "sad paths" exhaustive?
- Can we derive clear test cases from this flow?

### 4. The SRE/Reliability Lens (Resilience & Observability)
- What happens to the user when a backend service fails at step X?
- Is there enough observability (logs/metrics) to debug this flow in production?
- Does the flow handle retries and circuit breaking gracefully?

---

## Phase 5: Finalization & Handoff
Once the Review Report is signed off:
1. **Consolidate** all flows into the final `.commandcode/flows/` directory.
2. **Update** the PRD to link to these detailed flows.
3. **Generate Handoff YAML** for downstream skills (s04, s12, etc.).

---

## AI Agent Integration

### Autonomy Level
| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI drafts flows and identifies basic edge cases |
| Target | L2 | AI generates comprehensive flows, simulates 4-persona reviews, and audits gaps |

### Harness AI Agent
**Agent**: Harness AI DevOps Agent / Test Agent
**Capabilities**:
- Mermaid diagram generation
- Scenario simulation and edge-case brainstorming
- Role-playing different perspectives for review

---

## Success Criteria
- [ ] All personas from PRD have at least one mapped journey.
- [ ] Every "Happy Path" has at least 3 corresponding "Sad Paths."
- [ ] Multi-Perspective Review Report contains explicit feedback and resolutions for all 4 lenses.
- [ ] Edge Case Matrix covers at least 10 real-world business scenarios per major flow.
- [ ] All flows are rendered in Mermaid and verified for logical consistency.
- [ ] Handoff YAML includes a list of all critical "Failure Points" for the SRE/Chaos agent.

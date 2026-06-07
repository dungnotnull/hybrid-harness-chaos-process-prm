---
name: workflow-orchestrator
description: >
  Master orchestration skill that coordinates the complete end-to-end Agile workflow
  from ideation to production operations. Use this skill whenever the user starts a
  new project, says "start a workflow", "run the full process", "orchestrate my project",
  or needs to understand the overall workflow sequence. This skill reads CLAUDE.md,
  identifies the current project phase, dispatches to the correct domain skills, and
  ensures all inputs/outputs are chained correctly between skills. Every AI agent in
  this project must consult this skill first to understand the global workflow state.
---

# Workflow Orchestrator (s00)

## Purpose
Serve as the single entrypoint that coordinates the entire hybrid harness + chaos engineering workflow. This skill maps the full Agile lifecycle, knows the input/output contracts of every skill, and ensures agents follow the correct sequence without skipping steps.

---

## Prerequisites
- [ ] CLAUDE.md read and loaded into context
- [ ] `.commandcode/taste/` directory exists for memory persistence
- [ ] Current project context established (repo, team, stack)

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| User request / project description | User prompt | Yes |
| CLAUDE.md (project rules) | Repository root | Yes |
| Taste file (`.commandcode/taste/taste.md`) | Project repo | No (created if absent) |
| Progress state (`.commandcode/progress.json`) | Previous runs | No (created if absent) |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Workflow phase decision | Next skill invocation | Text + structured context |
| Updated progress state | `.commandcode/progress.json` | JSON |
| Cross-skill context handoff | Next skill's input | Structured YAML |
| Phase completion summary | User + progress tracker | Markdown |

---

## Complete Agile Workflow Map

```
PHASE 0: FOUNDATION
  s00 â†’ s01 â†’ s02 + s03 (parallel)
    â”‚
PHASE 1: PLANNING & REQUIREMENTS
  s01 (BA deep analysis â†’ PRD + ADRs + backlog)
    â”‚
PHASE 2: CI/CD SCAFFOLDING
  s04 â†’ s05 â†’ s06 â†’ s07 â†’ s08 â†’ s09 â†’ s10
  (pipeline design â†’ service onboard â†’ delegate â†’ secrets â†’ FF â†’ templates â†’ GitOps)
    â”‚
PHASE 3: SECURITY GATE
  s11 (SAST + SCA + container + secrets + IaC + SBOM + SLSA)
  â ï¸ BLOCKS all downstream if security gates fail
    â”‚
PHASE 4: TESTING
  s12 â†’ s13 (CloakBrowser E2E + baseline â†’ Performance/load profiling)
  â ï¸ Performance baseline required before chaos experiments
    â”‚
PHASE 5: CHAOS EXPERIMENT DESIGN
  s17 â†’ s14 â†’ s15 â†’ s16 â†’ s18 â†’ s19
  \(steady state â†’ experiment â†’ hypothesis â†’ blast radius â†’ infra faults â†’ app faults\)
    â”‚
PHASE 6: GAME DAY EXECUTION
  s20 (orchestrated resilience exercise)
    â”‚
PHASE 7: VERIFICATION & OBSERVABILITY
  s21 â†’ s22 â†’ s23
  (CV verification â†’ observability integration â†’ alerting & recommendations)
    â”‚
PHASE 8: GOVERNANCE
  s24 â†’ s25 â†’ s26 â†’ s27 â†’ s28
  (policy â†’ cost â†’ resilience scoring â†’ postmortem â†’ release management)
    â”‚
PHASE 9: RESILIENCE & CONTINUITY
  s29 â†’ s30
  (disaster recovery â†’ compliance & audit)

STRATEGIC INNOVATION (s31 â€” callable at ANY phase)
  Invoked when user says "think bigger", "brainstorm", "what am I missing",
  "upgrade requirements", "strategic review", "innovate"
  â†’ s31 produces proposals + trade-off analysis (advisory only)
  â†’ If user accepts a proposal, dispatches to relevant implementation skill
  â†’ If user declines, workflow continues from current phase unchanged

FEEDBACK LOOP:
  s27 (postmortem findings) â†’ s01 (re-analysis) â†’ full cycle
  s30 (compliance gaps) â†’ s01 (PRD update) â†’ remediation cycle
```

## Phase 0: Foundation

When the user initiates any workflow, execute these steps in order:

### Step 1 â€” Load Project Context
```yaml
action: read_and_load
files:
  - CLAUDE.md              # Project identity, stack, conventions
  - .commandcode/taste/taste.md  # Developer preferences (create if absent)
status: check_progress_file
  - .commandcode/progress.json   # Where are we in the workflow?
```

### Step 2 â€” Determine Phase
Based on user request and progress state, determine current phase:
- **No progress file exists** â†’ Start at s01 (BA Requirements) or s04 (CI/CD if project exists)
- **Progress file exists** â†’ Resume from last completed phase
- **User specifies phase** â†’ Jump to that phase (but warn about skipped prerequisites)

### Step 3 â€” Dispatch and Hand-off
```yaml
handoff_protocol:
  before_dispatch:
    - Read the target skill's SKILL.md fully
    - Gather all inputs listed in the skill's Input Contract
    - Verify prerequisites are satisfied from previous phase outputs
  during_dispatch:
    - Pass structured context object to the next skill
    - Update progress.json with "in_progress" status
  after_completion:
    - Verify skill's output matches its Output Contract
    - Update progress.json with "completed" status
    - Notify user of phase completion with summary
    - Load and dispatch to next skill in sequence
```

---

## Skill Index with I/O Chains

| # | Skill | Consumes From | Produces For |
|---|---|---|---|
| 00 | Orchestrator | User prompt, CLAUDE.md | Progress state, phase dispatch |
| 01 | BA Requirements | User prompt, taste file | PRD, specifications | s04, s14 |
| 02 | Taste & Memory | All skill outputs | User preference model | All skills |
| 03 | Progress Tracker | Orchestrator dispatch events | Progress state | Orchestrator |
| 04 | Pipeline Design | PRD (s01), service name, stack | Pipeline YAML | s05, s14, s21 |
| 05 | Service Onboarding | Pipeline YAML (s04), repo URL | Service definitions | s06, s08 |
| 06 | Delegate Management | Service defs (s05), cluster info | Deploy config | s05, s10 |
| 07 | Secrets Management | Service defs (s05) | Secret references | s04, s05, s08 |
| 08 | Feature Flags | PRD (s01), service defs (s05) | Flag configs, SDK code | s16, s23 |
| 09 | Template Library | Pipeline patterns (s04) | Reusable templates | s04, s10, s20 |
| 10 | GitOps | Templates (s09), service (s05) | GitOps config, Application YAML | s04, s20 |
| 11 | Security Scanning | Source code, images, deps | Scan reports, SBOM, gate verdict | s12 (gates testing), s24, s30 |
| 12 | CloakBrowser Testing | PRD (s01), pipeline (s04) | Test results, coverage | s20, s23, s27 |
| 13 | Performance Testing | Service endpoints, SLAs | Baselines, breaking points | s14 (chaos), s25, s26 |
| 14 | Experiment Design | PRD (s01), pipeline (s04) | Experiment manifests | s15, s16, s17 |
| 15 | Hypothesis Validation | Experiment (s14), steady state (s17) | Validated hypotheses | s20, s26, s27 |
| 16 | Blast Radius Control | Experiment (s14), env tiers | Blast radius config | s15, s20, s24 |
| 17 | Steady State Definition | Service defs (s05), pipeline (s04) | Probes, baseline metrics | s15, s21, s27 |
| 18 | Infrastructure Faults | Experiment (s14), delegate (s06) | Infra fault manifests | s20 |
| 19 | Application Faults | Experiment (s14), service (s05) | App fault manifests | s20 |
| 20 | Game Day Planning | Experiments (s14-s19), team info | Game day runbook, schedule | s22, s23, s27 |
| 21 | CV Verification | Pipeline (s04), monitors, s17 | CV config, monitored services | s22, s26 |
| 22 | Observability Integration | CV (s21), experiments (s14-s19) | Dashboards, chaos metrics | s20, s23 |
| 23 | Alerting & Recommendations | Obs (s22), experiments results | Alert rules, recommendations | s26, s27 |
| 24 | Policy Governance | All YAML outputs | OPA policies | All skills (gate) |
| 25 | Cloud Cost Management | Service defs (s05), infra | Cost configs, budgets | s26 |
| 26 | Resilience Scoring | All experiment results, obs data | Resilience score, report | s27, s28, s29 |
| 27 | Postmortem Learning | Game day results, scores, alerts | RCA, action items, runbook updates | s01 (feedback loop) |
| 28 | Release Management | Pipeline, scores, verifications | Release plan, go/no-go, notes | s30 (audit trail) |
| 29 | Disaster Recovery | Topology, resilience scores | DR plan, failover runbook, RTO/RPO | s26, s30 |
| 30 | Compliance & Audit | All evidence, scans, approvals | Audit trail, evidence bundle | s01 (feedback loop) |
| 31 | Strategic Creator | Current phase artifacts, PRD, taste | Proposals + trade-off analysis (advisory) | s01, s04, s11, s14, s22, s25, s30 (on acceptance) |

---

## Context Object Schema

Every handoff between skills passes this structured context:

```yaml
workflow_context:
  project:
    name: string
    description: string
    repository: string
    team: string
    stack: [string]

  phase:
    current: string       # e.g., "04-pipeline-design"
    completed: [string]   # e.g., ["01-ba-requirements"]
    next: string          # e.g., "05-service-onboarding"

  artifacts:
    prd_path: string|null
    pipeline_yaml: string|null
    service_defs: [string]|null
    experiment_manifests: [string]|null
    game_day_runbook: string|null
    resilience_score: number|null

  taste:
    preferences: object   # Injected from s02
    last_updated: string

  progress:
    state_file: string    # Path to progress.json
    completed_steps: [string]
    current_step: string
    blockers: [string]

  conventions:
    naming: object        # From CLAUDE.md
    env_tiers: [string]
    approval_required: boolean
```

---

## Dispatch Protocol (Step-by-Step)

When dispatching to skill sNN:

```bash
# 1. Load the skill
read_file(skills/sNN-<name>/SKILL.md)

# 2. Gather inputs from context object
# Every skill declares its inputs. The orchestrator ensures they exist.

# 3. Check prerequisites
# If any prerequisite is missing, call the upstream skill first.

# 4. Execute the skill
# The skill runs its workflow autonomously.

# 5. Capture outputs into context object
workflow_context.artifacts.<output_key> = skill_output

# 6. Save progress
write_file(.commandcode/progress.json, updated_progress)

# 7. Notify and dispatch next
# Present summary to user, then auto-dispatch to sNN+1
```

### Special Case: s31 Strategic Creator

s31 is NOT part of the linear workflow. It is callable at ANY phase:

```yaml
s31_invocation:
  triggers:
    - User says "think bigger", "brainstorm", "what am I missing"
    - User says "strategic review", "innovate", "upgrade requirements"
    - User says "challenge assumptions", "what would FAANG do"
    - User explicitly invokes /strategic-creator or s31

  behavior:
    - Pause current workflow phase (do NOT advance progress.json)
    - Load s31 with current phase context + PRD + taste
    - Present proposals (advisory only â€” no implementation)
    - Wait for user decision:
        accept: dispatch to relevant skills, update progress.json
        decline: resume current phase from where we paused
        defer: record proposal in context for later, resume current phase

  example_flow:
    current_phase: "05-service-onboarding (in_progress)"
    user: "Think bigger â€” what would Netflix do here?"
    â†’
    s31_invoked:
      - Pauses s05
      - Analyzes current architecture + PRD
      - Presents 3 proposals with trade-offs
      - User accepts Proposal #2 â†’ dispatches s01 (new ADR) + s05 (service update)
      - After dispatch, resumes s05 with updated context
```

---

## Progress JSON Schema

```json
{
  "project": "hybrid-harness-chaos-process-prm",
  "workflow_version": "1.0",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T10:05:00Z",
  "phases": {
    "00-orchestrator": { "status": "completed", "completed_at": "..." },
    "01-ba-requirements": { "status": "in_progress", "started_at": "..." },
    "02-taste-memory": { "status": "pending" },
    "03-progress-tracker": { "status": "pending" },
    "04-pipeline-design": { "status": "pending" },
    "...": {}
  },
  "artifacts": {
    "prd": null,
    "pipeline_yaml": null,
    "service_definitions": null,
    "experiment_manifests": null,
    "resilience_report": null
  },
  "blockers": [],
  "notes": []
}
```

---

## Agent Autonomy Rules

When operating as the orchestrator:

1. **Never skip phases** unless user explicitly confirms skipping
2. **Always verify upstream outputs** before passing them downstream
3. **Surface blockers immediately** â€” don't silently continue without prerequisites
4. **Update progress.json after every phase completion**
5. **Inject taste data** from s02 into every skill context
6. **Present phase summaries** with: what was done, what was produced, what comes next

---

## Workflow Decision Tree

```
User prompt received
    â”‚
    â”œâ”€â”€ "Start new project" or "Design/plan X"
    â”‚   â””â”€â”€ GOTO s01 (BA Requirements) â†’ full workflow
    â”‚
    â”œâ”€â”€ "Set up CI/CD" or "Deploy X"
    â”‚   â”œâ”€â”€ Is PRD/context available?
    â”‚   â”‚   â”œâ”€â”€ YES â†’ GOTO s04 (Pipeline Design)
    â”‚   â”‚   â””â”€â”€ NO â†’ GOTO s01 first, then s04
    â”‚
    â”œâ”€â”€ "Run chaos experiment" or "Test resilience"
    â”‚   â”œâ”€â”€ Is pipeline + service onboarded?
    â”‚   â”‚   â”œâ”€â”€ YES â†’ GOTO s14 (Experiment Design)
    â”‚   â”‚   â””â”€â”€ NO â†’ GOTO s04 first, then s14
    â”‚
    â”œâ”€â”€ "Game day" or "Chaos day"
    â”‚   â”œâ”€â”€ Are experiments designed and validated?
    â”‚   â”‚   â”œâ”€â”€ YES â†’ GOTO s20 (Game Day Planning)
    â”‚   â”‚   â””â”€â”€ NO â†’ GOTO s14 first, then s20
    â”‚
    â”œâ”€â”€ "Think bigger" / "Brainstorm" / "What am I missing" / "Innovate"
    â”‚   â””â”€â”€ GOTO s31 (Strategic Creator) â€” pause current phase, present proposals
    â”‚       â”œâ”€â”€ User accepts proposal â†’ dispatch to relevant skill(s)
    â”‚       â”œâ”€â”€ User declines â†’ resume paused phase
    â”‚       â””â”€â”€ User defers â†’ record in context, resume paused phase
    â”‚
    â”œâ”€â”€ "Review/audit" or "Governance check"
    â”‚   â””â”€â”€ GOTO s24 (Policy Governance) â†’ s26 (Scoring) â†’ s27 (Postmortem)
    â”‚
    â”œâ”€â”€ "Security audit" or "Vulnerability check"
    â”‚   â””â”€â”€ GOTO s11 (Security Scanning) â†’ s30 (Compliance Audit)
    â”‚
    â””â”€â”€ "Fix issue from postmortem" or "Remediate"
        â””â”€â”€ GOTO s27 (Postmortem) â†’ feeds back into s01 (re-analysis)
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | Phase detection, skill dispatch recommendations |
| Target | L3 | Auto-dispatch with human checkpoint at phase transitions |

### Harness AI Agent

**Agent**: Workflow Orchestration (Harness AI Intelligent Workflow Orchestration layer)
**Capabilities**:
- Phase detection from context
- Skill dispatch optimization
- Context handoff generation
- Blocker identification

### Human Gates

- Phase transitions require human confirmation
- Skip-phase requests require explicit approval
- Workflow restart requires human trigger

### MCP Integration

None required

---

## Success Criteria
- [ ] CLAUDE.md loaded and understood
- [ ] Progress file detected or created
- [ ] Correct phase determined from user request
- [ ] All prerequisites verified before skill dispatch
- [ ] Context object populated correctly for each handoff
- [ ] Progress.json updated after every phase
- [ ] User informed of workflow state at each transition
- [ ] No phases skipped without explicit user confirmation

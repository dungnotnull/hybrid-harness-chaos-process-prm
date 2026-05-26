---
name: progress-tracker
description: >
  Track and manage progress across the complete hybrid workflow for all agents and
  phases. Use this skill whenever the orchestrator (s00) initiates or updates the
  workflow, when an agent completes a phase, when blockers are identified, or when
  resuming a previously interrupted workflow. Also use to generate status reports
  and ensure no tasks are missed or duplicated across multiple agent sessions.
  This skill manages `.commandcode/progress.json` and produces human-readable
  burndown charts and status dashboards.
---

# Progress Tracker (s03)

## Purpose
Maintain a single source of truth for workflow progress across all phases and agent sessions. Prevent duplicated work, track blockers, surface missed tasks, and provide clear status visibility — ensuring work consistency even when switching between AI agents or resuming after interruptions.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Orchestrator dispatch events | s00 workflow_context | Yes |
| Skill completion signals | Each skill's output | Yes |
| Previous progress state | `.commandcode/progress.json` | No (created if absent) |
| Blocker reports | Any skill encountering issues | No |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Updated progress.json | `.commandcode/progress.json` | JSON |
| Workflow dashboard | Terminal output | Colored Markdown |
| Burndown data | Progress JSON (embedded) | JSON |
| Missed task alerts | User + orchestrator | Text |
| Agent handoff summary | Next agent session | Markdown |

---

## Progress State Schema

```json
{
  "project": "hybrid-harness-chaos-process-prm",
  "workflow_version": "1.0",
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-01-15T16:30:00Z",
  "total_phases": 26,
  "completed_phases": 12,
  "current_phase": "13-hypothesis-validation",
  "agent": "claude-code-3.5",
  "phases": {
    "00-orchestrator": {
      "status": "completed",
      "started_at": "2025-01-15T10:00:00Z",
      "completed_at": "2025-01-15T10:02:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["progress.json created"],
      "notes": ""
    },
    "01-ba-requirements": {
      "status": "completed",
      "started_at": "2025-01-15T10:02:00Z",
      "completed_at": "2025-01-15T11:45:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["prd.md", "adr/adr-001-kubernetes-deployment.md", "backlog.md"],
      "notes": "PRD approved by engineering lead"
    },
    "02-taste-memory": {
      "status": "completed",
      "started_at": "2025-01-15T10:00:00Z",
      "completed_at": "2025-01-15T10:01:00Z",
      "agent": "system",
      "artifacts": [],
      "notes": "Loaded 23 taste preferences"
    },
    "03-progress-tracker": {
      "status": "completed",
      "started_at": "2025-01-15T10:00:00Z",
      "completed_at": "2025-01-15T10:02:00Z",
      "agent": "system",
      "artifacts": [],
      "notes": "Initialized"
    },
    "04-pipeline-design": {
      "status": "completed",
      "started_at": "2025-01-15T11:45:00Z",
      "completed_at": "2025-01-15T14:20:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["pipeline-payment-service.yaml", "trigger-config.yaml"],
      "notes": "Pipeline generated with chaos step placeholder"
    },
    "05-service-onboarding": {
      "status": "completed",
      "started_at": "2025-01-15T14:20:00Z",
      "completed_at": "2025-01-15T15:30:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["service-payment.yaml", "env-dev.yaml", "env-staging.yaml", "infra-def.yaml"],
      "notes": ""
    },
    "06-delegate-management": {
      "status": "completed",
      "started_at": "2025-01-15T15:30:00Z",
      "completed_at": "2025-01-15T15:50:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["delegate-helm-values.yaml", "delegate-rbac.yaml"],
      "notes": ""
    },
    "07-secrets-management": {
      "status": "completed",
      "started_at": "2025-01-15T15:50:00Z",
      "completed_at": "2025-01-15T16:00:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["vault-connector.yaml", "secret-references.yaml"],
      "notes": "Using Vault with K8s auth"
    },
    "08-feature-flags": {
      "status": "completed",
      "started_at": "2025-01-15T16:00:00Z",
      "completed_at": "2025-01-15T16:10:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["ff-payment-new-checkout.yaml", "ff-chaos-payment.yaml"],
      "notes": "Chaos kill switch FF created"
    },
    "09-template-library": {
      "status": "completed",
      "started_at": "2025-01-15T16:10:00Z",
      "completed_at": "2025-01-15T16:15:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["template-standard-deploy.yaml", "template-security-scan.yaml"],
      "notes": ""
    },
    "10-gitops": {
      "status": "completed",
      "started_at": "2025-01-15T16:15:00Z",
      "completed_at": "2025-01-15T16:25:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["app-payment-production.yaml", "applicationset.yaml"],
      "notes": ""
    },
    "11-cloakbrowser-testing": {
      "status": "completed",
      "started_at": "2025-01-15T16:25:00Z",
      "completed_at": "2025-01-16T09:00:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["test-results.xml", "coverage-report.html"],
      "notes": "All tests passing, 85% coverage"
    },
    "12-experiment-design": {
      "status": "completed",
      "started_at": "2025-01-16T09:00:00Z",
      "completed_at": "2025-01-16T09:45:00Z",
      "agent": "claude-code-3.5",
      "artifacts": ["experiment-pod-delete.yaml", "engine-payment-pod-delete.yaml"],
      "notes": ""
    },
    "13-hypothesis-validation": {
      "status": "in_progress",
      "started_at": "2025-01-16T09:45:00Z",
      "completed_at": null,
      "agent": "claude-code-3.5",
      "artifacts": [],
      "notes": "Hypothesis written for pod-delete, validating acceptance criteria"
    },
    "14-blast-radius-control": { "status": "pending" },
    "15-steady-state": { "status": "pending" },
    "16-infrastructure-faults": { "status": "pending" },
    "17-application-faults": { "status": "pending" },
    "18-game-day-planning": { "status": "pending" },
    "19-cv-verification": { "status": "pending" },
    "20-observability-integration": { "status": "pending" },
    "21-alerting-recommendations": { "status": "pending" },
    "22-policy-governance": { "status": "pending" },
    "23-cloud-cost-management": { "status": "pending" },
    "24-resilience-scoring": { "status": "pending" },
    "25-postmortem-learning": { "status": "pending" }
  },
  "blockers": [],
  "metrics": {
    "estimated_total_hours": 40,
    "elapsed_hours": 6.5,
    "velocity_phases_per_hour": 1.85,
    "estimated_completion": "2025-01-18T14:00:00Z"
  }
}
```

---

## Workflow Lifecycle States

Each phase transitions through a strict state machine:

```
pending → in_progress → completed
                  ↘ blocked → in_progress → completed
                                ↘ skipped (with reason)
```

**State rules:**
- Only ONE phase can be `in_progress` at a time (agents serialize work)
- `blocked` requires a blocker entry with description and owner
- `skipped` requires an explicit reason recorded
- Phase `completed` cannot be reversed (use postmortem feedback to re-enter)

---

## Core Operations

### Operation 1 — Initialize Progress
```yaml
trigger: first workflow session or missing progress.json
action:
  - Create .commandcode/progress.json with default schema
  - Set all 26 phases to "pending"
  - Set phases 00-03 to "completed" (they run during init)
  - Record start time and agent identifier
```

### Operation 2 — Transition Phase
```yaml
trigger: skill completion or blocker hit
action:
  - Update phase status + timestamps
  - Record artifacts produced
  - Record agent identifier
  - Recalculate metrics (elapsed time, velocity, estimate)
  - If "completed": look up next pending phase and notify orchestrator
  - If "blocked": create blocker entry, do NOT advance
```

### Operation 3 — Add Blocker
```yaml
trigger: any skill identifies an unmet prerequisite or external dependency
blocker_format:
  id: string (e.g., BLK-001)
  phase: string (e.g., "16-infrastructure-faults")
  description: string
  blocked_by: string (what's missing)
  owner: string (who resolves it)
  created_at: ISO timestamp
  resolved_at: null | ISO timestamp
action:
  - Add to blockers array
  - Set phase status to "blocked"
  - Notify user with blocker details
  - Pause workflow advancement until resolved
```

### Operation 4 — Resolve Blocker
```yaml
trigger: blocker becomes resolved
action:
  - Set blocker.resolved_at
  - Set phase back to "in_progress"
  - Continue skill execution
  - Resume workflow advancement
```

### Operation 5 — Generate Status Report
```yaml
trigger: user asks for status, or at each phase transition
output: colored terminal dashboard
```

---

## Status Dashboard

```
╔══════════════════════════════════════════════════════════════╗
║           HYBRID HARNESS + CHAOS WORKFLOW STATUS            ║
╠══════════════════════════════════════════════════════════════╣
║ Project: payment-service-resilience                          ║
║ Progress: ████████████░░░░░░░░░░░░ 12/26 phases (46%)      ║
║ Current:  s13-hypothesis-validation (in_progress)           ║
║ Agent:    claude-code-3.5                                   ║
╠══════════════════════════════════════════════════════════════╣
║                                                            ║
║ FOUNDATION          ████████ 100% (00-03)                  ║
║ CI/CD SCAFFOLDING   ████████ 100% (04-10)                  ║
║ TESTING             ████████ 100% (11)                     ║
║ CHAOS DESIGN        ██░░░░░░  25% (12-17) ◄ HERE          ║
║   ✓ s12-experiment-design           completed               ║
║   ● s13-hypothesis-validation       in_progress             ║
║   ○ s14-blast-radius-control        pending                 ║
║   ○ s15-steady-state                pending                 ║
║   ○ s16-infrastructure-faults       pending                 ║
║   ○ s17-application-faults          pending                 ║
║ GAME DAY            ░░░░░░░░   0% (18)                     ║
║ VERIFY & OBSERVE    ░░░░░░░░   0% (19-21)                  ║
║ GOVERN & LEARN      ░░░░░░░░   0% (22-25)                  ║
║                                                            ║
╠══════════════════════════════════════════════════════════════╣
║ Blockers: 0                                                ║
║ Est. completion: 2025-01-18                                ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Missed Task Detection

Before completing the workflow, run this checklist:

```yaml
missed_task_checks:
  - Each completed phase produced expected artifacts (check phase.artifacts)
  - All P0 requirements from PRD have corresponding implementation skills run
  - Input contracts for each completed phase were satisfied
  - Output contracts for each completed phase feed into next phase correctly
  - No phase is "stuck" in blocking for >48 hours without escalation
  - Taste updates were captured during all interactions
  - At least one test phase (s11) completed before chaos phases (s12-s18)
  - Approval gates (from taste) were respected
```

If `missed_task_checks` finds gaps, surface:
```yaml
missed_task_report:
  format: "⚠️ Phase {X} ({name}) produced no artifacts but should have. Expected: {expected_outputs}"
  severity: warning | blocker
```

---

## Agent Handoff Protocol

When the workflow is handed from one agent to another (or session resumes):

```yaml
handoff_summary:
  to_provide:
    - Current phase and status
    - Last completed phase with artifacts
    - Any active blockers
    - Taste preferences loaded
    - Expected next 3 phases
    - Remaining P0 requirements to fulfill

  handoff_message: |
    ══════════════════════════════════════════════
    AGENT HANDOFF — hybrid-harness-chaos-process-prm
    ══════════════════════════════════════════════
    Previous:  claude-code-3.5 (completed s12)
    Current:   s13-hypothesis-validation
    Blockers:  0 active
    Tastes:    23 preferences loaded
    Next:      s13 → s14 → s15

    Artifacts from last session:
    - experiment-pod-delete.yaml
    - engine-payment-pod-delete.yaml

    P0 items remaining: 8
    ─────────────────────────────────────────────
    Continue from .commandcode/progress.json
```

---

## Burndown Metrics

Track velocity for estimation:

```json
{
  "burndown": {
    "total_phases": 26,
    "completed": 12,
    "remaining": 14,
    "sessions": 3,
    "phase_history": [
      {"phase": "04-pipeline-design", "duration_minutes": 155},
      {"phase": "05-service-onboarding", "duration_minutes": 70},
      {"phase": "06-delegate-management", "duration_minutes": 20},
      {"phase": "07-secrets-management", "duration_minutes": 10},
      {"phase": "08-feature-flags", "duration_minutes": 10},
      {"phase": "09-template-library", "duration_minutes": 5},
      {"phase": "10-gitops", "duration_minutes": 10},
      {"phase": "11-cloakbrowser-testing", "duration_minutes": 155},
      {"phase": "12-experiment-design", "duration_minutes": 45}
    ],
    "average_phase_minutes": 53,
    "estimated_remaining_minutes": 742
  }
}
```

---

## Success Criteria
- [ ] Progress.json created and initialized with all 26 phases
- [ ] State transitions follow the strict state machine (no invalid transitions)
- [ ] Only one phase in_progress at any time
- [ ] Blockers documented with owner and description
- [ ] Dashboard displays correctly at each phase boundary
- [ ] Missed task check runs before workflow completion
- [ ] Agent handoff includes full context for next agent
- [ ] Burndown metrics calculated and updated
- [ ] No phase marked complete without artifact entries

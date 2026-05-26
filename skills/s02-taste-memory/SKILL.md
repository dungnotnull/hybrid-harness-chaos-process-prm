---
name: taste-memory-management
description: >
  Manage developer preferences (taste) and session memory across all AI agent
  interactions. Use this skill whenever the user corrects an agent's behavior,
  expresses a preference ("I prefer X over Y", "always use Z pattern"),
  or when starting a new session that should benefit from previously learned
  preferences. Also use when the orchestrator (s00) initializes to load all
  stored tastes. This skill reads from and writes to .commandcode/taste/ and
  ensures preferences persist across sessions and are injected into every
  downstream skill's context object.
---

# Taste & Memory Management (s02)

## Purpose
Build and maintain a persistent model of the developer's preferences across all interactions — technology choices, code style, naming conventions, workflow habits, approval thresholds, and risk tolerance. Ensure every AI agent in this project has access to this preference model so they don't repeat mistakes or violate established conventions.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| User corrections / feedback | Real-time user messages | Yes |
| Skill execution history | Progress tracker (s03) | Yes |
| Previous taste file | `.commandcode/taste/taste.md` | No (created if absent) |
| CLAUDE.md conventions | Project root | Yes |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Updated taste file | `.commandcode/taste/taste.md` | Markdown |
| Taste context object | Injected into all skill contexts | JSON |
| Category-specific taste files | `.commandcode/taste/<category>/taste.md` | Markdown |
| Taste summary for new agents | New session bootstrap | Markdown |

---

## Taste Architecture

```
.commandcode/taste/
├── taste.md                    # Main file — all categories + learnings
├── pipeline-design/
│   └── taste.md                # Moved here when >5 learnings
├── chaos-engineering/
│   └── taste.md
├── governance/
│   └── taste.md
└── ...
```

Each taste learning follows this format:
```markdown
## Category Name

- Learning statement with specific guidance. Confidence: 0.XX
```

---

## Taste Categories

| Category | What It Tracks | Confidence Sources |
|---|---|---|
| Technology | Language, framework, cloud, tool choices | Explicit user statements |
| Code Style | Formatting, naming, patterns, conventions | Corrections to generated code |
| Workflow | Approval gates, skip patterns, phase ordering | Workflow overrides |
| Risk Tolerance | Blast radius limits, chaos intensity, env gates | Chaos-related corrections |
| Communication | Verbosity, format, emoji usage, language | Interaction patterns |
| Testing | Test framework, coverage threshold, approach | Testing-related corrections |
| Deployment | Strategy defaults, rollback behavior | Pipeline-related corrections |
| Observability | Tool preferences, alert thresholds | Monitoring-related corrections |

---

## Learning Mechanism

### When to Learn (Capture Triggers)
The agent MUST capture a taste learning whenever:

1. **Explicit correction**: "No, use TypeScript not JavaScript" → `Technology.Confidence: 0.95`
2. **Pattern enforcement**: "Always use object parameters for functions with 2+ params" → `CodeStyle.Confidence: 0.85`
3. **Workflow override**: "Skip the approval gate for dev deployments" → `Workflow.Confidence: 0.90`
4. **Preference statement**: "I prefer Commander.js for CLIs" → `Technology.Confidence: 0.80`
5. **Repeated correction**: User corrects same pattern 2+ times → `Confidence: 0.95`
6. **Outcome feedback**: "That blast radius was too aggressive" → `RiskTolerance.Confidence: 0.85`
7. **Silent acceptance**: User accepts generated code without changes 3+ times → `Confidence: 0.70`

### Confidence Scoring
```
0.95+ = Explicit, repeated user statement (very high confidence)
0.85  = Explicit user statement, first occurrence (high confidence)
0.70  = Inferred from consistent behavior (medium confidence)
0.50  = Inferred from single instance (low confidence — ask before using)
0.30  = Default assumption (only use as fallback)
```

---

## Core Workflow

### Step 1 — Load Existing Tastes (Session Start)
```yaml
action: read_taste_file
files:
  - .commandcode/taste/taste.md             # Main file
  - .commandcode/taste/*/taste.md           # Category files (if referenced)
on_missing: create_empty_taste_file()

action: load_into_context
destination: workflow_context.taste
format: structured_object
```

### Step 2 — Detect Learning Opportunities (During Work)
```yaml
monitor:
  - All user messages for correction patterns
  - All tool outputs for user acceptance/rejection signals
  - Workflow override commands
  - Explicit preference statements
  
detection_patterns:
  - "use X instead of Y" → Technology preference
  - "always/never do X"  → High-confidence rule
  - "I prefer X"         → Medium-confidence preference
  - "don't X" / "stop X" → Negative learning
```

### Step 3 — Capture and Store (Post-Interaction)
```yaml
action: write_taste_learning
rules:
  - NEVER overwrite without user confirmation if confidence < 0.95
  - ALWAYS timestamp new learnings
  - Group under correct category heading
  - If category >5 learnings, move to own file
  - Maintain chronological order within category
```

### Step 4 — Inject Into Context (Every Dispatch)
```yaml
action: inject_taste_into_context
timing: before_skill_dispatch
destination: context.taste
content:
  - All relevant category learnings with confidence > 0.70
  - Category summary table for quick reference
  - Recent learnings (last 5 interactions)
```

---

## Taste File Format

### Main Taste File (taste.md)
```markdown
# Taste — <PROJECT_NAME>

> Auto-generated developer preference model. Updated by s02-taste-memory.
> Last updated: 2025-06-15T14:30:00Z
> Sessions monitored: 47

## Technology
- Use TypeScript for all new code. Confidence: 0.95
- Use Commander.js for CLI tools (not yargs). Confidence: 0.90
- Deploy on AWS EKS. Use us-east-1 for prod, us-west-2 for DR. Confidence: 0.85
- Prefer PostgreSQL over MySQL for new services. Confidence: 0.80

## Code Style
- Use const, never let for non-reassigned variables. Confidence: 0.90
- Object parameters for functions with 2+ parameters. Confidence: 0.85
- No default exports — always named exports. Confidence: 0.80
- 2-space indentation, double quotes. Confidence: 0.95

## Workflow
- Skip approval gates for dev environment. Confidence: 0.95
- Auto-approve staging deployments if CV passes. Confidence: 0.85
- Never deploy to production on Fridays. Confidence: 0.95
- Requires 2 SRE approvals for production chaos. Confidence: 0.90

## Risk Tolerance
- Max pod-delete % in production: 30%. Confidence: 0.90
- Max chaos duration in production: 60s. Confidence: 0.90
- Auto-abort on error rate > 5%. Confidence: 0.95
- No chaos experiments during peak hours (9-17 Tue-Thu). Confidence: 0.85

## Communication
- Prefer bullet lists over dense paragraphs. Confidence: 0.80
- No emojis unless explicitly requested. Confidence: 0.85
- Include rollback steps in every recommendation. Confidence: 0.90

## Testing
- Use Playwright for E2E tests. Confidence: 0.90
- Minimum 80% code coverage required. Confidence: 0.85
- Always run integration tests before chaos experiments. Confidence: 0.95

## Deployment
- Default deploy strategy: Rolling (not Canary) for internal services. Confidence: 0.80
- Always enable auto-rollback on CV failure. Confidence: 0.95
- GitOps preferred over Harness CD for Kubernetes. Confidence: 0.70

## Observability
- Prometheus + Grafana for metrics. Confidence: 0.90
- Datadog for APM (existing investment). Confidence: 0.85
- Slack for alerts, PagerDuty for critical. Confidence: 0.90
```

### Category File (e.g., pipeline-design/taste.md)
When a category exceeds 5 learnings, move it to its own file:

```markdown
# Pipeline Design Preferences
> Moved to dedicated file — 8 learnings aggregated.

- Default to Rolling deploy for stateless services. Confidence: 0.85
- Always include CV step after deploy before approval. Confidence: 0.95
- Use `<+pipeline.variables.imageTag>` — never hardcode tags. Confidence: 0.95
- CI stage must include SAST (Semgrep) + container scan (Trivy). Confidence: 0.90
- Approval stage required between staging and production. Confidence: 0.95
- Feature flags gate all production chaos experiments. Confidence: 0.90
- Pipeline variables in SCREAMING_SNAKE_CASE. Confidence: 0.80
- Notifications via Slack webhook, not email. Confidence: 0.85
```

---

## Injecting Taste Into Skill Context

When orchestrator dispatches to any skill, the taste context is injected:

```yaml
# Injected into workflow_context for every skill
taste:
  technology:
    primary_language: TypeScript | Confidence: 0.95
    cli_framework: Commander.js | Confidence: 0.90
    cloud: AWS EKS | Confidence: 0.85
    database: PostgreSQL | Confidence: 0.80

  code_style:
    variable_declaration: const (never let) | Confidence: 0.90
    function_params: object params for 2+ args | Confidence: 0.85
    exports: named only, no defaults | Confidence: 0.80
    formatting: 2-space indent, double quotes | Confidence: 0.95

  risk_tolerance:
    prod_blast_radius: 30% pods max | Confidence: 0.90
    prod_chaos_duration: 60s max | Confidence: 0.90
    auto_abort_threshold: error_rate > 5% | Confidence: 0.95
    timing_restrictions: no chaos during peak hours Tue-Thu | Confidence: 0.85

  workflow:
    dev_approvals: skip | Confidence: 0.95
    staging_auto_approve: if CV passes | Confidence: 0.85
    friday_deploy_ban: true | Confidence: 0.95

  testing:
    e2e_framework: Playwright | Confidence: 0.90
    coverage_threshold: 80% | Confidence: 0.85
    pre_chaos_tests: integration tests must pass | Confidence: 0.95

  deployment:
    strategy: Rolling for internal | Confidence: 0.80
    auto_rollback: always on CV fail | Confidence: 0.95
    gitops_preferred: true | Confidence: 0.70
```

---

## Taste Conflict Resolution

When two learnings conflict:
1. Higher confidence wins
2. More recent wins if confidence equal
3. Explicit wins over inferred
4. Surface conflict to user if unresolved

```yaml
conflict_example:
  learning_1: "Use Canary deploy for production" (Confidence: 0.80, 2025-03)
  learning_2: "Use Rolling deploy for all services" (Confidence: 0.90, 2025-05)
  resolution: learning_2 wins (higher confidence + more recent)
```

---

## Memory Decay

Preferences can become stale. The agent should:
- Re-ask about any preference with confidence < 0.70 when context is relevant
- Mark preferences unused for 90+ days as "stale" and re-confirm
- Never apply stale preferences without re-asking

```yaml
stale_check:
  threshold: 90 days
  action: "I notice you preferred X historically. Is that still current?"
```

---

## Cross-Agent Memory Synchronization

When switching between Claude Code, Codex, GPT, Gemini:

```yaml
bootstrap_message:
  format: "You are working on <PROJECT>. Developer preferences loaded from taste file. Key preferences: [summary of top-5 highest-confidence tastes]."
  source: .commandcode/taste/taste.md
  importance: MUST be the first context message in any new agent session
```

---

## Success Criteria
- [ ] Taste file exists and is read at start of every session
- [ ] Tastes injected into every skill context
- [ ] New learnings captured with correct confidence score
- [ ] Category files created when >5 learnings accumulate
- [ ] Conflicting learnings resolved automatically or surfaced
- [ ] Stale preferences re-confirmed after 90 days
- [ ] Bootstrap message includes taste summary for new agents
- [ ] No manual edits to taste files — only this skill writes them
- [ ] At least 5 learnings accumulated per major category by project end

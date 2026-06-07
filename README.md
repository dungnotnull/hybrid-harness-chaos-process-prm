# hybrid-harness-chaos-process-prm (v0.5.0)

**A 37-skill agentic workflow for platform engineering — spanning CI/CD, security, chaos engineering, observability, governance, compliance, deep research, system optimization, documentation writing, and adversarial critique, purpose-built for the era of AI-assisted development.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-37-00b894.svg)](skills/)
[![AI Compatible](https://img.shields.io/badge/AI-Claude%20Code%20%7C%20Codex%20%7C%20Gemini%20%7C%20GPT--4-8A2BE2.svg)]()
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg)](tools/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-green.svg)](.github/workflows/)

---

## What Is This?

This repository is a **complete, production-grade skill library** designed to be consumed by AI coding agents (Claude Code, Codex, Gemini, GPT-4). It provides a standardized, 37-step Agile workflow that guides developers from project ideation through requirements gathering, CI/CD scaffolding, security scanning, chaos experimentation, observability integration, release governance, disaster recovery, compliance auditing, deep research, system optimization, documentation, and adversarial critique.

**It's not a framework you install. It's a workflow you clone and point your AI agent at.**

```text
Ideation → BA Analysis → CI/CD → Security Gate → Testing → Chaos → Game Day
→ Verification → Alerting → Governance → Release → DR → Compliance → Strategic Review
→ Deep Research (anytime) → System Optimization (anytime) → Documentation (anytime)
→ Devil's Advocate Critique (anytime)

Also: AI Agent Integration across all 37 skills with Harness AI agents + MCP
```

---

## Why This Exists

Modern development is increasingly agentic — AI agents write code, design pipelines, and execute operations. But agents are only as good as their instructions. Without structured, expert-level guidance, agents produce inconsistent, incomplete, or unsafe output.

**This project solves that by providing:**

- **Standardized workflows** — Every agent follows the same battle-tested process, regardless of which LLM powers it
- **Input/output contracts** — Skills declare what they consume and produce, preventing context loss between handoffs
- **Safety gates** — Security scanning blocks deployment, blast radius control prevents production chaos, release management prevents Friday night deploys
- **Adversarial critique** — Every major decision can be stress-tested through the Devil's Advocate skill (s35), adapted from the [Devil's Advocate Agent](https://github.com/dungnotnull/devils-advocate-agent)
- **Taste memory** — Developer preferences are learned, persisted, and injected into every agent session
- **Progress tracking** — Multi-agent sessions maintain state across interruptions; no duplicated or missed work

---

## What's New in v0.5.0

- **s35-devils-advocate**: New adversarial critique skill adapted from [dungnotnull/devils-advocate-agent](https://github.com/dungnotnull/devils-advocate-agent). Provides 4-intensity Socratic questioning, logical fallacy detection, argument strength scoring, and multi-perspective challenge generation. Callable at ANY phase as a quality gate.
- **Claude Plugin Manifest**: First-class [Claude Code/Cowork](https://github.com/anthropics/knowledge-work-plugins) integration via .claude-plugin/ with slash commands (/orchestrate, /critique, /progress, /validate)
- **Progress Tracker CLI**: Full CLI tool (progress-tracker) for managing workflow state — init, status, transition, block, resolve, report, handoff
- **GitHub Actions CI**: Automated skill validation, linting, and testing on push/PR
- **Pre-commit Hooks**: Validates skills, checks YAML/JSON, prevents direct commits to main
- **Issue/PR Templates**: Structured bug reports, feature requests, skill proposals, and PR checklists
- **Security Policy**: Full SECURITY.md with vulnerability reporting and security principles
- **Changelog**: CHANGELOG.md tracking all versions

---

## Skill Architecture

Every skill follows the same structure:

```text
skills/sNN-<name>/
└── SKILL.md              # Primary instruction file (YAML frontmatter + Markdown body)
    ├── Input Contract     # What this skill needs before it can run
    ├── Output Contract    # What this skill produces for downstream skills
    ├── Prerequisites      # External dependencies (tools, accounts, access)
    ├── Workflow            # Step-by-step execution instructions
    ├── AI Agent Integration  # Autonomy level, Harness AI agent, human gates, MCP
    ├── Templates/Examples # Runnable YAML, scripts, configuration
    └── Success Criteria   # Measurable completion checklist
```

---

## Complete Skill Index

### Phase 0: Foundation (00-03)
| # | Skill | Purpose |
|---|-------|---------|
| 00 | Orchestrator | Master workflow coordinator — dispatches phases, validates I/O contracts, maintains context |
| 01 | BA Requirements | Professional business analysis — produces PRD, ADRs, prioritized backlog |
| 01-1 | User Flow Writing | Multi-perspective user flow mapping with edge-case stress-testing |
| 02 | Taste Memory | Developer preference learning — persists tastes across sessions and agents |
| 03 | Progress Tracker | Multi-agent progress state machine — prevents duplicated and missed work |

### Phase 2: CI/CD Scaffolding (04-10)
| # | Skill | Purpose |
|---|-------|---------|
| 04 | Pipeline Design | Harness CI/CD pipeline YAML with verification, chaos steps, and approval gates |
| 05 | Service Onboarding | End-to-end service registration — connectors, environments, infrastructure definitions |
| 06 | Delegate Management | Harness delegate install, configuration, RBAC, and high availability |
| 07 | Secrets Management | Zero-hardcoded-secret policy — Vault, AWS SM, GCP SM integration with rotation |
| 08 | Feature Flags | Progressive delivery with flag pipelines, kill switches, and SDK integration |
| 09 | Template Library | Reusable pipeline building blocks with versioning and enforcement |
| 10 | GitOps | ArgoCD-backed GitOps with drift detection, self-healing, and ApplicationSets |

### Phase 3: Security Gate (11)
| # | Skill | Purpose |
|---|-------|---------|
| 11 | Security Scanning | SAST (Semgrep), SCA (Snyk/OWASP), container scanning (Trivy), secrets detection (Gitleaks), IaC security (Checkov), SBOM generation (Syft + Cosign), SLSA provenance — **hard blocks deployment on CRITICAL findings** |

### Phase 4: Testing (12-13)
| # | Skill | Purpose |
|---|-------|---------|
| 12 | CloakBrowser Testing | E2E testing with accessibility audit, visual regression, and pre/post-chaos baseline capture |
| 13 | Performance Testing | 7-level load testing ladder (smoke → baseline → load → stress → soak → spike → chaos-combined) with k6 |

### Phase 5: Chaos Experiment Design (14-19)
| # | Skill | Purpose |
|---|-------|---------|
| 14 | Experiment Design | ChaosExperiment + ChaosEngine YAML with probe configuration |
| 15 | Hypothesis Validation | Scientific hypothesis formulation with acceptance criteria and validation scripts |
| 16 | Blast Radius Control | Scope/isolation/abort mechanisms with progressive expansion matrix |
| 17 | Steady State | Baseline metrics, Prometheus probes, pre-experiment health checks |
| 18 | Infrastructure Faults | Node drain, disk fill, CPU/memory hog, EC2 stop, AZ failure |
| 19 | Application Faults | Pod delete, container kill, network latency/loss, DNS error, resource exhaustion |

### Phase 6: Game Day (20)
| # | Skill | Purpose |
|---|-------|---------|
| 20 | Game Day Planning | Orchestrated resilience exercises with incident response drills, composite scenarios, and team role assignments |

### Phase 7: Verification & Observability (21-23)
| # | Skill | Purpose |
|---|-------|---------|
| 21 | CV Verification | Continuous verification with SLO definition and automatic rollback on regression |
| 22 | Observability Integration | Chaos-specific Grafana dashboards, Prometheus alert rules, and observability health checks |
| 23 | Alerting & Recommendations | P0-P3 severity alert routing, Slack/PagerDuty templates, automated remediation engine |

### Phase 8: Governance (24-28)
| # | Skill | Purpose |
|---|-------|---------|
| 24 | Policy Governance | OPA (Rego) policies for pipeline tagging, deployment windows, approval gates, chaos blast radius |
| 25 | Cloud Cost Management | CCM with budget alerts, AutoStopping, cost perspectives, and FinOps review |
| 26 | Resilience Scoring | 5-component quantitative scoring (availability, performance, recovery, correctness, observability) with production gate |
| 27 | Postmortem Learning | Blameless RCA with 5 Whys, action item tracking, knowledge base entries, and s01 feedback loop |
| 28 | Release Management | Go/No-Go checklists, deployment calendar, auto-generated release notes, multi-service coordinated rollouts |

### Phase 9: Resilience & Continuity (29-30)
| # | Skill | Purpose |
|---|-------|---------|
| 29 | Disaster Recovery | RTO/RPO matrix, multi-region active-active architecture, failover runbook, backup validation |
| 30 | Compliance & Audit | SOC2/HIPAA/GDPR/PCI-DSS/ISO 27001 control mapping, auto-generated audit trail, signed evidence bundles |

### Strategic Innovation (31 — callable at any phase)
| # | Skill | Purpose |
|---|-------|---------|
| 31 | Strategic Creator | Advisory-only brainstorming with structured trade-off analysis — proposes, warns, never implements without user acceptance |

### Research (32 — callable at any phase)
| # | Skill | Purpose |
|---|-------|---------|
| 32 | Deep Research | Multi-source research engine (Google Scholar, arXiv, official docs, industry blogs) with evidence synthesis and interactive brainstorming debrief |

### System Optimization (33 — callable at any phase)
| # | Skill | Purpose |
|---|-------|---------|
| 33 | System Optimization | 7-module deep-dive audit: request latency analysis, N+1 query detection, concurrent user stress testing, atomicity verification, concurrency auditing, security vulnerability auditing, agent-proposed evaluations |

### Documentation (34 — callable at any phase)
| # | Skill | Purpose |
|---|-------|---------|
| 34 | Documentation Writing | Technical specs, user flow diagrams, usage guides, and README generation — audience-aware writing |

### Adversarial Critique (35 — callable at any phase) 🆕
| # | Skill | Purpose |
|---|-------|---------|
| 35 | Devil's Advocate | Stress-test every decision, design, hypothesis, and strategy with structured Socratic questioning, logical fallacy detection (14+ types), argument strength scoring (5 dimensions), and multi-perspective challenge generation. 4 intensity levels: Skeptic → Critic → Prosecutor → Demolisher. Adapted from [dungnotnull/devils-advocate-agent](https://github.com/dungnotnull/devils-advocate-agent). |

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/dungnotnull/hybrid-harness-chaos-process-prm.git
cd hybrid-harness-chaos-process-prm
```

### 2. Install tools

```bash
pip install -e .
```

### 3. Initialize progress tracking

```bash
progress-tracker init --project-name "my-project"
progress-tracker status
```

### 4. Point your AI agent at it

For **Claude Code** (Anthropic):
```bash
claude --project hybrid-harness-chaos-process-prm
```
Claude Code automatically reads CLAUDE.md and discovers the skill library.

For **other agents** (Codex, Gemini, GPT-4 via API):
Include the repository as context. Start with CLAUDE.md as the system prompt, then reference specific skills as needed.

### 5. Use slash commands

With the Claude Plugin installed:

| Command | Description |
|---|---|
| /orchestrate | Start or resume the full workflow |
| /critique [subject] | Invoke Devil's Advocate (s35) on any subject |
| /progress | Show workflow progress dashboard |
| /validate | Validate all SKILL.md files for structural correctness |

---

## Tools

The project includes CLI tools for validation, documentation, scaffolding, progress tracking, and chaos engineering integration:

| Tool | Purpose |
|---|---|
| validate-skills | Checks frontmatter, required sections, autonomy levels, cross-references, duplicates |
| generate-docs | Auto-generates SKILLS-CATALOG.md with agent coverage matrix, MCP matrix, autonomy distribution |
| scaffold-skill | Creates new skills with AI integration metadata auto-filled from phase/agent defaults |
| progress-tracker | Full CLI for workflow state management — init, status, transition, block, resolve, report, handoff |
| chaos-mcp-server | MCP server with 9 tools for LitmusChaos and Harness Chaos operations (dry-run by default) |

```bash
# Validate all 36 SKILL.md files
validate-skills --project-root .

# Generate SKILLS-CATALOG.md
generate-docs --project-root .

# Create a new skill with correct structure
scaffold-skill --number 36 --name "my-skill" --description "desc"

# Initialize workflow progress
progress-tracker init --project-name "my-project"

# Check status
progress-tracker status

# Transition a phase
progress-tracker transition 04-pipeline-design in_progress --agent "claude-code"

# Add a blocker
progress-tracker block "Waiting for security approval" --phase 11-security-scanning

# Generate a handoff summary
progress-tracker handoff
```

---

## AI Agent Architecture

All 37 skills integrate with **Harness AI's specialized agent ecosystem** and the broader chaos engineering MCP ecosystem.

### SRE Autonomy Levels (Google SRE Framework)

Every skill declares its autonomy level in its SKILL.md:

| Level | Name | Agent Role |
|---|---|---|
| **L0** | Manual | None |
| **L1** | Hypothesis | AI suggests, human decides |
| **L2** | Assisted | AI drafts, human approves |
| **L3** | Delegated | AI executes, human reviews |
| **L4** | Full Autonomy | AI acts independently |

Current project state: **L1-L2**. Target: **L2-L3**. Safety-critical skills (s16, s29) remain L1-L2 permanently. Devil's Advocate (s35) is **adversarial by design** — intentionally independent of any Harness AI agent.

### Harness AI Agent Coverage

| Agent | Model | Skills Covered |
|---|---|---|
| DevOps Agent | Claude Opus 4.5 (Vertex AI) | s01, s01-1, s04-s10, s24, s28, s33-M2 |
| Reliability Agent | Harness AI | s14-s20, s26 |
| SRE Agent | Harness AI | s21-s23, s27, s29, s33-M4/M5 |
| Test Agent | Harness AI | s12-s13, s33-M1/M3 |
| FinOps Agent | Harness AI | s25 |
| AppSec/STO Agent | Harness AI | s11, s30, s33-M6 |
| Knowledge Graph | Harness AI | s03 |
| **None (adversarial by design)** | — | **s35** |

### MCP Integration (Chaos Skills)

| Platform | Integration Skills |
|---|---|
| LitmusChaos MCP | s14-s20 |
| Gremlin MCP | s14-s17 |
| Steadybit MCP | s14-s20 |
| AWS FIS + Bedrock | s18 |
| Harness Chaos (native) | s14-s20 |

---

## Development Phase Tracking

This project uses **multiple layers** of development phase tracking:

### 1. Local State (.commandcode/progress.json)
The progress-tracker CLI manages local workflow state:
- Init: progress-tracker init
- Status: progress-tracker status
- Transition: progress-tracker transition <phase> <status>
- Block: progress-tracker block "description"
- Handoff: progress-tracker handoff

### 2. CI/CD Gates (GitHub Actions)
Every PR is validated by .github/workflows/ci.yml:
- All SKILL.md files pass structural validation
- Python code passes linting (ruff)
- YAML frontmatter is valid
- Cross-references between skills are correct
- SKILLS-CATALOG.md is up to date

### 3. Pre-commit Hooks
Install pre-commit for local quality enforcement:
```bash
pip install pre-commit
pre-commit install
```

Hooks enforce:
- Skill validation before commits
- YAML/JSON syntax checking
- Trailing whitespace removal
- Prevent direct commits to main

### 4. Issue Tracking (GitHub Issues)
Use structured templates for:
- Bug reports (.github/ISSUE_TEMPLATE/bug_report.md)
- Feature requests (.github/ISSUE_TEMPLATE/feature_request.md)
- Skill proposals (.github/ISSUE_TEMPLATE/skill_proposal.md)

---

## Project Principles

All 37 skills are designed around these core principles:

| Principle | Description |
|---|---|
| **Safety First** | Never run destructive operations without explicit human approval. All chaos experiments require dry-run validation. |
| **Hypothesis-Driven** | No pipeline stage without a success criterion. No chaos experiment without a formal hypothesis. No feature flag without a measurable rollout metric. |
| **Security as a Gate** | Security scanning runs on every build — no exceptions. Zero HIGH/CRITICAL CVEs = deployment blocked. SBOM generated and signed for every artifact. |
| **Performance Before Chaos** | Load testing must establish baselines before any fault injection. Chaos results are meaningless without a performance baseline. |
| **Observability as a Gate** | Every deployment has a verification step. Every chaos experiment has monitoring active. No observability = execution blocked. |
| **Infrastructure as Code** | All resources expressed as YAML. No manual UI-only changes. Everything reproducible from version control. |
| **Least Privilege** | Delegates scoped to namespaces. Chaos accounts scoped to targets. Secrets never in logs. |
| **Adversarial Quality Gates** | Every major decision can be stress-tested through s35 (Devil's Advocate). No design, hypothesis, or release goes unchallenged. |
| **Release Governance** | Every production deploy has a Go/No-Go checklist. Deployment calendars respected. Rollback tested before deployment. |
| **Compliance is Continuous** | Audit trails auto-generated quarterly. Evidence signed and timestamped. Control mapping updated with every new skill. |
| **Taste-Aware Execution** | Developer preferences learned and persisted. New agents inherit prior preferences. Corrections captured at high confidence. |

---

## Technology Stack

| Category | Tools |
|---|---|
| **CI/CD** | Harness (pipeline, FF, GitOps, CCM, Policy Engine) |
| **Chaos** | LitmusChaos, Harness Chaos Engineering |
| **Observability** | Prometheus, Grafana |
| **Testing** | CloakBrowser + Playwright (E2E), k6 (load/performance) |
| **Security** | Semgrep (SAST), Trivy (container), Snyk/OWASP DC (SCA), Gitleaks (secrets), Checkov (IaC), Syft (SBOM), Cosign + Rekor (signing) |
| **Infrastructure** | Kubernetes, Helm, ArgoCD, Velero |
| **Secrets** | HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager |
| **Governance** | Open Policy Agent (OPA/Rego) |
| **Adversarial Critique** | Devil's Advocate Agent (fallacy detection, argument scoring) |

---

## Directory Layout

```text
hybrid-harness-chaos-process-prm/
├── README.md                    <- You are here
├── CLAUDE.md                    <- Canonical entry point for all AI agents
├── CHANGELOG.md                 <- Version history
├── SECURITY.md                  <- Security policy and vulnerability reporting
├── pyproject.toml               <- Python tooling config + CLI entry points
├── .pre-commit-config.yaml      <- Pre-commit hooks for quality enforcement
├── .markdownlint.json           <- Markdown linting config
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               <- CI pipeline (validate, lint, test)
│   │   └── release.yml          <- Release automation
│   ├── ISSUE_TEMPLATE/           <- Bug reports, feature requests, skill proposals
│   └── PULL_REQUEST_TEMPLATE.md <- PR checklist with skill quality gate
│
├── .claude-plugin/              <- Claude Code/Cowork plugin manifest
│   ├── plugin.json              <- Plugin metadata and triggers
│   └── commands/                <- Slash commands
│       ├── orchestrate.md       <- /orchestrate - Start or resume workflow
│       ├── critique.md          <- /critique - Invoke Devil's Advocate
│       ├── progress.md          <- /progress - Check workflow state
│       └── validate.md          <- /validate - Validate all skills
│
├── .commandcode/
│   ├── taste/taste.md           <- Developer preferences (auto-managed by s02)
│   ├── progress.json            <- Workflow state (auto-managed by s03)
│   ├── prd.md                   <- Product Requirements Document (produced by s01)
│   ├── adr/                     <- Architecture Decision Records (produced by s01)
│   ├── backlog.md               <- Prioritized backlog (produced by s01)
│   └── artifacts/               <- All YAML, scripts, reports produced by skills
│       ├── pipeline-*.yaml
│       ├── security/*.sarif
│       ├── perf/*.json
│       ├── experiment-*.yaml
│       ├── resilience-*.json
│       ├── research/
│       ├── optimization/
│       ├── critique/             <- Devil's Advocate reports (produced by s35)
│       ├── dr/
│       ├── compliance/
│       └── releases/
│
├── scripts/
│   └── pre-commit-validate.py   <- Pre-commit validation script
│
├── tests/
│   ├── test_validate_skills.py  <- Unit tests for skill validation
│   └── test_progress_tracker.py <- Unit tests for progress tracker
│
├── tools/                       <- CLI tools for the skill framework
│   ├── validate_skills.py       <- Validate all SKILL.md files
│   ├── generate_docs.py         <- Auto-generate SKILLS-CATALOG.md
│   ├── scaffold_skill.py         <- Create new skills from templates
│   ├── progress_tracker.py       <- CLI for managing workflow state
│   ├── shared/                   <- Shared utilities (constants, models, parsers)
│   └── chaos_mcp_server/         <- MCP server for LitmusChaos + Harness Chaos
│
└── skills/                      <- 37 skills in Agile workflow order
    ├── AI-AGENT-MAPPING.md      <- Harness AI agent mapping + autonomy model
    ├── SKILLS-CATALOG.md        <- Auto-generated skill catalog
    ├── s00-orchestrator/SKILL.md
    ├── ...                      <- s01-s34
    └── s35-devils-advocate/SKILL.md  <- 🆕 Adversarial critique
```

---

## Environment Tiers

All skills respect these environment boundaries:

| Tier | Chaos Allowed | Blast Radius | Approval Required |
|---|---|---|---|
| dev | Yes | Pod-level only | None |
| staging | Yes | Service-level | Team lead |
| preprod | Yes, gated | Namespace-level | SRE + PM |
| production | Yes, with guard rails | Node-level max | SRE + CTO |

---

## Contributing

Contributions that extend, refine, or improve the skill library are welcome.

### What makes a good contribution
- New skills that fill gaps in the workflow
- Enhanced templates, scripts, or examples within existing skills
- Corrections to incorrect or outdated guidance
- Additional compliance framework mappings (s30)
- New innovation patterns for the strategic creator (s31)
- New critique perspectives or fallacy types for the Devil's Advocate (s35)
- Bug fixes for tools or validation

### Skill quality standards
Every SKILL.md must include:
- YAML frontmatter with 
ame and description
- Input Contract table
- Output Contract table
- Prerequisites checklist
- Step-by-step workflow
- Runnable examples (YAML, scripts, configs)
- AI Agent Integration section (Autonomy Level, Agent, Human Gates)
- Success Criteria checklist

### Development workflow
1. Fork the repository
2. Create a branch: git checkout -b feature/skill-description
3. Install pre-commit hooks: pip install pre-commit && pre-commit install
4. Write or modify skills following the quality standards
5. Validate: python tools/validate_skills.py
6. Generate docs: python tools/generate_docs.py
7. Run tests: pytest tests/ -v
8. Commit with descriptive messages
9. Open a pull request against main (use the PR template)

### Pull request process
All PRs are validated by GitHub Actions CI which runs:
- Skill validation (frontmatter, sections, autonomy levels, cross-references)
- Python linting (ruff)
- YAML linting (yamllint)
- Markdown linting (markdownlint-cli2)
- Unit tests (pytest)

---

## FAQ

**Q: Do I need Harness to use this?**
A: The CI/CD skills (s04-s10) are Harness-specific, but the workflow structure, chaos engineering (s14-s20), observability (s21-s23), governance (s24-s28), and compliance (s30) skills are platform-agnostic and work with any stack.

**Q: Can I skip phases?**
A: The orchestrator (s00) enforces phase ordering but allows skipping with explicit user confirmation. Security (s11) and testing (s12-s13) gates are hard blocks — they cannot be skipped for production-bound artifacts.

**Q: What happens if I switch between Claude Code, Codex, and GPT-4?**
A: Progress is stored in .commandcode/progress.json. Taste is stored in .commandcode/taste/taste.md. Any agent that loads the CLAUDE.md context will pick up exactly where the previous agent left off.

**Q: How does the Devil's Advocate (s35) work?**
A: s35 is callable at any phase. It provides 4 intensity levels of critique (Skeptic, Critic, Prosecutor, Demolisher), detects 14+ logical fallacies, scores arguments on 5 dimensions, and produces a PASS/CONDITIONAL/FAIL verdict. It can optionally integrate with the [Devil's Advocate Agent](https://github.com/dungnotnull/devils-advocate-agent) for ML-powered fallacy detection and RAG-grounded counter-arguments.

**Q: How do I track my workflow progress?**
A: Use the progress-tracker CLI: progress-tracker init to start, progress-tracker status to view, progress-tracker transition <phase> <status> to advance, progress-tracker handoff to generate agent handoff summaries.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built on years of platform engineering and chaos engineering practice. Inspired by:
- The [Harness](https://harness.io) platform's CI/CD, FF, GitOps, CCM, and Chaos modules
- [LitmusChaos](https://litmuschaos.io) for the chaos experiment DSL
- [CloakBrowser](https://github.com/CloakHQ/CloakBrowser) for advanced browser automation
- [Anthropic's Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins) for the plugin architecture pattern
- [Devil's Advocate Agent](https://github.com/dungnotnull/devils-advocate-agent) for the adversarial critique mechanism
- Netflix's Chaos Engineering philosophy
- Google's SRE workbook
- The Open Policy Agent community

---

*For AI agents: Read CLAUDE.md first, then s00-orchestrator/SKILL.md. All other skills are dispatched from there.*

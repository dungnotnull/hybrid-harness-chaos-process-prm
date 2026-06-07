# CLAUDE.md — hybrid-harness-chaos-process-prm (Pro Max)

## Project Identity

**Project**: hybrid-harness-chaos-process-prm
**Version**: 0.5.0
**Domain**: Platform Engineering — Continuous Delivery + Resilience Engineering + Security + Compliance + Adversarial Critique
**Audience**: Fullstack developers, SREs, Platform Engineers, DevOps practitioners, Security engineers
**AI Compatibility**: Claude Code (with plugin manifest), Codex, Gemini, GPT-4, and any instruction-following LLM agent

---

## What This Project Does

This repository defines a **37-skill Agile workflow** covering the complete SDLC from ideation to production operations, including adversarial critique:

| Domain | Purpose |
|---|---|
| **Foundation** | Orchestration, BA analysis, user flows, taste memory, progress tracking |
| **CI/CD Engineering** | Pipeline design, service onboarding, delegates, secrets, feature flags, templates, GitOps |
| **Security** | SAST, DAST, container scanning, dependency scanning, SBOM, supply chain security |
| **Testing** | CloakBrowser E2E, performance/load testing, visual regression |
| **Chaos Engineering** | Hypothesis-driven fault injection, blast radius control, steady state, game days |
| **Verification** | Continuous verification, observability, alerting, recommendations |
| **Governance** | OPA policies, cloud cost, release management, disaster recovery |
| **Learning** | Resilience scoring, postmortem RCA, compliance & audit |
| **Research** | Deep multi-source research, evidence synthesis, brainstorming debrief |
| **Optimization** | Latency, N+1, stress, atomicity, concurrency, security audit |
| **Documentation** | Technical specs, user flows, usage guides, README generation |
| **Adversarial Critique** | Devil's Advocate: stress-test decisions, detect fallacies, score arguments |

---

## Quick Reference: Skill Index (37 Skills)

| # | Skill | Phase | Triggers |
|---|---|---|---|
| 00 | Orchestrator | Foundation | workflow, start, orchestrate |
| 01 | BA Requirements | Foundation | analyze, PRD, requirements, spec |
| 01-1 | User Flow Writing | Foundation | user flow, journey map, edge case, sad path |
| 02 | Taste Memory | Foundation | preference, always, never, I prefer |
| 03 | Progress Tracker | Foundation | status, progress, where are we |
| 04 | Pipeline Design | CI/CD | pipeline, CI/CD, stages, deploy |
| 05 | Service Onboarding | CI/CD | onboard, new service, register |
| 06 | Delegate Management | CI/CD | delegate, agent, install |
| 07 | Secrets Management | CI/CD | secret, credential, vault |
| 08 | Feature Flags | CI/CD | feature flag, FF, rollout, toggle |
| 09 | Template Library | CI/CD | template, reusable, stage template |
| 10 | GitOps | CI/CD | GitOps, ArgoCD, sync, drift |
| 11 | Security Scanning | Security | SAST, vulnerability, CVE, SBOM, scan |
| 12 | CloakBrowser Testing | Testing | test, E2E, browser, a11y, visual |
| 13 | Performance Testing | Testing | load test, stress, benchmark, k6 |
| 14 | Experiment Design | Chaos | chaos experiment, fault, inject |
| 15 | Hypothesis Validation | Chaos | hypothesis, steady state, SLO |
| 16 | Blast Radius Control | Chaos | blast radius, scope, limit, abort |
| 17 | Steady State | Chaos | steady state, baseline, probe |
| 18 | Infrastructure Faults | Chaos | node drain, disk, CPU, EC2 stop |
| 19 | Application Faults | Chaos | pod delete, container kill, latency |
| 20 | Game Day Planning | Game Day | game day, chaos day, war game |
| 21 | CV Verification | Verify | continuous verification, canary |
| 22 | Observability | Verify | observability, dashboard, metrics |
| 23 | Alerting | Verify | alert, notify, recommend, remediate |
| 24 | Policy Governance | Govern | OPA, policy, governance, compliance |
| 25 | Cloud Cost | Govern | cost, budget, optimization, CCM |
| 26 | Resilience Scoring | Govern | resilience score, maturity, report |
| 27 | Postmortem | Learn | postmortem, RCA, learning, action |
| 28 | Release Management | Govern | release, deploy prod, change mgmt |
| 29 | Disaster Recovery | Govern | DR, failover, RTO, RPO, backup |
| 30 | Compliance & Audit | Learn | compliance, audit, SOC2, HIPAA, GDPR |
| 31 | Strategic Creator | Any | think bigger, brainstorm, propose, innovate, upgrade |
| 32 | Deep Research | Any | research this, find papers, literature review, evidence for |
| 33 | System Optimization | Any | optimize, latency, N+1, stress test, CCU, atomicity, race condition, security audit |
| 34 | Documentation Writing | Any | docs, README, user guide, technical spec, userflow, usage instructions, how to use |
| 35 | Devil's Advocate | Any | challenge this, stress-test, devil's advocate, find flaws, counter-argument, red team, critique |

---

## Complete Agile Workflow Map

`
PHASE 0: FOUNDATION
  s00 -> s01 -> s02 + s03 (parallel)

PHASE 1: PLANNING & REQUIREMENTS
  s01 (BA deep analysis -> PRD + ADRs + backlog)
  s01-1 (User Flow Writing -> journeys, edge cases, sad paths)

-- s31 (STRATEGIC CREATOR — callable at ANY phase) --
     ^v can be invoked before, during, or after any phase

-- s32 (DEEP RESEARCH — callable at ANY phase) --
     ^v evidence-grounded research + brainstorming debrief

-- s33 (SYSTEM OPTIMIZATION — callable at ANY phase) --
     ^v 7-module audit: latency, N+1, stress, atomicity, concurrency, security, agent-proposed

-- s34 (DOCUMENTATION — callable at ANY phase) --
     ^v Technical specs, userflow diagrams, beginner-friendly usage guides, README

-- s35 (DEVIL'S ADVOCATE — callable at ANY phase) --
     ^v Adversarial critique: challenge decisions, detect fallacies, score arguments, quality gates

PHASE 2: CI/CD SCAFFOLDING
  s04 -> s05 -> s06 -> s07 -> s08 -> s09 -> s10

PHASE 3: SECURITY GATE
  s11 (SAST + SCA + container + secrets + IaC + SBOM + SLSA)
  WARNING: BLOCKS all downstream phases if security gates fail

PHASE 4: TESTING
  s12 -> s13 (E2E baseline -> performance profiling)
  WARNING: Performance baseline required before chaos

PHASE 5: CHAOS EXPERIMENT DESIGN
  s14 -> s15 -> s16 -> s17 -> s18 -> s19

PHASE 6: GAME DAY EXECUTION
  s20 (orchestrated resilience exercise)

PHASE 7: VERIFICATION & OBSERVABILITY
  s21 -> s22 -> s23

PHASE 8: GOVERNANCE & RELEASE
  s24 -> s25 -> s26 -> s27 -> s28

PHASE 9: RESILIENCE & CONTINUITY
  s29 -> s30

FEEDBACK LOOP:
  s27 (findings) -> s01 (re-analysis) -> full cycle
  s30 (compliance gaps) -> s01 (PRD update) -> remediation cycle

DEVIL'S ADVOCATE GATES (s35, callable at ANY phase):
  s14 (experiment design) -> s35 (challenge hypothesis) -> revised experiment
  s15 (hypothesis validation) -> s35 (attack hypothesis) -> strengthened hypothesis
  s28 (release management) -> s35 (pre-deployment gate) -> Go/No-Go verdict
  s31 (strategic proposals) -> s35 (Demolisher-level critique) -> only survivors forwarded
  s01 (PRD review) -> s35 (Critic-level challenge) -> revised PRD
`

---

## Devil's Advocate Integration (s35)

Adapted from [dungnotnull/devils-advocate-agent](https://github.com/dungnotnull/devils-advocate-agent), s35 provides:

| Feature | Description |
|---|---|
| **4 Intensity Levels** | Skeptic (1) -> Critic (2) -> Prosecutor (3) -> Demolisher (4) |
| **14+ Fallacy Types** | Ad Hominem, Straw Man, Hasty Generalization, False Dichotomy, Slippery Slope, etc. |
| **5-Dimension Scoring** | Clarity, Evidence Quality, Logical Consistency, Novelty, Defense Improvement (0-100 each) |
| **4-Perspective Challenge** | Business, Engineering, Reliability, Security lenses |
| **Quality Gate Verdict** | PASS (>=70), CONDITIONAL (>=50), FAIL (<50 or any dimension <40) |
| **Optional ML Enhancement** | Can integrate with Devil's Advocate Agent for NLI-based fallacy detection and RAG-grounded counter-arguments |

Use /critique [subject] via the Claude Plugin or invoke s35 directly in any skill workflow.

---

## Progress Tracking & Development Phase Management

### Local State (.commandcode/progress.json)
The progress-tracker CLI manages workflow state:
`
progress-tracker init --project-name "my-project"
progress-tracker status          # Show dashboard
progress-tracker next            # Show next phase
progress-tracker transition 04-pipeline-design in_progress --agent "claude-code"
progress-tracker block "Waiting for security approval"
progress-tracker resolve BLK-001
progress-tracker report          # Generate full report
progress-tracker handoff         # Agent handoff summary
`

### CI/CD Gates (GitHub Actions)
Every PR is validated by .github/workflows/ci.yml:
- All SKILL.md files pass structural validation
- Python code passes linting (ruff)
- Cross-references between skills are correct
- SKILLS-CATALOG.md is up to date

### Pre-commit Hooks
`
pip install pre-commit && pre-commit install
`
Enforces: skill validation, YAML/JSON syntax, trailing whitespace, no direct commits to main.

---

## Plugin Integration (Claude Code/Cowork)

This project includes a .claude-plugin/ manifest for first-class Claude Code/Cowork integration:

| Command | Description |
|---|---|
| /orchestrate [phase] | Start or resume the full workflow from any phase |
| /critique [subject] | Invoke Devil's Advocate (s35) to stress-test any decision |
| /progress | Show workflow progress dashboard |
| /validate | Validate all SKILL.md files for structural correctness |

Adapted from [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) plugin architecture pattern.

---

## Global Engineering Principles

All AI agents working in this project MUST follow:

### 1. Safety First, Always
- Never run destructive operations without explicit human approval
- All chaos experiments require dryRun: true validation before live execution
- Blast radius must be documented and bounded before any fault injection

### 2. Hypothesis-Driven Everything
- No pipeline stage without a defined success criterion
- No chaos experiment without a formal hypothesis
- No feature flag without a measurable rollout metric

### 3. Security as a Gate (NOT an Afterthought)
- Security scanning (s11) runs on EVERY build — no exceptions
- Zero HIGH/CRITICAL CVEs with fixes available = deployment blocked
- SBOM generated for every artifact, signed, and archived
- SLSA Level 3 provenance for all production artifacts

### 4. Performance Before Chaos
- Load/stress testing (s13) MUST run before chaos (s14)
- Without performance baseline, chaos results are meaningless
- Combined chaos+load tests validate resilience under realistic traffic

### 5. Observability as a Gate
- Every deployment pipeline MUST have a verification step
- Every chaos experiment MUST have monitoring active before fault injection
- If observability is absent, block execution

### 6. Infrastructure as Code
- All Harness resources expressed as YAML
- All chaos experiments expressed as ChaosEngine / ChaosExperiment manifests
- No manual UI-only changes

### 7. Least Privilege
- Harness delegates scoped to minimum required namespaces
- Chaos service accounts scoped to target namespace
- Secrets never printed to logs

### 8. Adversarial Quality Gates
- Every major decision CAN be stress-tested through s35 (Devil's Advocate)
- No design, hypothesis, or release goes unchallenged
- Intensity level defaults: L2 (Critic) for design reviews, L3 (Prosecutor) for security, L4 (Demolisher) for release gates

### 9. Release Governance
- Every production deployment has a Go/No-Go checklist (s28)
- Deployment calendar respected — no Friday deploys, no freeze-period deploys
- Rollback plan tested and documented BEFORE deployment

### 10. Compliance is Continuous (Not Annual)
- Audit trail auto-generated quarterly (s30)
- Control mapping updated with every new skill implementation
- Evidence signed and timestamped (Cosign + Rekor)

### 11. Taste-Aware Execution
- Every agent loads .commandcode/taste/taste.md before acting
- Developer preferences override defaults
- New preferences learned and stored by s02

---

## Skill Execution Protocol

`
Step 1:  IDENTIFY current phase from progress.json (s03)
Step 2:  READ the orchestrator (s00) for context
Step 3:  READ the target skill's SKILL.md completely
Step 4:  VERIFY input contract — all prerequisites satisfied
Step 5:  LOAD taste data from .commandcode/taste/
Step 6:  CHECK AI Agent Integration section in SKILL.md
         - Identify applicable Harness AI agent (if any)
         - Determine current autonomy level
         - Prepare human gates for approval
Step 7:  EXECUTE following the skill's prescribed workflow
         - Call Harness AI agent when available (orchestration layer)
         - Fall back to manual/template execution when unavailable
Step 8:  CAPTURE outputs into workflow context
Step 9:  UPDATE progress.json via s03 / progress-tracker CLI
Step 10: NOTIFY orchestrator of completion
Step 11: DISPATCH to next skill in sequence

Optional: INVOKE s35 (Devil's Advocate) at any quality gate
         - After design decisions, before blast radius approval
         - After hypothesis formation, before acceptance criteria lock
         - Before Go/No-Go decisions (s28)
         - After strategic proposals (s31)
`

---

## Technology Stack Reference

| Tool | Role |
|---|---|
| Harness CI/CD | Pipeline orchestration |
| Harness Feature Flags | Progressive delivery |
| Harness Chaos Engineering | Enterprise chaos orchestration |
| Harness GitOps | ArgoCD-backed GitOps |
| Harness Cloud Cost Management | FinOps |
| Harness Policy Engine | OPA governance |
| LitmusChaos | Fault library |
| Prometheus + Grafana | Observability |
| CloakBrowser + Playwright | E2E testing |
| k6 | Performance/load testing |
| Semgrep | SAST |
| Trivy | Container scanning |
| Snyk / OWASP DC | Dependency scanning |
| Gitleaks | Secret detection |
| Checkov | IaC security |
| Syft | SBOM generation |
| Cosign + Rekor | Artifact signing + transparency |
| Velero | Kubernetes backup |
| Vault / AWS SM / GCP SM | Secrets management |
| Devil's Advocate Agent | Adversarial critique (optional ML-enhanced integration) |

---

## Naming Conventions

`yaml
# Harness Pipeline
<team>-<service>-<env>-pipeline.yaml

# Chaos Experiment
<fault-type>-<target-scope>-<env>-experiment.yaml

# Feature Flag
FF_<TYPE>_<DOMAIN>_<FEATURE>

# Critique Report
.commandcode/artifacts/critique/critique-<subject>-<date>.md

# Artifacts
.commandcode/artifacts/<category>/<type>-<service>.<ext>
`

---

## Environment Tiers

| Tier | Chaos Allowed | Blast Radius | Approval |
|---|---|---|---|
| dev | Yes | Pod-level | None |
| staging | Yes | Service-level | Team lead |
| preprod | Yes, gated | Namespace-level | SRE + PM |
| production | Yes, guard rails | Node-level max | SRE + CTO |

---

## AI Agent Architecture

All 37 skills integrate with **Harness AI's specialized agent ecosystem** and the broader chaos engineering MCP ecosystem. See skills/AI-AGENT-MAPPING.md for the complete mapping.

### SRE Autonomy Levels (Google SRE Framework)

Every skill declares its autonomy level in its SKILL.md:

| Level | Name | Agent Role |
|---|---|---|
| **L0** | Manual | None |
| **L1** | Hypothesis | AI suggests, human decides |
| **L2** | Assisted | AI drafts, human approves |
| **L3** | Delegated | AI executes, human reviews |
| **L4** | Full Autonomy | AI acts independently |

**Current project state**: L1-L2. **Target**: L2-L3. **Safety-critical skills (s16, s29)** remain L1-L2 permanently. **Devil's Advocate (s35)** is adversarial by design — intentionally independent of any Harness AI agent.

### Harness AI Agent Coverage

| Agent | Model | Skills Covered |
|---|---|---|
| DevOps Agent | Claude Opus 4.5 (Vertex AI) | s01, s01-1, s04-s10, s24, s28 |
| Reliability Agent | Harness AI | s14-s20, s26 |
| SRE Agent | Harness AI | s21-s23, s27, s29 |
| Test Agent | Harness AI | s12-s13 |
| FinOps Agent | Harness AI | s25 |
| AppSec/STO Agent | Harness AI | s11, s30 |
| Knowledge Graph | Harness AI | s03 |
| None (adversarial by design) | — | s35 |
| Multi-agent | Harness AI | s33 |

### MCP Integration (Chaos Skills)

| Platform | MCP Server | Integration Skills |
|---|---|---|
| LitmusChaos | litmuschaos-mcp | s14-s20 |
| Gremlin | gremlin-mcp | s14-s17 |
| Steadybit | steadybit-mcp | s14-s20 |
| AWS FIS | aws-fis-bedrock | s18 |
| Harness Chaos | Native AI | s14-s20 |

### Research Backing

Key evidence supporting this architecture (from 34-source deep research, 2026-05-27):
- **ChaosEater (ASE 2025)**: LLM agents automate full chaos lifecycle on Kubernetes
- **AIOpsLab (Microsoft 2024)**: Establish pattern: chaos injection + AI fault localization + resolution
- **Google SRE AI Operator**: L2/L3 autonomous mitigation across thousands of incidents
- **LLM RCA accuracy**: 60-74% few-shot vs 82% human — co-pilot, not autonomous
- **Application-level chaos**: Only 3.0% of real experiments (this project's s19 addresses this gap)
- **No published research** exists on integrated CI/CD + chaos + governance AI workflows

### Data Privacy

| Aspect | Policy |
|---|---|
| Model training | Disabled across all AI integrations |
| Data storage | Not stored or exposed to model providers beyond inference |
| Primary model | Claude Opus 4.5 via Google Vertex AI (0-day retention) |
| Fallback model | OpenAI GPT-4o (30-day retention, training opted out) |
| Data ownership | Customer owns all data |
| Compliance | Built on strongest governance framework |

---

*This CLAUDE.md is the canonical entry point. Always read it first, then consult s00-orchestrator for phase context. For AI agent mapping details, consult skills/AI-AGENT-MAPPING.md. For adversarial critique, invoke s35-devils-advocate.*

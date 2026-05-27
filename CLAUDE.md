# CLAUDE.md — hybrid-harness-chaos-process-prm (Pro Max)

## Project Identity

**Project**: `hybrid-harness-chaos-process-prm`
**Domain**: Platform Engineering — Continuous Delivery + Resilience Engineering + Security + Compliance
**Audience**: Fullstack developers, SREs, Platform Engineers, DevOps practitioners, Security engineers
**AI Compatibility**: Claude Code, Codex, Gemini, GPT-4, and any instruction-following LLM agent

---

## What This Project Does

This repository defines a **33-skill Agile workflow** covering the complete SDLC from ideation to production operations:

| Domain | Purpose |
|---|---|
| **Foundation** | Orchestration, BA analysis, taste memory, progress tracking |
| **CI/CD Engineering** | Pipeline design, service onboarding, delegates, secrets, feature flags, templates, GitOps |
| **Security** | SAST, DAST, container scanning, dependency scanning, SBOM, supply chain security |
| **Testing** | CloakBrowser E2E, performance/load testing, visual regression |
| **Chaos Engineering** | Hypothesis-driven fault injection, blast radius control, steady state, game days |
| **Verification** | Continuous verification, observability, alerting, recommendations |
| **Governance** | OPA policies, cloud cost, release management, disaster recovery |
| **Learning** | Resilience scoring, postmortem RCA, compliance & audit |
| **Research** | Deep multi-source research, evidence synthesis, brainstorming debrief |

---

## Repository Structure

```
hybrid-harness-chaos-process-prm/
├── CLAUDE.md                          ← You are here
├── .commandcode/
│   ├── taste/taste.md                 ← Developer preferences (s02)
│   ├── progress.json                  ← Workflow state (s03)
│   ├── prd.md                         ← Product requirements (s01)
│   ├── adr/                           ← Architecture Decision Records
│   ├── backlog.md                     ← Prioritized backlog
│   └── artifacts/                     ← All outputs produced by skills
│
└── skills/                            ← 33 skills in Agile workflow order

    AI-AGENT-MAPPING.md               ← Harness AI agent mapping + autonomy model

    FOUNDATION (00-03)
    ├── s00-orchestrator/              ← Master workflow coordinator
    ├── s01-ba-requirements/           ← BA analysis + PRD + ADRs + backlog
    ├── s02-taste-memory/              ← Developer preference learning
    └── s03-progress-tracker/          ← Multi-agent progress tracking

    CI/CD SCAFFOLDING (04-10)
    ├── s04-pipeline-design/           ← Harness pipeline YAML
    ├── s05-service-onboarding/        ← Service + env + infra definitions
    ├── s06-delegate-management/       ← Delegate install + config + RBAC
    ├── s07-secrets-management/        ← Vault / AWS SM / GCP SM integration
    ├── s08-feature-flags/             ← FF design + SDK + kill switches
    ├── s09-template-library/          ← Reusable pipeline templates
    └── s10-gitops/                    ← GitOps (ArgoCD-backed)

    SECURITY GATE (11)
    └── s11-security-scanning/         ← SAST + SCA + container + secrets + SBOM + SLSA

    TESTING (12-13)
    ├── s12-cloakbrowser-testing/      ← E2E + a11y + visual regression + baseline
    └── s13-performance-testing/       ← k6 load/stress/soak + capacity planning

    CHAOS DESIGN (14-19)
    ├── s14-experiment-design/         ← ChaosExperiment + ChaosEngine YAML
    ├── s15-hypothesis-validation/     ← Hypothesis writing + validation scripts
    ├── s16-blast-radius-control/      ← Blast radius scoping + abort mechanisms
    ├── s17-steady-state/              ← Baseline metrics + probes
    ├── s18-infrastructure-faults/     ← Node drain, disk fill, cloud faults
    └── s19-application-faults/        ← Pod-delete, container-kill, network, DNS

    GAME DAY (20)
    └── s20-game-day-planning/         ← Orchestrated resilience exercises

    VERIFY & OBSERVE (21-23)
    ├── s21-cv-verification/           ← Continuous verification + SLOs
    ├── s22-observability-integration/ ← Dashboards + chaos metrics + alerts
    └── s23-alerting-recommendations/  ← Alert routing + remediation engine

    GOVERNANCE (24-30)
    ├── s24-policy-governance/         ← OPA policies + compliance gates
    ├── s25-cloud-cost-management/     ← CCM + budgets + AutoStopping
    ├── s26-resilience-scoring/        ← Quantitative resilience analysis
    ├── s27-postmortem-learning/       ← RCA + action items + knowledge base
    ├── s28-release-management/        ← Change mgmt + deployment calendar + notes
    ├── s29-disaster-recovery/         ← RTO/RPO + failover + backup validation
    └── s30-compliance-audit/          ← SOC2/HIPAA/GDPR/PCI evidence + audit trail

    STRATEGIC INNOVATION (31 — callable anytime)
    └── s31-strategic-creator/         ← Brainstorming, proposals, trade-off analysis

    RESEARCH (32 — callable anytime)
    └── s32-deep-research/             ← Multi-source research, evidence synthesis, debrief
```

---

## Complete Agile Workflow Map

```
PHASE 0: FOUNDATION
  s00 → s01 → s02 + s03 (parallel)

PHASE 1: PLANNING & REQUIREMENTS
  s01 (BA deep analysis → PRD + ADRs + backlog)

── s31 (STRATEGIC CREATOR — callable at ANY phase) ──
     ↑↓ can be invoked before, during, or after any phase

── s32 (DEEP RESEARCH — callable at ANY phase) ──
     ↑↓ evidence-grounded research + brainstorming debrief

PHASE 2: CI/CD SCAFFOLDING
  s04 → s05 → s06 → s07 → s08 → s09 → s10

PHASE 3: SECURITY GATE
  s11 (SAST + SCA + container + secrets + IaC + SBOM + SLSA)
  ⚠️ BLOCKS all downstream phases if security gates fail

PHASE 4: TESTING
  s12 → s13 (E2E baseline → performance profiling)
  ⚠️ Performance baseline required before chaos

PHASE 5: CHAOS EXPERIMENT DESIGN
  s14 → s15 → s16 → s17 → s18 → s19

PHASE 6: GAME DAY EXECUTION
  s20 (orchestrated resilience exercise)

PHASE 7: VERIFICATION & OBSERVABILITY
  s21 → s22 → s23

PHASE 8: GOVERNANCE & RELEASE
  s24 → s25 → s26 → s27 → s28

PHASE 9: RESILIENCE & CONTINUITY
  s29 → s30

FEEDBACK LOOP:
  s27 (findings) → s01 (re-analysis) → full cycle
  s30 (compliance gaps) → s01 (PRD update) → remediation cycle
```

---

## Global Engineering Principles

All AI agents working in this project MUST follow:

### 1. Safety First, Always
- Never run destructive operations without explicit human approval
- All chaos experiments require `dryRun: true` validation before live execution
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

### 8. Release Governance
- Every production deployment has a Go/No-Go checklist (s28)
- Deployment calendar respected — no Friday deploys, no freeze-period deploys
- Rollback plan tested and documented BEFORE deployment

### 9. Compliance is Continuous (Not Annual)
- Audit trail auto-generated quarterly (s30)
- Control mapping updated with every new skill implementation
- Evidence signed and timestamped (Cosign + Rekor)

### 10. Taste-Aware Execution
- Every agent loads `.commandcode/taste/taste.md` before acting
- Developer preferences override defaults
- New preferences learned and stored by s02

---

## Skill Execution Protocol

```
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
Step 9:  UPDATE progress.json via s03
Step 10: NOTIFY orchestrator of completion
Step 11: DISPATCH to next skill in sequence
```

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

---

## Naming Conventions

```yaml
# Harness Pipeline
<team>-<service>-<env>-pipeline.yaml

# Chaos Experiment
<fault-type>-<target-scope>-<env>-experiment.yaml

# Feature Flag
FF_<TYPE>_<DOMAIN>_<FEATURE>

# Artifacts
.commandcode/artifacts/<category>/<type>-<service>.<ext>
```

---

## Environment Tiers

| Tier | Chaos Allowed | Blast Radius | Approval |
|---|---|---|---|
| `dev` | Yes | Pod-level | None |
| `staging` | Yes | Service-level | Team lead |
| `preprod` | Yes, gated | Namespace-level | SRE + PM |
| `production` | Yes, guard rails | Node-level max | SRE + CTO |

---

## Quick Reference: Skill Index

| # | Skill | Phase | Triggers |
|---|---|---|---|
| 00 | Orchestrator | Foundation | workflow, start, orchestrate |
| 01 | BA Requirements | Foundation | analyze, PRD, requirements, spec |
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

---

## AI Agent Architecture

This project integrates with **Harness AI's specialized agent ecosystem** and the broader chaos engineering MCP ecosystem. See `skills/AI-AGENT-MAPPING.md` for the complete mapping.

### SRE Autonomy Levels (Google SRE Framework)

Every skill declares its autonomy level in its SKILL.md:

| Level | Name | Agent Role |
|---|---|---|
| **L0** | Manual | None |
| **L1** | Hypothesis | AI suggests, human decides |
| **L2** | Assisted | AI drafts, human approves |
| **L3** | Delegated | AI executes, human reviews |
| **L4** | Full Autonomy | AI acts independently |

**Current project state**: L1-L2. **Target**: L2-L3. **Safety-critical skills (s16, s29)** remain L1-L2 permanently.

### Harness AI Agent Coverage

| Agent | Model | Skills Covered |
|---|---|---|
| DevOps Agent | Claude Opus 4.5 (Vertex AI) | s01, s04-s10, s24, s28 |
| Reliability Agent | Harness AI | s14-s20, s26 |
| SRE Agent | Harness AI | s21-s23, s27, s29 |
| Test Agent | Harness AI | s12-s13 |
| FinOps Agent | Harness AI | s25 |
| AppSec/STO Agent | Harness AI | s11, s30 |
| Knowledge Graph | Harness AI | s03 |

### MCP Integration (Chaos Skills)

Chaos engineering skills (s14-s20) can interact with chaos platforms through MCP servers:

| Platform | MCP Server | Integration Skills |
|---|---|---|
| LitmusChaos | litmuschaos-mcp | s14-s20 |
| Gremlin | gremlin-mcp | s14-s17 |
| Steadybit | steadybit-mcp | s14-s20 |
| AWS FIS | aws-fis-bedrock | s18 |
| Harness Chaos | Native AI | s14-s20 |

### Orchestration Pattern

Each skill follows: **Load Context -> AI Agent Call -> Validate -> Human Gate -> Execute -> Update Progress**. When Harness AI is unavailable, skills fall back to static templates and manual execution.

### Research Backing

Key evidence supporting this architecture (from 34-source deep research, 2026-05-27):
- **ChaosEater (ASE 2025)**: LLM agents automate full chaos lifecycle on Kubernetes
- **AIOpsLab (Microsoft 2024)**: Establish pattern: chaos injection + AI fault localization + resolution
- **Google SRE AI Operator**: L2/L3 autonomous mitigation across thousands of incidents
- **LLM RCA accuracy**: 60-74% few-shot vs 82% human -- co-pilot, not autonomous
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

*This CLAUDE.md is the canonical entry point. Always read it first, then consult s00-orchestrator for phase context. For AI agent mapping details, consult `skills/AI-AGENT-MAPPING.md`.*

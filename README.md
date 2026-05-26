# hybrid-harness-chaos-process-prm (v.0.1)

**A 32-skill agentic workflow for platform engineering — spanning CI/CD, security, chaos engineering, observability, governance, and compliance, purpose-built for the era of AI-assisted development.**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-32-00b894.svg)](skills/)
[![AI Compatible](https://img.shields.io/badge/AI-Claude%20Code%20%7C%20Codex%20%7C%20Gemini%20%7C%20GPT--4-8A2BE2.svg)]()

---

## What Is This?

This repository is a **complete, production-grade skill library** designed to be consumed by AI coding agents (Claude Code, Codex, Gemini, GPT-4). It provides a standardized, 32-step Agile workflow that guides developers from project ideation through requirements gathering, CI/CD scaffolding, security scanning, chaos experimentation, observability integration, release governance, disaster recovery, and compliance auditing.

**It's not a framework you install. It's a workflow you clone and point your AI agent at.**

```text
Ideation → BA Analysis → CI/CD → Security Gate → Testing → Chaos → Game Day
→ Verification → Alerting → Governance → Release → DR → Compliance → Strategic Review
```

---

## Why This Exists

Modern development is increasingly agentic — AI agents write code, design pipelines, and execute operations. But agents are only as good as their instructions. Without structured, expert-level guidance, agents produce inconsistent, incomplete, or unsafe output.

**This project solves that by providing:**

- **Standardized workflows** — Every agent follows the same battle-tested process, regardless of which LLM powers it
- **Input/output contracts** — Skills declare what they consume and produce, preventing context loss between handoffs
- **Safety gates** — Security scanning blocks deployment, blast radius control prevents production chaos, release management prevents Friday night deploys
- **Taste memory** — Developer preferences are learned, persisted, and injected into every agent session
- **Progress tracking** — Multi-agent sessions maintain state across interruptions; no duplicated or missed work

---

## Skill Architecture

Every skill follows the same structure:

```
skills/sNN-<name>/
└── SKILL.md              # Primary instruction file (YAML frontmatter + Markdown body)
    ├── Input Contract     # What this skill needs before it can run
    ├── Output Contract    # What this skill produces for downstream skills
    ├── Prerequisites      # External dependencies (tools, accounts, access)
    ├── Workflow           # Step-by-step execution instructions
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
| 02 | Taste Memory | Developer preference learning — persists tastes across sessions and agents |
| 03 | Progress Tracker | Multi-agent progress state machine — prevents duplicated and missed work |

### Phase 1: Planning & Requirements
| # | Skill | Purpose |
|---|-------|---------|
| 01 | BA Requirements | Deep project analysis with structured interview framework, gap detection |

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

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/dungnotnull/hybrid-harness-chaos-process-prm.git
cd hybrid-harness-chaos-process-prm
```

### 2. Point your AI agent at it

For **Claude Code** (Anthropic):
```bash
claude --project hybrid-harness-chaos-process-prm
```
Claude Code automatically reads `CLAUDE.md` and discovers the skill library.

For **other agents** (Codex, Gemini, GPT-4 via API):
Include the repository as context. Start with `CLAUDE.md` as the system prompt, then reference specific skills as needed:

```python
# Example: Loading the project into a custom agent
with open("CLAUDE.md") as f:
    system_prompt = f.read()

with open("skills/s00-orchestrator/SKILL.md") as f:
    orchestrator = f.read()

# Agent now understands the full workflow
response = agent.run(system_prompt + orchestrator, user_request)
```

### 3. Start your workflow

```
You: "I'm building a payment processing microservice on Kubernetes. Start the full workflow."
```

The orchestrator (s00) will:
1. Load project context and taste preferences
2. Initialize progress tracking
3. Dispatch to s01 (BA Requirements) for deep project analysis
4. Ask probing questions about your stack, SLAs, constraints, and risk tolerance
5. Produce a complete PRD and dispatch to Phase 2

---

## One-Click Install Script

For users who want to quickly set up the skill library in their project:

```bash
#!/bin/bash
# install-skills.sh — Clone and initialize the hybrid-harness-chaos skill library

set -euo pipefail

REPO_URL="https://github.com/dungnotnull/hybrid-harness-chaos-process-prm.git"
TARGET_DIR="${1:-.commandcode/skills}"

echo "============================================"
echo " Hybrid Harness + Chaos Skill Library Setup"
echo "============================================"
echo ""

# Clone or update
if [ -d "$TARGET_DIR/.git" ]; then
    echo "📦 Updating existing skill library..."
    git -C "$TARGET_DIR" pull --ff-only
else
    echo "📥 Cloning skill library into $TARGET_DIR..."
    git clone --depth 1 "$REPO_URL" "$TARGET_DIR"
fi

# Copy CLAUDE.md to project root
if [ -f "$TARGET_DIR/CLAUDE.md" ]; then
    cp "$TARGET_DIR/CLAUDE.md" ./CLAUDE.md
    echo "✅ CLAUDE.md copied to project root"
fi

# Create taste directory if missing
mkdir -p .commandcode/taste
if [ ! -f .commandcode/taste/taste.md ]; then
    cat > .commandcode/taste/taste.md << 'TASTE_EOF'
# Taste — Project Preferences
> Auto-generated developer preference model. Managed by s02-taste-memory.
> Last updated: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Technology
- No preferences learned yet. They will be captured as you work.

## Code Style
- No preferences learned yet.

## Workflow
- No preferences learned yet.

## Risk Tolerance
- No preferences learned yet.

## Communication
- No preferences learned yet.

## Testing
- No preferences learned yet.

## Deployment
- No preferences learned yet.

## Observability
- No preferences learned yet.
TASTE_EOF
    echo "✅ Taste file created at .commandcode/taste/taste.md"
fi

# Create artifacts directory
mkdir -p .commandcode/artifacts

echo ""
echo "============================================"
echo " ✅ Skill library installed successfully!"
echo "============================================"
echo ""
echo "   Skills: $TARGET_DIR/skills/ (32 skills)"
echo "   Taste:  .commandcode/taste/taste.md"
echo "   Config: CLAUDE.md"
echo ""
echo "To start: point your AI agent at this project directory."
echo "Example: claude --project $(pwd)"
echo "============================================"
```

### Windows (PowerShell) install script

```powershell
# install-skills.ps1
param(
    [string]$TargetDir = ".commandcode\skills"
)

$RepoUrl = "https://github.com/dungnotnull/hybrid-harness-chaos-process-prm.git"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Hybrid Harness + Chaos Skill Library Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if (Test-Path "$TargetDir\.git") {
    Write-Host "`n📦 Updating existing skill library..." -ForegroundColor Yellow
    git -C $TargetDir pull --ff-only
} else {
    Write-Host "`n📥 Cloning skill library into $TargetDir..." -ForegroundColor Yellow
    git clone --depth 1 $RepoUrl $TargetDir
}

if (Test-Path "$TargetDir\CLAUDE.md") {
    Copy-Item "$TargetDir\CLAUDE.md" ".\CLAUDE.md" -Force
    Write-Host "✅ CLAUDE.md copied to project root" -ForegroundColor Green
}

if (-not (Test-Path ".commandcode\taste")) {
    New-Item -ItemType Directory -Path ".commandcode\taste" -Force | Out-Null
}
if (-not (Test-Path ".commandcode\taste\taste.md")) {
    $date = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    @"
# Taste — Project Preferences
> Auto-generated developer preference model. Managed by s02-taste-memory.
> Last updated: $date

## Technology
- No preferences learned yet. They will be captured as you work.

## Code Style
- No preferences learned yet.

## Workflow
- No preferences learned yet.

## Risk Tolerance
- No preferences learned yet.

## Communication
- No preferences learned yet.

## Testing
- No preferences learned yet.

## Deployment
- No preferences learned yet.

## Observability
- No preferences learned yet.
"@ | Out-File -FilePath ".commandcode\taste\taste.md" -Encoding utf8
    Write-Host "✅ Taste file created at .commandcode\taste\taste.md" -ForegroundColor Green
}

if (-not (Test-Path ".commandcode\artifacts")) {
    New-Item -ItemType Directory -Path ".commandcode\artifacts" -Force | Out-Null
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " ✅ Skill library installed successfully!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Skills: $TargetDir\skills\ (32 skills)" -ForegroundColor White
Write-Host "   Taste:  .commandcode\taste\taste.md" -ForegroundColor White
Write-Host "   Config: CLAUDE.md" -ForegroundColor White
Write-Host ""
```

---

## Supported AI Agents

| Agent | Integration Method | Notes |
|---|---|---|
| **Claude Code** | Native — reads `CLAUDE.md` automatically | Best experience; built-in project context loading |
| **Codex (OpenAI)** | Include `CLAUDE.md` in system prompt + reference individual skills | Structured prompts recommended |
| **Gemini** | Upload repository, reference `CLAUDE.md` | Works best with filesystem access |
| **GPT-4 (Custom Agents)** | Include `CLAUDE.md` + `s00-orchestrator/SKILL.md` as context | Template system prompts provided below |
| **Any instruction-following LLM** | Structured context injection | See custom integration guide below |

### Custom Agent Integration

```python
# agent_setup.py — Minimal integration for any LLM-powered agent
from pathlib import Path

class SkillAgent:
    def __init__(self, skills_path: str = "skills"):
        self.skills_path = Path(skills_path)
        self.context = self._load_project_context()

    def _load_project_context(self) -> dict:
        """Load CLAUDE.md and initialize context."""
        with open("CLAUDE.md") as f:
            claude_md = f.read()

        # Load taste if available
        taste_path = Path(".commandcode/taste/taste.md")
        taste = taste_path.read_text() if taste_path.exists() else ""

        return {
            "claude_md": claude_md,
            "taste": taste,
            "phase": "00-orchestrator",
            "artifacts": {},
        }

    def load_skill(self, skill_id: str) -> str:
        """Load a specific skill's instructions."""
        skill_dir = next(self.skills_path.glob(f"{skill_id}-*"), None)
        if not skill_dir:
            raise FileNotFoundError(f"Skill {skill_id} not found")
        return (skill_dir / "SKILL.md").read_text()

    def run_phase(self, user_request: str) -> str:
        """Orchestrator-style dispatch."""
        orchestrator = self.load_skill("s00")
        # Append to system prompt, execute, capture outputs
        return self._execute(user_request, system_prompt=orchestrator)

agent = SkillAgent()
response = agent.run_phase("Set up a CI/CD pipeline for my payment service")
```

---

## System Prompt Template (for custom agents)

Use this as the base system prompt when integrating with any LLM agent:

```text
You are a platform engineering agent working on the hybrid-harness-chaos-process-prm project.

<project_context>
{CLAUDE.md content}
</project_context>

<developer_preferences>
{taste file content}
</developer_preferences>

<workflow_progress>
Current phase: s00-orchestrator
Next: User will specify their request. Dispatch to the appropriate skill.
</workflow_progress>

Your job:
1. Read CLAUDE.md to understand the project and workflow.
2. Load the orchestrator (skills/s00-orchestrator/SKILL.md) for phase dispatch logic.
3. Determine the correct starting phase based on the user's request.
4. Load the target skill's SKILL.md completely before acting.
5. Verify the skill's Input Contract is satisfied.
6. Execute following the skill's prescribed workflow.
7. Capture outputs and update progress.

Principles: Safety first. Hypothesis-driven. Security as a gate. Infrastructure as code. Always verify inputs before acting.
```

---

## Project Principles

All 32 skills are designed around these core principles:

| Principle | Description |
|---|---|
| **Safety First** | Never run destructive operations without explicit human approval. All chaos experiments require dry-run validation. |
| **Hypothesis-Driven** | No pipeline stage without a success criterion. No chaos experiment without a formal hypothesis. No feature flag without a measurable rollout metric. |
| **Security as a Gate** | Security scanning runs on every build — no exceptions. Zero HIGH/CRITICAL CVEs = deployment blocked. SBOM generated and signed for every artifact. |
| **Performance Before Chaos** | Load testing must establish baselines before any fault injection. Chaos results are meaningless without a performance baseline. |
| **Observability as a Gate** | Every deployment has a verification step. Every chaos experiment has monitoring active. No observability = execution blocked. |
| **Infrastructure as Code** | All resources expressed as YAML. No manual UI-only changes. Everything reproducible from version control. |
| **Least Privilege** | Delegates scoped to namespaces. Chaos accounts scoped to targets. Secrets never in logs. |
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

---

## Directory Layout

```
hybrid-harness-chaos-process-prm/
├── README.md                    ← You are here
├── LICENSE                      ← MIT
├── CLAUDE.md                    ← Canonical entry point for all AI agents
│
├── .commandcode/
│   ├── taste/taste.md           ← Developer preferences (auto-managed by s02)
│   ├── progress.json            ← Workflow state (auto-managed by s03)
│   ├── prd.md                   ← Product Requirements Document (produced by s01)
│   ├── adr/                     ← Architecture Decision Records (produced by s01)
│   ├── backlog.md               ← Prioritized backlog (produced by s01)
│   └── artifacts/               ← All YAML, scripts, reports produced by skills
│       ├── pipeline-*.yaml
│       ├── security/*.sarif
│       ├── perf/*.json
│       ├── experiment-*.yaml
│       ├── resilience-*.json
│       ├── dr/
│       ├── compliance/
│       └── releases/
│
└── skills/                      ← 32 skills in Agile workflow order
    ├── s00-orchestrator/SKILL.md
    ├── s01-ba-requirements/SKILL.md
    ├── s02-taste-memory/SKILL.md
    ├── s03-progress-tracker/SKILL.md
    ├── s04-pipeline-design/SKILL.md
    ├── s05-service-onboarding/SKILL.md
    ├── s06-delegate-management/SKILL.md
    ├── s07-secrets-management/SKILL.md
    ├── s08-feature-flags/SKILL.md
    ├── s09-template-library/SKILL.md
    ├── s10-gitops/SKILL.md
    ├── s11-security-scanning/SKILL.md
    ├── s12-cloakbrowser-testing/SKILL.md
    ├── s13-performance-testing/SKILL.md
    ├── s14-experiment-design/SKILL.md
    ├── s15-hypothesis-validation/SKILL.md
    ├── s16-blast-radius-control/SKILL.md
    ├── s17-steady-state/SKILL.md
    ├── s18-infrastructure-faults/SKILL.md
    ├── s19-application-faults/SKILL.md
    ├── s20-game-day-planning/SKILL.md
    ├── s21-cv-verification/SKILL.md
    ├── s22-observability-integration/SKILL.md
    ├── s23-alerting-recommendations/SKILL.md
    ├── s24-policy-governance/SKILL.md
    ├── s25-cloud-cost-management/SKILL.md
    ├── s26-resilience-scoring/SKILL.md
    ├── s27-postmortem-learning/SKILL.md
    ├── s28-release-management/SKILL.md
    ├── s29-disaster-recovery/SKILL.md
    ├── s30-compliance-audit/SKILL.md
    └── s31-strategic-creator/SKILL.md
```

---

## Environment Tiers

All skills respect these environment boundaries:

| Tier | Chaos Allowed | Blast Radius | Approval Required |
|---|---|---|---|
| `dev` | Yes | Pod-level only | None |
| `staging` | Yes | Service-level | Team lead |
| `preprod` | Yes, gated | Namespace-level | SRE + PM |
| `production` | Yes, with guard rails | Node-level max | SRE + CTO |

---

## Contributing

Contributions that extend, refine, or improve the skill library are welcome.

### What makes a good contribution
- New skills that fill gaps in the workflow
- Enhanced templates, scripts, or examples within existing skills
- Corrections to incorrect or outdated guidance
- Additional compliance framework mappings (s30)
- New innovation patterns for the strategic creator (s31)

### Skill quality standards
Every SKILL.md must include:
- YAML frontmatter with `name` and `description`
- Input Contract table
- Output Contract table
- Prerequisites checklist
- Step-by-step workflow
- Runnable examples (YAML, scripts, configs)
- Success Criteria checklist

### Pull request process
1. Fork the repository
2. Create a branch: `git checkout -b feature/skill-description`
3. Write or modify skills following the quality standards
4. Commit with descriptive messages
5. Open a pull request against `main`

---

## FAQ

**Q: Do I need Harness to use this?**
A: The CI/CD skills (s04-s10) are Harness-specific, but the workflow structure, chaos engineering (s14-s20), observability (s21-s23), governance (s24-s28), and compliance (s30) skills are platform-agnostic and work with any stack.

**Q: Can I skip phases?**
A: The orchestrator (s00) enforces phase ordering but allows skipping with explicit user confirmation. Security (s11) and testing (s12-s13) gates are hard blocks — they cannot be skipped for production-bound artifacts.

**Q: What happens if I switch between Claude Code, Codex, and GPT-4?**
A: Progress is stored in `.commandcode/progress.json`. Taste is stored in `.commandcode/taste/taste.md`. Any agent that loads the CLAUDE.md context will pick up exactly where the previous agent left off.

**Q: Is the strategic creator (s31) mandatory?**
A: No. s31 is entirely optional and advisory. It never implements anything — it only proposes. The user always makes the final call on whether to accept, defer, or decline proposals.

**Q: How do I add a new compliance framework?**
A: Edit s30-compliance-audit/SKILL.md. Add your framework to the `supported_frameworks` YAML block, map your controls in `control_mapping`, and the auto-generated audit trail will include your framework's evidence.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built on years of platform engineering and chaos engineering practice. Inspired by:
- The [Harness](https://harness.io) platform's CI/CD, FF, GitOps, CCM, and Chaos modules
- [LitmusChaos](https://litmuschaos.io) for the chaos experiment DSL
- [CloakBrowser](https://github.com/CloakHQ/CloakBrowser) for advanced browser automation
- Netflix's Chaos Engineering philosophy
- Google's SRE workbook
- The Open Policy Agent community

---

*For AI agents: Read CLAUDE.md first, then s00-orchestrator/SKILL.md. All other skills are dispatched from there.*

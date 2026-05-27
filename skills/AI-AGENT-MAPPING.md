# AI Agent Mapping -- Harness Engineering + Chaos Engineering

**Last Updated**: 2026-05-27
**Based On**: Deep Research Report (34 sources, comprehensive mode)

---

## SRE Autonomy Maturity Model (Google SRE Framework)

All skills in this project are classified against Google's 5-level SRE Autonomy framework:

| Level | Name | Agent Role | Human Role |
|---|---|---|---|
| **L0** | Manual | None | Does everything |
| **L1** | Hypothesis | Suggests, recommends | Decides and acts |
| **L2** | Assisted | Drafts and proposes | Reviews and approves |
| **L3** | Delegated | Executes within bounds | Reviews results |
| **L4** | Full Autonomy | Acts independently | Sets policy |

**Current industry state**: L2-L3 for most mature organizations (Google, Uber, Harness). No documented L4 deployments for production reliability.

---

## Harness AI Agent Ecosystem

Harness AI operates as a network of 6 specialized agents backed by a Software Delivery Knowledge Graph:

```
                    +-------------------------------+
                    |   Software Delivery           |
                    |   Knowledge Graph + RAG        |
                    +-------------------------------+
                               |
                    +-------------------------------+
                    |   Intelligent Workflow         |
                    |   Orchestration Layer          |
                    +-------------------------------+
                               |
        +----------+----------+----------+----------+----------+
        |          |          |          |          |          |
   DevOps      Reliability    SRE       Test     FinOps     AppSec
   Agent       Agent        Agent     Agent     Agent      Agent
   (Claude     (Chaos       (Incident (Test     (Cost      (STO
   Opus 4.5)   Recs)        Triage)   Creation) Optimize)  Remediate)
```

### Agent Capabilities Reference

| Agent | Primary Capabilities | Model | Key Features |
|---|---|---|---|
| **DevOps Agent** | Pipeline creation, error analysis, policy generation, GitOps, service/connector creation | Claude Opus 4.5 (via Vertex AI) | Natural language pipeline gen, Error Analyzer (change impact + RCA), OPA Rego policy gen, 50-stage pipeline validated |
| **Reliability Agent** | Chaos experiment recommendations, auto-remediation guidance, resilience analysis | Harness AI | Scans app events + infra changes + test results, recommends experiments, suggests mitigations |
| **SRE Agent** | Incident triage, proactive incident response, auto-postmortem generation | Harness AI | Auto-triage, postmortem reports, incident timeline analysis |
| **Test Agent** | AI test creation (10x faster), self-healing tests, intent-based testing | Harness AI | Natural language test creation, 70% test maintenance reduction, UI-change resilience |
| **FinOps Agent** | Cloud cost recommendations, dashboard creation, cost summaries, policy generation | Harness AI | Natural language cost queries, commitment analysis, K8s spend optimization |
| **AppSec/STO Agent** | Security test generation, vulnerability detection, auto-remediation (50-75% fix time reduction) | Harness AI | CVE/CWE explanation, remediation steps, PR-based fixes |

---

## Skill-to-Agent Mapping

### Foundation (s00-s03)

| Skill | Harness AI Agent | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|
| s00 Orchestrator | Workflow Orchestration | L1 | L3 | Phase detection, skill dispatch, context handoff | Phase transitions, skip approvals |
| s01 BA Requirements | DevOps Agent | L1 | L2 | PRD analysis, requirement extraction, spec generation | PRD approval, ADR decisions |
| s02 Taste Memory | None (internal) | L2 | L2 | Preference learning, pattern recognition | Preference confirmation |
| s03 Progress Tracker | Knowledge Graph | L2 | L3 | Auto-state updates, artifact linking, blocker detection | Progress overrides |

### CI/CD Scaffolding (s04-s10)

| Skill | Harness AI Agent | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|
| s04 Pipeline Design | DevOps Agent | L2 | L3 | Natural language pipeline YAML generation, error analysis, pipeline summarization | Pipeline approval, security-sensitive stages |
| s05 Service Onboarding | DevOps Agent | L2 | L3 | Service/env/connector creation via conversational prompts | Service definition approval |
| s06 Delegate Management | DevOps Agent | L1 | L2 | Delegate install guidance, RBAC template generation | Delegate installation, RBAC changes |
| s07 Secrets Management | DevOps Agent | L1 | L2 | Secret reference creation, vault integration templates | Secret creation, access grants |
| s08 Feature Flags | DevOps Agent | L2 | L3 | FF config generation, SDK code generation, kill switch setup | FF toggle in production, kill switch activation |
| s09 Template Library | DevOps Agent | L1 | L2 | Template pattern recognition, reusability analysis | Template publication |
| s10 GitOps | DevOps Agent | L2 | L3 | GitOps operations for 13 resource types, ArgoCD Application YAML | Sync policies, production drift resolution |

### Security Gate (s11)

| Skill | Harness AI Agent | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|
| s11 Security Scanning | AppSec/STO Agent | L2 | L3 | CVE detection, auto-remediation, SBOM generation, PR-based fixes | Security gate override, HIGH/CRITICAL exception approval |

### Testing (s12-s13)

| Skill | Harness AI Agent | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|
| s12 CloakBrowser Testing | Test Agent | L2 | L3 | AI test creation (10x faster), self-healing tests, intent-based testing | Test approval, baseline updates |
| s13 Performance Testing | Test Agent | L1 | L2 | Test selection optimization, baseline comparison, anomaly detection | Performance threshold approval, capacity decisions |

### Chaos Design (s14-s19)

| Skill | Harness AI Agent | MCP Integration | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|---|
| s14 Experiment Design | Reliability Agent | LitmusChaos MCP, Gremlin MCP | L1 | L2 | AI chaos recommendations, natural language experiment generation, service discovery | Hypothesis approval, experiment activation |
| s15 Hypothesis Validation | Reliability Agent | LitmusChaos MCP | L1 | L2 | Steady-state validation scripts, probe configuration | Hypothesis acceptance/rejection |
| s16 Blast Radius Control | Reliability Agent | Harness ChaosGuard | L1 | L2 | Blast radius scoping, abort mechanism design, ChaosGuard policies | Blast radius approval, abort threshold review |
| s17 Steady State | Reliability Agent | LitmusChaos MCP, Prometheus | L1 | L2 | Baseline metric identification, probe creation, anomaly detection | Steady-state definition approval |
| s18 Infrastructure Faults | Reliability Agent | LitmusChaos MCP, AWS FIS | L1 | L2 | Fault manifest generation, infrastructure targeting | Production fault approval |
| s19 Application Faults | Reliability Agent | LitmusChaos MCP, Harness Chaos | L1 | L2 | Application fault manifest generation, pod/container targeting | Production fault approval |

### Game Day (s20)

| Skill | Harness AI Agent | MCP Integration | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|---|
| s20 Game Day Planning | Reliability Agent | LitmusChaos MCP, Gremlin MCP | L1 | L2 | Game day scenario orchestration, timeline generation, team coordination | Game day approval, production go/no-go |

### Verify & Observe (s21-s23)

| Skill | Harness AI Agent | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|
| s21 CV Verification | SRE Agent | L1 | L2 | CV config generation, SLO validation, monitored service setup | Verification threshold approval |
| s22 Observability Integration | SRE Agent | L1 | L2 | Dashboard generation, chaos metric correlation, alert rule creation | Dashboard publication, metric baseline |
| s23 Alerting Recommendations | SRE Agent | L2 | L3 | Alert routing, remediation engine, recommendation generation | Alert rule activation, remediation approval |

### Governance (s24-s30)

| Skill | Harness AI Agent | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|
| s24 Policy Governance | DevOps Agent | L2 | L3 | OPA Rego policy generation, compliance gate design | Policy activation, compliance exception |
| s25 Cloud Cost | FinOps Agent | L2 | L3 | Cost recommendations, dashboard creation, commitment analysis, K8s spend optimization | Budget approval, cost anomaly investigation |
| s26 Resilience Scoring | Reliability Agent | L2 | L3 | Quantitative resilience analysis, scoring calculation, trend analysis | Score methodology approval |
| s27 Postmortem Learning | SRE Agent | L2 | L3 | Auto-postmortem generation, RCA analysis, action item extraction | Postmortem approval, action item assignment |
| s28 Release Management | DevOps Agent | L1 | L2 | Release notes generation, deployment calendar, go/no-go checklist | Production go/no-go, release approval |
| s29 Disaster Recovery | SRE Agent | L1 | L2 | DR plan generation, failover runbook creation, RTO/RPO validation | Failover execution, backup restoration |
| s30 Compliance Audit | AppSec/STO Agent | L1 | L2 | Evidence collection, control mapping, audit trail generation | Audit sign-off, exception approval |

### Strategic Innovation (s31-s32)

| Skill | Harness AI Agent | Current Level | Target Level | AI Capabilities | Human Gates |
|---|---|---|---|---|---|
| s31 Strategic Creator | None (advisory by design) | L1 | L1 | Innovation dimensions, proposal generation, trade-off analysis | All proposals (advisory only) |
| s32 Deep Research | None (research by design) | L1 | L1 | Multi-source research, evidence synthesis, debrief facilitation | All recommendations (advisory only) |

---

## Orchestration Layer Pattern

Each skill follows a standard pattern when integrating with Harness AI agents:

```
SKILL EXECUTION FLOW
    |
    v
[1. LOAD CONTEXT] -- Read s00 context, s02 taste, skill prerequisites
    |
    v
[2. AI AGENT CALL] -- If Harness AI agent available:
    |                  a. Construct prompt from skill inputs
    |                  b. Call Harness AI agent (DevOps/Reliability/SRE/Test/FinOps/STO)
    |                  c. Receive AI-generated draft
    |
    v
[3. VALIDATE] -- Check AI output against:
    |              a. Skill output contract
    |              b. Security/compliance policies
    |              c. Blast radius / safety bounds
    |              d. Taste preferences
    |
    v
[4. HUMAN GATE] -- If autonomy_level < L3:
    |                 Present to human for approval
    |                 Human can: approve / modify / reject
    |
    v
[5. EXECUTE] -- Apply approved output
    |
    v
[6. UPDATE PROGRESS] -- s03 progress tracker + knowledge graph update
    |
    v
[7. DISPATCH NEXT] -- Hand off to next skill in sequence
```

### Fallback Behavior

When Harness AI agent is NOT available (offline, unsupported module, API error):

```
FALLBACK FLOW
    |
    v
[1. DETECT] -- Harness AI agent unavailable or returned error
    |
    v
[2. DEGRADE] -- Fall back to manual/template-based execution:
    |              a. Use static templates from s09 Template Library
    |              b. Use pattern matching from skill definition
    |              c. Prompt user for manual input where needed
    |
    v
[3. LOG] -- Record fallback event in progress tracker
    |
    v
[4. CONTINUE] -- Proceed with manual output (no AI assistance)
```

---

## MCP Integration Matrix

Chaos engineering skills (s14-s20) can interact with chaos platforms through MCP servers:

| Platform | MCP Server | Capabilities | Skills |
|---|---|---|---|
| LitmusChaos | litmuschaos-mcp (Go) | Experiment CRUD, infra ops, environment mgmt, resilience probes, analytics, resiliency scores | s14-s20 |
| Gremlin | gremlin-mcp | Experiment analysis, recommended remediation, intelligent health checks, dependency discovery | s14-s17 |
| Steadybit | steadybit-mcp | Experiment insights, result analysis, target discovery | s14-s20 |
| Harness Chaos | Harness AI Reliability Agent | Native integration, experiment recommendations, ChaosGuard, Fault Flags | s14-s20 |
| AWS FIS | aws-fis-bedrock | Natural language experiment generation for AWS infrastructure | s18 |

### MCP Integration Pattern for Chaos Skills

```yaml
chaos_skill_execution:
  step_1: identify_target_platform  # LitmusChaos, Gremlin, Harness Chaos, AWS FIS
  step_2: construct_mcp_prompt      # Natural language experiment description
  step_3: call_mcp_server           # Platform-specific MCP server
  step_4: validate_manifest         # Schema validation, blast radius check
  step_5: human_gate                # Autonomy-level-dependent approval
  step_6: execute_or_save           # Run experiment or save to pipeline
```

---

## Data Privacy (from Harness AI Documentation)

| Aspect | Policy |
|---|---|
| Model training | Disabled across all AI integrations |
| Data storage | Not stored or exposed to model providers beyond inference |
| Primary model | Claude Opus 4.5 via Google Vertex AI (0-day retention) |
| Fallback model | OpenAI GPT-4o (30-day retention, training opted out) |
| Data ownership | Customer owns all data |
| Compliance | Built on strongest governance framework |

---

## Key Research Findings Informing This Architecture

1. **ChaosEater (ASE 2025)** validates LLM-driven full chaos lifecycle automation on Kubernetes
2. **AIOpsLab (Microsoft 2024)** establishes pattern: chaos injection + AI fault localization + resolution
3. **Google SRE AI Operator** demonstrates L2/L3 autonomous mitigation across thousands of incidents
4. **LLM RCA accuracy is 60-74% (few-shot)** vs 82% for human SREs (Szandala, ICCS 2025) -- co-pilot, not autonomous
5. **Application-level chaos faults represent only 3.0%** of real-world experiments (Owotogbe, 971 repos) -- this project's s19 addresses this gap
6. **No published research** exists on integrated CI/CD + chaos + governance AI workflows -- this project is novel

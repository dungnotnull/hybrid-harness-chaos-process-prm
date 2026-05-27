# Deep Research Report: AI Agents for Harness Engineering and Chaos Engineering

**Date**: 2026-05-27
**Researcher**: s32-deep-research
**Depth**: comprehensive
**Trigger**: User request for independent research on AI agents in Harness/Chaos Engineering

---

## Executive Summary

Research across 34 sources (12 academic papers, 20 documentation/industry sources) reveals a rapidly converging landscape where AI agents are transforming both CI/CD automation (Harness Engineering) and chaos engineering. The most significant finding is ChaosEater (ASE 2025), which demonstrates full automation of the chaos engineering lifecycle using LLM agents on Kubernetes -- directly validating this project's agentic architecture. Harness AI has evolved into a multi-agent platform with 6 specialized agents (DevOps, SRE, Test, Reliability, FinOps, AppSec) backed by a Software Delivery Knowledge Graph. The industry is converging on MCP (Model Context Protocol) as the integration standard, with LitmusChaos, Gremlin, and Steadybit all launching MCP servers in 2025. Google's SRE team provides the most authoritative autonomy framework (5 levels, L0-L4), demonstrating L2/L3 autonomous mitigation across thousands of production incidents. The critical insight: LLMs achieve 60-74% accuracy in chaos engineering RCA (vs 82% for human SREs), making them effective co-pilots but not yet autonomous operators -- validating this project's "safety first, human-in-the-loop" design.

---

## Key Findings

### Consensus (Strong Evidence)

| # | Finding | Sources | Confidence |
|---|---|---|---|
| 1 | LLM agents can automate the full chaos engineering lifecycle (design, execute, analyze, remediate) on Kubernetes systems | ChaosEater (ASE 2025), AIOpsLab (Microsoft 2024), OpenReview 2025 | High |
| 2 | Multi-agent AI architectures with specialized domain agents outperform monolithic AI systems for software delivery | Harness AI (6 agents), Google SRE (AI Operator + Actus + Detectr), GitLab Duo | High |
| 3 | MCP (Model Context Protocol) is becoming the standard for AI agent-to-tool integration in chaos/CI/CD platforms | LitmusChaos MCP, Gremlin MCP, Steadybit MCP, Google SRE, Red Hat cicaddy | High |
| 4 | LLMs are effective co-pilots for RCA but not yet autonomous operators (60-74% vs 82% human accuracy) | Szandala (ICCS 2025), Google SRE A/B testing (10% MTTM reduction) | High |
| 5 | Bounded autonomy with human escalation is the universal safety pattern across all mature implementations | Google Safety Trifecta, Uber tiered blast radius, Amazon Apollo auto-halt, Cloud Native Now maturity model | High |
| 6 | Knowledge Graphs + RAG provide the contextual intelligence layer that makes AI-driven software delivery accurate | Harness Software Delivery Knowledge Graph, Google IRM Analyzer, academic survey (124 papers) | High |

### Corroborated (Moderate Evidence)

| # | Finding | Sources | Confidence |
|---|---|---|---|
| 7 | Reinforcement learning can achieve 42% MTTR reduction for autonomous cloud recovery | Kumar & Zhao (2024), Cloud Native Now FinTrust case study (85% MTTR reduction) | Medium |
| 8 | Predictive test selection using ML reduces CI time 50-90% without sacrificing defect detection | Launchable/CloudBees, Harness Test Intelligence, Uber DragonCrawl prioritization | Medium |
| 9 | Chaos engineering tool adoption is growing but dominated by manual fault injection (network 40.9%, instance termination 32.7%) | Owotogbe GitHub study (971 repos), Gartner Market Guide 2025 | Medium |
| 10 | Application-level chaos faults remain critically underrepresented in practice (3.0% of experiments) | Owotogbe GitHub study, Uber DragonCrawl (addressing this gap for mobile) | Medium |

### Contested (Mixed Evidence)

| # | Claim | For | Against |
|---|---|---|---|
| 11 | Full autonomous chaos engineering (L4) is achievable by 2026-2028 | Netflix evolution analysis, SRAO blog prediction | Google SRE (operating at L2/L3 only), Szandala (LLMs not yet reliable enough), industry consensus on human-in-the-loop |
| 12 | AI-driven chaos engineering provides 245% ROI over 3 years | SRAO analysis citing mature chaos practices | High prerequisites ($100K-$500K monitoring, $400K-$1M team), alternative approaches (canary deployments deliver 80% of benefit at 10% cost) |

### Gaps (No Evidence Found)

- No academic research on integrated CI/CD + chaos engineering workflows driven by AI agents (this project's unique contribution)
- No published benchmarks for AI agent accuracy in automated experiment design (only RCA evaluation exists)
- No research on automated compliance/governance gates within chaos experiments
- No research on multi-environment chaos orchestration across dev/staging/production tiers with blast radius governance
- No published evaluation of LLM accuracy for blast radius prediction or steady-state hypothesis generation

---

## Project Implications

| # | Finding | Affects | Recommendation |
|---|---|---|---|
| 1 | ChaosEater validates LLM-driven full chaos lifecycle automation | s14-s20 (Chaos Design through Game Day) | Adopt ChaosEater's agentic workflow pattern (plan -> inject -> observe -> remediate) as the execution model for chaos skills. Reference the paper's architecture in s14 experiment design. |
| 2 | Harness AI provides 6 specialized agents with Knowledge Graph | s00 (Orchestrator), all skills | Align s00's dispatch architecture with Harness AI's agent model. Map each project skill to the corresponding Harness AI agent (DevOps->s04-s10, Reliability->s14-s20, SRE->s27, AppSec->s11, FinOps->s25, Test->s12-s13). |
| 3 | MCP is the integration standard for chaos + AI | s14-s19 (Chaos), s00 (Orchestrator) | Integrate LitmusChaos MCP server into the project workflow. Use MCP as the tool-interaction protocol for s14-s20 chaos skills to enable natural language chaos execution. |
| 4 | LLMs at 60-74% RCA accuracy, not yet autonomous | s22-s23 (Observability/Alerting), s27 (Postmortem) | Design s27 as a human-AI co-pilot process, not fully automated. Use few-shot prompting (which boosts accuracy to 74%) rather than zero-shot. Implement hallucination detection in s23 alerting. |
| 5 | Application-level chaos is critically underrepresented (3.0%) | s19 (Application Faults) | Prioritize s19 as a differentiator. The project's focus on application-level faults (pod-delete, container-kill, network, DNS) addresses a documented gap in industry practice. |
| 6 | Bounded autonomy is universal safety pattern | s16 (Blast Radius), s20 (Game Day) | Implement Google's Safety Trifecta (Transparency, Real-time Risk Evaluation, Progressive Authorization) in s16 blast radius control and s20 game day planning. |
| 7 | Knowledge Graph provides critical context layer | s00 (Orchestrator), s03 (Progress Tracker) | Design s03's progress tracking to function as a lightweight knowledge graph connecting artifacts across skills. Reference Harness's Knowledge Graph + RAG hybrid architecture. |
| 8 | No research on integrated CI/CD + chaos AI workflows | s00-s31 (entire project) | This project occupies a genuinely novel position. Document this gap and position the project as a contribution to the field. Consider publishing findings. |
| 9 | Predictive test selection reduces CI time 50-90% | s12 (Testing), s13 (Performance) | Integrate predictive test selection concepts into s12/s13 pipeline design. Reference Harness Test Intelligence and Launchable's ML approach. |
| 10 | 5-level SRE Autonomy framework (L0-L4) exists | s00 (Orchestrator), all skills | Adopt Google's L0-L4 framework as the maturity model for the project. Current state is L0-L1. Target L2-L3 for initial implementation with progressive advancement. |

---

## SRE Autonomy Maturity Model (from Google SRE)

| Level | Name | Description | Agent Role |
|---|---|---|---|
| L0 | Manual | Human does everything | None |
| L1 | Hypothesis | AI suggests, human decides and acts | Advisory |
| L2 | Assisted | AI suggests and drafts, human approves | Co-pilot |
| L3 | Delegated | AI executes within bounds, human reviews | Semi-autonomous |
| L4 | Full Autonomy | AI acts independently, human sets policy | Autonomous |

**Current industry state**: L2-L3 for most mature organizations (Google, Uber, Harness). No documented L4 deployments for production reliability.

---

## AI Agent Landscape Map

### CI/CD Automation

| Agent/Platform | Organization | Capability | Maturity |
|---|---|---|---|
| Harness DevOps Agent | Harness | Pipeline creation, error analysis, policy generation, GitOps | Production (GA) |
| Harness CI Agent | Harness | Build optimization, test intelligence, cache management | Production (GA) |
| Harness STO Agent | Harness | Security vulnerability detection and auto-remediation | Production (GA) |
| GitLab Duo | GitLab | Agentic CI/CD pipeline management, security remediation | Production (18.x) |
| Launchable/CloudBees | CloudBees | Predictive test selection (50-90% test reduction) | Production (acquired) |
| Amazon Apollo | Amazon | Automated fleet-wide deployment coordination | Internal (50M deploys/yr) |

### Chaos Engineering

| Agent/Platform | Organization | Capability | Maturity |
|---|---|---|---|
| Harness Reliability Agent | Harness | Chaos experiment recommendations, auto-remediation guidance | Production (GA Jan 2025) |
| ChaosEater | Academic (ASE 2025) | Full automated chaos lifecycle on Kubernetes | Research prototype |
| LitmusChaos MCP Server | LitmusChaos/CNCF | Natural language chaos experiment management via MCP | Open source (2025) |
| Gremlin Reliability Intelligence | Gremlin | AI experiment analysis, remediation, MCP server | Production (Aug 2025) |
| Steadybit MCP Server | Steadybit | Chaos experiment insights via MCP | Production (2025) |
| DragonCrawl + uHavoc | Uber | AI-driven mobile chaos testing (180K+ tests) | Internal (ICSE 2026 paper) |
| Google AI Operator | Google | L2/L3 autonomous incident mitigation | Internal (thousands of incidents) |
| AWS FIS + Bedrock | AWS | Natural language chaos experiment generation | Production |
| Red Hat Krkn AI | Red Hat | AI-enhanced chaos testing for OpenShift | Development |

---

## Bibliography

### Academic Papers

1. Kikuta D, Ikeuchi H, Tajiri K. "LLM-Powered Fully Automated Chaos Engineering: Towards Enabling Anyone to Build Resilient Software Systems at Low Cost" (ASE 2025) -- https://arxiv.org/abs/2511.07865
2. Liu J, Wang K, Chen Y, et al. "Large Language Model-Based Agents for Software Engineering: A Survey" (ACM TOSEM 2024, 124 papers) -- https://arxiv.org/abs/2409.02977
3. Shetty M, Chen Y, Somashekar G, et al. "Building AI Agents for Autonomous Clouds: Challenges and Design Principles" (Microsoft Research 2024) -- https://arxiv.org/abs/2407.12165
4. Szandala T. "AIOps for Reliability: Evaluating Large Language Models for Automated Root Cause Analysis in Chaos Engineering" (ICCS 2025, Springer LNCS) -- DOI: 10.1007/978-3-031-97564-6_25
5. Owotogbe J. "Assessing and Enhancing the Robustness of LLM-based Multi-Agent Systems Through Chaos Engineering" (2025) -- https://arxiv.org/abs/2505.03096
6. Owotogbe J, Kumara I, Van Den Heuvel W-J, Tamburri DA. "Chaos Engineering: A Multi-Vocal Literature Review" (ACM Computing Surveys 2024) -- https://arxiv.org/abs/2412.01416
7. Owotogbe J, Kumara I, Di Nucci D, et al. "Chaos Engineering in the Wild: Findings from GitHub" (2025, 971 repos) -- https://arxiv.org/abs/2505.13654
8. Zhou L, Liu A, Liu H, et al. "Root Cause Analysis Method Based on Large Language Models with Residual Connection Structures" (2026) -- https://arxiv.org/abs/2602.08804
9. Kumar and Zhao. "Self-Healing Infrastructure: Leveraging Reinforcement Learning for Autonomous Cloud Recovery and Enhanced Resilience" (2024, 42% MTTR reduction) -- ResearchGate
10. Uber Engineering. "Scaling Mobile Chaos Testing with AI-Driven Test Execution" (ICSE-SEIP 2026) -- https://arxiv.org/abs/2602.06223

### Official Documentation

11. Harness AI Product Page -- https://www.harness.io/products/harness-ai
12. Harness AI DevOps Agent Docs -- https://developer.harness.io/docs/platform/harness-ai/devops-agent
13. Harness AI STO Agent Docs -- https://developer.harness.io/docs/platform/harness-ai/sto-agent
14. Harness AI-Powered Chaos Engineering Blog (Jan 2025) -- https://www.harness.io/blog/harness-adds-8-new-features-to-redefine-resiliency-with-ai-powered-chaos-engineering
15. Harness Knowledge Graph + RAG Blog -- https://www.harness.io/blog/knowledge-graph-rag
16. Harness AI Chaos Simplification Blog -- https://www.harness.io/blog/how-harness-is-using-ai-to-simplify-chaos-engineering-adoption
17. LitmusChaos MCP Server -- https://dev.to/litmus-chaos/making-chaos-engineering-accessible-introducing-the-litmuschaos-mcp-server-kif
18. Gremlin Reliability Intelligence Launch (Aug 2025) -- https://www.prnewswire.com/news-releases/chaos-engineering-pioneer-gremlin-launches-ai-driven-reliability-intelligence-302525829.html
19. Steadybit MCP Server -- https://steadybit.com/news/steadybit-launches-the-first-mcp-server-for-chaos-engineering/
20. Red Hat AI Chaos Testing -- https://www.redhat.com/en/blog/supercharging-chaos-testing-using-ai
21. AWS FIS + Amazon Bedrock -- https://aws.amazon.com/blogs/publicsector/chaos-engineering-made-clear-generate-aws-fis-experiments-using-natural-language-through-amazon-bedrock/

### Industry Sources

22. Google SRE. "AI in SRE: How Google is Engineering the Future of Reliable Operations" -- https://sre.google/resources/practices-and-processes/ai-engineering-reliable-operations/
23. Netflix Evolution Analysis. "Chaos Engineering: The Evolution from Netflix's Chaos Monkey to AI-Powered Resilience" -- https://www.srao.blog/p/chaos-engineering-the-evolution-from
24. Amazon Apollo. "Apollo: Amazon's Deployment Engine" -- https://www.allthingsdistributed.com/2014/11/apollo-amazon-deployment-engine.html
25. Shopify Engineering. "Shopify's Machine Learning Platform for Real-Time Predictions" -- https://shopify.engineering/shopifys-machine-learning-platform-real-time-predictions
26. Gartner. "Market Guide for Chaos Engineering Tools" (March 2025)
27. Cloud Native Now. "How SREs are Using AI to Transform Incident Response" -- https://cloudnativenow.com/contributed-content/how-sres-are-using-ai-to-transform-incident-response-in-the-real-world/
28. CloudBees Smart Tests (Launchable) -- https://www.cloudbees.com/capabilities/cloudbees-smart-tests
29. GitLab Agentic AI -- https://about.gitlab.com/topics/agentic-ai/
30. Harness KubeCon 2025 Recap -- https://www.harness.io/blog/kubecon-2025-recap
31. Intuit AI Blog (2022) + Spotify Engineering (2023) on AI-driven deployment safety
32. OpenReview. "Fully Automating Chaos Engineering with Large Language Models" -- https://openreview.net/forum?id=8pbyay0prT
33. ResearchGate. "The Evolution of DevOps to AIOps: A Conceptual Framework" (2025)
34. ResearchGate. "Chaos Engineering 2.0: AI-Driven, Policy-Guided Resilience for Multi-Cloud Systems" (2025)

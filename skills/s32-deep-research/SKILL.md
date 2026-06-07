---
name: deep-research
description: >
  Conduct deep, multi-source research across academic papers (Google Scholar, arXiv),
  official documentation, and industry articles, then engage in an interactive brainstorming
  debrief with the user to present evidence-backed findings and co-develop actionable solutions.
  Use this skill whenever the user says "research this", "find papers on", "what does research
  say about", "literature review", "evidence for", "deep dive into", "academic sources on",
  "what's the state of", "survey the landscape", or explicitly invokes /deep-research.
  This skill is callable at ANY phase in the workflow (s00-s31).
  Unlike s31 (pure ideation), s32 is RESEARCH-FIRST -- every claim is grounded in external evidence.
  Produces a structured research report saved to artifacts and an interactive debrief session.
---

# Deep Research Engine (s32)

## Purpose

Enable evidence-grounded decision-making by systematically searching, reading, and analyzing academic papers, official documentation, and industry sources. Every finding is backed by citable evidence. The skill concludes with an interactive brainstorming debrief where the user evaluates and selects actionable directions.

**This skill produces research reports and recommendations. It does NOT produce code, YAML, or implementation artifacts.**

---

## Prerequisites
- [ ] Research question or topic clearly defined
- [ ] Internet access for multi-source research
- [ ] Access to academic databases (Google Scholar, arXiv) recommended
- [ ] No specific skill outputs required — can be invoked at any phase

## Input Contract

| Input | Source | Required |
|---|---|---|
| Research question or topic | User prompt | Yes |
| Current workflow phase + artifacts | s00 context | No |
| PRD / specifications in scope | s01 output | No |
| Taste preferences | s02 taste file | No |
| Research depth preference | User | No (default: standard) |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Structured research report | `.commandcode/artifacts/research/` | Markdown |
| Source bibliography | Within report | Structured list |
| Evidence-backed findings | Conversation + report | Categorized |
| Brainstorm debrief summary | Conversation | Structured Markdown |
| Actionable recommendations | Conversation | Prioritized list |

---

## Research Depth Modes

| Mode | Sources | Agents | Use Case |
|---|---|---|---|
| `quick` | 2-3 targeted searches | 1 agent | Validate a specific claim or find a citation |
| `standard` | 3 parallel agents | 3 agents | Understand a topic with multi-domain evidence |
| `comprehensive` | 3 agents + follow-up deep dives | 3+ agents | Full literature review for architectural decisions |

Default: `standard`. Auto-selects based on topic complexity if user does not specify.

---

## Execution Protocol

```
PHASE 1: HARVEST (parallel agents)
  Agent A: Academic Researcher  -- Google Scholar, arXiv, Semantic Scholar
  Agent B: Documentation Analyst -- Official vendor docs, RFCs, specs
  Agent C: Industry Researcher   -- Engineering blogs, case studies, conference talks

PHASE 2: SYNTHESIZE (main agent)
  Deduplicate -> Cross-reference -> Classify -> Contextualize -> Prioritize

PHASE 3: DEBRIEF (interactive with user)
  Present findings -> Challenge assumptions -> Co-develop solutions -> Converge & commit
```

---

## Phase 1: HARVEST

Launch three specialized agents in parallel. Each targets a different source domain.

### Agent A -- Academic Researcher

**Sources**: Google Scholar, arXiv, Semantic Scholar, ACM Digital Library
**Focus**: Peer-reviewed papers, dissertations, survey papers
**Returns per finding**:
- title, authors, year
- key finding (1-2 sentences)
- relevance score (1-5)
- methodology quality note
- URL

**Search strategy**: Construct keyword queries from the user's topic. Prefer recent work (last 3 years). Include seminal/foundational papers regardless of age.

### Agent B -- Documentation Analyst

**Sources**: Official vendor docs (Harness, LitmusChaos, Kubernetes, CNCF), RFCs, specs, canonical reference
**Focus**: Best practices, supported patterns, version-specific guidance
**Returns per finding**:
- source, section
- key recommendation
- applicability to project context
- URL

**Search strategy**: Target the official documentation sites for technologies in the project stack. Search for the specific topic within each.

### Agent C -- Industry Researcher

**Sources**: Engineering blogs (Netflix TechBlog, Stripe Engineering, Uber Engineering, Google SRE, Cloudflare Blog), case studies, conference talks (KubeCon, QCon, SREcon), tech media
**Focus**: Real-world implementations, lessons learned, failure stories, benchmarks
**Returns per finding**:
- source, organization
- what they did
- outcome
- lessons applicable to this project
- URL

**Search strategy**: Search for the topic combined with organization names known for thought leadership in the relevant domain. Include "postmortem", "case study", "lessons learned" as modifiers.

### Harvest Output Schema

```yaml
harvest_result:
  topic: string
  academic_findings:
    - title: string
      authors: string
      year: number
      key_finding: string
      relevance: number
      methodology: string
      url: string
  documentation_findings:
    - source: string
      section: string
      recommendation: string
      applicability: string
      url: string
  industry_findings:
    - source: string
      organization: string
      approach: string
      outcome: string
      lessons: string
      url: string
  search_queries_used: [string]
  sources_searched: [string]
  gaps_identified: [string]
```

---

## Phase 2: SYNTHESIZE

Process all harvest results through this pipeline:

### Step 1: Deduplicate
Remove overlapping findings across the three source domains. Keep the most authoritative source for each unique finding.

### Step 2: Cross-Reference
Find where academic, documentation, and industry sources agree or contradict each other. A finding supported by all three domains is the strongest possible evidence.

### Step 3: Classify
Group findings into four categories:

| Category | Criteria | Weight |
|---|---|---|
| **Consensus** | All 3 source types agree | Strongest evidence |
| **Corroborated** | 2+ source types agree | Strong evidence |
| **Contested** | Sources disagree | Present both sides |
| **Gaps** | No evidence found | Flag for user awareness |

### Step 4: Contextualize
Map findings to the current project state. If s00 context and s01 PRD are available, evaluate how each finding affects the existing architecture, pipelines, and experiments.

### Step 5: Prioritize
Rank findings by relevance to the user's original question. Cap at 15-20 total sources to maintain signal-to-noise ratio.

### Synthesis Output Schema

```yaml
synthesis:
  topic: string
  themes:
    - name: string
      evidence_level: string
      findings: [string]
      contradictions: [{ claim: string, for: [], against: [] }]
  consensus_points: [string]
  contested_points: [{ claim: string, for: [], against: [] }]
  gaps: [string]
  project_implications: [{ finding: string, affects: [], recommendation: string }]
  confidence_assessment: string
```

---

## Phase 3: DEBRIEF

A structured interactive conversation with the user. Follow this sequence:

### Step 1: Present Findings

```
"Here's what the research says about <topic>..."
- Top 5-7 key findings (evidence-backed)
- Where sources agree and disagree
- Gaps in current knowledge
- Confidence assessment (high/medium/low)
```

### Step 2: Challenge Assumptions

```
"Based on this evidence, your current approach..."
- What the evidence supports
- What the evidence contradicts
- What's unproven either way
- Risks that the research highlights
```

### Step 3: Co-Develop Solutions

```
"Let's brainstorm options based on this evidence..."
- Present 3-5 solution directions
- Each grounded in specific evidence
- Each with: evidence base, trade-offs, applicability
- Interactive: user can probe, redirect, combine
```

### Step 4: Converge & Commit

```
"Which direction(s) do you want to pursue?"
- User selects preferred approach(es)
- Document the decision and its evidence base
- Determine next steps and skill dispatch
```

### Debrief Output Schema

```yaml
debrief_result:
  findings_presented: number
  assumptions_challenged: [string]
  solutions_explored: number
  user_selected: [string]
  evidence_base: [{ claim: string, sources: [] }]
  next_steps: [{ action: string, dispatch_to: string }]
```

---

## Skill Integration

### Feeds Into

| Target Skill | What Gets Passed |
|---|---|
| s31 (Strategic Creator) | Research context for evidence-backed proposals |
| s01 (BA Requirements) | Evidence-grounded PRD updates |
| s14 (Experiment Design) | Chaos patterns validated by literature |
| s22 (Observability) | Monitoring best practices from papers |
| s26 (Resilience Scoring) | Scoring models from academic research |
| s00 (Orchestrator) | Replan affected phases if findings change scope |

### Consumes From

| Source | What It Provides |
|---|---|
| s00 | Context, current phase, workflow state |
| s01 | PRD, specs for contextual relevance |
| s02 | Taste preferences for research depth/format |

### Dispatch Map

```yaml
on_completion:
  user_wants_strategic_proposals: s31
  user_wants_spec_update: s01
  user_wants_experiment_design: s14
  user_wants_implementation: s00
  user_wants_nothing: end

on_partial:
  user_wants_deeper_research: re-enter Phase 1 with refined queries
  user_wants_different_angle: re-enter Phase 1 with new search terms
  user_wants_to_debate: stay in Phase 3 (extend debrief)
```

---

## Rules of Engagement

1. **Evidence over opinion** -- Every claim must cite a source. Replace "I think X" with "Paper Y found X" or "Netflix reported X."
2. **No cherry-picking** -- If evidence contradicts the user's hypothesis, present it clearly. If mixed, present both sides with weight.
3. **Recency matters** -- Prefer sources from the last 3 years. Older sources only when seminal/foundational.
4. **Relevance over volume** -- 5 highly relevant papers beat 50 tangentially related ones. Cap at 15-20 total sources.
5. **Accessibility** -- Prefer open-access and publicly available sources. Flag paywalled key findings.
6. **Honest about limits** -- If no strong evidence exists, say so. "The literature is sparse" is a valid finding.
7. **Taste-aware** -- Load s02 preferences. Compress for concise preference; expand for depth preference.
8. **No implementation** -- s32 produces research and recommendations only. It writes reports, not code or YAML.

---

## Artifact Structure

```
.commandcode/artifacts/research/
    YYYY-MM-DD-<topic-slug>/
        report.md          -- Full research report
        bibliography.md    -- All sources cited
        debrief-summary.md -- Debrief decisions and evidence base
```

---

## Research Report Template

```markdown
# Deep Research Report: <Topic>

**Date**: YYYY-MM-DD
**Researcher**: s32-deep-research
**Depth**: quick | standard | comprehensive
**Trigger**: User question or skill dispatch

---

## Executive Summary
3-5 sentences: What we researched, what we found, what it means.

---

## Key Findings

### Consensus (Strong Evidence)
| Finding | Sources | Confidence |
|---|---|---|
| <claim> | <citations> | High |

### Corroborated (Moderate Evidence)
| Finding | Sources | Confidence |
|---|---|---|
| <claim> | <citations> | Medium |

### Contested (Mixed Evidence)
| Claim | For | Against |
|---|---|---|
| <claim> | <supporting> | <contradicting> |

### Gaps (No Evidence Found)
- <what we couldn't find>

---

## Project Implications
| Finding | Affects | Recommendation |
|---|---|---|
| <evidence> | <area> | <action> |

---

## Bibliography
### Academic Papers
1. Author et al. "Title" (Year) -- URL

### Official Documentation
1. Source -- "Section" -- URL

### Industry Sources
1. Organization -- "Title" -- URL
```

---

## Triggers

```yaml
invoked_when:
  - User says: "research this", "find papers on", "what does research say about"
  - User says: "literature review", "evidence for", "deep dive into"
  - User says: "academic sources on", "what's the state of", "survey the landscape"
  - User explicitly invokes: /deep-research or s32
  - User asks "is there evidence that X?" or "what do papers say about Y?"
```

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | Research + interactive debrief, human evaluates all findings |
| Target | L1 | Permanently L1 by design (research advisory, not autonomous) |

### Harness AI Agent

**Agent**: None (research by design)
**Capabilities**:
- Multi-source parallel research (academic/docs/industry)
- Evidence synthesis and classification
- Interactive brainstorming debrief
- Research report generation

### Human Gates

- ALL research findings presented for user evaluation
- ALL recommendations require user selection
- ALL dispatch decisions require user approval

### Notes

This skill is permanently L1 by design. Research quality requires human judgment for source evaluation and solution selection.

---

## Success Criteria

- [ ] s32 can be invoked from any phase or directly by user
- [ ] Phase 1 launches parallel agents for academic, docs, and industry sources
- [ ] Phase 2 produces classified findings (consensus/corroborated/contested/gaps)
- [ ] Phase 3 runs an interactive debrief with the user
- [ ] Research report saved to `.commandcode/artifacts/research/`
- [ ] Bibliography included with every report
- [ ] Evidence cited for every claim
- [ ] Dispatch to other skills works on user selection
- [ ] Research depth modes (quick/standard/comprehensive) functional
- [ ] Taste preferences from s02 respected

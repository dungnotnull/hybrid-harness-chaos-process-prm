# Design Spec: s32-deep-research

**Date**: 2026-05-27
**Status**: Approved for implementation
**Affects**: New skill (s32-deep-research), optional integration with s31-strategic-creator

---

## 1. Overview

A new standalone skill (`s32-deep-research`) that enables the agent to conduct deep, multi-source research across academic papers (Google Scholar, arXiv), official documentation, and industry articles, then engage in an interactive brainstorming debrief with the user to present evidence-backed findings and co-develop actionable solutions.

**Why**: The existing 32-skill workflow (s00-s31) lacks a mechanism for grounding decisions in external evidence. s31 (Strategic Creator) is purely advisory ideation. s32 fills this gap by providing research-first, evidence-backed analysis that can feed into any skill in the workflow.

**Callable at**: ANY phase (like s31). Not part of the linear workflow sequence.

---

## 2. Architecture

```
USER REQUEST
    |
PHASE 1: HARVEST (parallel agents)
    |-- Agent A: Google Scholar + arXiv (academic)
    |-- Agent B: Official docs + vendor docs (canonical)
    |-- Agent C: Engineering blogs + case studies (industry)
    |
PHASE 2: SYNTHESIZE (main agent)
    |-- Deduplicate findings
    |-- Cross-reference across sources
    |-- Classify: consensus / corroborated / contested / gaps
    |-- Contextualize to project state
    |-- Prioritize by relevance
    |
PHASE 3: DEBRIEF (interactive with user)
    |-- Present key findings
    |-- Challenge assumptions with evidence
    |-- Co-develop solutions (3-5 directions)
    |-- User evaluates and selects
    |
OUTPUT: Research report artifact + debrief summary
```

---

## 3. Input/Output Contracts

### Input

| Input | Source | Required |
|---|---|---|
| Research question or topic | User prompt | Yes |
| Current workflow phase + artifacts | s00 context | No |
| PRD / specifications in scope | s01 output | No |
| Taste preferences | s02 taste file | No |
| Research depth preference | User | No (default: standard) |

### Output

| Output | Destination | Format |
|---|---|---|
| Structured research report | `.commandcode/artifacts/research/` | Markdown |
| Source bibliography | Within report | Structured list |
| Evidence-backed findings | Conversation + report | Categorized |
| Brainstorm debrief summary | Conversation | Structured Markdown |
| Actionable recommendations | Conversation | Prioritized list |

---

## 4. Phase 1: HARVEST

Three specialized agents launched in parallel, each targeting a different source domain.

### Agent A -- Academic Researcher

- **Sources**: Google Scholar, arXiv, Semantic Scholar, ACM Digital Library
- **Focus**: Peer-reviewed papers, dissertations, survey papers
- **Returns per finding**: title, authors, year, key finding, relevance score (1-5), methodology quality note, URL
- **Search strategy**: Keyword-based queries refined from the user's topic

### Agent B -- Documentation Analyst

- **Sources**: Official vendor docs (Harness, LitmusChaos, Kubernetes), RFCs, specs, canonical reference
- **Focus**: Best practices, supported patterns, version-specific guidance
- **Returns per finding**: source, section, key recommendation, applicability to project context, URL

### Agent C -- Industry Researcher

- **Sources**: Engineering blogs (Netflix, Stripe, Uber, Google SRE), case studies, conference talks, tech media
- **Focus**: Real-world implementations, lessons learned, failure stories, benchmarks
- **Returns per finding**: source, organization, what they did, outcome, lessons applicable here, URL

### Harvest Output Schema

```yaml
harvest_result:
  topic: string
  academic_findings:
    - title: string
      authors: string
      year: number
      key_finding: string
      relevance: number  # 1-5
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

## 5. Phase 2: SYNTHESIZE

The main agent processes all harvest results through this pipeline:

1. **Deduplicate** -- Remove overlapping findings across sources
2. **Cross-reference** -- Find where academic, docs, and industry agree or contradict
3. **Classify** findings into themes:
   - **Consensus** (all 3 source types agree) -- strongest evidence
   - **Corroborated** (2+ source types agree) -- strong evidence
   - **Contested** (sources disagree) -- present both sides with weight
   - **Gaps** (no evidence found) -- flag for user awareness
4. **Contextualize** -- Map findings to the current project state (from s00 context)
5. **Prioritize** -- Rank findings by relevance to the user's question

### Synthesis Output Schema

```yaml
synthesis:
  topic: string
  themes:
    - name: string
      evidence_level: string  # consensus | corroborated | contested | gap
      findings: [string]
      contradictions: [{ claim: string, for: [], against: [] }]
  consensus_points: [string]
  contested_points: [{ claim: string, for: [], against: [] }]
  gaps: [string]
  project_implications: [{ finding: string, affects: [], recommendation: string }]
  confidence_assessment: string  # high | medium | low
```

---

## 6. Phase 3: DEBRIEF

A structured conversation with the user following this flow:

```
1. PRESENT FINDINGS
   - Top 5-7 key findings (evidence-backed)
   - Where sources agree and disagree
   - Gaps in current knowledge

2. CHALLENGE ASSUMPTIONS
   - What the evidence supports
   - What the evidence contradicts
   - What's unproven either way

3. CO-DEVELOP SOLUTIONS
   - 3-5 solution directions grounded in evidence
   - Each with: evidence base, trade-offs, applicability
   - Interactive: user can probe, redirect, combine options

4. CONVERGE & COMMIT
   - User selects preferred approach(es)
   - Document the decision and its evidence base
   - Optional: dispatch to s31 or relevant implementation skills
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

## 7. Skill Integration

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

## 8. Rules of Engagement

1. **Evidence over opinion** -- Every claim must cite a source. No unsupported assertions.
2. **No cherry-picking** -- Present contradictory evidence clearly. Show both sides with weight.
3. **Recency matters** -- Prefer sources from the last 3 years. Older only when seminal/foundational.
4. **Relevance over volume** -- Cap at 15-20 total sources per session. 5 highly relevant beats 50 tangential.
5. **Accessibility** -- Prefer open-access and publicly available sources. Flag paywalled key findings.
6. **Honest about limits** -- "The literature is sparse" is a valid and important finding.
7. **Taste-aware** -- Load s02 preferences for format and depth.
8. **No implementation** -- s32 produces research and recommendations only. Writes reports, not code or YAML.

---

## 9. Research Depth Modes

| Mode | Sources | Agents | Use Case |
|---|---|---|---|
| `quick` | 2-3 targeted searches | 1 agent | Validate a specific claim |
| `standard` | 3 parallel agents | 3 agents | Understand a topic with multi-domain evidence |
| `comprehensive` | 3 agents + follow-up deep dives | 3+ agents | Full literature review for architectural decisions |

Default: `standard`. Auto-selects based on topic complexity if user does not specify.

---

## 10. Artifact Structure

```
.commandcode/artifacts/research/
    YYYY-MM-DD-<topic-slug>/
        report.md          -- Full research report
        bibliography.md    -- All sources cited
        debrief-summary.md -- Debrief decisions and evidence base
```

---

## 11. Research Report Template

```markdown
# Deep Research Report: <Topic>

**Date**: YYYY-MM-DD
**Researcher**: s32-deep-research
**Depth**: quick | standard | comprehensive
**Trigger**: User question or skill dispatch

---

## Executive Summary
3-5 sentences: What we researched, what we found, what it means for this project.

---

## Key Findings

### Consensus (Strong Evidence)
| Finding | Sources | Confidence |
|---|---|---|
| <claim> | <papers/docs/blogs> | High |

### Corroborated (Moderate Evidence)
| Finding | Sources | Confidence |
|---|---|---|
| <claim> | <papers/docs/blogs> | Medium |

### Contested (Mixed Evidence)
| Claim | For | Against |
|---|---|---|
| <claim> | <sources supporting> | <sources contradicting> |

### Gaps (No Evidence Found)
- <what we couldn't find evidence for>

---

## Project Implications
| Finding | Affects | Recommendation |
|---|---|---|
| <evidence> | <project area> | <what to do about it> |

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

## 12. File to Create

| File | Purpose |
|---|---|
| `skills/s32-deep-research/SKILL.md` | The complete skill definition following the project's SKILL.md convention |

---

## 13. Success Criteria

- [ ] s32 can be invoked from any phase or directly by user
- [ ] Phase 1 launches parallel agents for academic, docs, and industry sources
- [ ] Phase 2 produces classified findings (consensus/corroborated/contested/gaps)
- [ ] Phase 3 runs an interactive debrief with the user
- [ ] Research report saved to `.commandcode/artifacts/research/`
- [ ] Bibliography included with every report
- [ ] Evidence cited for every claim (no unsupported assertions)
- [ ] Dispatch to s31 or other skills works on user selection
- [ ] Research depth modes (quick/standard/comprehensive) functional
- [ ] Taste preferences from s02 respected

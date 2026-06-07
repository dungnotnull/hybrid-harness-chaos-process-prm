---
name: devils-advocate
description: >
  Adversarial critique and counter-argument skill that stress-tests every decision,
  design, hypothesis, and strategy across the entire workflow. Adapted from the
  Devil's Advocate Agent architecture (dungnotnull/devils-advocate-agent), this
  skill provides structured Socratic questioning, logical fallacy detection,
  argument strength scoring, and multi-perspective challenge generation. Use
  whenever a major decision is made, a design is proposed, a hypothesis is formed,
  or when the user explicitly requests critical review. Callable at ANY phase.
  Triggers: "challenge this", "stress-test", "play devil's advocate", "what's
  wrong with this", "critique", "find flaws", "counter-argument", "red team".
---

# Devil's Advocate (s35)

## Purpose
Systematically dismantle ideas, strategies, designs, and hypotheses to expose
every flaw, assumption, contradiction, and logical fallacy — so only the strongest
arguments survive. This skill operates as a quality gate across the entire workflow,
ensuring that no critical decision goes unchallenged.

Adapted from the Devil's Advocate Agent (github.com/dungnotnull/devils-advocate-agent),
which provides:
- Multi-intensity adversarial critique (Skeptic → Critic → Prosecutor → Demolisher)
- Real-time logical fallacy detection (14+ fallacy types)
- Multi-dimensional argument strength scoring (0-100 across clarity, evidence, logic, novelty, defense)
- RAG-grounded counter-arguments using external evidence
- Assumption hunting and implicit premise extraction

This skill integrates those capabilities into the workflow as a callable quality gate.

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Subject to critique | Any skill output, PRD, design, hypothesis, strategy | Yes |
| Critique intensity level (1-4) | User specification or auto-determined | No (default: 2) |
| Domain context | s01 PRD, s02 taste | Yes |
| Relevant evidence/research | s32 deep-research (if available) | No |
| Current phase context | s03 progress tracker | Yes |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Counter-argument report | .commandcode/artifacts/critique/ | Markdown |
| Argument strength scores | .commandcode/artifacts/critique/ | JSON |
| Identified fallacies | .commandcode/artifacts/critique/ | JSON |
| Assumption inventory | .commandcode/artifacts/critique/ | Markdown |
| Recommended revisions | Target skill's output (feedback loop) | Markdown |
| Quality gate verdict | s03 progress tracker | JSON |

---

## Prerequisites
- [ ] Subject matter (idea, design, hypothesis, strategy) clearly defined
- [ ] Domain context available (PRD, taste, or relevant background)
- [ ] User or orchestrator has explicitly invoked critique

---

## Intensity Levels (Adapted from Devil's Advocate Agent)

| Level | Name | Behavior | When to Use |
|---|---|---|---|
| 1 | Skeptic | Gentle probing questions; assumes good faith | Early ideation, brainstorming sessions |
| 2 | Critic | Direct challenges with evidence; names gaps explicitly | Design reviews, hypothesis validation, PRD reviews |
| 3 | Prosecutor | Systematic deconstruction of all premises; counts contradictions | Architecture decisions, security reviews, production readiness |
| 4 | Demolisher | Maximum adversarial intensity; tears apart piece by piece | Pre-deployment gates, game day pre-mortems, compliance audits |

**Default**: Level 2 (Critic)
**Auto-escalation**: Increase by one level when:
- The same weak argument is repeated without new evidence
- Score drops ≥5 points between consecutive critique rounds
- Critical assumption is left unaddressed after one challenge

---

## Critique Framework

### Phase 1: Input Analysis

`yaml
input_analysis:
  claim_extraction:
    - Identify every factual claim in the subject
    - Rate each claim: verifiable / unverifiable / opinion
    - Flag statistical claims without cited sources

  assumption_hunting:
    - Identify explicit assumptions (stated "we assume...")
    - Identify implicit assumptions (unstated but necessary for the argument)
    - Categorize: causal / universal / value / existence / comparison

  fallacy_detection:
    types:
      - ad_hominem: Attacking the person, not the argument
      - straw_man: Misrepresenting the opposing position
      - hasty_generalization: Drawing broad conclusions from limited data
      - false_dichotomy: Presenting only two options when more exist
      - appeal_to_authority: Citing authority without domain expertise
      - slippery_slope: Assuming one step inevitably leads to extreme outcomes
      - circular_reasoning: The conclusion is assumed in the premise
      - bandwagon: "Everyone is doing it" as sole justification
      - anecdotal_evidence: Generalizing from personal stories
      - confirmation_bias: Selectively citing supporting evidence only
      - sunk_cost: Continuing because of prior investment
      - survivorship_bias: Only considering successful cases
      - post_hoc: Assuming correlation implies causation
      - appeal_to_tradition: "This is how we've always done it"
`

### Phase 2: Multi-Perspective Challenge

Every subject is challenged through four lenses (adapted from s01-1 user-flow review):

`yaml
perspectives:
  business_lens:
    questions:
      - "Does this actually solve the stated business problem?"
      - "What is the ROI? Can you quantify it?"
      - "What happens if adoption is 10% of projections?"
      - "What are the regulatory/compliance risks?"
      - "How does this impact revenue, costs, or customer churn?"

  engineering_lens:
    questions:
      - "Is this implementable with the current architecture?"
      - "What are the hidden complexity costs?"
      - "How does this scale to 10x current load?"
      - "What are the failure modes?"
      - "What are the blast radius implications?"

  reliability_lens:
    questions:
      - "What happens when this fails?"
      - "How do we detect failure? (Observability)"
      - "What is the recovery time objective?"
      - "Has this been tested under chaos conditions?"
      - "What are the cascading failure risks?"

  security_lens:
    questions:
      - "What is the attack surface of this change?"
      - "Are there privilege escalation paths?"
      - "Does this introduce new secrets or credentials?"
      - "Does this comply with security policies (s24)?"
      - "What is the worst-case security scenario?"
`

### Phase 3: Argument Strength Scoring

Each argument is scored on a 0-100 scale across five dimensions:

`json
{
  "argument_strength": {
    "clarity": {
      "score": 0,
      "description": "How clearly is the claim stated?",
      "rubric": {
        "0-20": "Vague, ambiguous, or incomprehensible",
        "21-40": "Understandable but imprecise",
        "41-60": "Clear but could be more specific",
        "61-80": "Well-articulated with precise language",
        "81-100": "Crystal clear with measurable criteria"
      }
    },
    "evidence_quality": {
      "score": 0,
      "description": "Quality and relevance of supporting evidence",
      "rubric": {
        "0-20": "No evidence or purely anecdotal",
        "21-40": "Weak evidence, cherry-picked data",
        "41-60": "Some evidence but gaps in sourcing",
        "61-80": "Well-sourced evidence from credible sources",
        "81-100": "Comprehensive, peer-reviewed, and quantified evidence"
      }
    },
    "logical_consistency": {
      "score": 0,
      "description": "Freedom from contradictions and logical gaps",
      "rubric": {
        "0-20": "Major logical contradictions",
        "21-40": "Some contradictions or unsupported leaps",
        "41-60": "Mostly consistent with minor gaps",
        "61-80": "Consistent with well-reasoned connections",
        "81-100": "Ironclad logic with no gaps"
      }
    },
    "novelty": {
      "score": 0,
      "description": "Originality and depth of reasoning",
      "rubric": {
        "0-20": "Repetitive of known approaches",
        "21-40": "Minor variations on existing ideas",
        "41-60": "Some original insight combined with known approaches",
        "61-80": "Novel approach with clear advantages",
        "81-100": "Breakthrough insight that shifts the paradigm"
      }
    },
    "defense_improvement": {
      "score": 0,
      "description": "How well weaknesses were addressed in follow-up rounds",
      "rubric": {
        "0-20": "No defense offered or defense made it worse",
        "21-40": "Weak defense, ignored major counter-arguments",
        "41-60": "Partial defense, addressed some challenges",
        "61-80": "Strong defense, addressed most challenges effectively",
        "81-100": "Exceptional defense that strengthened the original argument"
      }
    }
  },
  "overall_score": "weighted average: (clarity*0.2 + evidence*0.25 + logic*0.25 + novelty*0.15 + defense*0.15)"
}
`

### Phase 4: Verdict Generation

`yaml
verdict:
  overall_assessment: one of [STRONG, MODERATE, WEAK, CRITICAL]
  confidence_level: percentage (0-100%)
  key_weaknesses: [list of top 3 weaknesses]
  key_strengths: [list of top 3 strengths]
  recommended_revisions: [list of specific, actionable revisions]
  escalation_needed: boolean (true if any dimension scores below 40)
  gate_result: PASS | CONDITIONAL_PASS | FAIL
    PASS: overall >= 70, no dimension below 50
    CONDITIONAL_PASS: overall >= 50, no dimension below 40
    FAIL: overall < 50 OR any dimension below 40
`

---

## Workflow Integration Points

The Devil's Advocate integrates with the workflow at critical decision gates:

### Integration with s14 (Experiment Design)
`yaml
trigger: After chaos experiment is designed, before blast radius approval
action: Challenge the hypothesis, question fault selection, test abort conditions
output: Counter-arguments fed back to s14 for revision, or gate PASSED
`

### Integration with s15 (Hypothesis Validation)
`yaml
trigger: After hypothesis is written, before acceptance criteria are locked
action: Attack the hypothesis from the reliability lens — what if it's wrong?
output: Strengthened hypothesis with better acceptance/rejection criteria
`

### Integration with s28 (Release Management)
`yaml
trigger: Before Go/No-Go decision
action: Full Prosecutor-level (3) critique of release readiness
output: Release gate verdict — PASS, CONDITIONAL, or FAIL
`

### Integration with s31 (Strategic Creator)
`yaml
trigger: After strategic proposals are generated
action: Challenge every proposal with Demolisher-level (4) intensity
output: Only proposals that survive are forwarded to user for acceptance
`

### Integration with s01 (BA Requirements)
`yaml
trigger: After PRD is drafted, before ADRs are locked
action: Critic-level (2) challenge of business assumptions, technical feasibility
output: Revised PRD with addressed counter-arguments documented
`

---

## Critique Execution Protocol

`
Step 1:  RECEIVE subject from invoking skill or user
Step 2:  LOAD domain context (PRD, taste, relevant research)
Step 3:  DETERMINE intensity level (default: 2, auto-escalate if needed)
Step 4:  EXTRACT claims, assumptions, and logical structure
Step 5:  DETECT fallacies (apply fallacy taxonomy)
Step 6:  GENERATE counter-arguments from each perspective lens
Step 7:  SCORE argument strength on 5 dimensions (0-100 each)
Step 8:  PRODUCE verdict (STRONG/MODERATE/WEAK/CRITICAL)
Step 9:  WRITE critique report to .commandcode/artifacts/critique/
Step 10: UPDATE progress.json with gate result
Step 11: RETURN verdict + recommended revisions to invoking skill
Step 12: IF gate FAIL → block progression, require revision
         IF gate CONDITIONAL → allow progression with documented risks
         IF gate PASS → proceed to next skill
`

---

## Counter-Argument Templates

### For Design Decisions
`
## Counter-Argument: [DESIGN DECISION]

**Claim**: [What the design claims to achieve]
**Challenge**: [Why it might not achieve this]

### Evidence Against
1. [Evidence point 1]
2. [Evidence point 2]
3. [Evidence point 3]

### Assumptions at Risk
- [Assumption 1]: [Why it might not hold]
- [Assumption 2]: [Why it might not hold]

### Alternative Approaches
1. [Alternative 1]: [Trade-offs]
2. [Alternative 2]: [Trade-offs]

### Score Impact
- Clarity: -[N] points ([reason])
- Evidence: -[N] points ([reason])
- Logic: -[N] points ([reason])
`

### For Hypotheses (Chaos Engineering)
`
## Counter-Argument: [HYPOTHESIS]

**Hypothesis**: [If X fails, then Y should happen, measured by Z]
**Challenge**: [Why the hypothesis might be wrong]

### What Could Go Wrong
1. [Failure mode 1]: [Description]
2. [Failure mode 2]: [Description]
3. [Failure mode 3]: [Description]

### Missing Considerations
- [Observability gap]: [What metrics are missing?]
- [Blast radius risk]: [What else could be affected?]
- [Cascading failure]: [What if X failure triggers Y?]

### Recommended Strengthening
1. [Add metric/condition]
2. [Add probe]
3. [Add abort condition]
`

### For Release Decisions
`
## Counter-Argument: [RELEASE GATE]

**Decision**: [Go/No-Go for release]
**Challenge**: [Why this release might not be ready]

### Open Risks
1. [Risk 1]: [Severity] - [Mitigation status]
2. [Risk 2]: [Severity] - [Mitigation status]
3. [Risk 3]: [Severity] - [Mitigation status]

### Outstanding Items
- [ ] [Checklist item 1]
- [ ] [Checklist item 2]

### Verdict: CONDITIONAL_PASS
**Conditions**: [List of conditions that must be met before Go]
**Escalation**: [Who needs to approve if conditions not met]
`

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI generates counter-arguments and scores; human decides on verdict |
| Target | L2 | AI auto-critiques at designated gates; human reviews verdicts |

### Harness AI Agent

**Agent**: None (adversarial by design — intentionally independent)
**Fallback**: Uses the skill's built-in critique framework and fallacy taxonomy

### Human Gates

- Final verdict acceptance (PASS/CONDITIONAL/FAIL)
- Intensity level selection for each critique session
- Escalation decisions when gate fails

### MCP Integration

None required. This skill operates as a pure reasoning quality gate.

### Integration with Devil's Advocate Agent

For enhanced critique, this skill can optionally integrate with the
Devil's Advocate Agent (github.com/dungnotnull/devils-advocate-agent):

`yaml
integration:
  mode: optional  # Skill works standalone; agent enhances it
  benefits:
    - ML-based fallacy detection (beyond rule-based taxonomy)
    - RAG-grounded counter-arguments from research papers
    - Argument strength scoring via cross-encoder NLI model
    - Persistent debate sessions for iterative improvement
  setup:
    - Clone devil-advocate-agent repository
    - Configure LLM provider (Anthropic/OpenAI/Ollama)
    - Start agent: python main.py --port 8001
    - Set environment: DEVILS_ADVOCATE_URL=http://localhost:8001
  usage:
    - Skill sends subject to /api/v1/debate/start
    - Receives counter-arguments with fallacy annotations
    - Incorporates into critique report
    - User can continue debate rounds for iterative strengthening
`

---

## Success Criteria
- [ ] Every claim in the subject is extracted and categorized
- [ ] At least 3 counter-arguments generated per perspective lens
- [ ] All detected fallacies are named and explained
- [ ] Argument strength scored on all 5 dimensions
- [ ] Verdict includes specific, actionable recommended revisions
- [ ] Gate result (PASS/CONDITIONAL/FAIL) is unambiguous
- [ ] Critique report stored in .commandcode/artifacts/critique/
- [ ] Progress tracker updated with gate result
- [ ] If gate FAIL, progression is blocked until revision
- [ ] If gate CONDITIONAL, documented risks are recorded

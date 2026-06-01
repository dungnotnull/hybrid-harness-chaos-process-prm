---
name: documentation-writing
description: >
  Generate comprehensive project documentation including technical specs, user flows,
  beginner-friendly usage guides, and README files. Use when the user says "write docs",
  "create documentation", "add README", "user guide", "technical spec", "usage instructions",
  "how to use this", "explain for beginners", "write a userflow", "onboarding docs",
  or explicitly invokes /documentation-writing. Covers four documentation types:
  (1) Technical — architecture, APIs, data models, infrastructure for engineers;
  (2) User Flow — step-by-step journey maps, interaction sequences, decision trees;
  (3) Usage Instructions — plain-language guides for non-technical users, screenshots-first;
  (4) README — project overview, quickstart, badges, contributing guide.
  Produces Markdown artifacts in docs/ or project root. Callable at ANY phase.
---

# Documentation Writing — Project Documentation Engine (s34)

## Purpose

Generate clear, accurate, audience-appropriate documentation that makes a project understandable and usable by every stakeholder — from backend engineers reviewing architecture to first-time users trying to get started. Every document follows the principle: **the reader should never have to guess.**

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| Project codebase / structure | Repository exploration | Yes |
| Target documentation type | User prompt (technical / userflow / usage / README) | Yes |
| Target audience | User prompt or inferred | Yes |
| PRD / specifications | s01 output | No |
| ADRs | s01 output | No |
| Existing documentation | docs/ directory scan | No |
| User's tone preference | s02 taste file | No |

## Output Contract

| Output | Destination | Format |
|---|---|---|
| Documentation artifact | `docs/<type>/` or project root | Markdown |
| README.md | Project root | Markdown with badges, TOC, sections |
| User flow diagram | `docs/userflows/` | Mermaid flowchart or numbered steps |
| Technical spec | `docs/technical/` | Markdown with code blocks, diagrams |
| Usage guide | `docs/guides/` | Markdown with screenshots, plain language |

---

## Documentation Types

### Type 1: Technical Documentation

**Audience**: Engineers, SREs, DevOps, platform teams

**Structure**:
```markdown
# <Component/Feature Name> — Technical Specification

## Overview
One paragraph: what it does, why it exists, what problem it solves.

## Architecture
High-level design. Mermaid diagrams for data flow, component relationships.

## Data Model
Tables, schemas, relationships. Include field types, constraints, defaults.

## API Reference
Endpoint, method, request/response schema, error codes, rate limits.

## Configuration
Environment variables, config files, feature flags. Include defaults.

## Error Handling
Error codes, retry logic, fallback behavior.

## Dependencies
External services, libraries, infrastructure requirements.

## Security Considerations
Auth requirements, data sensitivity, threat model.

## Testing
How to test locally, integration test setup, mocking external deps.
```

**Rules**:
- Use Mermaid diagrams for architecture and data flow
- Include runnable code examples (not pseudocode)
- Document error states as thoroughly as happy paths
- Link to ADRs for design decisions
- Every config option must show its default value

---

### Type 2: User Flow Documentation

**Audience**: Product managers, designers, QA, engineers

**Structure**:
```markdown
# <Flow Name> — User Flow

## Overview
What the user is trying to accomplish. Entry points.

## Flow Diagram
Mermaid flowchart or numbered step sequence.

## Happy Path
Step-by-step with expected outcomes at each step.

## Decision Points
Branching logic with conditions and outcomes.

## Error States
What happens when things go wrong. Recovery paths.

## Edge Cases
Unusual but valid scenarios and how they're handled.

## Related Flows
Links to adjacent or dependent flows.
```

**Rules**:
- Always include a visual flow diagram (Mermaid preferred)
- Number every step
- Decision points must have explicit conditions ("If X > threshold...")
- Error states must include the user-visible message and recovery action
- Keep to one primary flow per document; split sub-flows into linked docs

---

### Type 3: Usage Instructions (Non-Technical)

**Audience**: End users, business stakeholders, customer support, new team members

**Structure**:
```markdown
# How to <Action> — Usage Guide

## What You'll Learn
One sentence: what the reader will be able to do after reading.

## Before You Start
Prerequisites, required access, accounts, or setup steps.

## Step-by-Step Instructions
1. **Do this first** — Plain language explanation.
   - What you'll see: description of expected result.
2. **Then do this** — ...
   - What you'll see: ...

## Common Questions
**Q: What if I see X?**
A: Do Y.

## Need More Help?
Link to support, contact info, or escalation path.
```

**Rules**:
- Write at a 6th-grade reading level
- Use "you" language ("Click the button" not "The user clicks")
- Every step must describe what the user will see after performing it
- Include screenshots or image references where helpful (using `![alt](path)`)
- No jargon without inline explanation
- Bold the action verb at the start of each step
- Provide a "Common Questions" section for the top 3-5 likely issues
- Use numbered lists for sequential steps, bullets for options

---

### Type 4: README Documentation

**Audience**: Everyone — developers, users, contributors, evaluators

**Structure**:
```markdown
# Project Name

One-line description with key value proposition.

[badges]

## What Is This?
2-3 sentences. Who it's for, what it does, why it exists.

## Quick Start
Minimum steps to get running. Copy-pasteable.

## Features
Bullet list of key capabilities. Link to detailed docs.

## Installation
All supported methods (npm, pip, docker, source).

## Usage
Most common use case with code example.

## Configuration
Key options in a table.

## Contributing
How to contribute. Link to CONTRIBUTING.md if exists.

## License
License type + link.

## Acknowledgments
Credits, inspirations, dependencies.
```

**Rules**:
- The first 5 lines must answer: What is this? Who is it for? Why should I care?
- Quick Start must be copy-pasteable and work on a fresh machine
- Badge links must be valid
- Keep it under 500 lines — link to detailed docs for depth
- Include a table of contents if >100 lines
- Show, don't tell — one code example is worth 10 paragraphs
- Match the project's existing badge style

---

## Workflow

```
Step 1:  DETERMINE documentation type from user request
Step 2:  SCAN the codebase / existing docs for context
Step 3:  IDENTIFY target audience
Step 4:  LOAD taste preferences (tone, style, language)
Step 5:  SELECT the appropriate template from above
Step 6:  RESEARCH the codebase thoroughly — read source files,
         configs, tests, existing docs. Never guess.
Step 7:  DRAFT the documentation following the template
Step 8:  VALIDATE accuracy:
         - Every code example must be runnable
         - Every file path must exist
         - Every config option must be verified in source
         - Every link must resolve
Step 9:  REVIEW readability:
         - Technical docs: can an engineer understand without asking questions?
         - User flows: can QA write test cases from this alone?
         - Usage guides: can a non-technical person follow without help?
         - README: does a first-time visitor understand the project in 30 seconds?
Step 10: WRITE to the appropriate location
Step 11: UPDATE README.md if the new doc should be linked
```

---

## AI Agent Integration

| Aspect | Value |
|---|---|
| **Harness AI Agent** | DevOps Agent (Claude Opus 4.5) for technical docs; Knowledge Graph for cross-referencing |
| **Autonomy Level** | L2 (Assisted) — AI drafts, human reviews for accuracy |
| **Human Gates** | All documentation requires human review before merge |
| **MCP** | Not applicable |

---

## Success Criteria

- [ ] Documentation type matches user request
- [ ] Target audience is explicitly identified
- [ ] Template structure followed
- [ ] All code examples are tested/runnable
- [ ] All file paths and links are verified
- [ ] Reading level matches audience (technical = expert, usage = beginner)
- [ ] Diagrams included where structure or flow is described
- [ ] Document is discoverable (linked from README or docs index)
- [ ] No placeholder text ("TODO", "TBD", "lorem ipsum")
- [ ] Spell-checked and grammar-checked

---

## Examples

### Example: Technical Doc Generation

```
User: "Write technical documentation for the authentication module"

Agent:
1. Scans src/auth/, reads all files
2. Identifies JWT flow, OAuth providers, middleware chain
3. Generates docs/technical/authentication.md with:
   - Architecture diagram (Mermaid)
   - Token lifecycle diagram
   - API endpoint reference table
   - Configuration options table
   - Error code reference
4. Links from README.md
```

### Example: Usage Guide Generation

```
User: "Create a beginner guide for setting up the project"

Agent:
1. Reads README.md, package.json / pyproject.toml, config files
2. Identifies prerequisites (Node.js, Docker, etc.)
3. Generates docs/guides/getting-started.md with:
   - "What You'll Learn" section
   - Prerequisites checklist
   - Step-by-step install with expected outputs
   - "Common Questions" for top issues
4. Links from README.md Quick Start section
```

### Example: README Generation

```
User: "Generate a README for this project"

Agent:
1. Scans entire project structure
2. Reads package.json / pyproject.toml for metadata
3. Identifies key features from source code
4. Generates README.md with:
   - Project name and one-liner
   - Badges (license, version, CI status)
   - Quick Start (copy-pasteable)
   - Features list with doc links
   - Installation methods
   - Usage example
   - Contributing guide
   - License
```

---

*This skill is callable at any phase. It produces documentation artifacts only — no code changes, no configuration, no infrastructure.*
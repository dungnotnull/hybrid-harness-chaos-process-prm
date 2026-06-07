# Critique Command

Invoke the Devil's Advocate (s35) to stress-test any decision, design, or hypothesis.

## Usage

`/critique [subject] [--intensity 1-4]`

## Arguments

- **subject**: The idea, design, hypothesis, or strategy to critique
- **--intensity** (optional): Critique intensity level 1-4 (default: 2)

## Intensity Levels

| Level | Name | Behavior |
|---|---|---|
| 1 | Skeptic | Gentle probing questions |
| 2 | Critic | Direct challenges with evidence |
| 3 | Prosecutor | Systematic deconstruction |
| 4 | Demolisher | Maximum adversarial intensity |

## Behavior

1. Loads s35-devils-advocate skill
2. Extracts claims, assumptions, and logical structure
3. Detects fallacies and generates counter-arguments
4. Scores argument strength on 5 dimensions
5. Produces verdict (PASS/CONDITIONAL/FAIL)
6. Writes critique report to .commandcode/artifacts/critique/

## Examples

- /critique "Our microservice should use event-driven architecture" -- Critic level (default)
- /critique "The chaos hypothesis for pod-delete is valid" --intensity 3 -- Prosecutor level
- /critique "We are ready for production deployment" --intensity 4 -- Demolisher level (pre-deployment gate)

# Orchestrator Command

Start or resume the full workflow from any point.

## Usage

`/orchestrate [phase]`

## Arguments

- **phase** (optional): Phase to start from (e.g., "s04", "chaos", "security"). If omitted, resumes from last checkpoint.

## Behavior

1. Reads .commandcode/progress.json to determine current phase
2. Loads the orchestrator skill (s00)
3. Dispatches to the specified phase or resumes from checkpoint
4. Updates progress after each phase completion

## Examples

- /orchestrate -- Resume from last checkpoint
- /orchestrate s04 -- Start from CI/CD Scaffolding
- /orchestrate chaos -- Start from Chaos Experiment Design
- /orchestrate security -- Start from Security Gate

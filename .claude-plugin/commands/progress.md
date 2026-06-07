# Progress Command

Check workflow progress, view dashboard, or manage phase state.

## Usage

`/progress [subcommand]`

## Subcommands

- **status** (default): Show current workflow progress dashboard
- **next**: Show the next pending phase
- **block**: Add a blocker to the current phase
- **resolve**: Resolve a blocker
- **reset**: Reset workflow to a specific phase
- **report**: Generate full progress report

## Behavior

1. Reads .commandcode/progress.json
2. Renders a colored terminal dashboard showing phase statuses
3. Highlights current phase, blockers, and estimated completion

## Examples

- /progress -- Show current progress dashboard
- /progress next -- Show next pending phase
- /progress block "Waiting for security approval" -- Add a blocker
- /progress resolve BLK-001 -- Resolve a blocker
- /progress reset s04 -- Reset workflow to Phase 2
- /progress report -- Generate full report

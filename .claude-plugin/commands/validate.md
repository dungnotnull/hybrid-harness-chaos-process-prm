# Validate Command

Validate all SKILL.md files for structural correctness.

## Usage

`/validate [--project-root path] [--json] [--quiet]`

## Arguments

- **--project-root**: Path to project root (default: current directory)
- **--json**: Output results as JSON
- **--quiet**: Only show errors, suppress warnings

## Behavior

1. Scans all skills/ directories for SKILL.md files
2. Validates frontmatter, required sections, autonomy levels
3. Checks cross-references between skills
4. Detects duplicate skill numbers and names
5. Reports errors and warnings

## Examples

- /validate -- Validate all skills
- /validate --json -- Output as JSON
- /validate --quiet -- Only show errors

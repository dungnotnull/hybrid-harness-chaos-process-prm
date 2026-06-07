# Changelog

## [0.5.1] - 2026-06-07

### Fixed
- Fixed all 24 SKILL.md validation errors (missing Prerequisites, AI Agent Integration subsections)
- Fixed s01-ba-requirements: restructured flat AI Agent Integration into proper ### subsections
- Fixed s01-1-user-flow-writing: added missing ### Human Gates subsection
- Fixed s33-system-optimization: renamed ### Harness AI Agent Coverage to ### Harness AI Agent
- Fixed s00-orchestrator: removed UTF-8 BOM that prevented frontmatter parsing
- Fixed s33-system-optimization: added **Agent** name for multi-agent Harness AI Agent
- Fixed validator code: changed SkillMeta.number from int to float for sub-skill support (s01-1)
- Fixed generate_docs.py: added fmt_skill_num() helper for proper sub-skill number formatting
- Fixed cross-reference validator: added sub-skill ID support (s01-1)
- Fixed pyproject.toml: corrected TOML format (doubled quotes), removed BOM
- Fixed test_validate_skills.py: corrected corrupted triple-quoted strings
- Fixed test_progress_tracker.py: updated from 36 to 37 skills
- Updated TOTAL_SKILLS from 36 to 37
- Removed redundant Phase 1 (Planning & Requirements) from README (s01 already in Phase 0)
- Regenerated SKILLS-CATALOG.md with all 37 skills

### Changed
- Updated all references from 36 skills to 37 skills across README.md, CLAUDE.md, pyproject.toml, constants.py
- Updated SKILLS-CATALOG.md with correct s01-1 display and all agent mappings

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-06-07

### Added
- **s35-devils-advocate**: New adversarial critique skill adapted from the Devil's Advocate Agent (dungnotnull/devils-advocate-agent). Provides structured Socratic questioning, logical fallacy detection, argument strength scoring, and multi-perspective challenge generation at 4 intensity levels (Skeptic, Critic, Prosecutor, Demolisher). Callable at ANY phase as a quality gate.
- **Claude Plugin Manifest** (.claude-plugin/plugin.json): Makes the project consumable as a first-class Claude Code and Cowork plugin with slash commands (/orchestrate, /critique, /progress, /validate).
- **Plugin Commands**: Four slash commands for workflow orchestration, critique, progress checking, and validation.
- **GitHub Actions CI** (.github/workflows/ci.yml): Automated skill validation, Python linting, YAML linting, Markdown linting, and test execution on push/PR.
- **GitHub Actions Release** (.github/workflows/release.yml): Automated release creation on version tags with release notes from CHANGELOG.md.
- **Pre-commit Configuration** (.pre-commit-config.yaml): Validates skills, fixes trailing whitespace, checks YAML/JSON, prevents direct commits to main, runs ruff.
- **Pre-commit Validation Script** (scripts/pre-commit-validate.py): Standalone script for validating skills before commits.
- **GitHub Issue Templates**: Bug report, feature request, and skill proposal templates.
- **PR Template**: Structured pull request template with skill quality checklist.
- **Progress Tracker CLI** (	ools/progress_tracker.py): Full CLI tool for managing workflow state — init, status, transition, block, resolve, report, and next commands.
- **Tests Directory** (	ests/): Unit tests for skill validation, frontmatter parsing, cross-references, and progress tracking.

### Changed
- Updated 	ools/shared/constants.py to include s01-1 and s35 skill mappings and phase assignments.
- Updated SKILLS-CATALOG.md to reflect 36 skills (s00-s35 including s01-1).
- Updated README.md and CLAUDE.md with s35, plugin integration, CI, and development workflow documentation.
- Updated skill count from 35 to 36 across all documentation.

### Development Phase Tracking
This project now tracks development phases using GitHub Projects + Issue Labels + CI gates:
- Phase tracking issues use the label dev-phase
- CI validates all skills on every PR
- Pre-commit hooks enforce quality at commit time
- Progress tracker CLI provides local state management

## [0.4.0] - 2026-05-28

### Added
- **s34-documentation-writing**: Technical documentation, user flow diagrams, usage guides, and README generation skill.
- **s33-system-optimization**: 7-module deep-dive audit skill (latency, N+1, stress, atomicity, concurrency, security, agent-proposed).
- **s32-deep-research**: Multi-source research engine with evidence synthesis.
- **s31-strategic-creator**: Advisory-only brainstorming with trade-off analysis.
- Deep research report (34 sources) informing the project architecture.
- MCP server for LitmusChaos and Harness Chaos operations.
- Skill scaffolding tool (	ools/scaffold_skill.py).
- Documentation generation tool (	ools/generate_docs.py).
- Skill validation tool (	ools/validate_skills.py).

### Changed
- Expanded from 34 to 35 skills.
- Updated AI Agent Mapping with Harness AI specialized agents.
- Added MCP integration matrix for chaos skills.

## [0.3.0] - 2026-05-20

### Added
- Skills s01 through s30 covering the complete SDLC workflow.
- Progress tracker (s03) with state machine.
- Taste memory (s02) for developer preferences.
- Orchestrator (s00) for workflow coordination.

## [0.1.0] - 2026-05-15

### Added
- Initial project structure.
- Foundation skills (s00-s03).
- CI/CD skills (s04-s10).
- MIT License.

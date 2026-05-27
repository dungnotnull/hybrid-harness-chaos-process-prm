"""Skill Validator -- validates all SKILL.md files for structural correctness."""
import json
import os
import sys

# Ensure project root is on sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click

from tools.shared.constants import (
    REQUIRED_SECTIONS,
    REQUIRED_AGENT_SUBSECTIONS,
    VALID_AUTONOMY_LEVELS,
)
from tools.shared.models import ValidationError, ValidationResult, SkillMeta
from tools.shared.skill_discovery import load_all_skills
from tools.shared.crossrefs import validate_cross_references


def check_frontmatter(skill: SkillMeta) -> list[ValidationError]:
    """Validate frontmatter has required fields."""
    errors = []
    if not skill.frontmatter.name:
        errors.append(ValidationError(
            file_path=skill.file_path,
            skill_number=skill.number,
            skill_name=skill.dir_name,
            severity="error",
            category="frontmatter",
            message="Missing or empty 'name' field in frontmatter",
        ))
    if not skill.frontmatter.description:
        errors.append(ValidationError(
            file_path=skill.file_path,
            skill_number=skill.number,
            skill_name=skill.dir_name,
            severity="error",
            category="frontmatter",
            message="Missing or empty 'description' field in frontmatter",
        ))
    return errors


def check_required_sections(skill: SkillMeta) -> list[ValidationError]:
    """Validate all required ## sections are present."""
    errors = []
    for section in REQUIRED_SECTIONS:
        if section not in skill.sections:
            errors.append(ValidationError(
                file_path=skill.file_path,
                skill_number=skill.number,
                skill_name=skill.frontmatter.name,
                severity="error",
                category="section",
                message=f"Missing required section: '## {section}'",
            ))
    return errors


def check_agent_integration(skill: SkillMeta) -> list[ValidationError]:
    """Validate AI Agent Integration subsections and autonomy levels."""
    errors = []
    agent = skill.agent_integration

    # Check subsections via the AI Agent Integration section content
    from tools.shared.sections import extract_subsections
    ai_section = skill.sections.get("AI Agent Integration", "")
    if not ai_section:
        return errors

    subsections = extract_subsections(ai_section)
    for sub in REQUIRED_AGENT_SUBSECTIONS:
        if sub not in subsections:
            errors.append(ValidationError(
                file_path=skill.file_path,
                skill_number=skill.number,
                skill_name=skill.frontmatter.name,
                severity="error",
                category="section",
                message=f"Missing required AI Agent Integration subsection: '### {sub}'",
            ))

    # Check autonomy levels
    if agent.autonomy_level:
        if agent.autonomy_level.current not in VALID_AUTONOMY_LEVELS:
            errors.append(ValidationError(
                file_path=skill.file_path,
                skill_number=skill.number,
                skill_name=skill.frontmatter.name,
                severity="error",
                category="autonomy",
                message=f"Invalid current autonomy level: '{agent.autonomy_level.current}' (must be one of {sorted(VALID_AUTONOMY_LEVELS)})",
            ))
        if agent.autonomy_level.target not in VALID_AUTONOMY_LEVELS:
            errors.append(ValidationError(
                file_path=skill.file_path,
                skill_number=skill.number,
                skill_name=skill.frontmatter.name,
                severity="error",
                category="autonomy",
                message=f"Invalid target autonomy level: '{agent.autonomy_level.target}' (must be one of {sorted(VALID_AUTONOMY_LEVELS)})",
            ))
    else:
        errors.append(ValidationError(
            file_path=skill.file_path,
            skill_number=skill.number,
            skill_name=skill.frontmatter.name,
            severity="error",
            category="autonomy",
            message="Could not parse autonomy levels from Autonomy Level table",
        ))

    # Check agent name is set
    if not agent.harness_ai_agent:
        errors.append(ValidationError(
            file_path=skill.file_path,
            skill_number=skill.number,
            skill_name=skill.frontmatter.name,
            severity="warning",
            category="section",
            message="No Harness AI Agent name found in AI Agent Integration section",
        ))

    return errors


def check_duplicates(skills: list[SkillMeta]) -> list[ValidationError]:
    """Check for duplicate skill numbers and names."""
    errors = []
    seen_numbers = {}
    seen_names = {}

    for skill in skills:
        if skill.number in seen_numbers:
            errors.append(ValidationError(
                file_path=skill.file_path,
                skill_number=skill.number,
                skill_name=skill.frontmatter.name,
                severity="error",
                category="formatting",
                message=f"Duplicate skill number {skill.number} (also in {seen_numbers[skill.number]})",
            ))
        else:
            seen_numbers[skill.number] = skill.dir_name

        name = skill.frontmatter.name.lower()
        if name in seen_names and name:
            errors.append(ValidationError(
                file_path=skill.file_path,
                skill_number=skill.number,
                skill_name=skill.frontmatter.name,
                severity="warning",
                category="formatting",
                message=f"Duplicate skill name '{skill.frontmatter.name}' (also in {seen_names[name]})",
            ))
        elif name:
            seen_names[name] = skill.dir_name

    return errors


def validate_all_skills(project_root: str) -> ValidationResult:
    """Main validation entry point. Runs all checks."""
    skills = load_all_skills(project_root)

    all_errors = []
    for skill in skills:
        all_errors.extend(check_frontmatter(skill))
        all_errors.extend(check_required_sections(skill))
        all_errors.extend(check_agent_integration(skill))

    all_errors.extend(check_duplicates(skills))
    all_errors.extend(validate_cross_references(skills))

    failed_skills = set()
    warning_count = 0
    for err in all_errors:
        if err.severity == "error":
            failed_skills.add(err.skill_number)
        else:
            warning_count += 1

    return ValidationResult(
        total_skills=len(skills),
        passed=len(skills) - len(failed_skills),
        failed=len(failed_skills),
        warnings=warning_count,
        errors=all_errors,
    )


def format_results(result: ValidationResult, use_json: bool = False, quiet: bool = False) -> str:
    """Format validation results for output."""
    if use_json:
        data = {
            "total_skills": result.total_skills,
            "passed": result.passed,
            "failed": result.failed,
            "warnings": result.warnings,
            "errors": [
                {
                    "skill": f"s{e.skill_number:02d}",
                    "name": e.skill_name,
                    "severity": e.severity,
                    "category": e.category,
                    "message": e.message,
                }
                for e in result.errors
            ],
        }
        return json.dumps(data, indent=2)

    lines = []
    # Group errors by skill
    by_skill = {}
    for err in result.errors:
        key = f"s{err.skill_number:02d}"
        if key not in by_skill:
            by_skill[key] = []
        by_skill[key].append(err)

    for skill_key in sorted(by_skill.keys()):
        skill_errors = by_skill[skill_key]
        has_error = any(e.severity == "error" for e in skill_errors)
        symbol = "FAIL" if has_error else "WARN"
        lines.append(f"\n[{symbol}] {skill_key}: {skill_errors[0].skill_name}")
        for err in skill_errors:
            if quiet and err.severity != "error":
                continue
            prefix = "  ERROR" if err.severity == "error" else "  WARN"
            lines.append(f"  {prefix}: [{err.category}] {err.message}")

    # Summary
    status = "PASS" if result.failed == 0 else "FAIL"
    lines.append(f"\n{'=' * 60}")
    lines.append(f"Result: {status}")
    lines.append(f"Skills checked: {result.total_skills}")
    lines.append(f"Passed: {result.passed} | Failed: {result.failed} | Warnings: {result.warnings}")
    lines.append(f"{'=' * 60}")

    return "\n".join(lines)


@click.command()
@click.option("--project-root", default=".", help="Path to project root")
@click.option("--json", "use_json", is_flag=True, help="Output as JSON")
@click.option("--quiet", is_flag=True, help="Only show errors, suppress warnings")
def main(project_root: str, use_json: bool, quiet: bool):
    """Validate all SKILL.md files for structural correctness."""
    try:
        result = validate_all_skills(project_root)
    except FileNotFoundError as e:
        click.echo(f"ERROR: {e}", err=True)
        sys.exit(2)

    output = format_results(result, use_json, quiet)
    click.echo(output)

    if result.failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()

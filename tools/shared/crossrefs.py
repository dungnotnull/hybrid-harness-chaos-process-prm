from tools.shared.models import SkillMeta, ValidationError


def build_cross_reference_map(skills: list[SkillMeta]) -> dict[str, list[str]]:
    """Build a map of skill -> list of skills it references."""
    return {f"s{skill.number:02d}": skill.cross_refs_in for skill in skills}


def validate_cross_references(skills: list[SkillMeta]) -> list[ValidationError]:
    """Check that all cross-references point to existing skills."""
    existing = {f"s{skill.number:02d}" for skill in skills}
    errors = []

    for skill in skills:
        for ref in skill.cross_refs_in:
            if ref not in existing:
                errors.append(ValidationError(
                    file_path=skill.file_path,
                    skill_number=skill.number,
                    skill_name=skill.frontmatter.name,
                    severity="warning",
                    category="crossref",
                    message=f"References non-existent skill '{ref}' in Input Contract",
                ))

    return errors

"""Tests for the skill validator."""
import os
import sys
import tempfile

import pytest

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.shared.frontmatter import parse_frontmatter, validate_frontmatter
from tools.shared.sections import extract_sections, extract_subsections, extract_autonomy_levels
from tools.shared.crossrefs import validate_cross_references
from tools.shared.models import SkillMeta, SkillFrontmatter, AgentIntegration, AutonomyLevel
from tools.validate_skills import (
    check_frontmatter,
    check_required_sections,
    check_agent_integration,
    check_duplicates,
)


class TestFrontmatter:
    """Test YAML frontmatter parsing and validation."""

    def test_parse_valid_frontmatter(self):
        content = """---
name: test-skill
description: A test skill
---
# Test Skill
"""
        fm_data, body = parse_frontmatter(content)
        assert fm_data["name"] == "test-skill"
        assert fm_data["description"] == "A test skill"
        assert "# Test Skill" in body

    def test_parse_frontmatter_missing_closing(self):
        content = """---
name: test-skill
description: A test skill
"""
        with pytest.raises(ValueError):
            parse_frontmatter(content)

    def test_validate_frontmatter_missing_name(self):
        data = {"description": "A test skill"}
        errors = validate_frontmatter(data)
        assert len(errors) == 1
        assert "name" in errors[0]

    def test_validate_frontmatter_empty_name(self):
        data = {"name": "", "description": "A test skill"}
        errors = validate_frontmatter(data)
        assert len(errors) >= 1

    def test_validate_frontmatter_valid(self):
        data = {"name": "test-skill", "description": "A test skill"}
        errors = validate_frontmatter(data)
        assert len(errors) == 0


class TestSections:
    """Test section extraction."""

    def test_extract_sections(self):
        body = """## Purpose
Some purpose text.

## Input Contract
Some input text.

## Success Criteria
Some criteria text.
"""
        sections = extract_sections(body)
        assert "Purpose" in sections
        assert "Input Contract" in sections
        assert "Success Criteria" in sections
        assert "Some purpose text." in sections["Purpose"]

    def test_extract_subsections(self):
        content = """### Autonomy Level
Some autonomy text.

### Harness AI Agent
Some agent text.

### Human Gates
Some gates text.
"""
        subsections = extract_subsections(content)
        assert "Autonomy Level" in subsections
        assert "Harness AI Agent" in subsections
        assert "Human Gates" in subsections

    def test_extract_autonomy_levels(self):
        content = """| Aspect | Level | Description |
|---|---|---|
| Current | L1 | AI suggests, human decides |
| Target | L3 | AI executes, human reviews |
"""
        autonomy = extract_autonomy_levels(content)
        assert autonomy is not None
        assert autonomy.current == "L1"
        assert autonomy.target == "L3"


class TestCrossReferences:
    """Test cross-reference validation."""

    def test_valid_crossrefs(self):
        skills = [
            SkillMeta(
                number=0,
                dir_name="s00-orchestrator",
                file_path="skills/s00-orchestrator/SKILL.md",
                frontmatter=SkillFrontmatter(name="orchestrator", description="test"),
                sections={},
                agent_integration=AgentIntegration(),
                phase=0,
                phase_name="Foundation",
                cross_refs_in=[],
            ),
            SkillMeta(
                number=1,
                dir_name="s01-ba-requirements",
                file_path="skills/s01-ba-requirements/SKILL.md",
                frontmatter=SkillFrontmatter(name="ba-requirements", description="test"),
                sections={},
                agent_integration=AgentIntegration(),
                phase=0,
                phase_name="Foundation",
                cross_refs_in=["s00"],
            ),
            SkillMeta(
                number=4,
                dir_name="s04-pipeline-design",
                file_path="skills/s04-pipeline-design/SKILL.md",
                frontmatter=SkillFrontmatter(name="pipeline-design", description="test"),
                sections={},
                agent_integration=AgentIntegration(),
                phase=2,
                phase_name="CI/CD Scaffolding",
                cross_refs_in=["s01"],
            ),
        ]
        errors = validate_cross_references(skills)
        assert len(errors) == 0

    def test_invalid_crossrefs(self):
        skills = [
            SkillMeta(
                number=1,
                dir_name="s01-ba-requirements",
                file_path="skills/s01-ba-requirements/SKILL.md",
                frontmatter=SkillFrontmatter(name="ba-requirements", description="test"),
                sections={},
                agent_integration=AgentIntegration(),
                phase=0,
                phase_name="Foundation",
                cross_refs_in=["s99"],
            ),
        ]
        errors = validate_cross_references(skills)
        assert len(errors) == 1
        assert errors[0].category == "crossref"


class TestCheckFunctions:
    """Test the main check functions."""

    def test_check_frontmatter_valid(self):
        skill = SkillMeta(
            number=1,
            dir_name="s01-ba-requirements",
            file_path="skills/s01-ba-requirements/SKILL.md",
            frontmatter=SkillFrontmatter(name="ba-requirements", description="BA analysis skill"),
            sections={},
            agent_integration=AgentIntegration(),
            phase=0,
            phase_name="Foundation",
        )
        errors = check_frontmatter(skill)
        assert len(errors) == 0

    def test_check_frontmatter_missing_name(self):
        skill = SkillMeta(
            number=1,
            dir_name="s01-ba-requirements",
            file_path="skills/s01-ba-requirements/SKILL.md",
            frontmatter=SkillFrontmatter(name="", description="BA analysis skill"),
            sections={},
            agent_integration=AgentIntegration(),
            phase=0,
            phase_name="Foundation",
        )
        errors = check_frontmatter(skill)
        assert len(errors) >= 1

    def test_check_required_sections(self):
        skill = SkillMeta(
            number=1,
            dir_name="s01-ba-requirements",
            file_path="skills/s01-ba-requirements/SKILL.md",
            frontmatter=SkillFrontmatter(name="test", description="test"),
            sections={"Purpose": "text", "Input Contract": "text", "Output Contract": "text",
                      "Prerequisites": "text", "AI Agent Integration": "text", "Success Criteria": "text"},
            agent_integration=AgentIntegration(),
            phase=0,
            phase_name="Foundation",
        )
        errors = check_required_sections(skill)
        assert len(errors) == 0

    def test_check_duplicates(self):
        skills = [
            SkillMeta(
                number=1, dir_name="s01-test", file_path="",
                frontmatter=SkillFrontmatter(name="test", description=""),
                sections={}, agent_integration=AgentIntegration(),
                phase=0, phase_name="Foundation",
            ),
            SkillMeta(
                number=2, dir_name="s02-another", file_path="",
                frontmatter=SkillFrontmatter(name="another", description=""),
                sections={}, agent_integration=AgentIntegration(),
                phase=0, phase_name="Foundation",
            ),
        ]
        errors = check_duplicates(skills)
        assert len(errors) == 0

    def test_check_duplicates_conflict(self):
        skills = [
            SkillMeta(
                number=1, dir_name="s01-test", file_path="",
                frontmatter=SkillFrontmatter(name="test", description=""),
                sections={}, agent_integration=AgentIntegration(),
                phase=0, phase_name="Foundation",
            ),
            SkillMeta(
                number=1, dir_name="s01-test-dup", file_path="",
                frontmatter=SkillFrontmatter(name="test-dup", description=""),
                sections={}, agent_integration=AgentIntegration(),
                phase=0, phase_name="Foundation",
            ),
        ]
        errors = check_duplicates(skills)
        error_categories = [e.category for e in errors]
        assert "formatting" in error_categories
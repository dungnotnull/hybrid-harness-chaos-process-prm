import os
import re
from typing import Optional

from tools.shared.constants import SKILLS_DIR, SKILL_FILE, SKILL_PHASE_MAP, PHASE_MAP
from tools.shared.frontmatter import parse_frontmatter, validate_frontmatter
from tools.shared.sections import (
    extract_sections,
    extract_subsections,
    extract_autonomy_levels,
    extract_agent_name,
    extract_capabilities,
    extract_human_gates,
    extract_cross_references,
    extract_mcp_platforms,
)
from tools.shared.models import SkillMeta, SkillFrontmatter, AgentIntegration


def discover_skills(skills_dir: str) -> list[tuple[int, str, str]]:
    """Scan skills/ directory for all skill folders matching sNN-* pattern.
    Returns list of (skill_number, dir_name, skill_md_path).
    """
    skills = []
    if not os.path.isdir(skills_dir):
        raise FileNotFoundError(f"Skills directory not found: {skills_dir}")

    for entry in sorted(os.listdir(skills_dir)):
        entry_path = os.path.join(skills_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        skill_num = parse_skill_number(entry)
        if skill_num is not None:
            skill_md = os.path.join(entry_path, SKILL_FILE)
            if os.path.isfile(skill_md):
                skills.append((skill_num, entry, skill_md))

    return skills


def parse_skill_number(dir_name: str) -> Optional[int]:
    """Extract skill number from directory name like 's14-experiment-design'."""
    match = re.match(r'^s(\d+)-', dir_name)
    if match:
        return int(match.group(1))
    return None


def parse_skill(file_path: str, skill_number: int, dir_name: str) -> Optional[SkillMeta]:
    """Parse a single SKILL.md file into a SkillMeta object."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return None

    try:
        fm_data, body = parse_frontmatter(content)
    except ValueError:
        return None

    frontmatter_errors = validate_frontmatter(fm_data)
    if frontmatter_errors:
        fm_data.setdefault("name", dir_name)
        fm_data.setdefault("description", "")

    sections = extract_sections(body)

    agent_integration = AgentIntegration()
    ai_section = sections.get("AI Agent Integration", "")
    if ai_section:
        subsections = extract_subsections(ai_section)
        autonomy_content = subsections.get("Autonomy Level", "")
        agent_content = subsections.get("Harness AI Agent", "")
        gates_content = subsections.get("Human Gates", "")

        agent_integration.autonomy_level = extract_autonomy_levels(autonomy_content)
        agent_integration.harness_ai_agent = extract_agent_name(agent_content)
        agent_integration.capabilities = extract_capabilities(agent_content)
        agent_integration.human_gates = extract_human_gates(gates_content)

        # Check for MCP/Fallback/Notes subsections
        for key in ["MCP", "MCP Integration", "Fallback", "Notes"]:
            if key in subsections:
                content_sub = subsections[key]
                if "MCP" in key:
                    agent_integration.mcp_platforms = extract_mcp_platforms(content_sub)
                elif key == "Fallback":
                    agent_integration.fallback = content_sub[:200]
                elif key == "Notes":
                    agent_integration.notes = content_sub[:200]

    phase = SKILL_PHASE_MAP.get(skill_number, -1)
    phase_name = PHASE_MAP.get(phase, "Any") if phase >= 0 else "Any"

    input_contract = sections.get("Input Contract", "")
    cross_refs = extract_cross_references(input_contract)

    return SkillMeta(
        number=skill_number,
        dir_name=dir_name,
        file_path=file_path,
        frontmatter=SkillFrontmatter(
            name=fm_data.get("name", ""),
            description=fm_data.get("description", ""),
        ),
        sections=sections,
        agent_integration=agent_integration,
        phase=phase,
        phase_name=phase_name,
        cross_refs_in=cross_refs,
    )


def load_all_skills(project_root: str) -> list[SkillMeta]:
    """Discover and parse all skills. Returns fully populated SkillMeta objects."""
    skills_dir = os.path.join(project_root, SKILLS_DIR)
    raw_skills = discover_skills(skills_dir)

    skills = []
    for skill_num, dir_name, file_path in raw_skills:
        skill = parse_skill(file_path, skill_num, dir_name)
        if skill:
            skills.append(skill)

    # Build cross_refs_out by inverting cross_refs_in
    skill_map = {f"s{s.number:02d}": s for s in skills}
    for skill in skills:
        for ref in skill.cross_refs_in:
            if ref in skill_map:
                referenced = skill_map[ref]
                if skill.dir_name not in referenced.cross_refs_out:
                    referenced.cross_refs_out.append(skill.dir_name)

    return sorted(skills, key=lambda s: s.number)

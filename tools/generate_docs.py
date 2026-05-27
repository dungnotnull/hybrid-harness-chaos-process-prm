"""Doc Generator -- auto-generates documentation from SKILL.md metadata."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click

from tools.shared.models import SkillMeta
from tools.shared.skill_discovery import load_all_skills
from tools.shared.constants import HARNESS_AGENTS


def generate_skill_table(skills: list[SkillMeta]) -> str:
    """Generate the markdown skill catalog table."""
    lines = [
        "| # | Name | Phase | Autonomy (Current/Target) | AI Agent |",
        "|---|---|---|---|---|",
    ]
    for skill in skills:
        agent = skill.agent_integration
        autonomy = "N/A"
        if agent.autonomy_level:
            autonomy = f"{agent.autonomy_level.current}/{agent.autonomy_level.target}"
        ai_agent = agent.harness_ai_agent or "None"
        lines.append(f"| s{skill.number:02d} | {skill.frontmatter.name} | {skill.phase_name} | {autonomy} | {ai_agent} |")
    return "\n".join(lines)


def generate_agent_coverage_matrix(skills: list[SkillMeta]) -> str:
    """Generate the AI Agent coverage matrix."""
    agent_skills = {}
    for skill in skills:
        agent = skill.agent_integration.harness_ai_agent or "None"
        if agent not in agent_skills:
            agent_skills[agent] = []
        autonomy = "N/A"
        if skill.agent_integration.autonomy_level:
            autonomy = f"{skill.agent_integration.autonomy_level.current}/{skill.agent_integration.autonomy_level.target}"
        agent_skills[agent].append(f"s{skill.number:02d} ({autonomy})")

    lines = ["| AI Agent | Skills Covered |", "|---|---|"]
    for agent in sorted(agent_skills.keys()):
        skill_list = ", ".join(agent_skills[agent])
        lines.append(f"| {agent} | {skill_list} |")
    return "\n".join(lines)


def generate_mcp_matrix(skills: list[SkillMeta]) -> str:
    """Generate the MCP integration matrix."""
    # Collect MCP platforms from skills
    platform_skills = {}
    for skill in skills:
        for platform in skill.agent_integration.mcp_platforms:
            if platform not in platform_skills:
                platform_skills[platform] = []
            platform_skills[platform].append(f"s{skill.number:02d}")

    if not platform_skills:
        return "No MCP integrations found."

    lines = ["| MCP Platform | Skills |", "|---|---|"]
    for platform in sorted(platform_skills.keys()):
        skill_list = ", ".join(platform_skills[platform])
        lines.append(f"| {platform} | {skill_list} |")
    return "\n".join(lines)


def generate_autonomy_distribution(skills: list[SkillMeta]) -> str:
    """Generate autonomy level distribution summary."""
    current_counts = {}
    target_counts = {}
    for skill in skills:
        if skill.agent_integration.autonomy_level:
            c = skill.agent_integration.autonomy_level.current
            t = skill.agent_integration.autonomy_level.target
            current_counts[c] = current_counts.get(c, 0) + 1
            target_counts[t] = target_counts.get(t, 0) + 1

    lines = [
        "### Current Levels",
        "| Level | Count | Skills |",
        "|---|---|---|",
    ]
    current_skills = {}
    for skill in skills:
        if skill.agent_integration.autonomy_level:
            c = skill.agent_integration.autonomy_level.current
            if c not in current_skills:
                current_skills[c] = []
            current_skills[c].append(f"s{skill.number:02d}")

    for level in ["L0", "L1", "L2", "L3", "L4"]:
        count = current_counts.get(level, 0)
        if count > 0:
            skill_list = ", ".join(current_skills.get(level, []))
            lines.append(f"| {level} | {count} | {skill_list} |")

    lines.extend([
        "",
        "### Target Levels",
        "| Level | Count | Skills |",
        "|---|---|---|",
    ])
    target_skills = {}
    for skill in skills:
        if skill.agent_integration.autonomy_level:
            t = skill.agent_integration.autonomy_level.target
            if t not in target_skills:
                target_skills[t] = []
            target_skills[t].append(f"s{skill.number:02d}")

    for level in ["L0", "L1", "L2", "L3", "L4"]:
        count = target_counts.get(level, 0)
        if count > 0:
            skill_list = ", ".join(target_skills.get(level, []))
            lines.append(f"| {level} | {count} | {skill_list} |")

    return "\n".join(lines)


def generate_cross_reference_map(skills: list[SkillMeta]) -> str:
    """Generate cross-reference map showing skill dependencies."""
    lines = ["| Skill | References (Input From) | Referenced By (Output To) |", "|---|---|---|"]
    for skill in skills:
        refs_in = ", ".join(skill.cross_refs_in) if skill.cross_refs_in else "None"
        refs_out = ", ".join(skill.cross_refs_out) if skill.cross_refs_out else "None"
        lines.append(f"| s{skill.number:02d} {skill.frontmatter.name} | {refs_in} | {refs_out} |")
    return "\n".join(lines)


def generate_catalog(skills: list[SkillMeta]) -> str:
    """Generate the full SKILLS-CATALOG.md content."""
    lines = [
        "# Skills Catalog",
        "",
        f"**Generated from**: 33 SKILL.md files",
        f"**Total skills**: {len(skills)}",
        "",
        "---",
        "",
        "## Skill Catalog",
        "",
        generate_skill_table(skills),
        "",
        "---",
        "",
        "## AI Agent Coverage Matrix",
        "",
        generate_agent_coverage_matrix(skills),
        "",
        "---",
        "",
        "## MCP Integration Matrix",
        "",
        generate_mcp_matrix(skills),
        "",
        "---",
        "",
        "## Autonomy Level Distribution",
        "",
        generate_autonomy_distribution(skills),
        "",
        "---",
        "",
        "## Cross-Reference Map",
        "",
        generate_cross_reference_map(skills),
        "",
    ]
    return "\n".join(lines)


@click.command()
@click.option("--project-root", default=".", help="Path to project root")
@click.option("--output-dir", default=None, help="Where to write SKILLS-CATALOG.md")
@click.option("--update-readme", is_flag=True, help="Update README.md with skill metadata")
@click.option("--no-catalog", is_flag=True, help="Skip generating SKILLS-CATALOG.md")
def main(project_root: str, output_dir: str, update_readme: bool, no_catalog: bool):
    """Generate documentation from SKILL.md metadata."""
    skills = load_all_skills(project_root)
    click.echo(f"Loaded {len(skills)} skills")

    if not no_catalog:
        out_dir = output_dir or os.path.join(project_root, "skills")
        catalog_path = os.path.join(out_dir, "SKILLS-CATALOG.md")
        catalog_content = generate_catalog(skills)

        os.makedirs(out_dir, exist_ok=True)
        with open(catalog_path, "w", encoding="utf-8") as f:
            f.write(catalog_content)
        click.echo(f"Generated: {catalog_path}")

    if update_readme:
        readme_path = os.path.join(project_root, "README.md")
        if os.path.isfile(readme_path):
            click.echo(f"README update: feature not yet implemented (use --update-readme in next version)")
        else:
            click.echo(f"WARNING: README.md not found at {readme_path}", err=True)


if __name__ == "__main__":
    main()

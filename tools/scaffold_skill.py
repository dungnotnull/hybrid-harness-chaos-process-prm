"""Skill Scaffolder -- creates new skills with correct structure."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click

from tools.shared.constants import SKILLS_DIR, SKILL_FILE, SKILL_PHASE_MAP, PHASE_MAP


def get_default_agent_for_skill(number: int, phase: int) -> tuple[str, str, str]:
    """Return (agent_name, default_current_level, default_target_level) for a skill."""
    from tools.shared.constants import PHASE_AGENT_DEFAULTS

    phase_defaults = PHASE_AGENT_DEFAULTS.get(phase, "None (advisory by design)")
    if isinstance(phase_defaults, dict):
        key = f"s{number:02d}"
        agent = phase_defaults.get(key, phase_defaults.get(f"s{number}", "None (advisory by design)"))
    else:
        agent = phase_defaults

    # Advisory/research skills stay at L1
    if "advisory" in agent.lower() or "research" in agent.lower() or "None (internal)" in agent:
        return agent, "L1", "L1"

    # Security and safety-critical skills start at L1
    if phase in (3,) or number in (16, 29):
        return agent, "L1", "L2"

    # Most skills start at L1 or L2 depending on Harness AI availability
    if phase in (0,) and number > 0:
        return agent, "L1", "L2"
    if agent.startswith("None"):
        return agent, "L1", "L2"

    return agent, "L2", "L3"


def validate_new_skill(project_root: str, number: int, name: str) -> list[str]:
    """Check for conflicts. Returns list of error strings (empty = valid)."""
    errors = []
    skills_dir = os.path.join(project_root, SKILLS_DIR)

    if not os.path.isdir(skills_dir):
        errors.append(f"Skills directory not found: {skills_dir}")
        return errors

    dir_name = f"s{number:02d}-{name}"
    target_dir = os.path.join(skills_dir, dir_name)
    if os.path.exists(target_dir):
        errors.append(f"Skill directory already exists: {target_dir}")

    # Check for number conflicts
    for entry in os.listdir(skills_dir):
        entry_path = os.path.join(skills_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        import re
        match = re.match(r'^s(\d+)-', entry)
        if match and int(match.group(1)) == number:
            errors.append(f"Skill number {number} already used by: {entry}")

    return errors


def generate_skill_content(
    number: int,
    name: str,
    description: str,
    phase: int,
    template_content: str = "",
) -> str:
    """Generate the full SKILL.md content string."""
    title = name.replace("-", " ").title()
    agent, current_level, target_level = get_default_agent_for_skill(number, phase)
    phase_name = PHASE_MAP.get(phase, "Any") if phase >= 0 else "Any"

    if template_content:
        # If a template was provided, use it as the base and update the frontmatter
        # This is a simple approach -- the user can customize further
        return template_content

    mcp_section = ""
    if phase in (5, 6):  # Chaos Design, Game Day
        mcp_section = """\n### MCP Integration\n\n{platform_specific MCP configuration}"""

    fallback_section = ""
    if phase in (2, 3, 4):  # CI/CD, Security, Testing
        fallback_section = """\n\n### Fallback\n\nWhen Harness AI is unavailable: Use manual configuration following the relevant documentation."""

    return f"""---
name: {name}
description: >
  {description}
---

# {title} (s{number:02d})

## Purpose
[TODO: Describe what this skill does and when to use it]

---

## Input Contract

| Input | Source | Required |
|---|---|---|
| [TODO] | [TODO] | Yes |

---

## Output Contract

| Output | Destination | Format |
|---|---|---|
| [TODO] | [TODO] | [TODO] |

---

## Prerequisites
- [ ] [TODO: List prerequisites]

---

## [TODO: Domain-specific workflow sections]

---

## AI Agent Integration

### Autonomy Level

| Aspect | Level | Description |
|---|---|---|
| Current | {current_level} | [TODO: Describe current AI capability] |
| Target | {target_level} | [TODO: Describe target AI capability] |

### Harness AI Agent

**Agent**: {agent}
**Capabilities**:
- [TODO: List AI capabilities]

### Human Gates

- [TODO: List approval gates]
{mcp_section}{fallback_section}

---

## Success Criteria
- [ ] [TODO: Define measurable success criteria]
"""


def scaffold_skill(
    project_root: str,
    number: int,
    name: str,
    description: str,
    phase: int,
    template: int | None = None,
) -> str:
    """Create a new skill directory and SKILL.md. Returns the path created."""
    dir_name = f"s{number:02d}-{name}"
    skills_dir = os.path.join(project_root, SKILLS_DIR)
    target_dir = os.path.join(skills_dir, dir_name)
    skill_path = os.path.join(target_dir, SKILL_FILE)

    os.makedirs(target_dir, exist_ok=True)

    template_content = ""
    if template is not None:
        template_dir = os.path.join(skills_dir, f"s{template:02d}-*")
        import glob
        matches = glob.glob(template_dir)
        if matches:
            template_skill = os.path.join(matches[0], SKILL_FILE)
            if os.path.isfile(template_skill):
                with open(template_skill, "r", encoding="utf-8") as f:
                    template_content = f.read()

    content = generate_skill_content(number, name, description, phase, template_content)

    with open(skill_path, "w", encoding="utf-8") as f:
        f.write(content)

    return skill_path


def prompt_interactive() -> dict:
    """Interactive prompts for skill metadata."""
    number = int(click.prompt("Skill number", type=int))
    name = click.prompt("Skill name (kebab-case)")
    description = click.prompt("Description")
    phase = click.prompt("Phase number (0-9, or -1 for 'any')", type=int, default=-1)

    if phase == -1:
        phase = SKILL_PHASE_MAP.get(number, -1)

    return {
        "number": number,
        "name": name,
        "description": description,
        "phase": phase,
    }


@click.command()
@click.option("--number", type=int, help="Skill number (e.g., 33)")
@click.option("--name", help="Skill name in kebab-case (e.g., 'my-new-skill')")
@click.option("--description", help="Skill description for frontmatter")
@click.option("--phase", type=int, default=None, help="Phase number (0-9 or -1)")
@click.option("--template", type=int, default=None, help="Source skill number to use as template")
@click.option("--interactive", is_flag=True, help="Prompt for all fields interactively")
@click.option("--project-root", default=".", help="Path to project root")
def main(number, name, description, phase, template, interactive, project_root):
    """Create a new skill with correct structure and AI integration metadata."""
    if interactive:
        values = prompt_interactive()
        number = values["number"]
        name = values["name"]
        description = values["description"]
        phase = values["phase"]
    else:
        if number is None or name is None or description is None:
            click.echo("ERROR: --number, --name, and --description are required (or use --interactive)", err=True)
            sys.exit(2)

    if phase is None:
        phase = SKILL_PHASE_MAP.get(number, -1)

    # Validate
    errors = validate_new_skill(project_root, number, name)
    if errors:
        for err in errors:
            click.echo(f"ERROR: {err}", err=True)
        sys.exit(1)

    # Create
    skill_path = scaffold_skill(project_root, number, name, description, phase, template)
    click.echo(f"Created: {skill_path}")
    click.echo(f"  Number: s{number:02d}")
    click.echo(f"  Phase: {PHASE_MAP.get(phase, 'Any')}")
    agent, current, target = get_default_agent_for_skill(number, phase)
    click.echo(f"  Agent: {agent}")
    click.echo(f"  Autonomy: {current} -> {target}")
    click.echo(f"\nNext: Edit {skill_path} to fill in TODO sections.")


if __name__ == "__main__":
    main()

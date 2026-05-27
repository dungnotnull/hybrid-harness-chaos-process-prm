import re
from typing import Optional

from tools.shared.models import AutonomyLevel


def extract_sections(body: str) -> dict[str, str]:
    """Extract all ##-level sections from the markdown body.
    Returns dict mapping section title to raw content.
    """
    sections = {}
    pattern = re.compile(r"^## (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(body))

    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        sections[title] = content

    return sections


def extract_subsections(section_content: str) -> dict[str, str]:
    """Extract ###-level subsections within a section.
    Returns dict mapping subsection title to raw content.
    """
    subsections = {}
    pattern = re.compile(r"^### (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(section_content))

    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_content)
        content = section_content[start:end].strip()
        subsections[title] = content

    return subsections


def extract_autonomy_levels(autonomy_section: str) -> Optional[AutonomyLevel]:
    """Parse the Autonomy Level table to extract Current and Target levels.
    Table format: | Aspect | Level | Description |
    """
    current = None
    target = None

    for line in autonomy_section.split("\n"):
        line = line.strip()
        if line.startswith("|") and "Aspect" not in line and "---" not in line:
            cells = [c.strip() for c in line.split("|")]
            cells = [c for c in cells if c]
            if len(cells) >= 2:
                aspect = cells[0].lower()
                level = cells[1].strip()
                if "current" in aspect:
                    current = level
                elif "target" in aspect:
                    target = level

    if current and target:
        return AutonomyLevel(current=current, target=target)
    return None


def extract_agent_name(agent_section: str) -> str:
    """Extract agent name from: **Agent**: <name>"""
    match = re.search(r"\*\*Agent\*\*:\s*(.+)", agent_section)
    if match:
        return match.group(1).strip()
    return ""


def extract_capabilities(agent_section: str) -> list[str]:
    """Extract capability list items from the agent section."""
    capabilities = []
    for line in agent_section.split("\n"):
        line = line.strip()
        if line.startswith("- ") and "**Agent**" not in line and "**Capabilities**" not in line:
            capability = line[2:].strip()
            if capability and not capability.startswith("TODO"):
                capabilities.append(capability)
    return capabilities


def extract_human_gates(gates_section: str) -> list[str]:
    """Extract human gate items."""
    gates = []
    for line in gates_section.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            gate = line[2:].strip()
            if gate and not gate.startswith("TODO"):
                gates.append(gate)
    return gates


def extract_cross_references(input_contract: str) -> list[str]:
    """Parse Input Contract table to find cross-references to other skills.
    Looks for patterns like 's01 output', 's04 output', 's14 (workflow_context)'.
    """
    refs = set()
    matches = re.findall(r's(\d{2})', input_contract)
    for match in matches:
        refs.add(f"s{match}")
    return sorted(refs)


def validate_markdown_table(content: str) -> list[str]:
    """Check markdown tables have consistent column counts.
    Returns list of warning messages.
    """
    warnings = []
    in_table = False
    expected_cols = 0
    line_num = 0

    for line in content.split("\n"):
        line_num += 1
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cols = len(stripped.split("|")) - 2  # -2 for leading/trailing |
            if not in_table:
                in_table = True
                expected_cols = cols
            elif "---" in stripped:
                continue
            elif cols != expected_cols:
                warnings.append(f"Line {line_num}: Table has {cols} columns, expected {expected_cols}")
        else:
            in_table = False

    return warnings


def extract_mcp_platforms(section_content: str) -> list[str]:
    """Extract MCP platform names from the MCP/Fallback subsection."""
    platforms = []
    mcp_keywords = ["LitmusChaos", "Gremlin", "Steadybit", "AWS FIS", "Harness Chaos",
                    "ChaosGuard", "Fault Flags", "Prometheus", "MCP"]
    for line in section_content.split("\n"):
        for keyword in mcp_keywords:
            if keyword.lower() in line.lower() and keyword not in platforms:
                platforms.append(keyword)
    return platforms

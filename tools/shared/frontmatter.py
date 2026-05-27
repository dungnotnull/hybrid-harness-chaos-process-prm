import yaml


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md content.
    Returns (frontmatter_dict, body_content).
    Raises ValueError if frontmatter is malformed or missing.
    """
    if not content.startswith("---"):
        raise ValueError("File does not start with YAML frontmatter (---)")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Could not find closing --- for frontmatter")

    yaml_str = parts[1].strip()
    body = parts[2].strip()

    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in frontmatter: {e}")

    if not isinstance(data, dict):
        raise ValueError(f"Frontmatter must be a YAML mapping, got {type(data).__name__}")

    return data, body


def validate_frontmatter(data: dict) -> list[str]:
    """Validate required fields exist in frontmatter.
    Returns list of error messages (empty = valid).
    """
    from tools.shared.constants import REQUIRED_FRONTMATTER_FIELDS

    errors = []
    for field_name in REQUIRED_FRONTMATTER_FIELDS:
        if field_name not in data:
            errors.append(f"Missing required frontmatter field: '{field_name}'")
        elif not data[field_name] or (isinstance(data[field_name], str) and not data[field_name].strip()):
            errors.append(f"Frontmatter field '{field_name}' is empty")

    return errors

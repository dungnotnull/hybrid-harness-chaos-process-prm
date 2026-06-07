from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AutonomyLevel:
    current: str
    target: str


@dataclass
class AgentIntegration:
    autonomy_level: Optional[AutonomyLevel] = None
    harness_ai_agent: str = ""
    capabilities: list[str] = field(default_factory=list)
    human_gates: list[str] = field(default_factory=list)
    mcp_platforms: list[str] = field(default_factory=list)
    notes: str = ""
    fallback: str = ""


@dataclass
class SkillFrontmatter:
    name: str
    description: str


@dataclass
class SkillMeta:
    number: float
    dir_name: str
    file_path: str
    frontmatter: SkillFrontmatter
    sections: dict[str, str]
    agent_integration: AgentIntegration
    phase: int
    phase_name: str
    cross_refs_in: list[str] = field(default_factory=list)
    cross_refs_out: list[str] = field(default_factory=list)


@dataclass
class ValidationError:
    file_path: str
    skill_number: float
    skill_name: str
    severity: str  # "error" or "warning"
    category: str  # "frontmatter", "section", "autonomy", "crossref", "formatting"
    message: str
    line_number: Optional[int] = None


@dataclass
class ValidationResult:
    total_skills: int
    passed: int
    failed: int
    warnings: int
    errors: list[ValidationError] = field(default_factory=list)

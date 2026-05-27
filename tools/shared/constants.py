REQUIRED_FRONTMATTER_FIELDS = {"name", "description"}

REQUIRED_SECTIONS = [
    "Purpose",
    "Input Contract",
    "Output Contract",
    "Prerequisites",
    "AI Agent Integration",
    "Success Criteria",
]

REQUIRED_AGENT_SUBSECTIONS = [
    "Autonomy Level",
    "Harness AI Agent",
    "Human Gates",
]

OPTIONAL_AGENT_SUBSECTIONS = [
    "MCP",
    "MCP Integration",
    "Fallback",
    "Notes",
]

VALID_AUTONOMY_LEVELS = {"L0", "L1", "L2", "L3", "L4"}

PHASE_MAP = {
    0: "Foundation",
    1: "Planning & Requirements",
    2: "CI/CD Scaffolding",
    3: "Security Gate",
    4: "Testing",
    5: "Chaos Experiment Design",
    6: "Game Day Execution",
    7: "Verification & Observability",
    8: "Governance & Release",
    9: "Resilience & Continuity",
}

SKILL_PHASE_MAP = {
    0: 0, 1: 0, 2: 0, 3: 0,
    4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2,
    11: 3,
    12: 4, 13: 4,
    14: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5,
    20: 6,
    21: 7, 22: 7, 23: 7,
    24: 8, 25: 8, 26: 8, 27: 8, 28: 8,
    29: 9, 30: 9,
    31: -1,  # Any phase
    32: -1,  # Any phase
}

PHASE_AGENT_DEFAULTS = {
    0: {"s00": "Workflow Orchestration", "s01": "DevOps Agent", "s02": "None (internal)", "s03": "Knowledge Graph"},
    2: "DevOps Agent",
    3: "AppSec/STO Agent",
    4: "Test Agent",
    5: "Reliability Agent",
    6: "Reliability Agent",
    7: "SRE Agent",
    8: {"s24": "DevOps Agent", "s25": "FinOps Agent", "s26": "Reliability Agent", "s27": "SRE Agent", "s28": "DevOps Agent", "s29": "SRE Agent", "s30": "AppSec/STO Agent"},
    9: "SRE Agent",
    -1: "None (advisory by design)",
}

HARNESS_AGENTS = [
    "DevOps Agent",
    "Reliability Agent",
    "SRE Agent",
    "Test Agent",
    "FinOps Agent",
    "AppSec/STO Agent",
    "Knowledge Graph",
    "Workflow Orchestration",
    "None (internal)",
    "None (advisory by design)",
    "None (research by design)",
]

MCP_PLATFORMS = [
    "LitmusChaos MCP",
    "Gremlin MCP",
    "Steadybit MCP",
    "AWS FIS",
    "Harness Chaos",
    "Harness ChaosGuard",
    "Harness Fault Flags",
    "Prometheus",
]

SKILLS_DIR = "skills"
SKILL_FILE = "SKILL.md"

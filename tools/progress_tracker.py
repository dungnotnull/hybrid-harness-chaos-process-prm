"""Progress Tracker CLI -- manage workflow state for the 36-skill Agile workflow.

Commands:
  init          Initialize progress.json with all 36 phases
  status        Show current workflow progress dashboard
  next          Show the next pending phase
  transition    Transition a phase to a new status (pending/in_progress/completed/blocked/skipped)
  block         Add a blocker to the current phase
  resolve        Resolve a blocker by ID
  report        Generate a full progress report
  export        Export progress as JSON
  agent-handoff Generate an agent handoff summary
"""
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click

from tools.shared.constants import SKILLS_DIR, PHASE_MAP, SKILL_PHASE_MAP

PROGRESS_FILE = ".commandcode/progress.json"
ARTIFACTS_DIR = ".commandcode/artifacts"

PHASES = [
    {"id": "00-orchestrator", "name": "Orchestrator", "phase": 0},
    {"id": "01-ba-requirements", "name": "BA Requirements", "phase": 0},
    {"id": "01-1-user-flow-writing", "name": "User Flow Writing", "phase": 0},
    {"id": "02-taste-memory", "name": "Taste Memory", "phase": 0},
    {"id": "03-progress-tracker", "name": "Progress Tracker", "phase": 0},
    {"id": "04-pipeline-design", "name": "Pipeline Design", "phase": 2},
    {"id": "05-service-onboarding", "name": "Service Onboarding", "phase": 2},
    {"id": "06-delegate-management", "name": "Delegate Management", "phase": 2},
    {"id": "07-secrets-management", "name": "Secrets Management", "phase": 2},
    {"id": "08-feature-flags", "name": "Feature Flags", "phase": 2},
    {"id": "09-template-library", "name": "Template Library", "phase": 2},
    {"id": "10-gitops", "name": "GitOps", "phase": 2},
    {"id": "11-security-scanning", "name": "Security Scanning", "phase": 3},
    {"id": "12-cloakbrowser-testing", "name": "CloakBrowser Testing", "phase": 4},
    {"id": "13-performance-testing", "name": "Performance Testing", "phase": 4},
    {"id": "14-experiment-design", "name": "Experiment Design", "phase": 5},
    {"id": "15-hypothesis-validation", "name": "Hypothesis Validation", "phase": 5},
    {"id": "16-blast-radius-control", "name": "Blast Radius Control", "phase": 5},
    {"id": "17-steady-state", "name": "Steady State", "phase": 5},
    {"id": "18-infrastructure-faults", "name": "Infrastructure Faults", "phase": 5},
    {"id": "19-application-faults", "name": "Application Faults", "phase": 5},
    {"id": "20-game-day-planning", "name": "Game Day Planning", "phase": 6},
    {"id": "21-cv-verification", "name": "CV Verification", "phase": 7},
    {"id": "22-observability-integration", "name": "Observability Integration", "phase": 7},
    {"id": "23-alerting-recommendations", "name": "Alerting Recommendations", "phase": 7},
    {"id": "24-policy-governance", "name": "Policy Governance", "phase": 8},
    {"id": "25-cloud-cost-management", "name": "Cloud Cost Management", "phase": 8},
    {"id": "26-resilience-scoring", "name": "Resilience Scoring", "phase": 8},
    {"id": "27-postmortem-learning", "name": "Postmortem Learning", "phase": 8},
    {"id": "28-release-management", "name": "Release Management", "phase": 8},
    {"id": "29-disaster-recovery", "name": "Disaster Recovery", "phase": 9},
    {"id": "30-compliance-audit", "name": "Compliance Audit", "phase": 9},
    {"id": "31-strategic-creator", "name": "Strategic Creator", "phase": -1},
    {"id": "32-deep-research", "name": "Deep Research", "phase": -1},
    {"id": "33-system-optimization", "name": "System Optimization", "phase": -1},
    {"id": "34-documentation-writing", "name": "Documentation Writing", "phase": -1},
    {"id": "35-devils-advocate", "name": "Devil's Advocate", "phase": -1},
]

VALID_STATUSES = {"pending", "in_progress", "completed", "blocked", "skipped"}

PHASE_GROUPS = {
    0: "Foundation",
    2: "CI/CD Scaffolding",
    3: "Security Gate",
    4: "Testing",
    5: "Chaos Experiment Design",
    6: "Game Day",
    7: "Verification & Observability",
    8: "Governance & Release",
    9: "Resilience & Continuity",
    -1: "Callable Anytime",
}


def load_progress(project_root: str) -> dict:
    """Load progress.json from the project root."""
    path = os.path.join(project_root, PROGRESS_FILE)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(project_root: str, data: dict) -> None:
    """Save progress.json to the project root."""
    path = os.path.join(project_root, PROGRESS_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def init_progress(project_root: str, project_name: str = "my-project") -> dict:
    """Initialize a new progress.json with all 36 phases."""
    now = datetime.now(timezone.utc).isoformat()
    phases = {}
    for p in PHASES:
        phases[p["id"]] = {"status": "pending"}

    data = {
        "project": project_name,
        "workflow_version": "0.5.0",
        "created_at": now,
        "updated_at": now,
        "total_phases": len(PHASES),
        "completed_phases": 0,
        "current_phase": None,
        "agent": "unknown",
        "phases": phases,
        "blockers": [],
        "metrics": {
            "estimated_total_hours": 40,
            "elapsed_hours": 0,
            "velocity_phases_per_hour": 0,
        },
    }
    save_progress(project_root, data)
    return data


def get_status_emoji(status: str) -> str:
    """Return emoji for status."""
    return {
        "completed": "\u2705",
        "in_progress": "\U0001f535",
        "blocked": "\U0001f534",
        "skipped": "\u26aa",
        "pending": "\u26ab",
    }.get(status, "\u2753")


def render_dashboard(data: dict) -> str:
    """Render a colored terminal dashboard."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  HYBRID HARNESS + CHAOS WORKFLOW STATUS")
    lines.append("=" * 70)
    lines.append(f"  Project:  {data['project']}")
    lines.append(f"  Agent:    {data.get('agent', 'unknown')}")

    phases = data.get("phases", {})
    completed = sum(1 for p in phases.values() if p.get("status") == "completed")
    total = data.get("total_phases", len(PHASES))
    pct = int(completed / total * 100) if total > 0 else 0

    lines.append(f"  Progress: {completed}/{total} phases ({pct}%)")

    current = data.get("current_phase")
    if current:
        lines.append(f"  Current:  {current}")

    lines.append("")

    # Group by phase
    for phase_num, phase_name in sorted(PHASE_GROUPS.items()):
        if phase_num == -1:
            phase_skills = [p for p in PHASES if p["phase"] == -1]
        else:
            phase_skills = [p for p in PHASES if p["phase"] == phase_num]

        phase_completed = sum(
            1 for p in phase_skills
            if phases.get(p["id"], {}).get("status") == "completed"
        )
        phase_pct = int(phase_completed / len(phase_skills) * 100) if phase_skills else 0

        bar_len = 20
        filled = int(bar_len * phase_pct / 100)
        bar = "\u2588" * filled + "\u2591" * (bar_len - filled)

        lines.append(
            f"  {phase_name:25s} {bar} {phase_pct:3d}% ({phase_completed}/{len(phase_skills)})"
        )

        for p in phase_skills:
            status = phases.get(p["id"], {}).get("status", "pending")
            emoji = get_status_emoji(status)
            lines.append(f"    {emoji} s{p['id'].split('-')[0]}-{p['id'].split('-', 1)[1]:30s} {status}")

    lines.append("")
    blockers = data.get("blockers", [])
    active_blockers = [b for b in blockers if not b.get("resolved_at")]
    lines.append(f"  Blockers: {len(active_blockers)} active")
    for b in active_blockers:
        lines.append(f"    \U0001f534 {b.get('id', '???')}: {b.get('description', 'No description')}")

    lines.append("=" * 70)
    return "\n".join(lines)


def generate_report(data: dict) -> str:
    """Generate a detailed text report."""
    lines = []
    lines.append("# Workflow Progress Report")
    lines.append("")
    lines.append(f"**Project**: {data['project']}")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).isoformat()}")
    lines.append(f"**Workflow Version**: {data.get('workflow_version', 'unknown')}")
    lines.append("")

    phases = data.get("phases", {})
    completed = sum(1 for p in phases.values() if p.get("status") == "completed")
    total = data.get("total_phases", len(PHASES))
    lines.append(f"## Summary: {completed}/{total} phases completed ({int(completed/total*100)}%)")
    lines.append("")

    lines.append("## Phase Details")
    lines.append("")
    lines.append("| Phase | Status | Started | Completed | Agent | Artifacts |")
    lines.append("|---|---|---|---|---|---|")

    for p in PHASES:
        phase_data = phases.get(p["id"], {})
        status = phase_data.get("status", "pending")
        started = phase_data.get("started_at", "-")
        completed_at = phase_data.get("completed_at", "-")
        agent = phase_data.get("agent", "-")
        artifacts = ", ".join(phase_data.get("artifacts", [])) or "-"
        lines.append(f"| {p['id']} | {status} | {started} | {completed_at} | {agent} | {artifacts} |")

    blockers = data.get("blockers", [])
    if blockers:
        lines.append("")
        lines.append("## Blockers")
        lines.append("")
        for b in blockers:
            status = "RESOLVED" if b.get("resolved_at") else "ACTIVE"
            lines.append(f"- **{b.get('id', '???')}** [{status}]: {b.get('description', '')}")

    lines.append("")
    lines.append("---")
    lines.append("*Generated by progress_tracker.py*")
    return "\n".join(lines)


@click.group()
@click.option("--project-root", default=".", help="Path to project root")
@click.pass_context
def cli(ctx, project_root):
    """Progress Tracker CLI for the 36-skill Agile workflow."""
    ctx.ensure_object(dict)
    ctx.obj["project_root"] = os.path.abspath(project_root)


@cli.command()
@click.option("--project-name", default="my-project", help="Project name")
@click.pass_context
def init(ctx, project_name):
    """Initialize progress.json with all 36 phases."""
    project_root = ctx.obj["project_root"]
    data = init_progress(project_root, project_name)
    click.echo(f"Initialized progress.json for project '{project_name}'")
    click.echo(f"  Total phases: {data['total_phases']}")
    click.echo(f"  Location: {os.path.join(project_root, PROGRESS_FILE)}")


@cli.command()
@click.pass_context
def status(ctx):
    """Show current workflow progress dashboard."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)
    click.echo(render_dashboard(data))


@cli.command()
@click.pass_context
def next_cmd(ctx):
    """Show the next pending phase."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)

    phases = data.get("phases", {})
    for p in PHASES:
        if phases.get(p["id"], {}).get("status") == "pending":
            click.echo(f"Next phase: {p['id']} ({p['name']})")
            return
    click.echo("All phases completed!")


@cli.command()
@click.argument("phase_id")
@click.argument("status", type=click.Choice(VALID_STATUSES))
@click.option("--agent", default="unknown", help="Agent identifier")
@click.option("--artifacts", default="", help="Comma-separated list of artifacts produced")
@click.pass_context
def transition(ctx, phase_id, status, agent, artifacts):
    """Transition a phase to a new status."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)

    if phase_id not in data.get("phases", {}):
        valid_ids = list(data.get("phases", {}).keys())
        click.echo(f"Invalid phase ID: {phase_id}", err=True)
        click.echo(f"Valid IDs: {', '.join(valid_ids)}", err=True)
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()
    phase_data = data["phases"][phase_id]

    # Validate state transition
    current = phase_data.get("status", "pending")
    valid_transitions = {
        "pending": ["in_progress", "skipped"],
        "in_progress": ["completed", "blocked", "skipped"],
        "blocked": ["in_progress"],
        "completed": [],  # Terminal state
        "skipped": [],     # Terminal state
    }

    if status not in valid_transitions.get(current, []):
        click.echo(f"Invalid transition: {current} -> {status}", err=True)
        click.echo(f"Valid transitions from '{current}': {valid_transitions.get(current, [])}", err=True)
        sys.exit(1)

    phase_data["status"] = status
    phase_data["agent"] = agent

    if status == "in_progress":
        phase_data["started_at"] = now
        data["current_phase"] = phase_id
    elif status == "completed":
        phase_data["completed_at"] = now
        if artifacts:
            phase_data["artifacts"] = [a.strip() for a in artifacts.split(",")]
        # Check if this was the current phase
        if data.get("current_phase") == phase_id:
            data["current_phase"] = None
    elif status == "blocked":
        phase_data["blocked_at"] = now
    elif status == "skipped":
        phase_data["skipped_at"] = now
        phase_data["skipped_reason"] = "User skipped"

    # Update counts
    completed = sum(1 for p in data["phases"].values() if p.get("status") == "completed")
    data["completed_phases"] = completed

    save_progress(project_root, data)
    click.echo(f"Transitioned {phase_id}: {current} -> {status}")


@cli.command()
@click.argument("description")
@click.option("--phase", help="Phase ID to block")
@click.option("--blocked-by", default="unknown", help="What's blocking")
@click.option("--owner", default="unknown", help="Who resolves it")
@click.pass_context
def block(ctx, description, phase, blocked_by, owner):
    """Add a blocker to the current phase."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)

    now = datetime.now(timezone.utc).isoformat()
    blocker_id = f"BLK-{len(data.get('blockers', [])) + 1:03d}"

    if not phase:
        phase = data.get("current_phase", "unknown")

    blocker = {
        "id": blocker_id,
        "phase": phase,
        "description": description,
        "blocked_by": blocked_by,
        "owner": owner,
        "created_at": now,
        "resolved_at": None,
    }
    data.setdefault("blockers", []).append(blocker)

    # Set phase to blocked
    if phase in data.get("phases", {}):
        data["phases"][phase]["status"] = "blocked"
        data["phases"][phase]["blocked_at"] = now

    save_progress(project_root, data)
    click.echo(f"Created blocker {blocker_id}: {description}")
    click.echo(f"  Phase: {phase}")
    click.echo(f"  Blocked by: {blocked_by}")


@cli.command()
@click.argument("blocker_id")
@click.pass_context
def resolve(ctx, blocker_id):
    """Resolve a blocker by ID."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)

    blockers = data.get("blockers", [])
    found = False
    for b in blockers:
        if b.get("id") == blocker_id:
            b["resolved_at"] = datetime.now(timezone.utc).isoformat()
            phase = b.get("phase")
            if phase in data.get("phases", {}):
                data["phases"][phase]["status"] = "in_progress"
            found = True
            break

    if not found:
        click.echo(f"Blocker {blocker_id} not found.", err=True)
        sys.exit(1)

    save_progress(project_root, data)
    click.echo(f"Resolved blocker {blocker_id}")


@cli.command()
@click.pass_context
def report(ctx):
    """Generate a full progress report."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)

    report_text = generate_report(data)

    # Write to artifacts
    artifacts_dir = os.path.join(project_root, ARTIFACTS_DIR)
    os.makedirs(artifacts_dir, exist_ok=True)
    report_path = os.path.join(artifacts_dir, "progress-report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    click.echo(report_text)
    click.echo(f"\nReport saved to: {report_path}")


@cli.command()
@click.pass_context
def export(ctx):
    """Export progress as JSON to stdout."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)
    click.echo(json.dumps(data, indent=2, ensure_ascii=False))


@cli.command()
@click.pass_context
def handoff(ctx):
    """Generate an agent handoff summary."""
    project_root = ctx.obj["project_root"]
    data = load_progress(project_root)
    if not data:
        click.echo("No progress.json found. Run 'progress-tracker init' first.", err=True)
        sys.exit(1)

    phases = data.get("phases", {})
    completed_phases = [pid for pid, p in phases.items() if p.get("status") == "completed"]
    current = data.get("current_phase", "none")
    active_blockers = [b for b in data.get("blockers", []) if not b.get("resolved_at")]

    # Find last completed phase
    last_completed = completed_phases[-1] if completed_phases else "none"

    # Find next 3 pending phases
    next_phases = []
    for p in PHASES:
        if phases.get(p["id"], {}).get("status") == "pending" and len(next_phases) < 3:
            next_phases.append(p["id"])

    lines = []
    lines.append("=" * 60)
    lines.append("AGENT HANDOFF")
    lines.append("=" * 60)
    lines.append(f"Project:   {data['project']}")
    lines.append(f"Agent:     {data.get('agent', 'unknown')}")
    lines.append(f"Previous:  {last_completed} (completed)")
    lines.append(f"Current:   {current}")
    lines.append(f"Blockers:  {len(active_blockers)} active")
    lines.append(f"Next:      {' -> '.join(next_phases)}")
    lines.append(f"Taste:     Load .commandcode/taste/taste.md")
    lines.append("")
    lines.append("Completed phases:")
    for pid in completed_phases:
        phase_data = phases.get(pid, {})
        artifacts = ", ".join(phase_data.get("artifacts", []))
        lines.append(f"  {pid}: {artifacts or 'no artifacts recorded'}")
    lines.append("")
    lines.append("Active blockers:")
    for b in active_blockers:
        lines.append(f"  {b.get('id', '???')}: {b.get('description', '')} (owner: {b.get('owner', 'unknown')})")
    lines.append("=" * 60)
    lines.append(f"Continue from {os.path.join(project_root, PROGRESS_FILE)}")

    click.echo("\n".join(lines))


if __name__ == "__main__":
    # Register the 'next' command with click
    # (can't name a function 'next' since it's a builtin)
    cli.add_command(next_cmd, name="next")
    cli()

"""MCP tool definitions for chaos engineering operations."""
from typing import Optional

from tools.chaos_mcp_server.litmus_client import LitmusChaosClient
from tools.chaos_mcp_server.harness_chaos_client import HarnessChaosClient


FAULT_TAXONOMY = {
    "application": [
        "pod-delete", "pod-memory-hog", "pod-io-errors",
        "container-kill", "container-memory-hog",
        "network-latency", "network-loss", "network-corruption", "network-partition",
        "dns-error", "dns-spoof",
    ],
    "infrastructure": [
        "node-drain", "node-cpu-hog", "node-memory-hog",
        "disk-fill", "disk-loss",
        "aws-ec2-stop", "aws-ec2-terminate",
        "gcp-vm-stop", "gcp-vm-terminate",
        "azure-vm-stop",
    ],
    "network": [
        "network-latency", "network-loss", "network-corruption",
        "network-partition", "network-duplication",
    ],
}


def register_tools(mcp):
    """Register all chaos engineering MCP tools."""

    @mcp.tool()
    async def list_chaos_infrastructures(
        platform: str = "litmus",
        namespace: str = "litmus",
    ) -> str:
        """List all registered chaos infrastructure instances.
        Returns markdown table of infrastructure name, namespace, status, platform.

        Args:
            platform: Chaos platform to query ("litmus" or "harness")
            namespace: Kubernetes namespace for LitmusChaos
        """
        if platform == "litmus":
            client = LitmusChaosClient(namespace=namespace)
            infras = await client.list_chaos_infrastructures()
        else:
            client = HarnessChaosClient()
            infras = await client.get_infrastructures()

        if not infras:
            return "No chaos infrastructures found. Ensure the platform is configured and running."

        lines = ["| Name | Namespace | Status | Platform |", "|---|---|---|---|"]
        for infra in infras:
            lines.append(f"| {infra.get('name', 'N/A')} | {infra.get('namespace', namespace)} | {infra.get('status', 'N/A')} | {platform} |")
        return "\n".join(lines)

    @mcp.tool()
    async def list_chaos_experiments(
        platform: str = "litmus",
        namespace: Optional[str] = None,
    ) -> str:
        """List chaos experiments, optionally filtered by namespace.

        Args:
            platform: Chaos platform to query ("litmus" or "harness")
            namespace: Kubernetes namespace filter
        """
        if platform == "litmus":
            client = LitmusChaosClient(namespace=namespace or "litmus")
            experiments = await client.list_experiments(namespace=namespace)
        else:
            client = HarnessChaosClient()
            experiments = await client.list_experiments()

        if not experiments:
            return "No chaos experiments found."

        lines = ["| Name | Target | Fault Type | Status |", "|---|---|---|---|"]
        for exp in experiments:
            lines.append(f"| {exp.get('name', 'N/A')} | {exp.get('target', 'N/A')} | {exp.get('fault_type', 'N/A')} | {exp.get('status', 'N/A')} |")
        return "\n".join(lines)

    @mcp.tool()
    async def get_experiment_details(
        experiment_name: str,
        namespace: str = "litmus",
        platform: str = "litmus",
    ) -> str:
        """Get full details of a specific chaos experiment.

        Args:
            experiment_name: Name of the experiment to query
            namespace: Kubernetes namespace
            platform: Chaos platform
        """
        if platform == "litmus":
            client = LitmusChaosClient(namespace=namespace)
            details = await client.get_experiment(experiment_name, namespace)
        else:
            client = HarnessChaosClient()
            details = await client.get_experiment(experiment_name)

        lines = [f"## Experiment: {experiment_name}"]
        for key, value in details.items():
            lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)

    @mcp.tool()
    async def create_experiment(
        name: str,
        fault_type: str,
        target_app: str,
        namespace: str = "litmus",
        duration: int = 60,
        platform: str = "litmus",
        dry_run: bool = True,
    ) -> str:
        """Create a new chaos experiment. Returns the generated manifest.
        By default runs in dry-run mode (validation only).

        Args:
            name: Experiment name
            fault_type: Fault to inject (e.g., "pod-delete", "network-latency")
            target_app: Target application label selector or service name
            namespace: Kubernetes namespace
            duration: Experiment duration in seconds
            platform: Chaos platform
            dry_run: If True, only validate without creating (default: True)
        """
        manifest = {
            "apiVersion": "litmuschaos.io/v1alpha1",
            "kind": "ChaosEngine",
            "metadata": {"name": name, "namespace": namespace},
            "spec": {
                "appinfo": {"appns": namespace, "applabel": f"app={target_app}"},
                "chaosServiceAccount": f"{name}-sa",
                "experiments": [{
                    "name": fault_type,
                    "spec": {
                        "components": {"experimentPath": f"litmuschaos/chaos-chart-repo/{fault_type}/"},
                    },
                }],
            },
        }

        if dry_run:
            return f"DRY RUN: Experiment manifest validated successfully.\n\nManifest:\n```yaml\n{manifest}\n```\n\nSet dry_run=False to create."

        if platform == "litmus":
            client = LitmusChaosClient(namespace=namespace)
            result = await client.create_experiment(manifest, dry_run=False)
        else:
            client = HarnessChaosClient()
            result = await client.create_experiment(manifest)

        return f"Experiment created: {result.get('name', name)}"

    @mcp.tool()
    async def run_experiment(
        experiment_name: str,
        namespace: str = "litmus",
        platform: str = "litmus",
        confirm: bool = False,
    ) -> str:
        """Execute a chaos experiment. Requires explicit confirmation.

        Args:
            experiment_name: Name of the experiment to run
            namespace: Kubernetes namespace
            platform: Chaos platform
            confirm: Must be True to actually execute (safety gate)
        """
        if not confirm:
            return f"SAFETY GATE: Set confirm=True to execute experiment '{experiment_name}'. This will inject faults into the target."

        if platform == "litmus":
            client = LitmusChaosClient(namespace=namespace)
            result = await client.run_experiment(experiment_name, namespace)
        else:
            client = HarnessChaosClient()
            result = await client.run_experiment(experiment_name)

        return f"Experiment '{experiment_name}' triggered. Status: {result.get('status', 'unknown')}"

    @mcp.tool()
    async def get_resilience_score(
        service_name: Optional[str] = None,
        platform: str = "litmus",
    ) -> str:
        """Query resilience scores for a service.

        Args:
            service_name: Service to query (optional, returns all if omitted)
            platform: Chaos platform
        """
        if platform == "litmus":
            client = LitmusChaosClient()
            result = await client.get_resilience_score(service_name or "all")
        else:
            client = HarnessChaosClient()
            result = await client.get_resilience_score(service_name or "all")

        score = result.get("score")
        if score is None:
            return f"No resilience score available for '{service_name}'. Run chaos experiments first."

        return f"Resilience Score for '{service_name}': {score}/100"

    @mcp.tool()
    async def get_steady_state(
        service_name: str,
        namespace: str = "litmus",
    ) -> str:
        """Probe the current steady state of a service.

        Args:
            service_name: Service to probe
            namespace: Kubernetes namespace
        """
        client = LitmusChaosClient(namespace=namespace)
        result = await client.get_steady_state(service_name)

        lines = [f"## Steady State: {service_name}"]
        for key, value in result.items():
            lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)

    @mcp.tool()
    async def list_available_faults(
        category: Optional[str] = None,
    ) -> str:
        """List all available fault types organized by category.

        Args:
            category: Filter by category ("application", "infrastructure", "network")
        """
        if category:
            faults = FAULT_TAXONOMY.get(category, [])
            if not faults:
                return f"No faults found for category '{category}'. Available: {list(FAULT_TAXONOMY.keys())}"
            lines = [f"## {category.title()} Faults"]
            for fault in faults:
                lines.append(f"- {fault}")
            return "\n".join(lines)

        lines = []
        for cat, faults in FAULT_TAXONOMY.items():
            lines.append(f"## {cat.title()} Faults ({len(faults)})")
            for fault in faults:
                lines.append(f"- {fault}")
            lines.append("")
        return "\n".join(lines)

    @mcp.tool()
    async def abort_experiment(
        experiment_name: str,
        namespace: str = "litmus",
        platform: str = "litmus",
    ) -> str:
        """Immediately abort a running chaos experiment.

        Args:
            experiment_name: Name of the experiment to abort
            namespace: Kubernetes namespace
            platform: Chaos platform
        """
        if platform == "litmus":
            client = LitmusChaosClient(namespace=namespace)
            result = await client.abort_experiment(experiment_name, namespace)
        else:
            return f"Abort not yet implemented for platform '{platform}'"

        return f"Experiment '{experiment_name}' aborted. Status: {result.get('status', 'aborted')}"

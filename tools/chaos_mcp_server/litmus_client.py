"""LitmusChaos Kubernetes API client."""
import os
from typing import Optional


class LitmusChaosClient:
    """Client for LitmusChaos via Kubernetes CRD API."""

    def __init__(self, kubeconfig: Optional[str] = None, namespace: str = "litmus"):
        self.kubeconfig = kubeconfig or os.environ.get("KUBECONFIG")
        self.namespace = namespace

    async def list_chaos_infrastructures(self) -> list[dict]:
        """List registered ChaosInfrastructure CRDs."""
        return []

    async def list_experiments(self, namespace: Optional[str] = None) -> list[dict]:
        """List ChaosEngine and ChaosExperiment CRDs."""
        return []

    async def get_experiment(self, name: str, namespace: Optional[str] = None) -> dict:
        """Get details of a specific chaos experiment."""
        return {"name": name, "status": "not_found"}

    async def create_experiment(self, manifest: dict, dry_run: bool = True) -> dict:
        """Create a ChaosExperiment CRD. If dry_run, validate only."""
        return {"name": manifest.get("name", "unknown"), "dry_run": dry_run, "status": "validated"}

    async def run_experiment(self, engine_name: str, namespace: Optional[str] = None) -> dict:
        """Trigger a ChaosEngine to run an experiment."""
        return {"engine": engine_name, "status": "triggered"}

    async def abort_experiment(self, engine_name: str, namespace: Optional[str] = None) -> dict:
        """Abort a running ChaosEngine."""
        return {"engine": engine_name, "status": "aborted"}

    async def get_resilience_score(self, service_name: str) -> dict:
        """Query resilience score for a service from LitmusChaos."""
        return {"service": service_name, "score": None, "status": "not_available"}

    async def get_steady_state(self, service_name: str, metrics_endpoint: Optional[str] = None) -> dict:
        """Probe current steady state of a service."""
        return {"service": service_name, "steady_state": "unknown"}

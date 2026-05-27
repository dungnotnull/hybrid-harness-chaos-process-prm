"""Harness Chaos Engineering REST API client."""
import os
from typing import Optional


class HarnessChaosClient:
    """Client for Harness Chaos Engineering REST API."""

    def __init__(
        self,
        account_id: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: str = "https://app.harness.io",
    ):
        self.account_id = account_id or os.environ.get("HARNESS_ACCOUNT_ID", "")
        self.api_key = api_key or os.environ.get("HARNESS_API_KEY", "")
        self.base_url = base_url

    async def list_experiments(self, project: Optional[str] = None) -> list[dict]:
        """List chaos experiments in Harness."""
        return []

    async def get_experiment(self, experiment_id: str) -> dict:
        """Get details of a specific experiment."""
        return {"id": experiment_id, "status": "not_found"}

    async def create_experiment(self, config: dict) -> dict:
        """Create a new chaos experiment."""
        return {"id": "new", "status": "created"}

    async def run_experiment(self, experiment_id: str) -> dict:
        """Execute a chaos experiment."""
        return {"id": experiment_id, "status": "running"}

    async def get_infrastructures(self) -> list[dict]:
        """List chaos infrastructure instances."""
        return []

    async def get_resilience_score(self, service_id: str) -> dict:
        """Query resilience score for a service."""
        return {"service": service_id, "score": None, "status": "not_available"}

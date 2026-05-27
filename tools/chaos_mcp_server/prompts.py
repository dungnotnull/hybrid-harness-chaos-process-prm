"""MCP prompt definitions for chaos engineering workflows."""


def register_prompts(mcp):
    """Register all chaos engineering MCP prompts."""

    @mcp.prompt()
    async def design_chaos_experiment(user_request: str) -> str:
        """Interactive prompt guiding the user through designing a chaos experiment.
        Follows the s14 experiment design framework from the 33-skill workflow.

        Args:
            user_request: The user's natural language request for a chaos experiment
        """
        return f"""You are a chaos engineering expert following the s14-experiment-design framework.

The user wants to design a chaos experiment. Their request: "{user_request}"

Guide them through these steps:
1. **Target Selection**: Which service/infrastructure component to target?
2. **Hypothesis**: What do you expect to happen when the fault is injected?
3. **Steady State**: What does "normal" look like? (metrics, error rate, latency)
4. **Fault Selection**: Which fault type from the taxonomy fits?
5. **Blast Radius**: What is the scope? (pod, service, namespace, node)
6. **Abort Conditions**: When should the experiment auto-abort?
7. **Environment**: Which environment tier? (dev, staging, preprod, production)

Available fault types - use list_available_faults to see the full taxonomy.
After gathering info, use create_experiment with dry_run=True to validate.

SAFETY: All experiments default to dry-run mode. Never execute without explicit user confirmation."""

    @mcp.prompt()
    async def analyze_resilience(service_name: str) -> str:
        """Analyze the resilience posture of a service using s26 scoring methodology.

        Args:
            service_name: The service to analyze
        """
        return f"""Analyze the resilience posture of '{service_name}' using the s26 Resilience Scoring methodology.

Steps:
1. **Query Resilience Score**: Use get_resilience_score for the service
2. **Review Experiment History**: Use list_chaos_experiments to see past experiments
3. **Check Steady State**: Use get_steady_state to see current baseline
4. **Identify Gaps**: Compare against the s26 scoring dimensions:
   - Availability (can the service survive component failures?)
   - Recoverability (how fast does it recover?)
   - Observability (can we detect and diagnose issues?)
   - Fault Tolerance (what faults has it been tested against?)

5. **Recommend Improvements**: Suggest new experiments based on gaps found

Report findings in a structured format with scores and recommendations."""

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Health Orchestrator Script

Maps discovered API groups to specialized health check agents.
Returns an agent dispatch plan with parallelization groups.

Usage:
    uv run health_orchestrator.py [--discovery-json PATH]
    echo '{"detected_operators": [...]}' | uv run health_orchestrator.py
"""

import json
import sys
from dataclasses import dataclass
from typing import Any


@dataclass
class AgentConfig:
    """Configuration for a health check agent."""
    name: str
    api_groups: list[str]
    priority: int  # 1 = highest (core), 2 = operators
    parallel_group: int  # Agents in same group can run in parallel


# Define all available health check agents
AGENT_REGISTRY: list[AgentConfig] = [
    # Core agent - always runs
    AgentConfig(
        name="k8s-core-health-agent",
        api_groups=[],  # Empty means always active
        priority=1,
        parallel_group=1,
    ),
    # Operator agents - conditional based on API discovery
    AgentConfig(
        name="k8s-crossplane-health-agent",
        api_groups=["crossplane.io", "apiextensions.crossplane.io", "pkg.crossplane.io"],
        priority=2,
        parallel_group=2,
    ),
    AgentConfig(
        name="k8s-argocd-health-agent",
        api_groups=["argoproj.io"],
        priority=2,
        parallel_group=2,
    ),
    AgentConfig(
        name="k8s-certmanager-health-agent",
        api_groups=["cert-manager.io", "acme.cert-manager.io"],
        priority=2,
        parallel_group=2,
    ),
    AgentConfig(
        name="k8s-prometheus-health-agent",
        api_groups=["monitoring.coreos.com"],
        priority=2,
        parallel_group=2,
    ),
]


def get_active_agents(discovered_apis: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Determine which agents should be activated based on discovered APIs.

    Args:
        discovered_apis: Output from discover_apis.py

    Returns:
        List of agent configurations to dispatch
    """
    api_groups = set(discovered_apis.get("api_groups", []))

    active_agents = []

    for agent in AGENT_REGISTRY:
        # Core agent always runs
        if not agent.api_groups:
            active_agents.append({
                "name": agent.name,
                "priority": agent.priority,
                "parallel_group": agent.parallel_group,
                "trigger": "always",
            })
            continue

        # Check if any of the agent's API groups are present
        matching_groups = [g for g in agent.api_groups if g in api_groups]
        if matching_groups:
            active_agents.append({
                "name": agent.name,
                "priority": agent.priority,
                "parallel_group": agent.parallel_group,
                "trigger": matching_groups[0],
            })

    # Sort by priority (lower = higher priority)
    active_agents.sort(key=lambda a: (a["priority"], a["name"]))

    return active_agents


def create_dispatch_plan(active_agents: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Create an execution plan for dispatching agents.

    Args:
        active_agents: List of active agent configurations

    Returns:
        Dispatch plan with parallel and sequential groups
    """
    # Group agents by parallel_group
    groups: dict[int, list[dict[str, Any]]] = {}
    for agent in active_agents:
        group = agent["parallel_group"]
        if group not in groups:
            groups[group] = []
        groups[group].append(agent)

    # Build execution plan
    plan = {
        "total_agents": len(active_agents),
        "execution_groups": [],
    }

    for group_id in sorted(groups.keys()):
        group_agents = groups[group_id]
        plan["execution_groups"].append({
            "group": group_id,
            "parallel": len(group_agents) > 1,
            "agents": [a["name"] for a in group_agents],
        })

    return plan


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Map APIs to health agents")
    parser.add_argument("--discovery-json", help="Path to discovery JSON file")
    parser.add_argument("--pretty", action="store_true", help="Pretty print output")

    args = parser.parse_args()

    # Read discovery data from file or stdin
    if args.discovery_json:
        with open(args.discovery_json) as f:
            discovery_data = json.load(f)
    elif not sys.stdin.isatty():
        discovery_data = json.load(sys.stdin)
    else:
        # Default empty discovery for testing
        discovery_data = {"api_groups": [], "detected_operators": []}

    # Get active agents
    active_agents = get_active_agents(discovery_data)

    # Create dispatch plan
    dispatch_plan = create_dispatch_plan(active_agents)

    result = {
        "active_agents": active_agents,
        "dispatch_plan": dispatch_plan,
    }

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))


if __name__ == "__main__":
    main()

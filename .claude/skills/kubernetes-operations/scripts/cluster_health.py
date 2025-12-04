#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Quick Kubernetes cluster health check.

Usage:
    uv run cluster_health.py

Output:
    Condensed cluster status with node health and unhealthy pod count.
    Saves ~1200 tokens compared to running multiple commands.
"""

import subprocess
import sys


def run_kubectl(args: list[str]) -> tuple[str, int]:
    """Run kubectl command and return output and exit code."""
    try:
        result = subprocess.run(
            ["kubectl"] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout + result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "Command timed out", 1
    except FileNotFoundError:
        return "kubectl not found", 1


def get_current_context() -> str:
    """Get current kubectl context."""
    output, code = run_kubectl(["config", "current-context"])
    if code != 0:
        return "unknown"
    return output.strip()


def get_node_status() -> list[dict]:
    """Get node status summary."""
    jsonpath = (
        '{range .items[*]}'
        '{.metadata.name}|{.status.conditions[?(@.type=="Ready")].status}|'
        '{.status.allocatable.cpu}|{.status.allocatable.memory}\n'
        '{end}'
    )

    output, code = run_kubectl(["get", "nodes", "-o", f"jsonpath={jsonpath}"])

    if code != 0:
        return []

    nodes = []
    for line in output.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            nodes.append({
                "name": parts[0],
                "ready": parts[1] == "True",
                "cpu": parts[2],
                "memory": parts[3]
            })

    return nodes


def get_unhealthy_pods() -> list[dict]:
    """Get pods that are not Running or Succeeded."""
    output, code = run_kubectl([
        "get", "pods", "--all-namespaces",
        "--field-selector", "status.phase!=Running,status.phase!=Succeeded",
        "-o", "jsonpath={range .items[*]}{.metadata.namespace}/{.metadata.name}|{.status.phase}\n{end}"
    ])

    if code != 0:
        return []

    pods = []
    for line in output.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) >= 2:
            pods.append({
                "name": parts[0],
                "phase": parts[1]
            })

    return pods


def get_resource_pressure() -> dict:
    """Check for resource pressure conditions on nodes."""
    jsonpath = (
        '{range .items[*]}'
        '{.metadata.name}|'
        '{.status.conditions[?(@.type=="MemoryPressure")].status}|'
        '{.status.conditions[?(@.type=="DiskPressure")].status}|'
        '{.status.conditions[?(@.type=="PIDPressure")].status}\n'
        '{end}'
    )

    output, code = run_kubectl(["get", "nodes", "-o", f"jsonpath={jsonpath}"])

    if code != 0:
        return {}

    pressure = {
        "memory": [],
        "disk": [],
        "pid": []
    }

    for line in output.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("|")
        if len(parts) >= 4:
            name = parts[0]
            if parts[1] == "True":
                pressure["memory"].append(name)
            if parts[2] == "True":
                pressure["disk"].append(name)
            if parts[3] == "True":
                pressure["pid"].append(name)

    return pressure


def main():
    context = get_current_context()
    print(f"## Cluster Health: {context}\n")

    # Node status
    nodes = get_node_status()
    if not nodes:
        print("**Error:** Could not get node status")
        sys.exit(1)

    ready_count = sum(1 for n in nodes if n["ready"])
    total_count = len(nodes)

    print("### Nodes")
    print(f"- Ready: {ready_count}/{total_count}")

    if ready_count < total_count:
        not_ready = [n["name"] for n in nodes if not n["ready"]]
        print(f"- Not Ready: {', '.join(not_ready)}")

    # Resource pressure
    pressure = get_resource_pressure()
    has_pressure = any(pressure.values())

    if has_pressure:
        print("\n### Resource Pressure")
        if pressure["memory"]:
            print(f"- Memory: {', '.join(pressure['memory'])}")
        if pressure["disk"]:
            print(f"- Disk: {', '.join(pressure['disk'])}")
        if pressure["pid"]:
            print(f"- PID: {', '.join(pressure['pid'])}")
    else:
        print("- Pressure: None")

    # Unhealthy pods
    unhealthy = get_unhealthy_pods()

    print("\n### Pods")
    if unhealthy:
        print(f"- Unhealthy: {len(unhealthy)}")
        # Show first 5
        for pod in unhealthy[:5]:
            print(f"  - {pod['name']}: {pod['phase']}")
        if len(unhealthy) > 5:
            print(f"  - ... and {len(unhealthy) - 5} more")
    else:
        print("- Unhealthy: 0")

    # Summary
    print("\n### Summary")
    if ready_count == total_count and not unhealthy and not has_pressure:
        print("Cluster is healthy")
    else:
        issues = []
        if ready_count < total_count:
            issues.append(f"{total_count - ready_count} nodes not ready")
        if unhealthy:
            issues.append(f"{len(unhealthy)} unhealthy pods")
        if has_pressure:
            issues.append("resource pressure detected")
        print(f"Issues: {', '.join(issues)}")


if __name__ == "__main__":
    main()

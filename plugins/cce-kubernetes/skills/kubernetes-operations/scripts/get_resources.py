#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Get Kubernetes resources in compact format.

Usage:
    uv run get_resources.py <resource-type> [-n namespace] [-l label-selector]

Output:
    Compact table with name, status, age.
    Saves ~600 tokens compared to default kubectl output.
"""

import subprocess
import sys
import argparse
from datetime import datetime, timezone


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


def get_resources(resource_type: str, namespace: str, selector: str | None) -> str:
    """Get resources using jsonpath for minimal output."""

    # Different jsonpath based on resource type
    if resource_type in ["pods", "pod", "po"]:
        jsonpath = (
            '{range .items[*]}'
            '{.metadata.name}|{.status.phase}|{.metadata.creationTimestamp}\n'
            '{end}'
        )
    elif resource_type in ["deployments", "deployment", "deploy"]:
        jsonpath = (
            '{range .items[*]}'
            '{.metadata.name}|{.status.readyReplicas}/{.spec.replicas}|{.metadata.creationTimestamp}\n'
            '{end}'
        )
    elif resource_type in ["services", "service", "svc"]:
        jsonpath = (
            '{range .items[*]}'
            '{.metadata.name}|{.spec.type}|{.spec.clusterIP}|{.metadata.creationTimestamp}\n'
            '{end}'
        )
    elif resource_type in ["configmaps", "configmap", "cm"]:
        jsonpath = (
            '{range .items[*]}'
            '{.metadata.name}|{.metadata.creationTimestamp}\n'
            '{end}'
        )
    elif resource_type in ["secrets", "secret"]:
        jsonpath = (
            '{range .items[*]}'
            '{.metadata.name}|{.type}|{.metadata.creationTimestamp}\n'
            '{end}'
        )
    else:
        # Generic fallback
        jsonpath = (
            '{range .items[*]}'
            '{.metadata.name}|{.metadata.creationTimestamp}\n'
            '{end}'
        )

    args = ["get", resource_type, "-n", namespace, "-o", f"jsonpath={jsonpath}"]

    if selector:
        args.extend(["-l", selector])

    output, code = run_kubectl(args)

    if code != 0:
        return f"Error: {output.strip()}"

    return output.strip()


def format_age(timestamp: str) -> str:
    """Convert ISO timestamp to human-readable age."""
    if not timestamp:
        return "unknown"

    try:
        created = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - created

        if delta.days > 0:
            return f"{delta.days}d"
        elif delta.seconds >= 3600:
            return f"{delta.seconds // 3600}h"
        elif delta.seconds >= 60:
            return f"{delta.seconds // 60}m"
        else:
            return f"{delta.seconds}s"
    except (ValueError, TypeError):
        return timestamp[:10] if len(timestamp) > 10 else timestamp


def main():
    parser = argparse.ArgumentParser(description="Get Kubernetes resources")
    parser.add_argument("resource", help="Resource type (pods, deployments, services, etc.)")
    parser.add_argument("-n", "--namespace", default="default", help="Namespace")
    parser.add_argument("-l", "--selector", help="Label selector")
    args = parser.parse_args()

    print(f"## {args.resource} (ns: {args.namespace})\n")

    output = get_resources(args.resource, args.namespace, args.selector)

    if output.startswith("Error:"):
        print(output)
        sys.exit(1)

    if not output:
        print("No resources found")
        sys.exit(0)

    # Parse and format output
    lines = output.strip().split("\n")

    # Determine header based on resource type
    if args.resource in ["pods", "pod", "po"]:
        print("| Name | Status | Age |")
        print("|------|--------|-----|")
    elif args.resource in ["deployments", "deployment", "deploy"]:
        print("| Name | Ready | Age |")
        print("|------|-------|-----|")
    elif args.resource in ["services", "service", "svc"]:
        print("| Name | Type | ClusterIP | Age |")
        print("|------|------|-----------|-----|")
    elif args.resource in ["secrets", "secret"]:
        print("| Name | Type | Age |")
        print("|------|------|-----|")
    else:
        print("| Name | Age |")
        print("|------|-----|")

    for line in lines:
        if not line.strip():
            continue

        parts = line.split("|")

        # Format age from timestamp
        if len(parts) >= 2:
            parts[-1] = format_age(parts[-1])

        print(f"| {' | '.join(parts)} |")


if __name__ == "__main__":
    main()

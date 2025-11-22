#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Debug a Kubernetes pod with condensed output.

Usage:
    uv run debug_pod.py <pod-name> [-n namespace]

Output:
    Condensed summary with status, events, and log tail.
    Saves ~800 tokens compared to running commands separately.
"""

import subprocess
import sys
import argparse


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


def get_pod_status(pod: str, namespace: str) -> dict:
    """Get pod status using jsonpath for minimal output."""
    jsonpath = (
        '{.metadata.name}|'
        '{.status.phase}|'
        '{.status.containerStatuses[0].restartCount}|'
        '{.status.containerStatuses[0].state}|'
        '{.status.containerStatuses[0].lastState}'
    )

    args = ["get", "pod", pod, "-n", namespace, "-o", f"jsonpath={jsonpath}"]
    output, code = run_kubectl(args)

    if code != 0:
        return {"error": output.strip()}

    parts = output.split("|")
    if len(parts) >= 5:
        return {
            "name": parts[0],
            "phase": parts[1],
            "restarts": parts[2],
            "state": parts[3][:100] if parts[3] else "unknown",
            "lastState": parts[4][:100] if parts[4] else "none"
        }
    return {"error": "Could not parse pod status"}


def get_events(pod: str, namespace: str) -> list[str]:
    """Get recent events for the pod."""
    args = [
        "get", "events", "-n", namespace,
        "--field-selector", f"involvedObject.name={pod}",
        "--sort-by", ".lastTimestamp",
        "-o", "jsonpath={range .items[-5:]}{.reason}: {.message}\n{end}"
    ]
    output, code = run_kubectl(args)

    if code != 0 or not output.strip():
        return ["No recent events"]

    return [line.strip() for line in output.strip().split("\n") if line.strip()]


def get_logs(pod: str, namespace: str, previous: bool = False) -> str:
    """Get last 20 lines of logs."""
    args = ["logs", pod, "-n", namespace, "--tail=20"]
    if previous:
        args.append("--previous")

    output, code = run_kubectl(args)

    if code != 0:
        return f"Could not get logs: {output.strip()[:100]}"

    return output.strip() if output.strip() else "No logs available"


def main():
    parser = argparse.ArgumentParser(description="Debug a Kubernetes pod")
    parser.add_argument("pod", help="Pod name")
    parser.add_argument("-n", "--namespace", default="default", help="Namespace")
    args = parser.parse_args()

    print(f"## Pod Debug: {args.pod} (ns: {args.namespace})\n")

    # Status
    status = get_pod_status(args.pod, args.namespace)
    if "error" in status:
        print(f"**Error:** {status['error']}")
        sys.exit(1)

    print("### Status")
    print(f"- Phase: {status['phase']}")
    print(f"- Restarts: {status['restarts']}")
    print(f"- State: {status['state']}")
    if status['lastState'] != "none":
        print(f"- Last State: {status['lastState']}")

    # Events
    print("\n### Recent Events")
    events = get_events(args.pod, args.namespace)
    for event in events[-5:]:
        print(f"- {event}")

    # Logs
    print("\n### Logs (last 20 lines)")

    # Check if we need previous logs
    restarts = int(status['restarts']) if status['restarts'] else 0
    need_previous = "CrashLoopBackOff" in status['state'] or restarts > 0

    if need_previous:
        print("*(showing previous container logs due to restarts)*\n")
        logs = get_logs(args.pod, args.namespace, previous=True)
    else:
        logs = get_logs(args.pod, args.namespace)

    print("```")
    print(logs)
    print("```")


if __name__ == "__main__":
    main()

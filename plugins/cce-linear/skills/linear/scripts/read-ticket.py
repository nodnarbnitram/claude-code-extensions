#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Read a Linear ticket's details using linearis CLI.

Usage:
    uv run scripts/read-ticket.py ICE-2021

Returns:
    Full JSON from linearis including: identifier, title, description,
    branchName, state, team, project, projectMilestone, priority,
    labels, subIssues, comments, and url.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def check_auth() -> bool:
    """Check if Linear authentication is available."""
    if "LINEAR_API_TOKEN" in __import__("os").environ:
        return True
    token_file = Path.home() / ".linear_api_token"
    if token_file.exists():
        return True
    return False


def read_ticket(ticket_id: str) -> None:
    """Read a Linear ticket and output its details."""

    if not check_auth():
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        print("Set token: export LINEAR_API_TOKEN='lin_api_xxxxx'", file=sys.stderr)
        sys.exit(1)

    cmd = ["linearis", "issues", "read", ticket_id]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        data = json.loads(result.stdout)

        data["url"] = data.get("url", "")

        print(json.dumps(data, separators=(",", ":")))

    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr.lower() or "404" in e.stderr:
            print(f"Error: Ticket {ticket_id} not found", file=sys.stderr)
        else:
            print(f"Error running linearis: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(
            "Error: linearis CLI not found. Install with: npm install -g linearis",
            file=sys.stderr,
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Read a Linear ticket's details")
    parser.add_argument("ticket_id", help="Ticket identifier (e.g., ICE-2021)")

    args = parser.parse_args()
    read_ticket(args.ticket_id)


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Update a Linear ticket using linearis CLI.

Usage:
    uv run scripts/update-ticket.py ICE-2021 --status "In Progress"
    uv run scripts/update-ticket.py ICE-2021 --status "Done" --priority 2
    uv run scripts/update-ticket.py ICE-2021 --labels "security,urgent"

At least one update flag is required.

Returns:
    Full JSON of the updated ticket.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def check_auth() -> bool:
    if "LINEAR_API_TOKEN" in __import__("os").environ:
        return True
    token_file = Path.home() / ".linear_api_token"
    if token_file.exists():
        return True
    return False


FLAG_MAP = {
    "status": "--status",
    "priority": "--priority",
    "assignee": "--assignee",
    "labels": "--labels",
    "project": "--project",
    "project_milestone": "--project-milestone",
    "title": "--title",
    "description": "--description",
}


def update_ticket(ticket_id: str, updates: dict[str, str]) -> None:
    if not check_auth():
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        print("Set token: export LINEAR_API_TOKEN='lin_api_xxxxx'", file=sys.stderr)
        sys.exit(1)

    cmd = ["linearis", "issues", "update", ticket_id]
    for key, value in updates.items():
        if value is not None:
            cmd.extend([FLAG_MAP[key], str(value)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        data = json.loads(result.stdout)

        data["url"] = data.get("url", "")
        data["updated"] = True

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
    parser = argparse.ArgumentParser(description="Update a Linear ticket")
    parser.add_argument("ticket_id", help="Ticket identifier (e.g., ICE-2021)")
    parser.add_argument("--status", help="New status (e.g., 'In Progress', 'Done')")
    parser.add_argument(
        "--priority",
        type=int,
        choices=[1, 2, 3, 4],
        help="Priority: 1=urgent, 2=high, 3=normal, 4=low",
    )
    parser.add_argument("--assignee", help="Assignee user ID")
    parser.add_argument("--labels", help="Comma-separated label names")
    parser.add_argument("--project", help="Project name or ID")
    parser.add_argument(
        "--project-milestone", dest="project_milestone", help="Milestone name or ID"
    )
    parser.add_argument("--title", help="New title")
    parser.add_argument("--description", help="New description")

    args = parser.parse_args()

    updates = {
        k: v for k, v in vars(args).items() if k != "ticket_id" and v is not None
    }

    if not updates:
        parser.error(
            "At least one update flag is required (e.g., --status, --priority)"
        )

    update_ticket(args.ticket_id, updates)


if __name__ == "__main__":
    main()

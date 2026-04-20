#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Update a Linear ticket using the Linear GraphQL API.

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
import sys

from linear_graphql import LinearError, update_ticket


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

    try:
        issue = update_ticket(args.ticket_id, updates)
        issue["updated"] = True
        print(json.dumps(issue, separators=(",", ":")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

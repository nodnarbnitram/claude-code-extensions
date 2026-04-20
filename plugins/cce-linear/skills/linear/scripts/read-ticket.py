#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Read a Linear ticket's details using the Linear GraphQL API.

Usage:
    uv run scripts/read-ticket.py ICE-2021

Returns:
    Full ticket JSON including: identifier, title, description,
    branchName, state, team, project, projectMilestone, priority,
    labels, subIssues, comments, and url.
"""

import argparse
import json
import sys

from linear_graphql import LinearError, resolve_issue


def main():
    parser = argparse.ArgumentParser(description="Read a Linear ticket's details")
    parser.add_argument("ticket_id", help="Ticket identifier (e.g., ICE-2021)")

    args = parser.parse_args()

    try:
        issue = resolve_issue(args.ticket_id)
        print(json.dumps(issue, separators=(",", ":")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

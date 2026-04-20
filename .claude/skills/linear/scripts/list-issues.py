#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
List Linear issues for a team using the Linear GraphQL API.

Usage:
    uv run scripts/list-issues.py --team ICE-T
    uv run scripts/list-issues.py --team ICE-T --limit 50
    uv run scripts/list-issues.py --team ICE-T --status "Todo,In Progress"
    uv run scripts/list-issues.py --team ICE-T --project "Orca Security Remediation"

Returns:
    JSON array of issues, each with: identifier, title, state, priority,
    assignee, project, projectMilestone, labels, createdAt, updatedAt, url.
"""

import argparse
import json
import sys

from linear_graphql import LinearError, list_issues


def main():
    parser = argparse.ArgumentParser(
        description="List Linear issues, optionally filtered by team/status/project"
    )
    parser.add_argument("--team", help="Filter by team key or name (e.g., ICE-T)")
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=50,
        help="Max issues to fetch (default: 50)",
    )
    parser.add_argument(
        "--status",
        "-s",
        help="Filter by status (comma-separated, e.g., 'Todo,In Progress')",
    )
    parser.add_argument(
        "--project",
        help="Filter by project name or ID",
    )

    args = parser.parse_args()

    try:
        issues = list_issues(
            team=args.team,
            limit=args.limit,
            status=args.status,
            project=args.project,
        )
        print(json.dumps(issues, separators=(",", ":")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

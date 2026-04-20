#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Search Linear issues by query string using the Linear GraphQL API.

Usage:
    uv run scripts/search-issues.py "Orca Security"
    uv run scripts/search-issues.py "CVE" --team ICE-T
    uv run scripts/search-issues.py "Privileged Role" --status "Todo,Triage"
    uv run scripts/search-issues.py "Docker" --team ICE-T --limit 20

Returns:
    JSON array of matching issues, each with: identifier, title, state,
    priority, assignee, project, projectMilestone, labels, createdAt,
    updatedAt, url.
"""

import argparse
import json
import sys

from linear_graphql import LinearError, search_issues


def main():
    parser = argparse.ArgumentParser(description="Search Linear issues by query string")
    parser.add_argument("query", help="Search query (e.g., 'Orca Security', 'CVE')")
    parser.add_argument("--team", help="Filter by team key or name (e.g., ICE-T)")
    parser.add_argument(
        "--status",
        "-s",
        help="Filter by status (comma-separated, e.g., 'Todo,In Progress')",
    )
    parser.add_argument(
        "--project",
        help="Filter by project name or ID",
    )
    parser.add_argument(
        "--assignee",
        "-a",
        help="Filter by assignee user ID",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=25,
        help="Max results to return (default: 25)",
    )

    args = parser.parse_args()

    try:
        issues = search_issues(
            args.query,
            team=args.team,
            status=args.status,
            project=args.project,
            assignee=args.assignee,
            limit=args.limit,
        )
        print(json.dumps(issues, separators=(",", ":")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

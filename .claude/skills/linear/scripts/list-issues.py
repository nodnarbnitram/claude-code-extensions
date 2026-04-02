#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
List Linear issues for a team using linearis CLI.

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


def list_issues(
    team: str | None = None,
    limit: int = 50,
    status: str | None = None,
    project: str | None = None,
) -> None:
    """List Linear issues and output as JSON array."""

    if not check_auth():
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        print("Set token: export LINEAR_API_TOKEN='lin_api_xxxxx'", file=sys.stderr)
        sys.exit(1)

    # linearis issues list only supports --limit natively.
    # We fetch all and filter client-side for team/status/project.
    cmd = ["linearis", "issues", "list", "--limit", str(limit)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        data = json.loads(result.stdout)

        if not isinstance(data, list):
            data = [data]

        # Client-side filters
        filtered = data

        if team:
            team_lower = team.lower()
            filtered = [
                issue
                for issue in filtered
                if issue.get("team", {}).get("key", "").lower() == team_lower
                or issue.get("team", {}).get("name", "").lower() == team_lower
            ]

        if status:
            statuses = {s.strip().lower() for s in status.split(",")}
            filtered = [
                issue
                for issue in filtered
                if issue.get("state", {}).get("name", "").lower() in statuses
            ]

        if project:
            project_lower = project.lower()
            filtered = [
                issue
                for issue in filtered
                if issue.get("project", {}).get("name", "").lower() == project_lower
                or issue.get("project", {}).get("id", "").lower() == project_lower
            ]

        # Preserve returned URL if present
        for issue in filtered:
            issue["url"] = issue.get("url", "")

        print(json.dumps(filtered, separators=(",", ":")))

    except subprocess.CalledProcessError as e:
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

    list_issues(
        team=args.team,
        limit=args.limit,
        status=args.status,
        project=args.project,
    )


if __name__ == "__main__":
    main()

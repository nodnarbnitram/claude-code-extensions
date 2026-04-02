#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Search Linear issues by query string using linearis CLI.

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


def search_issues(
    query: str,
    team: str | None = None,
    status: str | None = None,
    project: str | None = None,
    assignee: str | None = None,
    limit: int = 25,
) -> None:
    """Search Linear issues and output as JSON array."""

    if not check_auth():
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        print("Set token: export LINEAR_API_TOKEN='lin_api_xxxxx'", file=sys.stderr)
        sys.exit(1)

    cmd = ["linearis", "issues", "search", query, "--limit", str(limit)]

    # linearis search supports these filters natively
    if team:
        cmd.extend(["--team", team])
    if status:
        cmd.extend(["--status", status])
    if project:
        cmd.extend(["--project", project])
    if assignee:
        cmd.extend(["--assignee", assignee])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        data = json.loads(result.stdout)

        if not isinstance(data, list):
            data = [data]

        # Preserve returned URL if present
        for issue in data:
            issue["url"] = issue.get("url", "")

        print(json.dumps(data, separators=(",", ":")))

    except subprocess.CalledProcessError as e:
        # linearis returns non-zero if no results found
        if "no issues found" in e.stderr.lower() or not e.stderr.strip():
            print("[]")
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

    search_issues(
        query=args.query,
        team=args.team,
        status=args.status,
        project=args.project,
        assignee=args.assignee,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()

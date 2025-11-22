#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear ticket using linearis CLI and return the ticket identifier.

Usage:
    uv run scripts/create_linear_ticket.py "Issue title" --team TeamName [options]

Options:
    --team         Team name or key (required)
    --description  Issue description
    --priority     Priority 1-4 (1=urgent, 4=low)
    --labels       Comma-separated labels
    --project      Project name
    --assignee     Assignee user ID

Returns:
    Prints the ticket identifier (e.g., ICE-1965) to stdout
"""

import argparse
import json
import subprocess
import sys


def create_ticket(
    title: str,
    team: str,
    description: str = None,
    priority: int = None,
    labels: str = None,
    project: str = None,
    assignee: str = None,
) -> str:
    """Create a Linear ticket and return its identifier."""

    cmd = ["linearis", "issues", "create", title, "--team", team]

    if description:
        cmd.extend(["--description", description])
    if priority:
        cmd.extend(["--priority", str(priority)])
    if labels:
        cmd.extend(["--labels", labels])
    if project:
        cmd.extend(["--project", project])
    if assignee:
        cmd.extend(["--assignee", assignee])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        # Parse JSON response
        data = json.loads(result.stdout)
        identifier = data.get("identifier")

        if not identifier:
            print("Error: No identifier in response", file=sys.stderr)
            print(f"Response: {result.stdout}", file=sys.stderr)
            sys.exit(1)

        return identifier

    except subprocess.CalledProcessError as e:
        print(f"Error running linearis: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: linearis CLI not found. Install with: npm install -g linearis", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a Linear ticket and return its identifier"
    )
    parser.add_argument("title", help="Issue title")
    parser.add_argument("--team", required=True, help="Team name or key")
    parser.add_argument("--description", "-d", help="Issue description")
    parser.add_argument("--priority", "-p", type=int, choices=[1, 2, 3, 4],
                        help="Priority (1=urgent, 4=low)")
    parser.add_argument("--labels", help="Comma-separated labels")
    parser.add_argument("--project", help="Project name")
    parser.add_argument("--assignee", "-a", help="Assignee user ID")

    args = parser.parse_args()

    identifier = create_ticket(
        title=args.title,
        team=args.team,
        description=args.description,
        priority=args.priority,
        labels=args.labels,
        project=args.project,
        assignee=args.assignee,
    )

    print(identifier)


if __name__ == "__main__":
    main()

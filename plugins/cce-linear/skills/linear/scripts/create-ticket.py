#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear ticket using linearis CLI.

Usage:
    uv run scripts/create-ticket.py "Issue title" --team ICE-T [options]

Options:
    --team         Team key (required)
    --description  Issue description
    --priority     Priority 1-4 (1=urgent, 4=low)
    --labels       Comma-separated labels
    --json         Output full JSON instead of just identifier

Returns:
    Without --json: Prints the ticket identifier (e.g., ICE-2021)
    With --json: Prints full JSON with identifier, title, branchName, state, url
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


def create_ticket(
    title: str,
    team: str,
    description: str | None = None,
    priority: int | None = None,
    labels: str | None = None,
    output_json: bool = False,
) -> None:
    """Create a Linear ticket and output result."""

    if not check_auth():
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        print("Set token: export LINEAR_API_TOKEN='lin_api_xxxxx'", file=sys.stderr)
        sys.exit(1)

    cmd = ["linearis", "issues", "create", title, "--team", team]

    if description:
        cmd.extend(["--description", description])
    if priority:
        cmd.extend(["--priority", str(priority)])
    if labels:
        cmd.extend(["--labels", labels])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Parse JSON response from linearis
        data = json.loads(result.stdout)

        identifier = data.get("identifier")
        if not identifier:
            print("Error: No identifier in response", file=sys.stderr)
            print(f"Response: {result.stdout}", file=sys.stderr)
            sys.exit(1)

        if output_json:
            # Build structured output
            output = {
                "identifier": identifier,
                "title": data.get("title", title),
                "branchName": data.get("branchName", ""),
                "state": data.get("state", {}).get("name", "Backlog")
                if isinstance(data.get("state"), dict)
                else data.get("state", "Backlog"),
                "url": data.get("url", ""),
            }
            print(json.dumps(output, separators=(",", ":")))
        else:
            print(identifier)

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
        description="Create a Linear ticket and return its identifier"
    )
    parser.add_argument("title", help="Issue title")
    parser.add_argument("--team", required=True, help="Team key (e.g., ICE-T)")
    parser.add_argument("--description", "-d", help="Issue description")
    parser.add_argument(
        "--priority",
        "-p",
        type=int,
        choices=[1, 2, 3, 4],
        help="Priority (1=urgent, 4=low)",
    )
    parser.add_argument("--labels", help="Comma-separated labels")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output full JSON instead of just identifier",
    )

    args = parser.parse_args()

    create_ticket(
        title=args.title,
        team=args.team,
        description=args.description,
        priority=args.priority,
        labels=args.labels,
        output_json=args.output_json,
    )


if __name__ == "__main__":
    main()

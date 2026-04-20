#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear ticket using the Linear GraphQL API.

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
import sys

from linear_graphql import LinearError, create_ticket


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

    try:
        issue = create_ticket(
            args.title,
            args.team,
            description=args.description,
            priority=args.priority,
            labels=args.labels,
        )

        if args.output_json:
            output = {
                "identifier": issue.get("identifier"),
                "title": issue.get("title", args.title),
                "branchName": issue.get("branchName", ""),
                "state": issue.get("state", {}).get("name", "Backlog"),
                "url": issue.get("url", ""),
            }
            print(json.dumps(output, separators=(",", ":")))
        else:
            print(issue.get("identifier", ""))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

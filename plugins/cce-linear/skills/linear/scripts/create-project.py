#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear project using the Linear GraphQL API.

Usage:
    uv run scripts/create-project.py "Project name" --team ICE-T [options]

Options:
    --team          Team key (required)
    --description   Short description (max 255 chars, shown in list views)
    --content       Full project content (markdown, shown in project page)
    --priority      Priority 0-4 (0=none, 1=urgent, 4=low)
    --target-date   Target date (YYYY-MM-DD)
    --json          Output full JSON instead of just ID

Returns:
    Without --json: Prints the project ID
    With --json: Prints full JSON with id, name, url, etc.

Note:
    This script uses the Linear GraphQL API directly.
"""

import argparse
import json
import sys

from linear_graphql import LinearError, create_project


def main():
    parser = argparse.ArgumentParser(
        description="Create a Linear project and return its ID"
    )
    parser.add_argument("name", help="Project name")
    parser.add_argument("--team", required=True, help="Team key (e.g., ICE-T)")
    parser.add_argument("--description", "-d", help="Short description (max 255 chars)")
    parser.add_argument("--content", "-c", help="Full project content (markdown)")
    parser.add_argument(
        "--priority",
        "-p",
        type=int,
        choices=[0, 1, 2, 3, 4],
        help="Priority (0=none, 1=urgent, 4=low)",
    )
    parser.add_argument("--target-date", help="Target date (YYYY-MM-DD)")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output full JSON instead of just ID",
    )

    args = parser.parse_args()

    try:
        project = create_project(
            args.name,
            args.team,
            description=args.description,
            content=args.content,
            priority=args.priority,
            target_date=args.target_date,
        )
        if args.output_json:
            print(json.dumps(project, separators=(",", ":")))
        else:
            print(project.get("id", ""))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear project milestone using the GraphQL API.

Usage:
    uv run scripts/create-milestone.py "Milestone name" --project PROJECT_ID [options]

Options:
    --project       Project UUID (required)
    --description   Milestone description
    --target-date   Target date (YYYY-MM-DD)
    --json          Output full JSON instead of just ID

Returns:
    Without --json: Prints the milestone ID
    With --json: Prints full JSON with id, name, targetDate, etc.

Note:
    This script uses the Linear GraphQL API directly.

Schema Reference:
    https://studio.apollographql.com/public/Linear-API/variant/current/schema/reference
"""

import argparse
import json
import sys

from linear_graphql import LinearError, create_milestone


def main():
    parser = argparse.ArgumentParser(
        description="Create a Linear project milestone and return its ID"
    )
    parser.add_argument("name", help="Milestone name")
    parser.add_argument("--project", required=True, help="Project UUID")
    parser.add_argument("--description", "-d", help="Milestone description")
    parser.add_argument("--target-date", help="Target date (YYYY-MM-DD)")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="output_json",
        help="Output full JSON instead of just ID",
    )

    args = parser.parse_args()

    try:
        milestone = create_milestone(
            args.name,
            args.project,
            description=args.description,
            target_date=args.target_date,
        )
        if args.output_json:
            print(json.dumps(milestone, separators=(",", ":")))
        else:
            print(milestone.get("id", ""))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Add a comment to a Linear ticket using the Linear GraphQL API.

Usage:
    uv run scripts/add-comment.py ICE-2021 "Fixed in PR #123"

Arguments:
    ticket_id   Ticket identifier (e.g., ICE-2021)
    body        Comment text

Returns:
    JSON confirmation with ticket ID and comment status
"""

import argparse
import json
import sys

from linear_graphql import LinearError, add_comment


def main():
    parser = argparse.ArgumentParser(description="Add a comment to a Linear ticket")
    parser.add_argument("ticket_id", help="Ticket identifier (e.g., ICE-2021)")
    parser.add_argument("body", help="Comment text")

    args = parser.parse_args()

    try:
        result = add_comment(args.ticket_id, args.body)
        print(json.dumps(result, separators=(",", ":")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

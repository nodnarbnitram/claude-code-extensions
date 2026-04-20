#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
List Linear documents using the GraphQL API.

Usage:
    uv run scripts/list-documents.py --project PROJECT_ID
    uv run scripts/list-documents.py --project "Security Remediation" --limit 100

Returns:
    JSON object with `nodes` and `pageInfo`.
"""

import argparse
import json
import sys

from linear_graphql import LinearError, list_documents


def main():
    parser = argparse.ArgumentParser(description="List Linear documents")
    parser.add_argument("--project", help="Filter by project name or ID")
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=50,
        help="Max documents to fetch (default: 50)",
    )

    args = parser.parse_args()

    try:
        documents = list_documents(project=args.project, limit=args.limit)
        print(json.dumps(documents, separators=(",", ":")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Read a Linear document using the GraphQL API.

Usage:
    uv run scripts/read-document.py DOCUMENT_ID
"""

import argparse
import json
import sys

from linear_graphql import LinearError, read_document


def main():
    parser = argparse.ArgumentParser(description="Read a Linear document")
    parser.add_argument("document_id", help="Document UUID")

    args = parser.parse_args()

    try:
        document = read_document(args.document_id)
        print(json.dumps(document, separators=(",", ":")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

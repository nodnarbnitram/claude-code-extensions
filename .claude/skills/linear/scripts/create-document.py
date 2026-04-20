#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear document attached to a project using the GraphQL API.

Usage:
    uv run scripts/create-document.py --title "Doc Title" --project PROJECT_ID [options]
    uv run scripts/create-document.py --title "Doc Title" --project PROJECT_ID --content-file report.md

Options:
    --title         Document title (required)
    --project       Project name or ID (required)
    --content       Document content (markdown)
    --content-file  Read content from file
    --json          Output full JSON

Returns:
    Without --json: Prints the document URL
    With --json: Prints full JSON with id, title, url, etc.
"""

import argparse
import json
import sys
from pathlib import Path

from linear_graphql import LinearError, create_document


def main():
    parser = argparse.ArgumentParser(description="Create a Linear document")
    parser.add_argument("--title", required=True, help="Document title")
    parser.add_argument("--project", required=True, help="Project name or ID")
    parser.add_argument("--content", help="Document content (markdown)")
    parser.add_argument("--content-file", help="Read content from file")
    parser.add_argument("--json", action="store_true", dest="output_json")

    args = parser.parse_args()

    content = args.content
    if args.content_file:
        content_path = Path(args.content_file)
        if not content_path.exists():
            print(f"Error: File not found: {args.content_file}", file=sys.stderr)
            sys.exit(1)
        content = content_path.read_text()

    try:
        document = create_document(
            title=args.title,
            project=args.project,
            content=content,
        )

        if args.output_json:
            output = {
                "id": document.get("id"),
                "title": document.get("title"),
                "url": document.get("url"),
                "project": document.get("project"),
            }
            print(json.dumps(output, separators=(",", ":")))
        else:
            print(document.get("url", document.get("id", "")))
    except LinearError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

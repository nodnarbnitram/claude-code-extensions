#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear document attached to a project.

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
import subprocess
import sys
from pathlib import Path


def check_auth() -> bool:
    if "LINEAR_API_TOKEN" in __import__("os").environ:
        return True
    token_file = Path.home() / ".linear_api_token"
    return token_file.exists()


def create_document(
    title: str,
    project: str,
    content: str | None = None,
    output_json: bool = False,
) -> None:
    if not check_auth():
        print("Error: LINEAR_API_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    cmd = ["linearis", "documents", "create", "--title", title, "--project", project]

    if content:
        cmd.extend(["--content", content])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)

        if output_json:
            output = {
                "id": data.get("id"),
                "title": data.get("title"),
                "url": data.get("url"),
                "project": data.get("project", {}).get("name"),
            }
            print(json.dumps(output, separators=(",", ":")))
        else:
            print(data.get("url", data.get("id")))

    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: linearis CLI not found", file=sys.stderr)
        sys.exit(1)


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

    create_document(
        title=args.title,
        project=args.project,
        content=content,
        output_json=args.output_json,
    )


if __name__ == "__main__":
    main()

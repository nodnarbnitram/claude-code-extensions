#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Add a comment to a Linear ticket using linearis CLI.

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


def add_comment(ticket_id: str, body: str) -> None:
    """Add a comment to a Linear ticket."""

    if not check_auth():
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        print("Set token: export LINEAR_API_TOKEN='lin_api_xxxxx'", file=sys.stderr)
        sys.exit(1)

    cmd = ["linearis", "comments", "create", ticket_id, "--body", body]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # linearis may or may not return JSON for comments
        # Handle both cases
        try:
            data = json.loads(result.stdout)
            output = {
                "ticket": ticket_id,
                "commented": True,
                "commentId": data.get("id", ""),
                "url": data.get("url", "") or data.get("issue", {}).get("url", ""),
            }
        except json.JSONDecodeError:
            # If no JSON response, just confirm success
            output = {
                "ticket": ticket_id,
                "commented": True,
                "url": "",
            }

        print(json.dumps(output, separators=(",", ":")))

    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr.lower() or "404" in e.stderr:
            print(f"Error: Ticket {ticket_id} not found", file=sys.stderr)
        else:
            print(f"Error running linearis: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(
            "Error: linearis CLI not found. Install with: npm install -g linearis",
            file=sys.stderr,
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Add a comment to a Linear ticket")
    parser.add_argument("ticket_id", help="Ticket identifier (e.g., ICE-2021)")
    parser.add_argument("body", help="Comment text")

    args = parser.parse_args()
    add_comment(args.ticket_id, args.body)


if __name__ == "__main__":
    main()

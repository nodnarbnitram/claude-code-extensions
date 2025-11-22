#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a git branch from a ticket identifier with GitHub username prefix.

Usage:
    uv run scripts/create_branch.py ICE-1965
    uv run scripts/create_branch.py ICE-1965 --push
    uv run scripts/create_branch.py ICE-1965 --username myuser

Branch format: username/identifier (e.g., nodnarbnitram/ICE-1965)

Options:
    --push      Push the branch to origin with upstream tracking
    --username  Override GitHub username

Returns:
    Prints the full branch name to stdout
"""

import argparse
import json
import subprocess
import sys


def get_github_username() -> str:
    """Get the GitHub username from gh auth status."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status", "--json", "hosts"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        # Extract username from the first host (usually github.com)
        hosts = data.get("hosts", {})
        for accounts in hosts.values():
            # accounts is a list of auth entries for this host
            for account in accounts:
                if account.get("active"):
                    username = account.get("login")
                    if username:
                        return username
            # Fallback to first account if none active
            if accounts and accounts[0].get("login"):
                return accounts[0]["login"]

        print("Error: Could not find GitHub username in auth status", file=sys.stderr)
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Error getting GitHub username: {e.stderr}", file=sys.stderr)
        print("Make sure you're logged in with: gh auth login", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing gh auth output: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: gh CLI not found. Install from: https://cli.github.com/", file=sys.stderr)
        sys.exit(1)


def create_branch(identifier: str, username: str = None, push: bool = False) -> str:
    """Create a git branch with username/identifier format."""

    if not username:
        username = get_github_username()

    # Build branch name: username/identifier
    branch_name = f"{username}/{identifier}"

    try:
        # Create and checkout branch
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            check=True,
            capture_output=True,
            text=True
        )

        if push:
            # Push with upstream tracking
            subprocess.run(
                ["git", "push", "-u", "origin", branch_name],
                check=True,
                capture_output=True,
                text=True
            )

        return branch_name

    except subprocess.CalledProcessError as e:
        print(f"Git error: {e.stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a git branch with username/identifier format"
    )
    parser.add_argument("identifier", help="Ticket identifier (e.g., ICE-1965)")
    parser.add_argument("--push", action="store_true",
                        help="Push branch to origin with upstream tracking")
    parser.add_argument("--username", help="Override GitHub username")

    args = parser.parse_args()

    branch_name = create_branch(
        identifier=args.identifier,
        username=args.username,
        push=args.push
    )

    print(branch_name)


if __name__ == "__main__":
    main()

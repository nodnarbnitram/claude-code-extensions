#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Create a Linear project using the GraphQL API.

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
    The linearis CLI only supports listing projects, not creating them.
    This script uses the Linear GraphQL API directly.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def get_api_token() -> str | None:
    """Get Linear API token from environment or file."""
    if token := os.environ.get("LINEAR_API_TOKEN"):
        return token
    token_file = Path.home() / ".linear_api_token"
    if token_file.exists():
        return token_file.read_text().strip()
    return None


def get_team_id(team_key: str) -> str | None:
    """Get team UUID from team key using linearis CLI."""
    try:
        result = subprocess.run(
            ["linearis", "teams", "list"],
            capture_output=True,
            text=True,
            check=True,
        )
        teams = json.loads(result.stdout)
        for team in teams:
            if team.get("key") == team_key or team.get("name") == team_key:
                return team.get("id")
        return None
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return None


def create_project(
    name: str,
    team: str,
    description: str | None = None,
    content: str | None = None,
    priority: int | None = None,
    target_date: str | None = None,
    output_json: bool = False,
) -> None:
    """Create a Linear project using GraphQL API."""

    token = get_api_token()
    if not token:
        print(
            "Error: LINEAR_API_TOKEN not set and ~/.linear_api_token not found",
            file=sys.stderr,
        )
        sys.exit(1)

    # Get team ID
    team_id = get_team_id(team)
    if not team_id:
        print(f"Error: Team '{team}' not found", file=sys.stderr)
        sys.exit(1)

    # Build GraphQL mutation
    mutation = """
    mutation CreateProject($input: ProjectCreateInput!) {
      projectCreate(input: $input) {
        success
        project {
          id
          name
          description
          content
          state
          url
        }
      }
    }
    """

    variables = {
        "input": {
            "teamIds": [team_id],
            "name": name,
        }
    }

    if description:
        # Linear has 255 char limit on description
        if len(description) > 255:
            print(
                f"Warning: Description truncated to 255 chars (was {len(description)})",
                file=sys.stderr,
            )
            description = description[:252] + "..."
        variables["input"]["description"] = description

    if priority is not None:
        variables["input"]["priority"] = priority

    if target_date:
        variables["input"]["targetDate"] = target_date

    # Make GraphQL request
    payload = json.dumps({"query": mutation, "variables": variables})

    try:
        result = subprocess.run(
            [
                "curl",
                "-s",
                "-X",
                "POST",
                "https://api.linear.app/graphql",
                "-H",
                "Content-Type: application/json",
                "-H",
                f"Authorization: {token}",
                "-d",
                payload,
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        if "errors" in data:
            print(f"Error: {data['errors'][0]['message']}", file=sys.stderr)
            sys.exit(1)

        project = data["data"]["projectCreate"]["project"]
        project_id = project["id"]

        # If content provided, update project with content (separate mutation)
        if content:
            update_content(token, project_id, content)

        if output_json:
            print(json.dumps(project, separators=(",", ":")))
        else:
            print(project_id)

    except subprocess.CalledProcessError as e:
        print(f"Error making API request: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}", file=sys.stderr)
        sys.exit(1)


def update_content(token: str, project_id: str, content: str) -> None:
    """Update project content using GraphQL API."""
    mutation = """
    mutation UpdateProject($id: String!, $input: ProjectUpdateInput!) {
      projectUpdate(id: $id, input: $input) {
        success
      }
    }
    """

    variables = {"id": project_id, "input": {"content": content}}

    payload = json.dumps({"query": mutation, "variables": variables})

    subprocess.run(
        [
            "curl",
            "-s",
            "-X",
            "POST",
            "https://api.linear.app/graphql",
            "-H",
            "Content-Type: application/json",
            "-H",
            f"Authorization: {token}",
            "-d",
            payload,
        ],
        capture_output=True,
        text=True,
        check=True,
    )


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

    create_project(
        name=args.name,
        team=args.team,
        description=args.description,
        content=args.content,
        priority=args.priority,
        target_date=args.target_date,
        output_json=args.output_json,
    )


if __name__ == "__main__":
    main()

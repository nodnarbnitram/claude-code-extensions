#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from pathlib import Path

# noqa: E402 - sys.path modification needed before imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.state import (  # noqa: E402
    read_state,
    update_blog_status,
)


def extract_session_id(hook_input: dict) -> str:
    """Extract session_id from hook input, checking both camelCase and snake_case."""
    return hook_input.get("sessionId") or hook_input.get("session_id") or ""


def find_blog_by_session_id(session_id: str) -> tuple[str | None, dict]:
    """
    Find blog entry with matching session_id.

    Args:
        session_id: The session ID to search for

    Returns:
        Tuple of (blog_id, metadata) if found, (None, {}) if not found
    """
    state = read_state()
    for blog_id, metadata in state["blogs"].items():
        if metadata.get("session_id") == session_id:
            return blog_id, metadata
    return None, {}


def main():
    try:
        # Read JSON from stdin (hook protocol requirement)
        hook_input = json.load(sys.stdin)

        # Extract session_id from hook input
        session_id = extract_session_id(hook_input)
        if not session_id:
            sys.exit(0)

        # Find blog with matching session_id
        blog_id, metadata = find_blog_by_session_id(session_id)
        if not blog_id:
            # No blog found for this session - exit silently
            sys.exit(0)

        # Update blog status to "captured"
        update_blog_status(blog_id, "captured")

        print(f"Blog session captured: {blog_id}")

        sys.exit(0)

    except Exception:
        # Silent failure - hook protocol pattern
        sys.exit(0)


if __name__ == "__main__":
    main()

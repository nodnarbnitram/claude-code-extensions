#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.state import read_state, update_blog_status


def extract_session_id(hook_input: dict) -> str:
    return hook_input.get("sessionId") or hook_input.get("session_id") or ""


def find_blog_by_session_id(session_id: str) -> str | None:
    state = read_state()
    for blog_id, metadata in state.get("blogs", {}).items():
        if metadata.get("session_id") == session_id:
            return blog_id
    return None


def main():
    try:
        hook_input = json.load(sys.stdin)

        session_id = extract_session_id(hook_input)
        if not session_id:
            sys.exit(0)

        blog_id = find_blog_by_session_id(session_id)
        if not blog_id:
            sys.exit(0)

        update_blog_status(blog_id, "captured")
        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()

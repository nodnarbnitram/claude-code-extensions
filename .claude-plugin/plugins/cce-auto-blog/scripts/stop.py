#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

# noqa: E402 - sys.path modification needed before imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.state import (  # noqa: E402
    read_state,
    write_state,
    increment_sequence_id,
)


def extract_session_id(hook_input: dict) -> str:
    """Extract session_id from hook input, checking both camelCase and snake_case."""
    return hook_input.get("sessionId") or hook_input.get("session_id") or ""


def extract_transcript_path(hook_input: dict) -> str:
    """Extract transcript_path from hook input, checking both camelCase and snake_case."""
    return hook_input.get("transcriptPath") or hook_input.get("transcript_path") or ""


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


def copy_transcript_to_blog(
    transcript_path: str, blog_id: str, sequence_id: int
) -> str | None:
    """
    Copy transcript file to blog's transcripts directory.

    Args:
        transcript_path: Path to source transcript file
        blog_id: The blog ID to copy to
        sequence_id: Sequence number for naming

    Returns:
        The destination path if successful, None if file doesn't exist or copy fails
    """
    try:
        source = Path(transcript_path)
        if not source.exists():
            # Gracefully handle missing transcript file
            return None

        # Create destination path: .blog/{blog_id}/transcripts/{seq:03d}-{timestamp}.jsonl
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest_dir = Path(".blog") / blog_id / "transcripts"
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / f"{sequence_id:03d}-{timestamp}.jsonl"

        # Copy transcript file
        shutil.copy2(source, dest_path)
        return str(dest_path)

    except Exception:
        # Gracefully handle copy errors
        return None


def update_blog_with_transcript(blog_id: str, transcript_path: str) -> None:
    """
    Update blog metadata with transcript_path.

    Args:
        blog_id: The blog ID to update
        transcript_path: The path to the transcript file
    """
    state = read_state()
    if blog_id in state["blogs"]:
        state["blogs"][blog_id]["transcript_path"] = transcript_path
        write_state(state)


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

        # Get next sequence ID and increment
        sequence_id = increment_sequence_id()

        # Extract transcript path from hook input
        transcript_path = extract_transcript_path(hook_input)

        # Copy transcript to blog directory if path provided
        if transcript_path:
            dest_path = copy_transcript_to_blog(transcript_path, blog_id, sequence_id)
            if dest_path:
                # Update blog metadata with transcript path
                update_blog_with_transcript(blog_id, dest_path)

        # Silent success
        sys.exit(0)

    except Exception:
        # Silent failure - hook protocol pattern
        sys.exit(0)


if __name__ == "__main__":
    main()

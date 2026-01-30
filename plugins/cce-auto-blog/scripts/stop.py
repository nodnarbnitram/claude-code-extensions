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

sys.path.insert(0, str(Path(__file__).parent))

from utils.state import read_state, write_state, increment_sequence_id, get_base_dir


def extract_session_id(hook_input: dict) -> str:
    return hook_input.get("sessionId") or hook_input.get("session_id") or ""


def extract_transcript_path(hook_input: dict) -> str:
    return hook_input.get("transcriptPath") or hook_input.get("transcript_path") or ""


def find_blog_by_session_id(session_id: str) -> tuple[str | None, dict | None]:
    state = read_state()
    for blog_id, metadata in state.get("blogs", {}).items():
        if (
            metadata.get("session_id") == session_id
            and metadata.get("status") == "draft"
        ):
            return blog_id, dict(metadata)
    return None, None


def copy_transcript_to_blog(
    transcript_path: str, blog_id: str, sequence_id: int
) -> str | None:
    try:
        source = Path(transcript_path)
        if not source.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest_dir = get_base_dir() / ".blog" / blog_id / "transcripts"
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_path = dest_dir / f"{sequence_id:03d}-{timestamp}.jsonl"
        shutil.copy2(source, dest_path)
        return str(dest_path)
    except Exception:
        return None


def update_blog_with_transcript(blog_id: str, transcript_path: str) -> None:
    state = read_state()
    if blog_id in state["blogs"]:
        state["blogs"][blog_id]["transcript_path"] = transcript_path
        write_state(state)


def main():
    try:
        hook_input = json.load(sys.stdin)

        session_id = extract_session_id(hook_input)
        if not session_id:
            sys.exit(0)

        blog_id, _ = find_blog_by_session_id(session_id)
        if not blog_id:
            sys.exit(0)

        sequence_id = increment_sequence_id()
        transcript_path = extract_transcript_path(hook_input)

        if transcript_path:
            saved_path = copy_transcript_to_blog(transcript_path, blog_id, sequence_id)
            if saved_path:
                update_blog_with_transcript(blog_id, saved_path)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()

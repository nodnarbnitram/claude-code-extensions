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

from utils.state import (
    read_state,
    write_state,
    increment_sequence_id,
)
from utils.ai import invoke_ai_background


def extract_session_id(hook_input: dict) -> str:
    return hook_input.get("sessionId") or hook_input.get("session_id") or ""


def extract_transcript_path(hook_input: dict) -> str:
    return hook_input.get("transcriptPath") or hook_input.get("transcript_path") or ""


def find_blog_by_session_id(session_id: str) -> tuple[str | None, dict]:
    state = read_state()
    for blog_id, metadata in state["blogs"].items():
        if metadata.get("session_id") == session_id:
            return blog_id, metadata
    return None, {}


def copy_transcript_to_blog(
    transcript_path: str, blog_id: str, sequence_id: int
) -> str | None:
    try:
        source = Path(transcript_path)
        if not source.exists():
            return None

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest_dir = Path(".blog") / blog_id / "transcripts"
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


def generate_note_path(blog_id: str, sequence_id: int) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    notes_dir = Path(".blog") / blog_id / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    return str(notes_dir / f"{sequence_id:03d}-{timestamp}.mdx")


AI_SUMMARIZE_PROMPT = """Summarize this coding session transcript into structured blog notes.

Extract:
1. Key accomplishments and decisions made
2. Problems solved and how
3. Code patterns or techniques used
4. Lessons learned

Format as markdown with clear sections.
Be concise - focus on insights, not debugging noise.

Start your response with YAML frontmatter in this format:
---
title: "A descriptive title based on the main accomplishment"
tags: ["tag1", "tag2"]
---

Then provide the markdown content."""


def main():
    try:
        hook_input = json.load(sys.stdin)

        session_id = extract_session_id(hook_input)
        if not session_id:
            sys.exit(0)

        blog_id, metadata = find_blog_by_session_id(session_id)
        if not blog_id:
            sys.exit(0)

        sequence_id = increment_sequence_id()
        transcript_path = extract_transcript_path(hook_input)

        if transcript_path:
            dest_path = copy_transcript_to_blog(transcript_path, blog_id, sequence_id)
            if dest_path:
                update_blog_with_transcript(blog_id, dest_path)
                print(f"Captured session transcript for blog: {blog_id}")

                note_path = generate_note_path(blog_id, sequence_id)
                invoke_ai_background(AI_SUMMARIZE_PROMPT, dest_path, note_path)
                print("Generating blog notes in background...")
            else:
                print(f"Warning: Could not copy transcript for blog: {blog_id}")
        else:
            print(f"No transcript path provided for blog: {blog_id}")

        sys.exit(0)

    except Exception as e:
        print(f"Stop hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from datetime import datetime
from pathlib import Path

# noqa: E402 - sys.path modification needed before imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.state import (  # noqa: E402
    create_blog_dir,
    add_blog_to_state,
)


def detect_blog_trigger(prompt: str) -> bool:
    """
    Check if user prompt contains blog trigger keywords.

    Detects: "#blog", "blog this", "write blog" (case-insensitive)

    Args:
        prompt: The user prompt text to check

    Returns:
        bool: True if blog trigger keywords found, False otherwise
    """
    if not prompt:
        return False

    # Convert to lowercase for case-insensitive matching
    prompt_lower = prompt.lower()

    # Check for trigger keywords
    triggers = ["#blog", "blog this", "write blog"]
    return any(trigger in prompt_lower for trigger in triggers)


def extract_session_id(hook_input: dict) -> str:
    """Extract session_id from hook input, checking both camelCase and snake_case."""
    return hook_input.get("sessionId") or hook_input.get("session_id") or ""


def extract_title_from_prompt(prompt: str) -> str:
    """
    Extract title from prompt intelligently.

    Strategy:
    1. Strip #blog and trigger keywords
    2. Find first sentence (ends with . ? !)
    3. If no sentence boundary, use first 50 chars
    4. Capitalize first letter
    """
    if not prompt:
        return ""

    # Strip #blog and common trigger keywords
    text = (
        prompt.replace("#blog", "").replace("blog this", "").replace("write blog", "")
    )
    text = text.strip()

    if not text:
        return ""

    # Find first sentence boundary (. ? !)
    for i, char in enumerate(text):
        if char in ".?!":
            sentence = text[:i].strip()
            if sentence:
                return sentence.capitalize()

    # No sentence boundary - use first 50 chars
    title = text[:50].strip()
    return title.capitalize() if title else ""


def generate_blog_id() -> str:
    """Generate a unique blog ID using timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"blog-{timestamp}"


def main():
    try:
        # Read JSON from stdin (hook protocol requirement)
        hook_input = json.load(sys.stdin)

        # Extract user prompt from hook input
        prompt = hook_input.get("prompt", "")

        # Check if prompt contains blog trigger keywords
        if not detect_blog_trigger(prompt):
            sys.exit(0)

        # Blog trigger detected - extract session_id and title
        session_id = extract_session_id(hook_input)
        extracted_title = extract_title_from_prompt(prompt)

        # Create blog entry
        blog_id = generate_blog_id()
        create_blog_dir(blog_id)

        # Create metadata with session_id and extracted title
        metadata = {
            "title": extracted_title or f"Blog Post - {blog_id}",
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "transcript_path": "",
            "session_path": "",
            "session_id": session_id,
            "extracted_title": extracted_title,
        }

        # Add blog to state
        add_blog_to_state(blog_id, metadata)

        # Silent success
        sys.exit(0)

    except Exception:
        # Silent failure - hook protocol pattern
        sys.exit(0)


if __name__ == "__main__":
    main()

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


def generate_blog_id() -> str:
    """
    Generate a unique blog ID using timestamp.

    Format: blog-YYYYMMDD-HHMMSS

    Returns:
        str: A unique blog ID
    """
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"blog-{timestamp}"


def main():
    try:
        # Read JSON from stdin (hook protocol requirement)
        hook_input = json.load(sys.stdin)

        # Extract user prompt from hook input
        # Hook input format: {"prompt": "user text", ...}
        prompt = hook_input.get("prompt", "")

        # Check if prompt contains blog trigger keywords
        if not detect_blog_trigger(prompt):
            # No blog trigger - exit silently
            sys.exit(0)

        # Blog trigger detected - create blog entry
        blog_id = generate_blog_id()

        # Create blog directory structure
        create_blog_dir(blog_id)

        # Create placeholder metadata
        metadata = {
            "title": f"Blog Post - {blog_id}",
            "created_at": datetime.now().isoformat(),
            "status": "draft",
            "transcript_path": "",
            "session_path": "",
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

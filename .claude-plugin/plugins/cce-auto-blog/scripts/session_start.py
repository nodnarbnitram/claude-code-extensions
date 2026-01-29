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

from utils.state import ensure_blog_dir, read_state, write_state  # noqa: E402


def main():
    try:
        # Read JSON from stdin (hook protocol requirement)
        json.load(sys.stdin)

        # Initialize blog directory structure
        ensure_blog_dir()

        # Initialize or read blog state and persist it
        state = read_state()
        write_state(state)

        # Silent success
        sys.exit(0)
    except Exception:
        # Silent failure - hook protocol pattern
        sys.exit(0)


if __name__ == "__main__":
    main()

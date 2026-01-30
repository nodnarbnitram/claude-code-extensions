#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.state import ensure_blog_dir, read_state, write_state


def main():
    try:
        json.load(sys.stdin)
        ensure_blog_dir()
        state = read_state()
        write_state(state)
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()

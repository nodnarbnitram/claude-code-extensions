"""State management utilities for auto-blog plugin."""

from pathlib import Path


def ensure_blog_dir() -> Path:
    """
    Ensure .blog/ directory exists, creating it if necessary.

    Handles first-run scenario gracefully by creating the directory
    with all parent directories if they don't exist.

    Returns:
        Path: The .blog directory path

    Raises:
        OSError: If directory creation fails due to permissions or other OS errors
    """
    blog_dir = Path(".blog")
    blog_dir.mkdir(parents=True, exist_ok=True)
    return blog_dir

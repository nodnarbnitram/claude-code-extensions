"""State management utilities for auto-blog plugin."""

from pathlib import Path
from typing import TypedDict


class BlogMetadata(TypedDict):
    """Metadata for a single blog entry.

    Tracks essential information about a blog post being tracked,
    including creation timestamp, current status, and file paths.
    """

    title: str
    created_at: str
    status: str
    transcript_path: str
    session_path: str


class BlogState(TypedDict):
    """Root state schema for state.json.

    Manages global blog tracking state including the next sequence ID
    and a mapping of blog IDs to their metadata.
    """

    next_sequence_id: int
    blogs: dict[str, BlogMetadata]


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

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


def read_state() -> BlogState:
    """
    Read blog state from .blog/state.json.

    Handles first-run scenario by creating default state if file doesn't exist.
    Gracefully handles JSON parse errors by returning default state.

    Returns:
        BlogState: The current blog state with next_sequence_id and blogs mapping

    Raises:
        OSError: If directory creation fails due to permissions or other OS errors
    """
    import json

    blog_dir = ensure_blog_dir()
    state_path = blog_dir / "state.json"

    # First-run: create default state if file doesn't exist
    if not state_path.exists():
        default_state: BlogState = {"next_sequence_id": 1, "blogs": {}}
        return default_state

    # Read existing state
    try:
        with open(state_path, "r") as f:
            state = json.load(f)
            return state
    except (json.JSONDecodeError, IOError):
        # Gracefully handle parse errors by returning default state
        default_state: BlogState = {"next_sequence_id": 1, "blogs": {}}
        return default_state


def write_state(state: BlogState) -> None:
    """
    Write blog state to .blog/state.json using atomic write pattern.

    Uses tempfile + os.replace() for atomic writes to prevent corruption
    if the process is interrupted during write.

    Args:
        state: The BlogState to persist

    Raises:
        OSError: If directory creation or file operations fail
    """
    import json
    import os
    import tempfile

    blog_dir = ensure_blog_dir()
    state_path = blog_dir / "state.json"

    # Atomic write: tempfile in .blog/ + os.replace()
    with tempfile.NamedTemporaryFile(
        "w", dir=str(blog_dir), delete=False, suffix=".json"
    ) as f:
        json.dump(state, f, indent=2)
        temp_path = f.name

    # Atomic replace
    os.replace(temp_path, state_path)


def backup_state() -> Path:
    """
    Create a timestamped backup of state.json for disaster recovery.

    Copies .blog/state.json to .blog/state.json.bak.{timestamp} using
    shutil.copy2 to preserve metadata. Enables recovery from accidental
    state corruption or data loss.

    Returns:
        Path: The backup file path

    Raises:
        OSError: If backup creation fails due to permissions or I/O errors
    """
    import shutil
    from datetime import datetime

    blog_dir = ensure_blog_dir()
    state_path = blog_dir / "state.json"

    # Generate timestamp for unique backup filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = blog_dir / f"state.json.bak.{timestamp}"

    # Copy with metadata preservation
    if state_path.exists():
        shutil.copy2(state_path, backup_path)

    return backup_path


def restore_state() -> bool:
    """
    Restore state from the most recent backup file.

    Finds the most recent .blog/state.json.bak.* file and restores it
    using write_state() for atomic writes. Enables recovery from
    accidental state corruption.

    Returns:
        bool: True if restore succeeded, False if no backup found

    Raises:
        OSError: If restore operation fails due to permissions or I/O errors
    """
    import json

    blog_dir = ensure_blog_dir()

    # Find all backup files and sort by modification time (newest first)
    backup_files = sorted(
        blog_dir.glob("state.json.bak.*"), key=lambda p: p.stat().st_mtime, reverse=True
    )

    if not backup_files:
        return False

    # Restore from most recent backup
    most_recent_backup = backup_files[0]
    with open(most_recent_backup, "r") as f:
        state = json.load(f)

    write_state(state)
    return True

"""Note capture utilities for auto-blog plugin.

Provides functions for parsing, storing, and retrieving blog notes with
metadata management and sequence numbering.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import TypedDict

from .state import create_blog_dir, get_next_sequence_id, increment_sequence_id


class NoteMetadata(TypedDict):
    """Metadata for a single note.

    Tracks essential information about a note including creation timestamp,
    tags, and sequence number for ordering.
    """

    title: str
    created_at: str
    tags: list[str]
    sequence_id: int


def parse_note(content: str) -> dict:
    """Parse note content and extract title, body, and tags.

    Extracts the first line as title (or first 50 chars if no newline),
    identifies #hashtags as tags, and returns structured note data.

    Args:
        content: Raw note content as string

    Returns:
        dict with keys:
        - title: str - First line or first 50 chars
        - body: str - Remaining content after title
        - tags: list[str] - Extracted hashtags (without #)

    Example:
        >>> note = parse_note("My Note\\n\\nContent #python #testing")
        >>> note['title']
        'My Note'
        >>> 'python' in note['tags']
        True
    """
    lines = content.split("\n", 1)
    title = lines[0].strip()

    # If title is too long, truncate to 50 chars
    if len(title) > 50:
        title = title[:50]

    # Body is everything after first line
    body = lines[1].strip() if len(lines) > 1 else ""

    # Extract hashtags from entire content
    tags = re.findall(r"#(\w+)", content)
    # Remove duplicates while preserving order
    seen = set()
    unique_tags = []
    for tag in tags:
        if tag.lower() not in seen:
            seen.add(tag.lower())
            unique_tags.append(tag.lower())

    return {"title": title, "body": body, "tags": unique_tags}


def save_note(blog_id: str, note_data: dict) -> Path:
    """Save note with sequence number and metadata.

    Saves note to `.blog/{blog_id}/notes/{seq:03d}-{timestamp}.md` with
    accompanying metadata JSON sidecar file.

    Args:
        blog_id: Blog identifier (e.g., "my-blog")
        note_data: Dict with 'title', 'body', 'tags' keys

    Returns:
        Path: The saved note file path

    Raises:
        OSError: If directory creation or file operations fail
        KeyError: If required keys missing from note_data
    """
    # Ensure blog directory exists
    blog_path = create_blog_dir(blog_id)
    notes_dir = blog_path / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)

    # Get next sequence ID and increment
    seq_id = get_next_sequence_id()
    increment_sequence_id()

    # Create filename with sequence and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{seq_id:03d}-{timestamp}.md"
    note_path = notes_dir / filename

    # Create metadata
    metadata: NoteMetadata = {
        "title": note_data["title"],
        "created_at": datetime.now().isoformat(),
        "tags": note_data.get("tags", []),
        "sequence_id": seq_id,
    }

    # Write note content with YAML frontmatter
    frontmatter = json.dumps(metadata, indent=2)
    content = f"---\n{frontmatter}\n---\n\n# {metadata['title']}\n\n{note_data.get('body', '')}"

    with open(note_path, "w") as f:
        f.write(content)

    # Write metadata sidecar
    metadata_path = note_path.with_suffix(".json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)

    return note_path


def list_notes(blog_id: str) -> list[dict]:
    """List all notes for a blog.

    Returns metadata for all notes in `.blog/{blog_id}/notes/` directory,
    sorted by sequence number.

    Args:
        blog_id: Blog identifier

    Returns:
        list[dict]: List of note metadata dicts, sorted by sequence_id

    Raises:
        OSError: If directory read fails
    """
    blog_path = Path(".blog") / blog_id
    notes_dir = blog_path / "notes"

    if not notes_dir.exists():
        return []

    notes = []
    for metadata_file in sorted(notes_dir.glob("*.json")):
        try:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
                notes.append(metadata)
        except (json.JSONDecodeError, IOError):
            # Skip corrupted metadata files
            continue

    # Sort by sequence_id
    notes.sort(key=lambda n: n.get("sequence_id", 0))
    return notes


def get_note(blog_id: str, sequence_id: int) -> dict | None:
    """Retrieve specific note by sequence ID.

    Args:
        blog_id: Blog identifier
        sequence_id: Sequence number of note to retrieve

    Returns:
        dict: Note metadata if found, None otherwise

    Raises:
        OSError: If directory read fails
    """
    notes = list_notes(blog_id)
    for note in notes:
        if note.get("sequence_id") == sequence_id:
            return note
    return None

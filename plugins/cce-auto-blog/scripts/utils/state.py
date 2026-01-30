import os
from pathlib import Path
from typing import TypedDict


class BlogMetadata(TypedDict):
    title: str
    created_at: str
    status: str
    transcript_path: str
    session_path: str
    session_id: str
    extracted_title: str


class BlogState(TypedDict):
    next_sequence_id: int
    blogs: dict[str, BlogMetadata]


def get_base_dir() -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))


def ensure_blog_dir() -> Path:
    blog_dir = get_base_dir() / ".blog"
    blog_dir.mkdir(parents=True, exist_ok=True)
    return blog_dir


def read_state() -> BlogState:
    import json

    blog_dir = ensure_blog_dir()
    state_path = blog_dir / "state.json"

    if not state_path.exists():
        return {"next_sequence_id": 1, "blogs": {}}

    try:
        with open(state_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"next_sequence_id": 1, "blogs": {}}


def write_state(state: BlogState) -> None:
    import json
    import tempfile

    blog_dir = ensure_blog_dir()
    state_path = blog_dir / "state.json"

    with tempfile.NamedTemporaryFile(
        "w", dir=str(blog_dir), delete=False, suffix=".json"
    ) as f:
        json.dump(state, f, indent=2)
        temp_path = f.name

    os.replace(temp_path, state_path)


def backup_state() -> Path:
    import shutil
    from datetime import datetime

    blog_dir = ensure_blog_dir()
    state_path = blog_dir / "state.json"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = blog_dir / f"state.json.bak.{timestamp}"

    if state_path.exists():
        shutil.copy2(state_path, backup_path)

    return backup_path


def restore_state() -> bool:
    import json

    blog_dir = ensure_blog_dir()
    backup_files = sorted(
        blog_dir.glob("state.json.bak.*"), key=lambda p: p.stat().st_mtime, reverse=True
    )

    if not backup_files:
        return False

    with open(backup_files[0], "r") as f:
        state = json.load(f)

    write_state(state)
    return True


def create_blog_dir(blog_id: str) -> Path:
    blog_dir = ensure_blog_dir()
    blog_path = blog_dir / blog_id

    (blog_path / "notes").mkdir(parents=True, exist_ok=True)
    (blog_path / "transcripts").mkdir(parents=True, exist_ok=True)
    (blog_path / "drafts").mkdir(parents=True, exist_ok=True)

    return blog_path


def get_next_sequence_id() -> int:
    return read_state()["next_sequence_id"]


def increment_sequence_id() -> int:
    state = read_state()
    state["next_sequence_id"] += 1
    write_state(state)
    return state["next_sequence_id"]


def add_blog_to_state(blog_id: str, metadata: BlogMetadata) -> None:
    state = read_state()
    state["blogs"][blog_id] = metadata
    write_state(state)


def update_blog_status(blog_id: str, status: str) -> None:
    state = read_state()
    if blog_id not in state["blogs"]:
        raise KeyError(f"Blog '{blog_id}' not found in state")
    state["blogs"][blog_id]["status"] = status
    write_state(state)

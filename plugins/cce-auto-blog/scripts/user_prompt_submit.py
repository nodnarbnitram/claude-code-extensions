#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils.state import (
    create_blog_dir,
    add_blog_to_state,
    read_state,
    write_state,
    BlogMetadata,
)


def detect_blog_trigger(prompt: str) -> bool:
    if not prompt:
        return False
    prompt_lower = prompt.lower()
    triggers = ["#blog", "blog this", "write blog"]
    return any(trigger in prompt_lower for trigger in triggers)


def detect_stop_tracking(prompt: str) -> bool:
    if not prompt:
        return False
    return "stop tracking" in prompt.lower()


def get_active_blog_for_session(session_id: str) -> tuple[str | None, dict | None]:
    state = read_state()
    for blog_id, metadata in state.get("blogs", {}).items():
        if (
            metadata.get("session_id") == session_id
            and metadata.get("status") == "draft"
        ):
            return blog_id, dict(metadata)
    return None, None


def extract_session_id(hook_input: dict) -> str:
    return hook_input.get("sessionId") or hook_input.get("session_id") or ""


def extract_title_from_prompt(prompt: str) -> str:
    if not prompt:
        return ""
    text = (
        prompt.replace("#blog", "")
        .replace("blog this", "")
        .replace("write blog", "")
        .strip()
    )
    if not text:
        return ""
    for i, char in enumerate(text):
        if char in ".?!":
            sentence = text[:i].strip()
            if sentence:
                return sentence.capitalize()
    return text[:50].strip().capitalize() if text else ""


def generate_blog_id() -> str:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"blog-{timestamp}"


def main():
    try:
        hook_input = json.load(sys.stdin)
        prompt = hook_input.get("prompt", "")
        session_id = extract_session_id(hook_input)

        if detect_stop_tracking(prompt):
            active_blog_id, active_meta = get_active_blog_for_session(session_id)
            if active_blog_id and active_meta:
                state = read_state()
                state["blogs"][active_blog_id]["status"] = "captured"
                write_state(state)
                title = active_meta.get("title", active_blog_id)
                context = f"""[AUTO-BLOG PLUGIN]
Blog tracking stopped for: {title}
Blog ID: {active_blog_id}
Status: captured

The session transcripts have been saved. Use "write blog draft for {active_blog_id}" to compose a draft."""
                print(json.dumps({"additionalContext": context}))
            sys.exit(0)

        if detect_blog_trigger(prompt):
            new_blog_id = generate_blog_id()
            extracted_title = extract_title_from_prompt(prompt)

            create_blog_dir(new_blog_id)

            new_metadata: BlogMetadata = {
                "title": extracted_title or f"Blog Post - {new_blog_id}",
                "created_at": datetime.now().isoformat(),
                "status": "draft",
                "transcript_path": "",
                "session_path": "",
                "session_id": session_id,
                "extracted_title": extracted_title,
            }
            add_blog_to_state(new_blog_id, new_metadata)

            context = f"""[AUTO-BLOG PLUGIN]
Started tracking blog: "{new_metadata["title"]}"
Blog ID: {new_blog_id}
Status: draft

I'll capture notes from this conversation. Say "stop tracking" when you're done with this topic."""
            print(json.dumps({"additionalContext": context}))
            sys.exit(0)

        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()

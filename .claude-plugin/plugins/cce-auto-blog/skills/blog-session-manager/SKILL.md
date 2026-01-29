---
name: blog-session-manager
description: Manage and view blog sessions. Use when user asks to "list blogs", "view blog", "show blog status", or wants to see captured blog content.
---

# Blog Session Manager

Manages blog capture sessions and provides commands to view, list, and inspect captured blog content.

## When to Use

Activate this skill when the user:
- Asks to "list blogs" or "show all blogs"
- Wants to "view blog [name]" or see blog details
- Asks about "blog status" or capture progress
- Wants to see what blogs have been captured
- Needs to inspect blog metadata or transcripts

## Commands

### List All Blogs
Shows all captured blogs with their status and metadata.

**Usage**: `list blogs` or `show all blogs`

**Example**:
```
User: list blogs
Assistant: Here are your captured blogs:

1. blog-20260129-120000 (captured)
   Title: "How to test Python code effectively"
   Created: 2026-01-29 12:00:00
   Transcripts: 3 sessions
   Notes: 5 captured

2. blog-20260128-150000 (draft)
   Title: "Building REST APIs with Django"
   Created: 2026-01-28 15:00:00
   Transcripts: 1 session
   Notes: 2 captured
```

### View Blog Details
Shows detailed information about a specific blog including transcript paths, notes, and metadata.

**Usage**: `view blog [blog-id]` or `show blog [blog-id]`

**Example**:
```
User: view blog blog-20260129-120000
Assistant: Blog Details:

ID: blog-20260129-120000
Title: "How to test Python code effectively"
Status: captured
Created: 2026-01-29 12:00:00 UTC
Session ID: ses_abc123xyz

Transcripts:
- 001-20260129-120000.jsonl (1.2 MB)
- 002-20260129-130000.jsonl (800 KB)
- 003-20260129-140000.jsonl (1.5 MB)

Notes:
- 001-20260129-120500.md: "Unit testing patterns"
- 002-20260129-121000.md: "Mocking external dependencies"
- 003-20260129-122000.md: "Test fixtures and factories"
```

### Show Blog Status
Displays a summary of blog capture status across all blogs.

**Usage**: `blog status` or `show blog status`

**Example**:
```
User: blog status
Assistant: Blog Capture Status:

Total Blogs: 5
- Captured: 3
- Draft: 2
- Archived: 0

Recent Activity:
- blog-20260129-120000: Last updated 2 hours ago
- blog-20260128-150000: Last updated 1 day ago

Storage:
- Total transcripts: 12 files (15.3 MB)
- Total notes: 23 files
```

## Implementation

This skill reads from the blog state management system:
- State file: `.blog/state.json`
- Blog directories: `.blog/{blog-id}/`
- Transcripts: `.blog/{blog-id}/transcripts/`
- Notes: `.blog/{blog-id}/notes/`

The skill uses the state management utilities from `hooks/utils/state.py`:
- `read_state()`: Load blog state
- `list_notes()`: Enumerate notes for a blog
- Blog metadata includes: title, created_at, status, transcript_path, session_id

## Related Skills

- **blog-note-capture**: Captures and filters notes from transcripts (background process)
- **blog-draft-composer**: Composes blog drafts from captured notes
- **blog-image-manager**: Manages image prompts and placeholders for blog posts

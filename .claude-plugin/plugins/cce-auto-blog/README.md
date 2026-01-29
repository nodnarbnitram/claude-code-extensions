# Auto-Blog Plugin for Claude Code

Automatically capture, organize, and compose blog posts from your Claude Code sessions.

## Overview

The Auto-Blog plugin transforms your Claude Code conversations into structured blog content. It intelligently captures notes, filters out noise, and helps you compose publication-ready blog posts with minimal effort.

### Features

- **Automatic Capture**: Trigger blog tracking with `#blog` in any prompt
- **Smart Filtering**: Extracts key insights while filtering out debugging noise
- **Structured Notes**: Organizes content into MDX notes with frontmatter
- **Draft Composition**: Composes polished blog drafts from captured notes
- **Image Management**: Tracks screenshot prompts and AI image placeholders
- **Session Tracking**: Maintains blog state across multiple sessions

## Installation

1. **Clone or copy** this plugin to your Claude Code plugins directory:
   ```bash
   cp -r .claude-plugin/plugins/cce-auto-blog ~/.claude/plugins/
   ```

2. **Enable the plugin** in your Claude Code settings:
   ```bash
   # Add to ~/.claude/settings.json
   {
     "plugins": ["cce-auto-blog"]
   }
   ```

3. **Verify installation**:
   ```bash
   ls ~/.claude/plugins/cce-auto-blog
   # Should show: hooks/, skills/, docs/, plugin.json, settings.json
   ```

## Quick Start

### 1. Start Tracking a Blog

Use any of these trigger keywords in your prompt:
- `#blog`
- `"blog this"`
- `"write blog"`

**Example**:
```
You: #blog How to build a REST API with Django

Claude: ✓ Started tracking blog: "How to build a rest api with django"
Blog ID: blog-20260129-120000
Status: draft

I'll capture notes from our conversation. Say "stop tracking" when done.
```

### 2. Work Normally

Continue your conversation with Claude. The plugin automatically:
- Captures transcripts after each Stop event
- Filters and extracts meaningful content
- Saves structured notes to `.blog/{blog-id}/notes/`

### 3. Stop Tracking

When you're done with the topic:
```
You: stop tracking

Claude: ✓ Stopped tracking blog: "How to build a rest api with django"
Blog ID: blog-20260129-120000
Status: captured

Captured:
- 3 transcript sessions
- 5 notes extracted
- Ready for draft composition
```

### 4. Compose Draft

Generate a polished blog post from your notes:
```
You: write blog draft for blog-20260129-120000

Claude: I'll compose a blog draft from your captured notes...

✓ Draft created: .blog/blog-20260129-120000/drafts/draft-v1.mdx

Sections:
- Title: "Building a REST API with Django and PostgreSQL"
- Introduction (2 paragraphs)
- The Problem (3 paragraphs)
- The Solution (5 steps with code)
- Results (metrics and outcomes)
- Lessons Learned (4 key insights)
- Conclusion (1 paragraph)

Image placeholders: 7 (3 screenshots, 4 AI-generated)
Code blocks: 12 (Python, YAML, Bash)
```

### 5. Manage Images

List pending image placeholders:
```
You: list pending images for blog-20260129-120000

Claude: Found 7 pending images:

**Screenshots (3)**:
1. Line 45: Dashboard showing test coverage at 95%
2. Line 89: pytest output with all tests passing
3. Line 134: Database schema with relationships

**AI Images (4)**:
1. Line 12 (Hero): Isometric REST API architecture diagram
...
```

Mark images as captured:
```
You: mark image captured at line 45, path is ./images/dashboard-coverage.png

Claude: ✓ Replaced placeholder at line 45
Remaining: 6 pending images
```

## Command Reference

### Blog Management

| Command | Description |
|---------|-------------|
| `#blog [topic]` | Start tracking a new blog |
| `stop tracking` | End current blog tracking |
| `list blogs` | Show all captured blogs |
| `view blog [blog-id]` | Show blog details |
| `blog status` | Show capture status summary |

### Draft Composition

| Command | Description |
|---------|-------------|
| `write blog draft for [blog-id]` | Compose draft from notes |
| `compose blog for [name]` | Compose by blog title |
| `review notes for [blog-id]` | Review notes before composing |
| `expand the [section]` | Expand a specific section |
| `add a section about [topic]` | Add new section to draft |

### Image Management

| Command | Description |
|---------|-------------|
| `list pending images for [blog-id]` | Show all image placeholders |
| `mark image captured at line [N], path is [path]` | Replace placeholder |
| `mark images captured: [list]` | Batch replace multiple images |

## Directory Structure

```
.blog/
├── state.json                          # Blog state and metadata
└── blog-YYYYMMDD-HHMMSS/              # Individual blog directory
    ├── notes/                          # Captured notes
    │   ├── 001-YYYY-MM-DD-HHMM.mdx
    │   ├── 001-YYYY-MM-DD-HHMM.json   # Metadata sidecar
    │   └── ...
    ├── transcripts/                    # Session transcripts
    │   ├── 001-YYYYMMDD-HHMMSS.jsonl
    │   └── ...
    ├── drafts/                         # Composed drafts
    │   ├── draft-v1.mdx
    │   ├── draft-v2.mdx
    │   └── ...
    └── images/                         # Blog images (user-managed)
        ├── screenshot-1.png
        └── hero-image.png
```

## How It Works

### 1. Hook System

The plugin uses Claude Code lifecycle hooks:

- **SessionStart**: Initializes `.blog/` directory and state
- **UserPromptSubmit**: Detects blog triggers and creates blog entries
- **Stop**: Copies transcripts and spawns background note capture
- **SessionEnd**: Updates blog status to "captured"

### 2. Note Capture (Background)

After each Stop event, a background agent:
1. Reads the session transcript
2. Filters out noise (file listings, errors, debugging)
3. Extracts key insights, decisions, and working code
4. Generates structured MDX notes with frontmatter
5. Saves to `.blog/{blog-id}/notes/`

### 3. Draft Composition (User-Triggered)

When you request a draft:
1. Reads all notes in sequence order
2. Analyzes structure and flow
3. Generates 8-section blog template
4. Inserts code blocks with proper formatting
5. Adds image placeholders for screenshots and AI images
6. Saves to `.blog/{blog-id}/drafts/draft-v1.mdx`

## Configuration

### Hook Timeouts

Configured in `settings.json`:
- **SessionStart**: 5s
- **UserPromptSubmit**: 2s
- **Stop**: 5s
- **SessionEnd**: 10s

### Blog Triggers

Case-insensitive keywords:
- `#blog`
- `"blog this"`
- `"write blog"`

### Note Format

MDX with YAML frontmatter:
```yaml
---
title: "Accomplishment-based title"
date: "2026-01-29T12:00:00Z"
sequence: 1
blog: "blog-20260129-120000"
transcript: "001-20260129-120000.jsonl"
tags: ["python", "django", "api"]
---
```

## Troubleshooting

### Blog not capturing

**Problem**: Used trigger keyword but blog not created

**Solutions**:
- Check `.blog/state.json` exists
- Verify SessionStart hook executed: `ls .blog/`
- Check UserPromptSubmit hook logs

### Notes not generated

**Problem**: Transcripts captured but no notes in `.blog/{blog-id}/notes/`

**Solutions**:
- Background agent may still be running (1-2 minutes)
- Check transcript file exists: `ls .blog/{blog-id}/transcripts/`
- Verify Stop hook executed

### Draft composition fails

**Problem**: "write blog draft" command fails or produces empty draft

**Solutions**:
- Ensure notes exist: `ls .blog/{blog-id}/notes/`
- Check note format (YAML frontmatter + MDX body)
- Try "review notes" first to verify content

### Multiple blogs tracked

**Problem**: Accidentally started new blog without stopping previous

**Solutions**:
- Say "stop tracking" to end current blog
- Use "list blogs" to see all active blogs
- Only one blog can be tracked per session

## Advanced Usage

### Custom Note Filtering

Edit `.claude-plugin/plugins/cce-auto-blog/skills/blog-note-capture/SKILL.md` to customize:
- Filtering heuristics
- Section structure
- Title generation rules

### Draft Template Customization

Edit `.claude-plugin/plugins/cce-auto-blog/skills/blog-draft-composer/SKILL.md` to customize:
- Section order and names
- Code block formatting
- Image placeholder syntax

### State Management

Direct state file manipulation (advanced):
```bash
# View all blogs
cat .blog/state.json | jq '.blogs'

# Get next sequence ID
cat .blog/state.json | jq '.next_sequence_id'

# Backup state
cp .blog/state.json .blog/state.backup.json
```

## Development

### Running Tests

```bash
# Test hooks individually
echo '{"event": "SessionStart"}' | uv run ./hooks/session_start.py

# Test state management
python3 -c "from hooks.utils.state import read_state; print(read_state())"

# Test note parsing
python3 -c "from hooks.utils.notes import parse_note; print(parse_note('# Title\nBody'))"
```

### Adding New Hooks

1. Create hook script in `hooks/`
2. Register in `plugin.json` and `settings.json`
3. Set appropriate timeout
4. Test with sample JSON input

### Extending Skills

1. Create skill directory in `skills/`
2. Add `SKILL.md` with frontmatter
3. Document commands and workflows
4. Test with Claude Code

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Support

- **Issues**: https://github.com/nodnarbnitram/claude-code-extensions/issues
- **Discussions**: https://github.com/nodnarbnitram/claude-code-extensions/discussions
- **Documentation**: See `docs/` directory for detailed specs

## Changelog

### v0.1.0 (2026-01-29)

- Initial release
- Blog capture and tracking
- Smart note filtering
- Draft composition
- Image placeholder management
- Four lifecycle hooks (SessionStart, UserPromptSubmit, Stop, SessionEnd)
- Four skills (blog-session-manager, blog-note-capture, blog-draft-composer, blog-image-manager)

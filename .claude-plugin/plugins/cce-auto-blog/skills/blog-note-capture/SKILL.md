---
name: blog-note-capture
description: Intelligently filters and captures notes from Claude Code transcripts for blog posts. Invoked by background agent after Stop hook, not user-triggered.
---

# Blog Note Capture

Analyzes Claude Code session transcripts and extracts meaningful content for blog posts, filtering out noise and preserving key insights.

## Invocation Context

**This skill is NOT user-triggered.** It is automatically invoked by:
- Stop hook's background agent (spawned via `subprocess.Popen`)
- SessionEnd hook's background agent
- PreCompact hook's background agent

The background agent receives:
- Transcript path (`.blog/{blog-id}/transcripts/{seq}-{timestamp}.jsonl`)
- Blog ID and metadata
- Sequence number for file naming

## Smart Filtering Logic

### Filter OUT (Noise)
- File listings and directory structures (`ls`, `tree` output)
- Typos and correction attempts
- Debugging loops and failed attempts
- Error messages without resolution
- Repetitive tool calls
- Exploratory commands without insights

### KEEP (Signal)
- Key decisions and rationale
- Working solutions and successful implementations
- Insights and "aha!" moments
- Successful code with explanations
- Architecture choices
- Problem-solving approaches that worked
- User questions and assistant explanations

### Filtering Heuristics
1. **Outcome-focused**: Prioritize what WORKED, not what was tried
2. **Insight-driven**: Keep content that teaches or explains
3. **Context-aware**: Preserve enough context to understand decisions
4. **Concise**: Summarize repetitive patterns, don't repeat them

## MDX Note Format

### Frontmatter Fields
```yaml
---
title: "Accomplishment-based title (not attempt-based)"
date: "2026-01-29T12:00:00Z"
sequence: 1
blog: "blog-20260129-120000"
transcript: "001-20260129-120000.jsonl"
tags: ["python", "testing", "pytest"]
---
```

### Body Sections

#### 1. Prompts
User's original questions or requests that drove the work.

```markdown
## Prompts
- "How do I set up pytest fixtures for database testing?"
- "Can you help me mock external API calls?"
```

#### 2. Work Done
Summary of what was accomplished (not attempted).

```markdown
## Work Done
- Set up pytest fixtures for PostgreSQL test database
- Implemented factory pattern for test data generation
- Created mock decorators for external API calls
- Added 15 unit tests with 95% coverage
```

#### 3. Key Learnings
Insights, gotchas, and important discoveries.

```markdown
## Key Learnings
- pytest fixtures with `scope="session"` reduce test time by 60%
- Factory Boy's `SubFactory` handles nested relationships elegantly
- `@patch` decorator must match import path, not definition path
```

#### 4. Code Highlights
Significant code snippets with explanations.

````markdown
## Code Highlights

### Pytest Fixture for Test Database
```python
@pytest.fixture(scope="session")
def test_db():
    """Create test database once per session."""
    db = create_test_database()
    yield db
    db.drop()
```

This fixture creates the database once and reuses it across all tests, dramatically improving test performance.
````

#### 5. Screenshot Opportunities
UI-related tasks that should be captured visually.

```markdown
## Screenshot Opportunities
- Dashboard showing test coverage metrics
- pytest output with all tests passing
- Database schema visualization
```

#### 6. Image Prompts
AI-generated image prompts for blog illustrations.

```markdown
## Image Prompts
1. **Hero Image**: "Isometric illustration of a testing pyramid with pytest logo, clean modern style, blue and green color scheme, technical but approachable"
2. **Fixture Diagram**: "Flowchart showing pytest fixture lifecycle, minimalist design, arrows indicating setup/teardown, professional technical diagram"
```

## Title Generation

Generate titles from **ACCOMPLISHMENTS**, not attempts.

**Good Examples**:
- ✅ "Setting up Home Assistant Energy Monitoring"
- ✅ "Building a REST API with Django and PostgreSQL"
- ✅ "Implementing JWT Authentication in FastAPI"

**Bad Examples**:
- ❌ "Trying to fix Home Assistant errors"
- ❌ "Debugging Django database issues"
- ❌ "Attempting to add authentication"

**Pattern**: `[Action Verb] + [What Was Built/Achieved]`

## File Naming Convention

Format: `{seq:03d}-{YYYY-MM-DD}-{HHMM}.mdx`

**Examples**:
- `001-2026-01-29-1200.mdx` (first note)
- `002-2026-01-29-1430.mdx` (second note)
- `015-2026-02-01-0900.mdx` (fifteenth note)

**Rules**:
- Sequence: Zero-padded 3 digits (001-999)
- Date: ISO 8601 date format (YYYY-MM-DD)
- Time: 24-hour format, no separators (HHMM)
- Extension: `.mdx` (Markdown with JSX support)

## Fallback Behavior

**If filtering fails or produces empty output**:
1. Create minimal note with metadata
2. Include link to raw transcript
3. Add error context for debugging
4. **Never lose data** - preserve transcript reference

**Minimal Note Template**:
```markdown
---
title: "Session {sequence} - {date}"
date: "{iso-timestamp}"
sequence: {seq}
blog: "{blog-id}"
transcript: "{transcript-filename}"
tags: ["unprocessed"]
---

## Note

Automatic filtering failed for this session. See raw transcript for details.

**Transcript**: `.blog/{blog-id}/transcripts/{transcript-filename}`

**Error**: {error-message}
```

## Screenshot Opportunity Detection

Detect UI-related work by analyzing:
- Tool calls to browser automation (Playwright, Puppeteer)
- Frontend file modifications (`.tsx`, `.jsx`, `.vue`, `.svelte`)
- CSS/styling changes
- Component creation or updates
- Dashboard or visualization work

**Suggest screenshots for**:
- Before/after UI changes
- New components or features
- Dashboard views
- Error states and loading states
- Responsive design breakpoints

## AI Image Prompt Generation

Generate DALL-E/Midjourney style prompts for blog illustrations.

**Prompt Structure**:
```
[Subject] + [Style] + [Color Scheme] + [Mood] + [Technical Details]
```

**Examples**:

1. **Technical Diagrams**:
   - "Isometric 3D diagram of microservices architecture, clean modern style, blue and purple gradient, professional and technical, white background"

2. **Hero Images**:
   - "Abstract representation of data flowing through pipelines, geometric shapes, vibrant blue and green colors, energetic and modern, high-tech aesthetic"

3. **Concept Illustrations**:
   - "Minimalist illustration of a developer at a desk with code on screen, flat design, warm orange and teal colors, focused and productive mood"

**Guidelines**:
- Keep prompts under 100 words
- Specify style (isometric, flat, 3D, minimalist, etc.)
- Include 2-3 colors for consistency
- Define mood (professional, playful, technical, etc.)
- Avoid copyrighted references

## Implementation Notes

This skill uses:
- `hooks/utils/notes.py`: `save_note()`, `parse_note()`
- `hooks/utils/state.py`: `read_state()`, `get_next_sequence_id()`, `increment_sequence_id()`
- Transcript parsing: JSONL format with `user`, `tool_use`, `tool_result` entries
- LLM analysis: Claude Sonnet for intelligent filtering and summarization

**Performance**:
- Runs in background (1-2 minutes per transcript)
- Does not block user's Claude Code session
- Spawned by hooks via `subprocess.Popen(..., start_new_session=True)`

## Related Skills

- **blog-session-manager**: View and manage captured blogs
- **blog-draft-composer**: Compose final blog drafts from notes
- **blog-image-manager**: Manage image prompts and placeholders

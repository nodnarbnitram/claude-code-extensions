---
name: blog-draft-composer
description: Compose blog drafts from captured notes and transcripts. Use when user asks to "write blog draft", "compose blog", or wants to create final blog post from captured content.
---

# Blog Draft Composer

Transforms captured notes and transcripts into polished, publication-ready blog posts with proper structure, code formatting, and image placeholders.

## When to Use

Activate this skill when the user:
- Asks to "write blog draft" or "compose blog"
- Wants to "create blog post from [blog-name]"
- Says "turn my notes into a blog post"
- Requests "generate draft for [blog-id]"
- Wants to review or refine an existing draft

## Compose Command Workflow

### Basic Usage
```
User: write blog draft for blog-20260129-120000
Assistant: I'll compose a blog draft from your captured notes...

[Reads all notes from .blog/blog-20260129-120000/notes/]
[Analyzes structure and flow]
[Generates draft with proper sections]

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

Ready for review! Say "expand the Introduction" or "add troubleshooting section" to refine.
```

### With Blog Name
```
User: compose blog for my Django API tutorial
Assistant: [Searches state for blog with matching title]
[Composes draft as above]
```

## Draft Structure Template

Every blog draft follows this structure:

```markdown
---
title: "Accomplishment-Based Title"
date: "2026-01-29"
author: "Your Name"
tags: ["tag1", "tag2", "tag3"]
status: "draft"
---

# Title

![Hero Image](<!-- IMAGE: AI prompt for hero image -->)

## Introduction

Hook the reader with the problem or opportunity. Explain why this matters.

## The Problem

Describe the challenge or situation that motivated this work. Include:
- Context and background
- Why existing solutions weren't sufficient
- What you needed to accomplish

## The Solution

Step-by-step walkthrough of what you built. Each major step gets:

### Step 1: [Descriptive Title]

Explanation of what this step accomplishes.

\`\`\`python
# Working code with context
def example_function():
    """Clear docstring."""
    return result
\`\`\`

![Screenshot](<!-- SCREENSHOT: Description of what to capture -->)

**Key Points:**
- Important detail 1
- Important detail 2

### Step 2: [Next Step]

[Continue pattern...]

## Results

What you achieved:
- Metrics (performance, coverage, etc.)
- Outcomes (features working, problems solved)
- Validation (tests passing, deployment successful)

## Lessons Learned

Key insights and gotchas discovered:
1. **Insight 1**: Explanation and why it matters
2. **Insight 2**: Explanation and why it matters
3. **Insight 3**: Explanation and why it matters

## Conclusion

Summary of what was accomplished and next steps or future improvements.
```

## Reading from Notes and Transcripts

### Source Priority
1. **MDX Notes** (primary): Read all notes in sequence order
   - Use for structure, flow, and high-level narrative
   - Extract key decisions, insights, and working solutions
   - Preserve code highlights and learnings

2. **Transcripts** (reference): Consult for additional detail
   - Use when notes lack specific implementation details
   - Extract exact commands, error messages, or configurations
   - Verify technical accuracy

### Reading Pattern
```python
# Pseudocode for draft composition
notes = list_notes(blog_id)  # Sorted by sequence
for note in notes:
    # Extract sections
    prompts = note["Prompts"]
    work_done = note["Work Done"]
    learnings = note["Key Learnings"]
    code = note["Code Highlights"]
    
    # Build narrative
    # Map to draft structure
    # Preserve working code
    # Include insights
```

## Code Block Formatting

### Language Tags
Always specify language for syntax highlighting:

````markdown
```python
# Python code
```

```yaml
# YAML configuration
```

```bash
# Shell commands
```

```typescript
// TypeScript code
```
````

### Context Before Code
Every code block needs explanation:

**Good Example:**
```markdown
To configure the database connection, create a `settings.py` file:

\`\`\`python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
    }
}
\`\`\`

This configuration uses PostgreSQL with connection pooling enabled.
```

**Bad Example:**
```markdown
\`\`\`python
DATABASES = {'default': {...}}
\`\`\`
```

### Working Code Only
- Include ONLY code that worked
- Filter out failed attempts, debugging, and errors
- Show the final, successful implementation
- If showing evolution, clearly label "Before" and "After"

## Image Placeholder Insertion

### Hero Image
Insert immediately after title:

```markdown
# Building a REST API with Django

![Hero Image](<!-- IMAGE: Isometric 3D illustration of REST API architecture, modern clean style, blue and purple gradient, professional technical aesthetic -->)

## Introduction
```

### Step Screenshots
Insert after key steps that have visual output:

```markdown
### Step 3: Configure the Admin Interface

[Explanation of admin setup...]

\`\`\`python
# Admin configuration code
\`\`\`

![Admin Dashboard](<!-- SCREENSHOT: Django admin dashboard showing User and Post models with search and filters enabled -->)

The admin interface now provides...
```

### Placeholder Syntax
- **Screenshot**: `![Alt Text](<!-- SCREENSHOT: Detailed description of what to capture -->)`
- **AI Image**: `![Alt Text](<!-- IMAGE: Full DALL-E/Midjourney prompt -->)`

### Placement Guidelines
- Hero image: After title, before introduction
- Step screenshots: After code/explanation, before next step
- Concept diagrams: In "The Problem" or "The Solution" sections
- Results screenshots: In "Results" section

## Review Notes Mode

Before composing, allow user to review and curate notes.

### Usage
```
User: review notes for blog-20260129-120000
Assistant: Here are your captured notes:

1. 001-2026-01-29-1200.mdx
   Title: "Setting up Django project structure"
   Tags: python, django, setup
   Sections: 4
   Code blocks: 3

2. 002-2026-01-29-1430.mdx
   Title: "Implementing user authentication"
   Tags: django, auth, jwt
   Sections: 5
   Code blocks: 7

3. 003-2026-01-29-1600.mdx
   Title: "Debugging CORS issues"
   Tags: django, cors, debugging
   Sections: 3
   Code blocks: 2

Would you like to:
- Compose draft from all notes
- Exclude specific notes (e.g., "exclude note 3")
- View a specific note in detail
```

### Exclusion
```
User: exclude note 3, it's just debugging
Assistant: ✓ Will compose draft using notes 1 and 2 only.

Proceeding with composition...
```

## Iterative Refinement Commands

After initial draft, support refinement requests:

### Expand Sections
```
User: expand the Introduction
Assistant: I'll expand the Introduction section with more context...

[Reads relevant notes again]
[Adds 2-3 more paragraphs]
[Maintains flow with existing content]

✓ Introduction expanded from 2 to 4 paragraphs
```

### Add Sections
```
User: add a section about troubleshooting
Assistant: I'll add a Troubleshooting section after The Solution...

[Extracts error handling and debugging from notes]
[Creates new section with common issues and solutions]

✓ Added "Troubleshooting" section with 5 common issues
```

### Refine Code
```
User: add more comments to the authentication code
Assistant: I'll add detailed comments to the auth code blocks...

[Updates code blocks with inline comments]
[Preserves functionality, improves clarity]

✓ Updated 3 code blocks in authentication section
```

### Adjust Tone
```
User: make it more beginner-friendly
Assistant: I'll adjust the tone for beginners...

[Adds more explanations]
[Defines technical terms]
[Includes "why" context]

✓ Revised draft with beginner-friendly explanations
```

## Implementation Notes

This skill uses:
- `hooks/utils/notes.py`: `list_notes()`, `get_note()`
- `hooks/utils/state.py`: `read_state()`
- Transcript parsing: For additional detail when needed
- LLM composition: Claude Sonnet for narrative generation

**Draft Versioning**:
- Drafts saved as `.blog/{blog-id}/drafts/draft-v{N}.mdx`
- Each refinement creates new version (v1, v2, v3...)
- Previous versions preserved for comparison

**Performance**:
- Composition time: 30-60 seconds per draft
- Depends on: Number of notes, transcript size, complexity
- User-triggered (not background process)

## Related Skills

- **blog-session-manager**: View and manage captured blogs
- **blog-note-capture**: Captures notes from transcripts (background)
- **blog-image-manager**: Manage image prompts and placeholders

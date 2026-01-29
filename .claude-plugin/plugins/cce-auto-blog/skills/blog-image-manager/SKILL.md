---
name: blog-image-manager
description: Manage image placeholders and prompts for blog posts. Use when user asks to "add image", "screenshot prompt", "list pending images", or wants to manage blog visuals.
---

# Blog Image Manager

Manages image placeholders, screenshot prompts, and AI-generated image prompts for blog posts. Tracks pending images and helps replace placeholders with actual assets.

## When to Use

Activate this skill when the user:
- Asks to "add image" or "insert screenshot"
- Wants to "create screenshot prompt"
- Says "list pending images" or "show image placeholders"
- Requests "mark image captured" or "replace placeholder"
- Wants to generate AI image prompts

## Screenshot Prompt Format

Screenshot prompts provide clear instructions for what to capture.

### Format
```markdown
![Alt Text](<!-- SCREENSHOT: Detailed description of what to capture -->)
```

### Checklist Style
For multiple screenshots in a section:

```markdown
## Screenshots Needed

- [ ] Dashboard showing test coverage at 95%
- [ ] pytest output with all 47 tests passing in green
- [ ] Database schema diagram with relationships highlighted
- [ ] Admin interface with User and Post models visible
```

### Good Screenshot Prompts
Clear, specific, actionable:

✅ **Good Examples**:
- "Django admin dashboard showing User and Post models with search filters enabled and 5 sample entries visible"
- "Terminal output of `pytest -v` showing all 47 tests passing with green checkmarks and total time of 2.3s"
- "VS Code editor with `models.py` open, showing the User model class with highlighted docstring and type hints"

❌ **Bad Examples**:
- "Admin dashboard" (too vague)
- "Test output" (not specific)
- "Code editor" (no context)

### Screenshot Prompt Guidelines
1. **Be specific**: Mention exact UI elements, text, or states
2. **Include context**: What should be visible in the frame
3. **Specify state**: "with 5 entries", "showing error message", "after clicking Save"
4. **Mention highlights**: "with relationships highlighted", "error in red"

## AI Image Prompt Format

AI image prompts for DALL-E, Midjourney, or Stable Diffusion.

### Format
```markdown
![Alt Text](<!-- IMAGE: Full AI generation prompt -->)
```

### Prompt Structure
```
[Subject] + [Style] + [Color Scheme] + [Mood] + [Technical Details]
```

### Examples by Category

#### Technical Diagrams
```markdown
![Architecture Diagram](<!-- IMAGE: Isometric 3D diagram of microservices architecture with API gateway, service mesh, and databases, clean modern style, blue and purple gradient, professional technical aesthetic, white background, high detail -->)
```

#### Hero Images
```markdown
![Hero Image](<!-- IMAGE: Abstract representation of data flowing through pipelines with geometric shapes and nodes, vibrant blue and green colors, energetic and modern, high-tech aesthetic, wide aspect ratio 16:9 -->)
```

#### Concept Illustrations
```markdown
![Developer Workflow](<!-- IMAGE: Minimalist flat design illustration of developer at desk with dual monitors showing code and terminal, warm orange and teal color palette, focused and productive mood, simple clean lines -->)
```

#### Code Visualization
```markdown
![Code Flow](<!-- IMAGE: Flowchart showing pytest fixture lifecycle with setup, test execution, and teardown phases, minimalist design with arrows, professional technical diagram style, blue and gray colors -->)
```

### AI Prompt Guidelines
1. **Subject**: What is being depicted (architecture, workflow, concept)
2. **Style**: Isometric, flat, 3D, minimalist, realistic, abstract
3. **Colors**: 2-3 specific colors for brand consistency
4. **Mood**: Professional, playful, technical, energetic, calm
5. **Details**: Aspect ratio, background, level of detail
6. **Length**: Keep under 100 words for best results

## Placeholder Syntax

### Screenshot Placeholder
```markdown
![Dashboard View](<!-- SCREENSHOT: Django admin dashboard showing User model with 10 entries, search bar at top, and blue "Add User" button in top right -->)
```

### AI Image Placeholder
```markdown
![Hero Image](<!-- IMAGE: Isometric 3D illustration of REST API architecture, modern clean style, blue and purple gradient, professional technical aesthetic -->)
```

### Syntax Rules
- **Alt text**: Descriptive, used if image fails to load
- **Comment syntax**: `<!-- TYPE: description -->`
- **Types**: `SCREENSHOT` or `IMAGE`
- **Description**: Detailed for screenshots, full prompt for AI images

## List Pending Images Command

Scan draft for placeholders and list all pending images.

### Usage
```
User: list pending images for blog-20260129-120000
Assistant: Scanning draft for image placeholders...

Found 7 pending images:

**Screenshots (3)**:
1. Line 45: Dashboard showing test coverage at 95%
2. Line 89: pytest output with all tests passing
3. Line 134: Database schema with relationships

**AI Images (4)**:
1. Line 12 (Hero): Isometric REST API architecture diagram
2. Line 67: Flowchart of authentication flow
3. Line 112: Abstract data pipeline visualization
4. Line 178: Developer workflow illustration

Use "mark image captured" to replace placeholders with actual paths.
```

### Output Format
- **Location**: Line number in draft
- **Type**: Screenshot or AI Image
- **Description**: Brief summary of what's needed
- **Status**: Pending, Captured, or Replaced

## Mark Image Captured Workflow

Replace placeholder with actual image path after capturing/generating.

### Usage
```
User: mark image captured at line 45, path is ./images/dashboard-coverage.png
Assistant: ✓ Replaced placeholder at line 45

Before:
![Dashboard View](<!-- SCREENSHOT: Dashboard showing test coverage at 95% -->)

After:
![Dashboard View](./images/dashboard-coverage.png)

Remaining: 6 pending images (2 screenshots, 4 AI images)
```

### Workflow Steps
1. User captures screenshot or generates AI image
2. User saves image to blog directory (e.g., `.blog/{blog-id}/images/`)
3. User provides line number and image path
4. Skill replaces placeholder with actual path
5. Draft updated with new version

### Path Conventions
- **Relative paths**: `./images/filename.png` (relative to draft)
- **Absolute paths**: `/full/path/to/image.png` (if needed)
- **Naming**: Descriptive filenames (e.g., `dashboard-coverage.png`, not `img1.png`)

## Batch Operations

### Mark Multiple Images
```
User: mark images captured:
- line 45: ./images/dashboard-coverage.png
- line 89: ./images/pytest-output.png
- line 134: ./images/db-schema.png
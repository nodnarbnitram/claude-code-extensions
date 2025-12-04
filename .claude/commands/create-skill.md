---
description: Create a new Claude Code skill from a description
argument-hint: <skill-name> "<description/purpose>" [doc-url...]
---

# Create New Skill

You will create a new skill for Claude Code based on the provided name, description, and optional documentation URLs.

**Arguments**: $ARGUMENTS

**Important**:
- First argument: **skill name** (kebab-case)
- Second argument: **description/purpose** (in quotes)
- Remaining arguments (optional): **documentation URLs** to analyze

## Your Task

Follow these steps to create the skill:

### Step 1: Parse Arguments

Extract from $ARGUMENTS:
- **Skill Name**: The first argument (kebab-case identifier, e.g., `pdf-processor`)
- **Description/Purpose**: The second argument (in quotes) describing what the skill does
- **Documentation URLs**: Any remaining arguments (optional)

Examples:
- `/create-skill pdf-processor "Extract text and tables from PDF files"`
- `/create-skill temporal-workflow "Build durable workflows" https://docs.temporal.io https://typescript.temporal.io`

### Step 2: Gather Context

**If documentation URLs were provided:**
Launch **technical-researcher agents in parallel** (one per URL) to analyze the documentation. Each researcher should investigate:
- Key concepts, APIs, and patterns relevant to the skill's purpose
- Best practices and conventions
- Common workflows and use cases
- Important implementation details
- Configuration examples and templates that should be bundled

**IMPORTANT**: Do NOT use WebFetch directly. Always use the technical-researcher agent to ensure comprehensive analysis and proper extraction of reusable content.

**If NO documentation URLs were provided:**
Use the **AskUserQuestion** tool to gather more information. Ask about:
- What specific problem does this skill solve?
- Are there documentation URLs or references to analyze?
- What tools will the skill need access to? (Read-only? Bash access?)
- What are the key workflows and steps?
- What trigger keywords should activate this skill?

Adapt questions based on the description provided - skip questions that are already answered.

### Step 3: Copy Skeleton Template

Copy the skeleton template from `templates/skill-skeleton/` to `.claude/skills/<skill-name>/`:
- This provides the base directory structure
- You'll customize the placeholders based on gathered context

### Step 4: Generate SKILL.md

Create the main skill file with proper YAML frontmatter:

```yaml
---
name: skill-name-here
description: Clear description of what it does AND when to use it
allowed-tools: Tool1, Tool2  # Only if restrictions needed
---
```

**Required sections in SKILL.md:**
- **⚠️ BEFORE YOU START**: Metrics table (setup time, error count, token usage) and numbered list of prevented issues
- **Quick Start**: 3 steps with code examples and "Why this matters" explanations
- **Critical Rules**: ✅ Always Do and ❌ Never Do with visual indicators, plus Common Mistakes (wrong vs correct code)
- **Known Issues Prevention**: Table with Issue, Root Cause, Solution columns
- **Configuration Reference**: Example configs with key settings explained
- **Common Patterns**: Code examples for typical usage
- **Bundled Resources**: Linked scripts/, references/, templates/ contents (if created)
- **Dependencies**: Required and optional packages with versions
- **Troubleshooting**: Problem/symptom/solution pairs
- **Setup Checklist**: Verification items before using

### Step 5: Generate README.md (REQUIRED)

Always include README.md with discovery-focused content:

**Required sections:**
- **Metadata table**: Status, Version, Last Updated, Confidence (X/5), Production Tested URL
- **What This Skill Does**: Core capabilities list
- **Auto-Trigger Keywords**: Primary, Secondary, and Error-based keywords
- **Known Issues Prevention**: Table format
- **When to Use**: "Use for" and "Don't use for" lists
- **Quick Usage**: Single code example
- **Token Efficiency**: Table comparing manual vs skill-assisted approach
- **File Structure**: Directory tree
- **Dependencies**: Package versions with verification dates
- **Related Skills**: Links to complementary skills

### Step 6: Evaluate and Create Optional Directories

**Create `templates/`** when the skill involves:
- Configuration files (wrangler.jsonc, docker-compose.yaml, terraform.tf)
- Starter templates users would copy
- Example project structures

**Create `scripts/`** when the skill has:
- Repeatable validation commands that run locally
- Setup automation (install dependencies, configure tools)
- Diagnostic utilities (API queries, config validation)

**Create `references/`** when:
- Documentation URLs were provided (extract key API patterns, examples)
- Complex reference material should be bundled for offline use

**Create `assets/`** when:
- Static resources are needed (images, diagrams, data files)

**For simpler skills**: Remove directories that aren't needed. A small skill may only have SKILL.md and README.md.

### Step 7: Validate

Before completing, verify:
- [ ] SKILL.md has valid YAML frontmatter
- [ ] Name uses only lowercase letters, numbers, hyphens (max 64 chars)
- [ ] Description includes what AND when with specific trigger keywords
- [ ] allowed-tools is appropriate (or omitted to inherit all)
- [ ] Instructions are clear and actionable
- [ ] README.md exists with auto-trigger keywords
- [ ] Evaluated need for templates/ (config-heavy skills)
- [ ] Evaluated need for scripts/ (automation opportunities)
- [ ] Evaluated need for references/ (if docs URLs provided)
- [ ] Token efficiency documented in README.md
- [ ] Unnecessary skeleton directories removed

## Best Practices

### Description Writing
**Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files, forms, or document extraction.
```

**Bad:**
```yaml
description: Helps with documents
```

### Tool Restrictions
Use `allowed-tools` for:
- Read-only skills (Read, Grep, Glob)
- Security-sensitive operations
- Limited-scope workflows

Omit `allowed-tools` to inherit all tools from main thread.

## Output Location

Write all files to `.claude/skills/<skill-name>/`:
```
.claude/skills/
└── skill-name/
    ├── SKILL.md        # Required
    ├── README.md       # Required
    ├── templates/      # If config-heavy
    ├── scripts/        # If automation needed
    ├── references/     # If docs URLs provided
    └── assets/         # If static resources needed
```

### Step 8: Report Results

Provide a summary including:
- Path to the newly created skill directory
- Skill name and description
- What the skill does and when Claude should use it
- Auto-trigger keywords (from README.md)
- Tool restrictions (if any)
- What optional directories were created and why
- Suggested test prompts to validate the skill works correctly

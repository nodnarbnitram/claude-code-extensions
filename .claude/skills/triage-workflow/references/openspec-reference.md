# OpenSpec Reference

Quick reference for spec-driven development workflow.

## Slash Commands

| Command | Description |
|---------|-------------|
| `/openspec:proposal [desc]` | Create a new change proposal |
| `/openspec:apply [name]` | Implement an approved change |
| `/openspec:archive [name]` | Archive a deployed change |

## CLI Commands

```bash
openspec list              # View active changes
openspec list --specs      # View all specs
openspec show [item]       # Display details
openspec validate [id]     # Check formatting
openspec archive [id] --yes # Archive completed change
```

## Workflow Steps

### 1. Create Proposal

```
/openspec:proposal Add two-factor authentication
```

Creates:
```
openspec/changes/add-two-factor-auth/
├── proposal.md    # Why, What Changes, Impact
├── tasks.md       # Implementation checklist
└── specs/         # Delta specs
```

### 2. Review & Validate

- Share proposal with user
- Iterate until approved
- Run: `openspec validate [id] --strict`

### 3. Apply Changes

```
/openspec:apply add-two-factor-auth
```

Works through tasks.md checklist.

### 4. Archive (after deploy)

```bash
openspec archive add-two-factor-auth --yes
```

## Proposal Format

**proposal.md:**
```markdown
## Why
[Motivation and context]

## What Changes
- Add feature X
- **BREAKING**: API change Y
- Update behavior Z

## Impact
- Affected specs: auth, notifications
- Affected code: backend/auth, frontend/login
```

**tasks.md:**
```markdown
## 1. Backend
- [ ] 1.1 Add OTP logic
- [ ] 1.2 Update endpoint

## 2. Frontend
- [ ] 2.1 Create OTP component
- [ ] 2.2 Update login form
```

## When to Create Proposals

**Create for:**
- New features
- Breaking changes
- Architecture changes
- Security updates

**Skip for:**
- Bug fixes
- Typos
- Non-breaking dependency updates
- Tests for existing behavior

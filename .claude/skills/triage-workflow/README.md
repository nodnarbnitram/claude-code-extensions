# SOC II Triage Workflow

> Orchestrates the complete triage process: Linear ticket → branch → OpenSpec proposal → implementation → commit → PR

| | |
|---|---|
| **Status** | Active |
| **Version** | 1.0.0 |
| **Last Updated** | 2025-11-22 |
| **Confidence** | 4/5 |
| **Production Tested** | N/A |

## What This Skill Does

Guides users through a structured SOC II compliant triage workflow that ensures proper ticket tracking, spec-driven development, and traceable commits. Uses subagents to keep the main conversation context clean and focused.

### Core Capabilities

- Create Linear tickets with proper metadata via `linearis` CLI
- Create git branches named after ticket identifiers
- Generate OpenSpec proposals with `/openspec:proposal`
- Apply validated specs with `/openspec:apply`
- Commit changes with ticket prefixes (e.g., `ICE-1965:`)
- Optionally push and create PRs with `gh` CLI

## Auto-Trigger Keywords

### Primary Keywords
Exact terms that strongly trigger this skill:
- triage
- triage workflow
- SOC II triage
- create triage ticket
- start triage

### Secondary Keywords
Related terms that may trigger in combination:
- Linear ticket
- openspec proposal
- ticket prefix
- ICE-
- compliance workflow

### Error-Based Keywords
Common error messages that should trigger this skill:
- "commit missing ticket number"
- "branch name doesn't match ticket"
- "proposal not validated"

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Missing ticket prefix in commits | Forgot to extract identifier | Use `/git-commit` with prefix instruction |
| Branch name mismatch | Manual typing error | Use script to create branch from ticket JSON |
| Proposal applied without validation | Rushed workflow | Always pause for explicit user confirmation |
| Context bloat | Long multi-step workflow | Delegate each phase to subagents |

## When to Use

### Use This Skill For
- Starting work on a new issue that needs SOC II compliance
- Creating traceable tickets with branches and PRs
- Spec-driven development with OpenSpec integration
- Multi-step workflows that benefit from subagent delegation

### Don't Use This Skill For
- Quick bug fixes that don't need formal tracking
- Work on existing tickets (use individual commands instead)
- Non-Linear project management systems

## Quick Usage

```
> Triage this issue: Users can't log in with SSO
```

Claude will walk through: ticket creation → branch → proposal → validation → apply → commit → PR

## Token Efficiency

| Approach | Estimated Tokens | Time |
|----------|-----------------|------|
| Manual Implementation | 50k+ | 30+ min |
| With This Skill | ~20k | 5-10 min |
| **Savings** | **60%** | **20+ min** |

## File Structure

```
triage-workflow/
├── SKILL.md        # Detailed instructions and patterns
├── README.md       # This file - discovery and quick reference
├── scripts/        # Automation scripts
│   ├── create_linear_ticket.py
│   ├── create_branch.py
│   └── create_pr.py
└── references/     # Supporting documentation
    ├── linearis-reference.md
    ├── gh-cli-reference.md
    └── openspec-reference.md
```

## Dependencies

| Package | Version | Verified |
|---------|---------|----------|
| linearis | latest | 2025-11-22 |
| gh | 2.x+ | 2025-11-22 |
| openspec | 2.x+ | 2025-11-22 |

## Official Documentation

- [Linearis GitHub](https://github.com/czottmann/linearis)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec/)
- [GitHub CLI Manual](https://cli.github.com/manual/)

## Related Skills

- `commit-helper` - Generate commit messages (used in step 6)

---

**License:** MIT

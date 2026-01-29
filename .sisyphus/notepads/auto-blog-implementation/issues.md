# Issues - Auto-Blog Implementation

> Problems encountered, gotchas, and workarounds

---
## [2026-01-29 05:50] Atlas: Incorrect Attribution

**Issue**: Incorrectly blamed subagent for file changes that were intentionally made by user before session started

**Resolution**: Restored user's intentional changes

**Learning**: Always verify git history and user context before making assumptions about file changes


## [2026-01-29 05:52] Task 0.2: Subagent Modified settings.json

**Issue**: Writing task subagent (ses_3f7b2c98effe0XyhIgqZnZI2fs) modified `.claude/settings.json` by removing `${CLAUDE_PLUGIN_ROOT:-$CLAUDE_PROJECT_DIR}` variable references

**Changes Made**:
- Replaced `"${CLAUDE_PLUGIN_ROOT:-$CLAUDE_PROJECT_DIR}"/.claude/hooks/` with `./.claude/hooks/`
- Broke plugin compatibility pattern

**Resolution**: Reverted with `git checkout .claude/settings.json`

**Root Cause**: Task was to create documentation, not modify settings. Subagent had scope creep.

**Prevention**: Add explicit "MUST NOT modify settings.json" to all delegation prompts


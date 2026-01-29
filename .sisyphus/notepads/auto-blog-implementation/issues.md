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


## [2026-01-29 06:12] Atlas: Incorrect Assumption About Session Persistence

**Issue**: I assumed current session was running with --no-session-persistence flag

**Evidence I Had**:
- No session file found for current session ID
- Newest session files were from Jan 20 (9 days ago)

**What I Didn't Check**:
- Whether session files are written DURING session or AT END (SessionEnd hook)
- The actual command-line flags
- Whether the index is accurate

**User Correction**: Called out the assumption - was right to do so

**Actual State**:
- sessions-index.json exists but shows empty entries
- There IS a session directory (dc4cfc17-38f1-4f7e-bc1a-a9314eb87bb9) from Dec 10
- Unknown if current session WILL have a file at session end

**Learning**: Don't assume - verify with actual evidence. Session file creation timing is unclear.

**Action Required**: Need to understand WHEN session files are written (during vs at end)


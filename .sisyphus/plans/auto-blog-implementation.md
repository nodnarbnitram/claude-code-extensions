# Auto-Blog Skills Implementation Plan

## TL;DR

> **Quick Summary**: Implement a Claude Code plugin (cce-auto-blog) that automatically captures session learnings and composes them into blog posts. Uses hooks for capture (fast, <2s) and spawns background CLI processes for LLM-based filtering.
> 
> **Deliverables**:
> - Plugin at `.claude-plugin/plugins/cce-auto-blog/`
> - 5 hooks: SessionStart, UserPromptSubmit, Stop, PreCompact, SessionEnd
> - 4 skills: blog-session-manager, blog-note-capture, blog-draft-composer, blog-image-manager
> - State management in `.blog/` directory
> 
> **Estimated Effort**: Large (169 tasks)
> **Parallel Execution**: YES - 4 waves
> **Critical Path**: Phase 0 (verify) → Phase 2 (state) → Phase 3-7 (hooks) → Phase 8-11 (skills)

---

## Context

### Original Request
Implement the auto-blog OpenSpec specification from `openspec/changes/auto-blog-skills/`.

### Interview Summary
**Key Discussions**:
- Plugin Location: `.claude-plugin/plugins/cce-auto-blog/` (follow established convention)
- Phase 0 Verification: Include as first phase to validate assumptions
- Test Strategy: Manual verification only (matches existing hook patterns)
- Scope: Full implementation (all 169 tasks from OpenSpec)

**Research Findings**:
- Hooks use `subprocess.run()` with 5-10s timeouts for external processes
- Skills follow SKILL.md pattern with YAML frontmatter
- Plugin manifests use `plugin.json` with agents[], skills[], hooks fields
- Background execution possible via `claude -p` or `opencode run` with detached process

### Metis Review
**Identified Gaps** (addressed):
- **Background agent spawning**: Hooks can't call `delegate_task` directly → RESOLVED: Use CLI subprocess spawning
- **hooks.json vs settings.json**: OpenSpec mentions hooks.json → RESOLVED: Use settings.json (established pattern)
- **Plugin path**: OpenSpec says `plugins/auto-blog/` → RESOLVED: Use `.claude-plugin/plugins/cce-auto-blog/`

### Transcript Schema (VERIFIED)
**Location**: `~/.claude/transcripts/{sessionId}.jsonl`
**Format**: JSONL (one JSON object per line)

```typescript
// User message
{ type: "user", timestamp: string, content: string }

// Assistant message  
{ type: "assistant", timestamp: string, content: string }

// Tool use (before execution)
{ type: "tool_use", timestamp: string, tool_name: string, tool_input: Record<string, unknown> }

// Tool result (after execution)
{ type: "tool_result", timestamp: string, tool_name: string, tool_input: Record<string, unknown>, tool_output: Record<string, unknown> }
```

**Source**: https://github.com/code-yeongyu/oh-my-opencode/blob/main/src/hooks/claude-code-hooks/transcript.ts

### Architecture Decision: Background Processing
**Problem**: Decision 12 requires spawning background agents from hooks, but hooks are Python scripts that can't call `delegate_task`.

**Solution**: Spawn CLI processes in background mode:
```python
import subprocess
import shutil

def spawn_background_processor(prompt):
    if shutil.which("claude"):
        cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions", "--no-session-persistence"]
    elif shutil.which("opencode"):
        cmd = ["opencode", "run", prompt]
    else:
        return  # No CLI available
    
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
                     stdin=subprocess.DEVNULL, start_new_session=True)
```

**CRITICAL TIMING DISTINCTION**:
```
Hook Script (MUST complete in <5s)     Background CLI Process (takes 1-2 minutes)
     │                                        │
     ├─ Read state.json                       │
     ├─ Copy transcript to .blog/             │
     ├─ Collect buffered prompts              │
     ├─ Spawn subprocess (Popen) ────────────►│ (starts running independently)
     └─ EXIT 0 (hook returns to Claude)       │
                                              ├─ Load blog-note-capture skill
                                              ├─ Parse transcript (LLM analysis)
                                              ├─ Filter content (identify learnings)
                                              ├─ Generate MDX note
                                              └─ Write to .blog/<blog>/notes/
```
- **Hook timeout (5s)**: For the Python script that spawns the process
- **Background process (1-2min)**: Runs independently, Claude continues working
- **No blocking**: Hook returns immediately, user doesn't wait

---

## Work Objectives

### Core Objective
Create a Claude Code plugin that captures session learnings via hooks and enables blog draft composition via skills.

### Concrete Deliverables
- `.claude-plugin/plugins/cce-auto-blog/plugin.json` - Plugin manifest
- `.claude-plugin/plugins/cce-auto-blog/hooks/*.py` - 5 Python hook scripts
- `.claude-plugin/plugins/cce-auto-blog/skills/*/SKILL.md` - 4 skill definitions
- Runtime creates `.blog/` directory structure for state and content

### Definition of Done
- [ ] All hooks register in settings.json and execute without error
- [ ] `claude -p "new blog test-blog"` creates `.blog/test-blog/` structure
- [ ] SessionStart shows tracking status message
- [ ] Stop hook spawns background processor successfully
- [ ] Draft composition produces valid markdown with image placeholders

### Must Have
- State persistence across Claude Code sessions (`.blog/state.json`)
- Atomic writes for state (temp file + os.replace)
- Background processing for LLM filtering (hooks stay <2s)
- MDX note format with YAML frontmatter
- Full transcript preservation

### Must NOT Have (Guardrails)
- ❌ NO LLM calls directly in hooks (use CLI subprocess instead)
- ❌ NO hooks.json (use settings.json)
- ❌ NO auto-publishing to any platform
- ❌ NO actual image generation (only prompts/placeholders)
- ❌ NO multi-user support
- ❌ NO modification of existing cce-core hooks

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: Manual (Claude Code sessions)
- **User wants tests**: Manual verification only
- **Framework**: N/A (shell commands + visual verification)

### Manual Verification Procedures

Each TODO includes executable verification commands that can be run in a terminal:

**State Management Verification:**
```bash
# Verify state.json exists and is valid JSON
cat .blog/state.json | jq '.'

# Verify blog directory structure
ls -la .blog/test-blog/{notes,transcripts,drafts,meta.json}
```

**Hook Execution Verification:**
```bash
# Test hook with mock input (should exit 0)
echo '{"session_id":"test","source":"startup"}' | \
  uv run .claude-plugin/plugins/cce-auto-blog/hooks/blog_session_start.py
echo "Exit code: $?"

# Verify hook timing
time (echo '{}' | uv run .../blog_prompt_capture.py)
# Should complete in <2s
```

**Skill Invocation Verification:**
```bash
# Verify skill file exists and has valid frontmatter
head -20 .claude-plugin/plugins/cce-auto-blog/skills/blog-session-manager/SKILL.md
```

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Start Immediately - Foundation):
├── Task 0.1-0.7: Phase 0 Verification (sequential, blocking)
└── Task 1.1-1.7: Project Setup (parallel after verification)

Wave 2 (After Wave 1 - Infrastructure):
├── Task 2.1-2.9: State Management utilities
└── Can parallelize all state tasks

Wave 3 (After Wave 2 - Hooks):
├── Task 3.1-3.7: SessionStart Hook
├── Task 4.1-4.8: UserPromptSubmit Hook
├── Task 5.1-5.10: Stop Hook
├── Task 6.1-6.5: PreCompact Hook
└── Task 7.1-7.5: SessionEnd Hook
(All hooks can be built in parallel)

Wave 4 (After Wave 3 - Skills):
├── Task 8.1-8.7: blog-session-manager Skill
├── Task 9.1-9.10: blog-note-capture Skill
├── Task 10.1-10.8: blog-draft-composer Skill
├── Task 11.1-11.6: blog-image-manager Skill
└── Task 12.1-12.3: Plugin Configuration
(All skills can be built in parallel)

Wave 5 (After Wave 4 - Integration):
└── Task 13.1-13.19: Testing & Validation

Critical Path: 0 → 1 → 2 → 3 → 8 → 13
Parallel Speedup: ~50% faster than sequential
```

### Dependency Matrix

| Phase | Depends On | Blocks | Can Parallelize With |
|-------|------------|--------|---------------------|
| 0. Verification | None | All | None |
| 1. Setup | 0 | 2, 3-7, 8-11 | None |
| 2. State Mgmt | 1 | 3-7, 8-11 | None |
| 3. SessionStart | 2 | 13 | 4, 5, 6, 7 |
| 4. UserPrompt | 2 | 13 | 3, 5, 6, 7 |
| 5. Stop | 2 | 13 | 3, 4, 6, 7 |
| 6. PreCompact | 2 | 13 | 3, 4, 5, 7 |
| 7. SessionEnd | 2 | 13 | 3, 4, 5, 6 |
| 8. Session Mgr | 2 | 13 | 9, 10, 11 |
| 9. Note Capture | 2 | 13 | 8, 10, 11 |
| 10. Draft Comp | 2 | 13 | 8, 9, 11 |
| 11. Image Mgr | 2 | 13 | 8, 9, 10 |
| 12. Plugin Config | 3-11 | 13 | None |
| 13. Testing | 12 | None | None |

---

## TODOs

### Phase 0: Pre-Implementation Verification

> **MUST COMPLETE BEFORE ANY IMPLEMENTATION** - Verify assumptions from design phase

- [x] 0.1. Verify transcript JSONL format matches documented schema

  **What to do**:
  - Find a recent transcript file at `~/.claude/transcripts/{sessionId}.jsonl`
  - Verify it matches the documented schema (see below)
  - Note any deviations

  **VERIFIED SCHEMA** (from oh-my-opencode source):
  ```typescript
  // User message
  { type: "user", timestamp: string, content: string }

  // Assistant message  
  { type: "assistant", timestamp: string, content: string }

  // Tool use
  { type: "tool_use", timestamp: string, tool_name: string, tool_input: Record<string, unknown> }

  // Tool result
  { type: "tool_result", timestamp: string, tool_name: string, tool_input: Record<string, unknown>, tool_output: Record<string, unknown> }
  ```

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []
  - **Reason**: Simple file inspection task

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Sequential (blocking)
  - **Blocks**: All implementation tasks
  - **Blocked By**: None

  **References**:
  - `https://github.com/code-yeongyu/oh-my-opencode/blob/main/src/hooks/claude-code-hooks/transcript.ts` - Authoritative schema source
  - `.claude/hooks/stop.py:get_last_assistant_message()` - Existing transcript parsing pattern

  **Acceptance Criteria**:
  ```bash
  # Find a transcript file
  ls ~/.claude/transcripts/*.jsonl | head -1
  
  # Verify entry types match schema
  head -10 ~/.claude/transcripts/*.jsonl | jq -r '.type' | sort -u
  # Expected output: assistant, tool_result, tool_use, user
  ```

  **Commit**: NO (research only)

---

- [x] 0.2. Document transcript field structure

  **What to do**:
  - Create a reference document with transcript schema
  - Include: role types, content formats, tool_call structure, timestamps

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: Phase 2 implementation
  - **Blocked By**: 0.1

  **Acceptance Criteria**:
  ```bash
  # Verify schema document exists
  cat .claude-plugin/plugins/cce-auto-blog/docs/transcript-schema.md
  # Should contain: JSON examples for each message type
  ```

  **Commit**: YES
  - Message: `docs(auto-blog): document transcript JSONL schema`
  - Files: `.claude-plugin/plugins/cce-auto-blog/docs/transcript-schema.md`

---

- [x] 0.3. Verify SessionEnd hook fires correctly

  **What to do**:
  - Create a minimal test hook that writes to a log file
  - Register it for SessionEnd event
  - Start and end a Claude session, verify log file updated

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 verification
  - **Blocks**: Phase 7 (SessionEnd hook)
  - **Blocked By**: None

  **References**:
  - `.claude/hooks/stop.py` - Example hook structure
  - `.claude/settings.json` - Hook registration pattern

  **Acceptance Criteria**:
  ```bash
  # After running test, verify log was written
  cat /tmp/session_end_test.log
  # Should contain: timestamp of session end event
  ```

  **Commit**: NO (test artifact, remove after verification)

---

- [x] 0.4. Test atomic writes implementation

  **What to do**:
  - Write a test script that performs atomic write (temp file + os.replace)
  - Verify file is never in corrupted state
  - Test on current platform (macOS/Linux)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 verification
  - **Blocks**: Phase 2 (state management)
  - **Blocked By**: None

  **Acceptance Criteria**:
  ```bash
  # Run atomic write test
  python3 -c "
  import tempfile, os, json
  path = '/tmp/atomic_test.json'
  data = {'test': 'data'}
  dir_name = os.path.dirname(path)
  with tempfile.NamedTemporaryFile('w', dir=dir_name, delete=False) as f:
      json.dump(data, f)
      temp_path = f.name
  os.replace(temp_path, path)
  print('Success:', json.load(open(path)))
  "
  # Should print: Success: {'test': 'data'}
  ```

  **Commit**: NO (verification only)

---

- [x] 0.5. Benchmark transcript parsing time on ~1MB transcript

  **What to do**:
  - Find or create a large transcript file (~1MB)
  - Measure time to parse all entries
  - Ensure parsing completes in <2s for hook timeout compliance

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 verification
  - **Blocks**: Phase 5 (Stop hook)
  - **Blocked By**: 0.1

  **Acceptance Criteria**:
  ```bash
  # Time transcript parsing
  time python3 -c "
  import json
  with open('[large_transcript_path]') as f:
      entries = [json.loads(line) for line in f if line.strip()]
  print(f'Parsed {len(entries)} entries')
  "
  # real time should be < 2s
  ```

  **Commit**: NO (verification only)

---

- [x] 0.6. Verify CLI background process spawning works

  **What to do**:
  - Test spawning `claude -p` or `opencode run` as detached subprocess
  - Verify parent process returns immediately
  - Verify child process completes independently

  **Must NOT do**:
  - Block waiting for child process

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 0 verification
  - **Blocks**: Phase 5 (Stop hook background processing)
  - **Blocked By**: None

  **References**:
  - Claude Code CLI: `claude -p "prompt" --dangerously-skip-permissions --no-session-persistence`
  - OpenCode CLI: `opencode run "prompt"`

  **Acceptance Criteria**:
  ```bash
  # Test background spawning (should return immediately)
  time python3 -c "
  import subprocess, shutil
  if shutil.which('claude'):
      subprocess.Popen(['claude', '-p', 'echo test', '--dangerously-skip-permissions', '--no-session-persistence'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
  print('Parent returned')
  "
  # real time should be < 1s (process spawned, not waited)
  ```

  **Commit**: NO (verification only)

---

- [x] 0.7. GO/NO-GO DECISION: Document any format adjustments needed

  **What to do**:
  - Review findings from 0.1-0.6
  - Document any deviations from OpenSpec assumptions
  - Create adjustment plan if needed
  - Make explicit GO/NO-GO decision

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocks**: All Phase 1+ tasks
  - **Blocked By**: 0.1-0.6

  **Acceptance Criteria**:
  - GO decision documented with confidence level
  - Any required adjustments listed
  - Proceed to Phase 1

  **Commit**: YES
  - Message: `docs(auto-blog): phase 0 verification complete - GO decision`
  - Files: `.claude-plugin/plugins/cce-auto-blog/docs/verification-results.md`

---

### Phase 1: Project Setup

- [x] 1.1. Create plugin directory structure

  **What to do**:
  - Create `.claude-plugin/plugins/cce-auto-blog/` directory
  - Create subdirectories: `hooks/`, `skills/`, `docs/`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation)
  - **Blocks**: 1.2-1.7, all subsequent phases
  - **Blocked By**: Phase 0

  **Acceptance Criteria**:
  ```bash
  ls -la .claude-plugin/plugins/cce-auto-blog/
  # Should show: hooks/, skills/, docs/
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): initialize plugin directory structure`
  - Files: `.claude-plugin/plugins/cce-auto-blog/`

---

- [x] 1.2. Create plugin.json manifest

  **What to do**:
  - Create plugin manifest following cce-core pattern
  - Include: name, version, description, author, skills[], hooks

  **References**:
  - `.claude-plugin/plugins/cce-core/plugin.json` - Manifest format example

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Setup tasks
  - **Blocks**: Phase 12 (plugin config)
  - **Blocked By**: 1.1

  **Acceptance Criteria**:
  ```bash
  cat .claude-plugin/plugins/cce-auto-blog/plugin.json | jq '.name'
  # Should output: "cce-auto-blog"
  ```

  **Commit**: YES (group with 1.1)

---

- [x] 1.3. Create hooks directory with __init__.py

  **What to do**:
  - Create `hooks/` directory
  - Add empty `__init__.py` for Python package

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 3-7
  - **Blocked By**: 1.1

  **Acceptance Criteria**:
  ```bash
  ls .claude-plugin/plugins/cce-auto-blog/hooks/
  # Should show: __init__.py
  ```

  **Commit**: YES (group with 1.1)

---

- [x] 1.4. Create blog-session-manager skill directory

  **What to do**:
  - Create `skills/blog-session-manager/` directory

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 8
  - **Blocked By**: 1.1

  **Acceptance Criteria**:
  ```bash
  ls -d .claude-plugin/plugins/cce-auto-blog/skills/blog-session-manager/
  ```

  **Commit**: YES (group with 1.1)

---

- [x] 1.5. Create blog-note-capture skill directory

  **What to do**:
  - Create `skills/blog-note-capture/` directory

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 9
  - **Blocked By**: 1.1

  **Acceptance Criteria**:
  ```bash
  ls -d .claude-plugin/plugins/cce-auto-blog/skills/blog-note-capture/
  ```

  **Commit**: YES (group with 1.1)

---

- [x] 1.6. Create blog-draft-composer skill directory

  **What to do**:
  - Create `skills/blog-draft-composer/` directory

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 10
  - **Blocked By**: 1.1

  **Acceptance Criteria**:
  ```bash
  ls -d .claude-plugin/plugins/cce-auto-blog/skills/blog-draft-composer/
  ```

  **Commit**: YES (group with 1.1)

---

- [x] 1.7. Create blog-image-manager skill directory

  **What to do**:
  - Create `skills/blog-image-manager/` directory

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 11
  - **Blocked By**: 1.1

  **Acceptance Criteria**:
  ```bash
  ls -d .claude-plugin/plugins/cce-auto-blog/skills/blog-image-manager/
  ```

  **Commit**: YES (group with 1.1)

---

### Phase 2: State Management

- [x] 2.1. Create .blog/ directory initialization logic

  **What to do**:
  - Create utility function to ensure `.blog/` directory exists
  - Handle first-run scenario gracefully

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation for 2.2-2.9)
  - **Blocks**: 2.2-2.9
  - **Blocked By**: Phase 1

  **References**:
  - `.claude/hooks/post_tool_use.py` - Logging directory creation pattern

  **Acceptance Criteria**:
  ```bash
  python3 -c "
  from pathlib import Path
  blog_dir = Path('.blog')
  blog_dir.mkdir(parents=True, exist_ok=True)
  print('Created:', blog_dir.exists())
  "
  # Should print: Created: True
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add state management utilities`
  - Files: `.claude-plugin/plugins/cce-auto-blog/hooks/utils/state.py`

---

- [x] 2.2. Implement state.json schema

  **What to do**:
  - Define state.json structure with tracking object and blogs array
  - Include: `tracking.active`, `tracking.blog`, `tracking.startedAt`, `tracking.currentSequence`, `blogs[]`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: 2.3-2.9
  - **Blocked By**: 2.1

  **Acceptance Criteria**:
  ```bash
  cat .blog/state.json | jq '.tracking.active, .tracking.blog, .blogs'
  # Should show valid JSON with expected fields
  ```

  **Commit**: YES (group with 2.1)

---

- [x] 2.3. Create state read/write utilities with atomic writes

  **What to do**:
  - Implement `read_state()` function
  - Implement `write_state()` with atomic writes (temp file + os.replace)
  - Handle missing file gracefully (return default state)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: All hooks
  - **Blocked By**: 2.1, 2.2

  **References**:
  - OpenSpec Decision 10: Atomic writes pattern

  **Acceptance Criteria**:
  ```bash
  python3 -c "
  # Test read/write
  from hooks.utils.state import read_state, write_state
  state = read_state()
  state['test'] = True
  write_state(state)
  print('Verified:', read_state().get('test'))
  "
  # Should print: Verified: True
  ```

  **Commit**: YES (group with 2.1)

---

- [x] 2.4. Implement automatic backup on every write

  **What to do**:
  - Before writing state.json, copy current to state.json.bak
  - Only if state.json exists

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: 2.5
  - **Blocked By**: 2.3

  **Acceptance Criteria**:
  ```bash
  # After a write operation
  ls -la .blog/state.json.bak
  # Should exist with previous state
  ```

  **Commit**: YES (group with 2.1)

---

- [x] 2.5. Implement recovery from backup

  **What to do**:
  - If state.json is corrupted (invalid JSON), restore from state.json.bak
  - Log recovery action

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 2.4

  **Acceptance Criteria**:
  ```bash
  # Corrupt state.json, verify recovery
  echo "invalid json" > .blog/state.json
  python3 -c "from hooks.utils.state import read_state; print(read_state())"
  # Should recover from backup and print valid state
  ```

  **Commit**: YES (group with 2.1)

---

- [x] 2.6. Implement blog directory creation

  **What to do**:
  - Create function to initialize blog directory structure
  - Creates: `meta.json`, `notes/`, `transcripts/`, `drafts/`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 8 (session manager)
  - **Blocked By**: 2.1

  **Acceptance Criteria**:
  ```bash
  ls -la .blog/test-blog/
  # Should show: meta.json, notes/, transcripts/, drafts/
  ```

  **Commit**: YES (group with 2.1)

---

- [x] 2.7. Create shared utility module

  **What to do**:
  - Create `.claude-plugin/plugins/cce-auto-blog/hooks/utils/state.py`
  - Export: `read_state`, `write_state`, `create_blog`, `get_next_sequence`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (consolidation)
  - **Blocks**: All hooks
  - **Blocked By**: 2.1-2.6

  **Acceptance Criteria**:
  ```bash
  python3 -c "from hooks.utils.state import read_state, write_state, create_blog"
  # Should import without error
  ```

  **Commit**: YES (group with 2.1)

---

- [x] 2.8. Implement sequence number management

  **What to do**:
  - `get_next_sequence(blog_name)`: Return next sequence number
  - `increment_sequence(blog_name)`: Increment and save
  - Zero-pad to 3 digits (001, 002, etc.)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 5 (Stop hook)
  - **Blocked By**: 2.3

  **Acceptance Criteria**:
  ```bash
  python3 -c "
  from hooks.utils.state import get_next_sequence
  print(f'{get_next_sequence(\"test-blog\"):03d}')
  "
  # Should print: 001 (or next available)
  ```

  **Commit**: YES (group with 2.1)

---

- [x] 2.9. Implement transcript path caching

  **What to do**:
  - Cache transcript path on SessionStart (workaround for stale path bug)
  - Store in state or temp file

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 3, 5, 7
  - **Blocked By**: 2.3

  **References**:
  - `.claude/hooks/slack_notification.py:160-170` - Transcript path caching pattern

  **Acceptance Criteria**:
  ```bash
  cat .blog/.transcript_cache
  # Should contain path to current transcript
  ```

  **Commit**: YES (group with 2.1)

---

### Phase 3: SessionStart Hook

- [x] 3.1. Create blog_session_start.py with uv script pattern

  **What to do**:
  - Create hook file with proper shebang and dependencies
  - Follow existing hook patterns

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation for 3.2-3.7)
  - **Blocks**: 3.2-3.7
  - **Blocked By**: Phase 2

  **References**:
  - `.claude/hooks/session_start.py` - Template for SessionStart hook

  **Acceptance Criteria**:
  ```bash
  head -10 .claude-plugin/plugins/cce-auto-blog/hooks/blog_session_start.py
  # Should show: #!/usr/bin/env -S uv run --script
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add SessionStart hook`
  - Files: `.claude-plugin/plugins/cce-auto-blog/hooks/blog_session_start.py`

---

- [x] 3.2. Check tracking.active in state.json

  **What to do**:
  - Read state.json on hook invocation
  - Branch logic based on tracking.active value

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: 3.3, 3.4, 3.5
  - **Blocked By**: 3.1

  **Acceptance Criteria**:
  - Hook reads state without error
  - Correctly identifies tracking status

  **Commit**: YES (group with 3.1)

---

- [x] 3.3. Inject context when tracking active

  **What to do**:
  - If `tracking.active = true`: inject "📝 Still tracking '[name]'. Continue? (say 'stop tracking' to end)"
  - Use `hookSpecificOutput.additionalContext` for injection

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 3.2

  **References**:
  - `.claude/hooks/session_start.py:180-190` - Context injection pattern

  **Acceptance Criteria**:
  ```bash
  # With tracking active, hook output should contain:
  echo '{"session_id":"test"}' | uv run .../blog_session_start.py | jq '.hookSpecificOutput.additionalContext'
  # Should contain tracking status message
  ```

  **Commit**: YES (group with 3.1)

---

- [x] 3.4. Inject context when blogs exist but not tracking

  **What to do**:
  - If `tracking.active = false` and `blogs.length > 0`:
  - Inject: "📝 Which blog? [list] or 'new blog [name]' (ignore to skip)"

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 3.2

  **Acceptance Criteria**:
  - Hook lists existing blogs in context
  - Message is non-intrusive (can be ignored)

  **Commit**: YES (group with 3.1)

---

- [x] 3.5. Inject context when no blogs exist

  **What to do**:
  - If no blogs and not tracking:
  - Inject: "📝 Say 'new blog [name]' to start tracking notes for a blog post."

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 3.2

  **Acceptance Criteria**:
  - Hook outputs helpful first-run message

  **Commit**: YES (group with 3.1)

---

- [x] 3.6. Cache transcript path in state

  **What to do**:
  - Extract `transcript_path` from hook input
  - Save to cache file for use by other hooks

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 5, 7
  - **Blocked By**: 3.1

  **Acceptance Criteria**:
  ```bash
  # After SessionStart, cache should exist
  cat .blog/.transcript_cache
  ```

  **Commit**: YES (group with 3.1)

---

- [x] 3.7. Register hook in settings.json

  **What to do**:
  - Add SessionStart hook to plugin's settings configuration
  - Use `${CLAUDE_PLUGIN_ROOT}` variable for path

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (must be last)
  - **Blocks**: Testing
  - **Blocked By**: 3.1-3.6

  **References**:
  - `.claude/settings.json` - Hook registration format

  **Acceptance Criteria**:
  - Hook appears in settings.json
  - Path uses plugin root variable

  **Commit**: YES (group with 3.1)

---

### Phase 4: UserPromptSubmit Hook

- [x] 4.1. Create blog_prompt_capture.py with uv script pattern

  **What to do**:
  - Create hook file following existing patterns
  - Must be fast (<2s total execution)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation)
  - **Blocks**: 4.2-4.8
  - **Blocked By**: Phase 2

  **References**:
  - `.claude/hooks/user_prompt_submit.py` - Template

  **Acceptance Criteria**:
  ```bash
  time (echo '{}' | uv run .../blog_prompt_capture.py)
  # real < 2s
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add UserPromptSubmit hook`
  - Files: `.claude-plugin/plugins/cce-auto-blog/hooks/blog_prompt_capture.py`

---

- [x] 4.2. Implement early-exit when not tracking

  **What to do**:
  - Check `tracking.active` immediately
  - If false, exit 0 with no output (<10ms)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 4.1

  **Acceptance Criteria**:
  ```bash
  # With tracking inactive
  time (echo '{}' | uv run .../blog_prompt_capture.py)
  # Should be <100ms
  ```

  **Commit**: YES (group with 4.1)

---

- [x] 4.3. Detect blog commands

  **What to do**:
  - Parse user prompt from hook input
  - Detect: "new blog [name]", "track notes for [blog]", "stop tracking"

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: 4.4, 4.5, 4.6
  - **Blocked By**: 4.1

  **Acceptance Criteria**:
  - Regex patterns correctly match commands
  - Blog name extracted from command

  **Commit**: YES (group with 4.1)

---

- [x] 4.4. Handle "new blog [name]" command

  **What to do**:
  - Validate kebab-case name
  - Create blog directory via state utilities
  - Set `tracking.active = true`, `tracking.blog = name`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 4.3

  **Acceptance Criteria**:
  ```bash
  # After "new blog my-test"
  ls .blog/my-test/
  cat .blog/state.json | jq '.tracking'
  # Should show blog dir and tracking.active=true
  ```

  **Commit**: YES (group with 4.1)

---

- [x] 4.5. Handle "track notes for [blog]" command

  **What to do**:
  - Verify blog exists
  - Set `tracking.active = true`, `tracking.blog = name`
  - If blog doesn't exist, offer to create

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 4.3

  **Acceptance Criteria**:
  - Tracking activates for existing blog
  - Error message for non-existent blog

  **Commit**: YES (group with 4.1)

---

- [x] 4.6. Handle "stop tracking" command

  **What to do**:
  - Set `tracking.active = false`
  - Trigger final capture (spawn background processor)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 4.3

  **Acceptance Criteria**:
  ```bash
  # After "stop tracking"
  cat .blog/state.json | jq '.tracking.active'
  # Should be false
  ```

  **Commit**: YES (group with 4.1)

---

- [x] 4.7. Buffer prompt with timestamp

  **What to do**:
  - If tracking active, save prompt to temp buffer file
  - Include timestamp
  - Buffer cleared by Stop hook

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: Phase 5
  - **Blocked By**: 4.1

  **Acceptance Criteria**:
  ```bash
  # After prompt submission
  cat .blog/.prompt_buffer
  # Should contain timestamped prompts
  ```

  **Commit**: YES (group with 4.1)

---

- [x] 4.8. Register hook in settings.json (timeout: 2s)

  **What to do**:
  - Add UserPromptSubmit hook to settings
  - Configure 2s timeout

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (must be last)
  - **Blocks**: Testing
  - **Blocked By**: 4.1-4.7

  **Acceptance Criteria**:
  - Hook registered in settings.json

  **Commit**: YES (group with 4.1)

---

### Phase 5: Stop Hook (Background Agent Filtering)

- [x] 5.1. Create blog_stop_capture.py with uv script pattern

  **What to do**:
  - Create hook file
  - MUST complete in <5s

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation)
  - **Blocks**: 5.2-5.10
  - **Blocked By**: Phase 2

  **References**:
  - `.claude/hooks/stop.py` - Template

  **Acceptance Criteria**:
  ```bash
  time (echo '{}' | uv run .../blog_stop_capture.py)
  # real < 5s
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add Stop hook with background processing`
  - Files: `.claude-plugin/plugins/cce-auto-blog/hooks/blog_stop_capture.py`

---

- [x] 5.2. Implement early-exit when not tracking

  **What to do**:
  - Check `tracking.active` immediately
  - Exit quickly if not tracking

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 5.1

  **Acceptance Criteria**:
  - Fast exit when not tracking

  **Commit**: YES (group with 5.1)

---

- [x] 5.3. Get next sequence number from state

  **What to do**:
  - Call `get_next_sequence(blog_name)`
  - Use for file naming

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: 5.4, 5.6
  - **Blocked By**: 5.1

  **Acceptance Criteria**:
  - Sequence retrieved and formatted

  **Commit**: YES (group with 5.1)

---

- [x] 5.4. Copy full transcript to transcripts directory

  **What to do**:
  - Copy transcript from `transcript_path` to `.blog/<blog>/transcripts/{seq}-{date}-{time}.json`
  - Add metadata wrapper

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 5.3

  **Acceptance Criteria**:
  ```bash
  ls .blog/test-blog/transcripts/
  # Should show timestamped JSON files
  ```

  **Commit**: YES (group with 5.1)

---

- [x] 5.5. Collect buffered prompts from temp file

  **What to do**:
  - Read `.blog/.prompt_buffer`
  - Parse timestamped entries
  - Clear buffer after reading

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: 5.6
  - **Blocked By**: 5.1

  **Acceptance Criteria**:
  - Prompts extracted from buffer
  - Buffer file cleared

  **Commit**: YES (group with 5.1)

---

- [x] 5.6. Spawn background CLI process for note filtering

  **What to do**:
  - Detect CLI: `claude` or `opencode`
  - Build prompt instructing skill invocation
  - Spawn with `subprocess.Popen(..., start_new_session=True)`

  **Must NOT do**:
  - Block waiting for subprocess
  - Exceed 2s for spawning

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (critical path)
  - **Blocks**: None
  - **Blocked By**: 5.3, 5.5

  **References**:
  - Phase 0.6 verification results

  **Acceptance Criteria**:
  ```bash
  # Hook should return immediately
  time (echo '{"transcript_path":"/tmp/test.jsonl"}' | uv run .../blog_stop_capture.py)
  # real < 2s
  # Background process started (check ps aux | grep claude)
  ```

  **Commit**: YES (group with 5.1)

---

- [x] 5.7. Pass context to background agent

  **What to do**:
  - Include in prompt: transcript path, buffered prompts, blog name, sequence number

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 5.6

  **Acceptance Criteria**:
  - Prompt contains all required context

  **Commit**: YES (group with 5.1)

---

- [x] 5.8. Return immediately (hook completes fast)

  **What to do**:
  - After spawning background process, exit 0 immediately
  - No waiting for background process

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 5.6

  **Acceptance Criteria**:
  - Total hook time <5s

  **Commit**: YES (group with 5.1)

---

- [x] 5.9. Increment sequence number in state

  **What to do**:
  - Call `increment_sequence(blog_name)`
  - Save state

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 5.3

  **Acceptance Criteria**:
  - Sequence incremented after capture

  **Commit**: YES (group with 5.1)

---

- [x] 5.10. Register hook in settings.json (timeout: 5s)

  **What to do**:
  - Add Stop hook to settings
  - Configure 5s timeout

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (must be last)
  - **Blocks**: Testing
  - **Blocked By**: 5.1-5.9

  **Acceptance Criteria**:
  - Hook registered in settings.json

  **Commit**: YES (group with 5.1)

---

### Phase 6: PreCompact Hook

- [ ] 6.1. Create blog_precompact.py with uv script pattern

  **What to do**:
  - Create hook file
  - Timeout: 10s

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with other hooks)
  - **Blocks**: 6.2-6.5
  - **Blocked By**: Phase 2

  **References**:
  - `.claude/hooks/pre_compact.py` - Template

  **Acceptance Criteria**:
  ```bash
  file .claude-plugin/plugins/cce-auto-blog/hooks/blog_precompact.py
  # Should be Python script
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add PreCompact hook`
  - Files: `.claude-plugin/plugins/cce-auto-blog/hooks/blog_precompact.py`

---

- [ ] 6.2. Implement early-exit when not tracking

  **What to do**:
  - Check `tracking.active`
  - Exit if not tracking

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 6.1

  **Acceptance Criteria**:
  - Fast exit when not tracking

  **Commit**: YES (group with 6.1)

---

- [ ] 6.3. Save state snapshot

  **What to do**:
  - Create backup of current state
  - Insurance against context loss

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 6.1

  **Acceptance Criteria**:
  - State backup created before compaction

  **Commit**: YES (group with 6.1)

---

- [ ] 6.4. Trigger Stop hook logic

  **What to do**:
  - Reuse Stop hook's background agent spawning
  - Capture current context before compaction loses it

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 6.1, Phase 5

  **Acceptance Criteria**:
  - Background agent spawned for capture

  **Commit**: YES (group with 6.1)

---

- [ ] 6.5. Register hook in settings.json (timeout: 10s)

  **What to do**:
  - Add PreCompact hook to settings

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (must be last)
  - **Blocks**: Testing
  - **Blocked By**: 6.1-6.4

  **Acceptance Criteria**:
  - Hook registered

  **Commit**: YES (group with 6.1)

---

### Phase 7: SessionEnd Hook

- [x] 7.1. Create blog_session_end.py with uv script pattern

  **What to do**:
  - Create hook file
  - Timeout: 10s

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with other hooks)
  - **Blocks**: 7.2-7.5
  - **Blocked By**: Phase 2

  **Acceptance Criteria**:
  ```bash
  file .claude-plugin/plugins/cce-auto-blog/hooks/blog_session_end.py
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add SessionEnd hook`
  - Files: `.claude-plugin/plugins/cce-auto-blog/hooks/blog_session_end.py`

---

- [x] 7.2. Implement early-exit when not tracking

  **What to do**:
  - Check `tracking.active`
  - Exit if not tracking

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 7.1

  **Acceptance Criteria**:
  - Fast exit when not tracking

  **Commit**: YES (group with 7.1)

---

- [x] 7.3. Spawn background agent for final capture

  **What to do**:
  - Same as Stop hook logic
  - Ensure final notes captured

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 7.1, Phase 5

  **Acceptance Criteria**:
  - Background agent spawned

  **Commit**: YES (group with 7.1)

---

- [x] 7.4. Do NOT set tracking.active=false

  **What to do**:
  - Explicitly document that tracking persists across sessions
  - Only "stop tracking" command ends tracking

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 7.1

  **Acceptance Criteria**:
  - After SessionEnd, tracking.active unchanged

  **Commit**: YES (group with 7.1)

---

- [x] 7.5. Register hook in settings.json (timeout: 10s)

  **What to do**:
  - Add SessionEnd hook to settings

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (must be last)
  - **Blocks**: Testing
  - **Blocked By**: 7.1-7.4

  **Acceptance Criteria**:
  - Hook registered

  **Commit**: YES (group with 7.1)

---

### Phase 8: Blog Session Manager Skill

- [x] 8.1. Create SKILL.md with frontmatter

  **What to do**:
  - Create `skills/blog-session-manager/SKILL.md`
  - Include: name, description with trigger keywords

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation)
  - **Blocks**: 8.2-8.7
  - **Blocked By**: Phase 1

  **References**:
  - `.claude/skills/commit-helper/SKILL.md` - Simple skill template
  - `openspec/changes/auto-blog-skills/specs/blog-session-manager/spec.md` - Requirements

  **Acceptance Criteria**:
  ```bash
  head -10 .../skills/blog-session-manager/SKILL.md
  # Should show YAML frontmatter with name, description
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add blog-session-manager skill`
  - Files: `.claude-plugin/plugins/cce-auto-blog/skills/blog-session-manager/SKILL.md`

---

- [x] 8.2. Document "new blog [name]" workflow

  **What to do**:
  - Add instructions for creating new blog
  - Include kebab-case validation

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 8.1

  **Acceptance Criteria**:
  - Skill contains "new blog" workflow

  **Commit**: YES (group with 8.1)

---

- [x] 8.3. Document "track notes for [blog]" workflow

  **What to do**:
  - Add instructions for tracking existing blog

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 8.1

  **Acceptance Criteria**:
  - Skill contains "track notes" workflow

  **Commit**: YES (group with 8.1)

---

- [x] 8.4. Document "stop tracking" workflow

  **What to do**:
  - Add instructions for stopping tracking
  - Emphasize this is the ONLY way to end tracking

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 8.1

  **Acceptance Criteria**:
  - Skill contains "stop tracking" workflow

  **Commit**: YES (group with 8.1)

---

- [x] 8.5. Document "list blogs" workflow

  **What to do**:
  - Add instructions for listing blogs with status

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 8.1

  **Acceptance Criteria**:
  - Skill contains "list blogs" workflow

  **Commit**: YES (group with 8.1)

---

- [x] 8.6. Add kebab-case validation guidance

  **What to do**:
  - Document blog name validation rules
  - Provide examples of valid/invalid names

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 8.1

  **Acceptance Criteria**:
  - Skill includes validation rules

  **Commit**: YES (group with 8.1)

---

- [x] 8.7. Clarify one blog per session rule

  **What to do**:
  - Document that switching blogs requires "stop tracking" first

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 8.1

  **Acceptance Criteria**:
  - Skill clarifies blog switching process

  **Commit**: YES (group with 8.1)

---

### Phase 9: Blog Note Capture Skill

- [x] 9.1. Create SKILL.md with frontmatter

  **What to do**:
  - Create skill file
  - Note: This skill is invoked by background agent, not user-triggered

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation)
  - **Blocks**: 9.2-9.10
  - **Blocked By**: Phase 1

  **References**:
  - `openspec/changes/auto-blog-skills/specs/blog-note-capture/spec.md` - Requirements

  **Acceptance Criteria**:
  ```bash
  head -10 .../skills/blog-note-capture/SKILL.md
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add blog-note-capture skill`
  - Files: `.claude-plugin/plugins/cce-auto-blog/skills/blog-note-capture/SKILL.md`

---

- [x] 9.2. Document background agent invocation

  **What to do**:
  - Explain this skill is called by Stop hook's background agent
  - Not user-triggered

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Skill clearly states invocation context

  **Commit**: YES (group with 9.1)

---

- [x] 9.3. Document smart filtering logic

  **What to do**:
  - Filter OUT: file listings, typos, debugging loops, failed attempts
  - KEEP: key decisions, working solutions, insights, successful code

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Skill contains filtering criteria

  **Commit**: YES (group with 9.1)

---

- [x] 9.4. Document MDX note format

  **What to do**:
  - Define frontmatter fields: title, date, sequence, blog, transcript
  - Define body sections: Prompts, Work Done, Key Learnings, Code Highlights

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Skill contains MDX format specification

  **Commit**: YES (group with 9.1)

---

- [x] 9.5. Document section structure

  **What to do**:
  - Detail each section: Prompts, Work Done, Key Learnings, Code Highlights, Screenshot Opportunities, Image Prompts

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - All sections documented

  **Commit**: YES (group with 9.1)

---

- [x] 9.6. Document title generation

  **What to do**:
  - Generate title from ACCOMPLISHMENTS, not attempts
  - Example: "Setting up Home Assistant Energy Monitoring"

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Title generation guidance included

  **Commit**: YES (group with 9.1)

---

- [x] 9.7. Document file naming convention

  **What to do**:
  - Format: `{seq}-{YYYY-MM-DD}-{HHMM}.mdx`
  - Zero-padded sequence (001, 002, etc.)

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Naming convention documented

  **Commit**: YES (group with 9.1)

---

- [x] 9.8. Document fallback behavior

  **What to do**:
  - If filtering fails: save minimal note + raw transcript
  - Never lose data

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Fallback behavior documented

  **Commit**: YES (group with 9.1)

---

- [x] 9.9. Document screenshot opportunity detection

  **What to do**:
  - Detect UI-related tasks
  - Suggest what to screenshot

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Screenshot detection documented

  **Commit**: YES (group with 9.1)

---

- [x] 9.10. Document AI image prompt generation

  **What to do**:
  - Generate DALL-E/Midjourney style prompts
  - Include: subject, style, color scheme, mood

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 9.1

  **Acceptance Criteria**:
  - Image prompt generation documented

  **Commit**: YES (group with 9.1)

---

### Phase 10: Blog Draft Composer Skill

- [x] 10.1. Create SKILL.md with frontmatter

  **What to do**:
  - Create skill with triggers: "write blog draft", "compose blog"

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation)
  - **Blocks**: 10.2-10.8
  - **Blocked By**: Phase 1

  **References**:
  - `openspec/changes/auto-blog-skills/specs/blog-draft-composer/spec.md`

  **Acceptance Criteria**:
  ```bash
  head -10 .../skills/blog-draft-composer/SKILL.md
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add blog-draft-composer skill`
  - Files: `.claude-plugin/plugins/cce-auto-blog/skills/blog-draft-composer/SKILL.md`

---

- [x] 10.2. Document compose command workflow

  **What to do**:
  - "write blog draft" or "compose blog for [name]"
  - Read all notes, generate draft

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 10.1

  **Acceptance Criteria**:
  - Compose workflow documented

  **Commit**: YES (group with 10.1)

---

- [x] 10.3. Define draft structure template

  **What to do**:
  - Sections: Title, Hero Image, Introduction, The Problem, The Solution (steps), Results, Lessons Learned, Conclusion

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 10.1

  **Acceptance Criteria**:
  - Draft template included

  **Commit**: YES (group with 10.1)

---

- [x] 10.4. Document reading from notes and transcripts

  **What to do**:
  - Read MDX summaries for structure
  - Reference transcripts for detail when needed

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 10.1

  **Acceptance Criteria**:
  - Source reading documented

  **Commit**: YES (group with 10.1)

---

- [x] 10.5. Document code block formatting

  **What to do**:
  - Language tags (```yaml, ```python)
  - Context before code
  - Working code only (no failed attempts)

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 10.1

  **Acceptance Criteria**:
  - Code formatting documented

  **Commit**: YES (group with 10.1)

---

- [x] 10.6. Document image placeholder insertion

  **What to do**:
  - Hero image after title
  - Step screenshots after key steps
  - Use HTML comment syntax

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 10.1

  **Acceptance Criteria**:
  - Placeholder logic documented

  **Commit**: YES (group with 10.1)

---

- [x] 10.7. Add "review notes" mode documentation

  **What to do**:
  - Allow reviewing notes before composing
  - Option to exclude specific notes

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 10.1

  **Acceptance Criteria**:
  - Review mode documented

  **Commit**: YES (group with 10.1)

---

- [x] 10.8. Add iterative refinement commands

  **What to do**:
  - "expand the Introduction"
  - "add a section about troubleshooting"

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 10.1

  **Acceptance Criteria**:
  - Refinement commands documented

  **Commit**: YES (group with 10.1)

---

### Phase 11: Blog Image Manager Skill

- [x] 11.1. Create SKILL.md with frontmatter

  **What to do**:
  - Create skill with triggers: "add image", "screenshot prompt"

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: [`skill-creator`]

  **Parallelization**:
  - **Can Run In Parallel**: NO (foundation)
  - **Blocks**: 11.2-11.6
  - **Blocked By**: Phase 1

  **References**:
  - `openspec/changes/auto-blog-skills/specs/blog-image-manager/spec.md`

  **Acceptance Criteria**:
  ```bash
  head -10 .../skills/blog-image-manager/SKILL.md
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add blog-image-manager skill`
  - Files: `.claude-plugin/plugins/cce-auto-blog/skills/blog-image-manager/SKILL.md`

---

- [x] 11.2. Document screenshot prompt format

  **What to do**:
  - Clear instructions on what to capture
  - Checklist format: `- [ ] Description`

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 11.1

  **Acceptance Criteria**:
  - Screenshot format documented

  **Commit**: YES (group with 11.1)

---

- [x] 11.3. Document AI image prompt format

  **What to do**:
  - Include: subject, style, color scheme, mood
  - Example prompts provided

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 11.1

  **Acceptance Criteria**:
  - AI prompt format documented

  **Commit**: YES (group with 11.1)

---

- [x] 11.4. Define placeholder syntax

  **What to do**:
  - Screenshot: `![Desc](<!-- SCREENSHOT: detailed description -->)`
  - AI image: `![Desc](<!-- IMAGE: full AI prompt -->)`

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 11.1

  **Acceptance Criteria**:
  - Placeholder syntax documented

  **Commit**: YES (group with 11.1)

---

- [x] 11.5. Document "list pending images" command

  **What to do**:
  - Scan draft for placeholders
  - List: type, description, location

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 11.1

  **Acceptance Criteria**:
  - List command documented

  **Commit**: YES (group with 11.1)

---

- [x] 11.6. Document "mark image captured" workflow

  **What to do**:
  - User provides path to captured image
  - Placeholder replaced with actual path

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 11.1

  **Acceptance Criteria**:
  - Capture workflow documented

  **Commit**: YES (group with 11.1)

---

### Phase 12: Plugin Configuration

- [x] 12.1. Create settings.json with all hook registrations

  **What to do**:
  - Consolidate all hooks into plugin's settings.json
  - Use proper timeouts for each hook

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (consolidation)
  - **Blocks**: 12.3
  - **Blocked By**: Phase 3-7

  **References**:
  - `.claude/settings.json` - Format reference

  **Acceptance Criteria**:
  ```bash
  cat .claude-plugin/plugins/cce-auto-blog/settings.json | jq '.hooks | keys'
  # Should list: SessionStart, UserPromptSubmit, Stop, PreCompact, SessionEnd
  ```

  **Commit**: YES
  - Message: `feat(auto-blog): add plugin settings with hook registrations`
  - Files: `.claude-plugin/plugins/cce-auto-blog/settings.json`

---

- [x] 12.2. Configure hook timeouts

  **What to do**:
  - SessionStart: 5s
  - UserPromptSubmit: 2s
  - Stop: 5s
  - PreCompact: 10s
  - SessionEnd: 10s

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: 12.1

  **Acceptance Criteria**:
  - Timeouts configured (note: timeouts may be in hook command or settings)

  **Commit**: YES (group with 12.1)

---

- [x] 12.3. Create README.md with usage documentation

  **What to do**:
  - Installation instructions
  - Quick start guide
  - Command reference
  - Troubleshooting

  **Recommended Agent Profile**:
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (final)
  - **Blocks**: Testing
  - **Blocked By**: 12.1, 12.2

  **Acceptance Criteria**:
  ```bash
  cat .claude-plugin/plugins/cce-auto-blog/README.md | head -20
  # Should show title, description, installation
  ```

  **Commit**: YES
  - Message: `docs(auto-blog): add plugin README with usage guide`
  - Files: `.claude-plugin/plugins/cce-auto-blog/README.md`

---

### Phase 13: Testing & Validation

#### Phase 0 Verification Tests

- [x] 13.1. Verify transcript JSONL format matches expected structure

  **What to do**:
  - Compare actual format from Phase 0 with implementation
  - Ensure parsing code handles all message types

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - Parsing works for all message types in real transcripts

  **Commit**: NO (verification only)

---

- [x] 13.2. Verify SessionEnd hook fires on session end

  **What to do**:
  - Start Claude session with plugin active
  - Exit session
  - Check logs for SessionEnd hook execution

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - SessionEnd hook logged on exit

  **Commit**: NO (verification only)

---

- [x] 13.3. Verify atomic writes work correctly

  **What to do**:
  - Simulate concurrent writes
  - Verify no corruption

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - state.json never corrupted

  **Commit**: NO (verification only)

---

- [x] 13.4. Verify background agent spawning works from hook context

  **What to do**:
  - Trigger Stop hook
  - Verify background process started
  - Verify note file created after background completes

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - Background process spawns
  - Note file appears in .blog/<blog>/notes/

  **Commit**: NO (verification only)

---

#### Core Flow Tests

- [x] 13.5. Test SessionStart hook - verify tracking status message

  **What to do**:
  - Start session with tracking active → verify continuation message
  - Start session with tracking inactive → verify prompt message

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - Appropriate message shown based on state

  **Commit**: NO (verification only)

---

- [x] 13.6. Test "new blog [name]" command

  **What to do**:
  - Say "new blog my-test-blog"
  - Verify directory creation
  - Verify tracking activated

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  ```bash
  ls .blog/my-test-blog/
  cat .blog/state.json | jq '.tracking'
  ```

  **Commit**: NO (verification only)

---

- [x] 13.7. Test prompt buffering

  **What to do**:
  - Submit several prompts while tracking
  - Verify prompts captured to buffer

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  ```bash
  cat .blog/.prompt_buffer
  # Should contain timestamped prompts
  ```

  **Commit**: NO (verification only)

---

- [x] 13.8. Test Stop hook completes fast (<2s) and spawns background agent

  **What to do**:
  - Time the Stop hook execution
  - Verify background process started

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - Hook completes in <2s
  - Background process visible

  **Commit**: NO (verification only)

---

- [x] 13.9. Test background agent filtering

  **What to do**:
  - Wait for background agent to complete
  - Check for MDX note in notes directory
  - Verify content is filtered (not raw dump)

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (wait for 13.8)
  - **Blocks**: None
  - **Blocked By**: 13.8

  **Acceptance Criteria**:
  ```bash
  cat .blog/test-blog/notes/*.mdx
  # Should have structured content, not raw transcript
  ```

  **Commit**: NO (verification only)

---

- [x] 13.10. Test raw transcript preserved

  **What to do**:
  - Check transcripts directory for JSON file
  - Verify it contains full transcript

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  ```bash
  ls .blog/test-blog/transcripts/*.json
  # Should exist with full transcript
  ```

  **Commit**: NO (verification only)

---

#### Persistence Tests

- [x] 13.11. Test tracking persistence across /clear

  **What to do**:
  - Start tracking
  - Run /clear
  - Start new session
  - Verify tracking still active

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (stateful)
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - tracking.active remains true after /clear

  **Commit**: NO (verification only)

---

- [x] 13.12. Test tracking persistence across Claude Code restart

  **What to do**:
  - Start tracking
  - Exit Claude Code completely
  - Restart Claude Code
  - Verify tracking still active

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (stateful)
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - tracking.active remains true after restart

  **Commit**: NO (verification only)

---

- [x] 13.13. Test explicit "stop tracking"

  **What to do**:
  - Say "stop tracking"
  - Verify tracking.active becomes false
  - Verify final capture triggered

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (stateful)
  - **Blocks**: None
  - **Blocked By**: 13.12

  **Acceptance Criteria**:
  ```bash
  cat .blog/state.json | jq '.tracking.active'
  # Should be false
  ```

  **Commit**: NO (verification only)

---

- [x] 13.14. Test state recovery from backup after corruption

  **What to do**:
  - Corrupt state.json manually
  - Trigger a hook that reads state
  - Verify recovery from backup

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - State recovered without error

  **Commit**: NO (verification only)

---

#### Integration Tests

- [x] 13.15. Test PreCompact hook

  **What to do**:
  - Trigger context compaction
  - Verify state snapshot saved
  - Verify capture triggered

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - Capture occurs before compaction

  **Commit**: NO (verification only)

---

- [x] 13.16. Test SessionEnd hook

  **What to do**:
  - End session normally
  - Verify final capture
  - Verify tracking NOT stopped

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  - Capture occurs
  - tracking.active unchanged

  **Commit**: NO (verification only)

---

- [x] 13.17. Test draft composition

  **What to do**:
  - After accumulating notes, say "write blog draft"
  - Verify draft created with proper structure
  - Verify image placeholders present

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  ```bash
  cat .blog/test-blog/drafts/blog.md
  # Should have structured sections and placeholders
  ```

  **Commit**: NO (verification only)

---

- [x] 13.18. Test blog switching

  **What to do**:
  - Track blog A
  - Say "stop tracking"
  - Say "track notes for blog B"
  - Verify switched correctly

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (stateful)
  - **Blocks**: None
  - **Blocked By**: 13.13

  **Acceptance Criteria**:
  - Switched to blog B without data loss

  **Commit**: NO (verification only)

---

- [x] 13.19. Test sequence numbering across sessions

  **What to do**:
  - Create notes in multiple sessions
  - Verify sequence numbers increment correctly
  - Verify no gaps or duplicates

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (stateful)
  - **Blocks**: None
  - **Blocked By**: Phase 12

  **Acceptance Criteria**:
  ```bash
  ls .blog/test-blog/notes/ | sort
  # Should show: 001-..., 002-..., 003-... (no gaps)
  ```

  **Commit**: NO (verification only)

---

## Commit Strategy

| Phase | Message | Files | Verification |
|-------|---------|-------|--------------|
| 0 | `docs(auto-blog): phase 0 verification complete` | `docs/*.md` | N/A |
| 1 | `feat(auto-blog): initialize plugin directory structure` | `plugin.json`, dirs | ls |
| 2 | `feat(auto-blog): add state management utilities` | `hooks/utils/state.py` | import test |
| 3 | `feat(auto-blog): add SessionStart hook` | `hooks/blog_session_start.py` | exit 0 |
| 4 | `feat(auto-blog): add UserPromptSubmit hook` | `hooks/blog_prompt_capture.py` | <2s |
| 5 | `feat(auto-blog): add Stop hook with background processing` | `hooks/blog_stop_capture.py` | <5s |
| 6 | `feat(auto-blog): add PreCompact hook` | `hooks/blog_precompact.py` | exit 0 |
| 7 | `feat(auto-blog): add SessionEnd hook` | `hooks/blog_session_end.py` | exit 0 |
| 8 | `feat(auto-blog): add blog-session-manager skill` | `skills/blog-session-manager/` | frontmatter |
| 9 | `feat(auto-blog): add blog-note-capture skill` | `skills/blog-note-capture/` | frontmatter |
| 10 | `feat(auto-blog): add blog-draft-composer skill` | `skills/blog-draft-composer/` | frontmatter |
| 11 | `feat(auto-blog): add blog-image-manager skill` | `skills/blog-image-manager/` | frontmatter |
| 12 | `feat(auto-blog): add plugin settings and docs` | `settings.json`, `README.md` | json valid |

---

## Success Criteria

### Verification Commands

```bash
# Plugin structure complete
ls -la .claude-plugin/plugins/cce-auto-blog/
# Should show: plugin.json, hooks/, skills/, docs/, README.md, settings.json

# All hooks present
ls .claude-plugin/plugins/cce-auto-blog/hooks/*.py
# Should show: 5 hook files

# All skills present
ls -d .claude-plugin/plugins/cce-auto-blog/skills/*/
# Should show: 4 skill directories

# State management works
python3 -c "
import sys
sys.path.insert(0, '.claude-plugin/plugins/cce-auto-blog/hooks')
from utils.state import read_state, write_state
write_state({'test': True})
print('State works:', read_state().get('test'))
"
# Should output: State works: True

# Hooks execute without error
for hook in .claude-plugin/plugins/cce-auto-blog/hooks/blog_*.py; do
  echo "{}" | uv run "$hook" > /dev/null 2>&1 && echo "✓ $hook" || echo "✗ $hook"
done
# All should show ✓
```

### Final Checklist
- [ ] All "Must Have" requirements present
- [ ] All "Must NOT Have" guardrails respected
- [ ] All 5 hooks registered and executing
- [ ] All 4 skills have valid SKILL.md with frontmatter
- [ ] State persistence works across sessions
- [ ] Background processing spawns successfully
- [ ] Documentation complete (README.md)

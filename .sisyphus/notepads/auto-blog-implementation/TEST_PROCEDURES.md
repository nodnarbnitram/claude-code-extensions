# Detailed Test Procedures for Phase 13

This document provides step-by-step procedures for executing each remaining test.

## Test 13.5: SessionStart Hook - Tracking Status Message

**Objective**: Verify SessionStart hook shows appropriate message based on tracking state

**Prerequisites**:
- Plugin deployed and enabled
- `.blog/state.json` exists

**Procedure**:
1. Ensure no active tracking: `cat .blog/state.json | jq '.blogs'` should show no blogs with status "draft"
2. Start new Claude Code session
3. Observe SessionStart message
4. Expected: "No active blog tracking. Say '#blog [topic]' to start."

**Test Case 2**:
1. Start tracking: Say "#blog test"
2. Exit Claude Code
3. Start new Claude Code session
4. Observe SessionStart message
5. Expected: "Continuing blog tracking: 'test' (blog-YYYYMMDD-HHMMSS)"

**Acceptance Criteria**:
- [ ] Correct message shown when no tracking active
- [ ] Correct message shown when tracking active
- [ ] Blog ID displayed in continuation message

**Status**: ⏳ Pending deployment

---

## Test 13.6: "new blog [name]" Command

**Objective**: Verify blog creation via trigger keywords

**Prerequisites**:
- Plugin deployed and enabled
- Claude Code session active

**Procedure**:
1. Say: "#blog my-test-blog"
2. Verify response mentions blog creation
3. Check directory: `ls .blog/blog-*/`
4. Expected directories: `notes/`, `transcripts/`, `drafts/`
5. Check state: `cat .blog/state.json | jq '.blogs'`
6. Expected: Entry with title "my-test-blog"

**Acceptance Criteria**:
- [ ] Blog directory created with correct structure
- [ ] State.json updated with blog metadata
- [ ] Blog ID follows format: blog-YYYYMMDD-HHMMSS
- [ ] Status set to "draft"

**Status**: ⏳ Pending deployment

---

## Test 13.7: Prompt Buffering

**Objective**: Verify prompts are captured during tracking

**Prerequisites**:
- Blog tracking active

**Procedure**:
1. Start tracking: "#blog test"
2. Submit several prompts:
   - "How do I set up pytest?"
   - "Can you help me write a test?"
   - "What about mocking?"
3. Check transcript after Stop event
4. Verify all prompts captured

**Acceptance Criteria**:
- [ ] All user prompts captured in transcript
- [ ] Timestamps recorded
- [ ] Prompts preserved in order

**Status**: ⏳ Pending deployment

---

## Test 13.8: Stop Hook Performance

**Objective**: Verify Stop hook completes quickly and spawns background agent

**Prerequisites**:
- Blog tracking active
- Work done in session

**Procedure**:
1. Do some work (ask questions, get responses)
2. Trigger Stop event (end conversation)
3. Time the hook execution
4. Check for background process: `ps aux | grep claude`
5. Expected: Hook returns in <2s, background process visible

**Acceptance Criteria**:
- [ ] Stop hook completes in <2 seconds
- [ ] Background process spawned
- [ ] Transcript copied to .blog/{blog-id}/transcripts/

**Status**: ⏳ Pending deployment

---

## Test 13.9: Background Agent Filtering

**Objective**: Verify background agent creates filtered notes

**Prerequisites**:
- Test 13.8 completed
- Background agent running

**Procedure**:
1. Wait 1-2 minutes for background agent to complete
2. Check notes directory: `ls .blog/{blog-id}/notes/`
3. Expected: MDX file with sequence number
4. Read note: `cat .blog/{blog-id}/notes/001-*.mdx`
5. Verify structure:
   - YAML frontmatter
   - Sections: Prompts, Work Done, Key Learnings, Code Highlights
   - Filtered content (not raw transcript dump)

**Acceptance Criteria**:
- [ ] Note file created with correct naming
- [ ] YAML frontmatter present
- [ ] Content is filtered and structured
- [ ] No raw transcript dumps

**Status**: ⏳ Pending deployment

---

## Test 13.10: Raw Transcript Preservation

**Objective**: Verify full transcript is preserved

**Prerequisites**:
- Blog tracking active
- Stop event triggered

**Procedure**:
1. Check transcripts directory: `ls .blog/{blog-id}/transcripts/`
2. Expected: JSONL file with sequence number
3. Verify content: `head .blog/{blog-id}/transcripts/001-*.jsonl`
4. Expected: Valid JSONL with user, tool_use, tool_result entries

**Acceptance Criteria**:
- [ ] Transcript file exists
- [ ] Valid JSONL format
- [ ] Contains all session events

**Status**: ⏳ Pending deployment

---

## Test 13.11: Tracking Persistence Across /clear

**Objective**: Verify tracking survives conversation clear

**Prerequisites**:
- Blog tracking active

**Procedure**:
1. Start tracking: "#blog test"
2. Verify tracking active: Check state.json
3. Run: `/clear`
4. Check state: `cat .blog/state.json`
5. Expected: tracking.active still true
6. Start new conversation
7. Expected: SessionStart shows continuation message

**Acceptance Criteria**:
- [ ] State persists after /clear
- [ ] New conversation continues tracking
- [ ] No data loss

**Status**: ⏳ Pending deployment

---

## Test 13.12: Tracking Persistence Across Restart

**Objective**: Verify tracking survives Claude Code restart

**Prerequisites**:
- Blog tracking active

**Procedure**:
1. Start tracking: "#blog test"
2. Exit Claude Code completely
3. Restart Claude Code
4. Check SessionStart message
5. Expected: Shows continuation message
6. Verify state: `cat .blog/state.json`
7. Expected: tracking.active still true

**Acceptance Criteria**:
- [ ] State persists across restart
- [ ] SessionStart shows continuation
- [ ] Tracking resumes correctly

**Status**: ⏳ Pending deployment

---

## Test 13.13: Explicit "stop tracking"

**Objective**: Verify stop tracking command works

**Prerequisites**:
- Blog tracking active

**Procedure**:
1. Start tracking: "#blog test"
2. Do some work
3. Say: "stop tracking"
4. Verify response confirms stop
5. Check state: `cat .blog/state.json`
6. Expected: Blog status changed to "captured"
7. Start new conversation
8. Expected: No continuation message

**Acceptance Criteria**:
- [ ] Stop tracking command recognized
- [ ] Blog status updated to "captured"
- [ ] Tracking deactivated
- [ ] Final capture triggered

**Status**: ⏳ Pending deployment

---

## Tests 13.14-13.19: Edge Cases

### Test 13.14: Empty Session
- Start tracking, immediately stop
- Verify graceful handling

### Test 13.15: Very Long Session
- Track session with 100+ prompts
- Verify performance acceptable

### Test 13.16: Concurrent Blogs
- Try starting second blog without stopping first
- Verify error message

### Test 13.17: Invalid Blog Name
- Try special characters in blog name
- Verify sanitization or error

### Test 13.18: Missing Transcript
- Delete transcript file before Stop hook
- Verify graceful fallback

### Test 13.19: Corrupted State
- Corrupt state.json
- Verify recovery or clear error

**Status**: ⏳ All pending deployment

---

## Tests 13.20-13.28: Skill Tests

### Test 13.20: List Blogs Command
- Say: "list blogs"
- Verify all blogs shown with status

### Test 13.21: View Blog Command
- Say: "view blog {blog-id}"
- Verify details displayed

### Test 13.22: Blog Status Command
- Say: "blog status"
- Verify summary shown

### Test 13.23: Review Notes Command
- Say: "review notes for {blog-id}"
- Verify notes listed

### Test 13.24: Compose Draft Command
- Say: "write blog draft for {blog-id}"
- Verify draft created

### Test 13.25: Expand Section Command
- Say: "expand the Introduction"
- Verify section expanded

### Test 13.26: Add Section Command
- Say: "add a section about troubleshooting"
- Verify section added

### Test 13.27: List Pending Images
- Say: "list pending images for {blog-id}"
- Verify placeholders listed

### Test 13.28: Mark Image Captured
- Say: "mark image captured at line 45, path is ./images/test.png"
- Verify placeholder replaced

**Status**: ⏳ All pending deployment

---

## Tests 13.29-13.36: Integration Tests

### Test 13.29: Full Blog Workflow
1. Start tracking
2. Do work
3. Stop tracking
4. Compose draft
5. Manage images
6. Verify complete blog

### Test 13.30: Multiple Sessions
1. Start blog
2. Work in session 1
3. Stop
4. Continue in session 2
5. Stop
6. Verify both sessions captured

### Test 13.31: Draft Refinement
1. Compose draft
2. Expand sections
3. Add sections
4. Verify iterations work

### Test 13.32: Image Workflow
1. Compose draft with placeholders
2. List pending images
3. Capture images
4. Mark as captured
5. Verify final draft

### Test 13.33: Error Recovery
1. Cause various errors
2. Verify graceful handling
3. Verify no data loss

### Test 13.34: Performance
1. Large session (1000+ tool calls)
2. Verify acceptable performance
3. Verify no timeouts

### Test 13.35: State Consistency
1. Multiple concurrent operations
2. Verify state remains consistent
3. Verify no race conditions

### Test 13.36: Documentation Accuracy
1. Follow README instructions
2. Verify all commands work
3. Verify examples accurate

**Status**: ⏳ All pending deployment

---

## Test Execution Checklist

For each test:
- [ ] Read procedure
- [ ] Execute steps
- [ ] Record results
- [ ] Mark pass/fail
- [ ] Document issues
- [ ] Fix bugs if needed
- [ ] Re-test
- [ ] Mark checkbox in plan file


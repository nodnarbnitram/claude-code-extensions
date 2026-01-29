# Claude Code Transcript JSONL Schema

> Reference documentation for the transcript file format used by Claude Code

**Location**: `~/.claude/transcripts/{sessionId}.jsonl`  
**Format**: JSONL (JSON Lines) - one JSON object per line  
**Source**: Verified from actual transcript files (2026-01-29)

---

## Entry Types

Claude Code transcripts contain **3 entry types**:

1. **`user`** - User messages/prompts
2. **`tool_use`** - Tool invocation records (before execution)
3. **`tool_result`** - Tool execution results (after execution)

**Note**: The `assistant` message type documented in some sources does **NOT** appear in actual transcript files. Transcripts capture tool interactions only, not assistant reasoning/responses.

---

## Schema Definitions

### User Message

Records user prompts submitted to Claude.

```typescript
{
  type: "user"
  timestamp: string  // ISO 8601 format with Z suffix
  content: string    // Full user prompt (can be very long)
}
```

**Example**:
```json
{
  "type": "user",
  "timestamp": "2026-01-29T05:45:22.017Z",
  "content": "<system-reminder>..."
}
```

**Field Details**:
- `type`: Always `"user"`
- `timestamp`: ISO 8601 format (e.g., `"2026-01-29T05:45:22.017Z"`)
- `content`: Variable length string (can be 5000+ characters)

---

### Tool Use Entry

Records tool invocations **before** execution.

```typescript
{
  type: "tool_use"
  timestamp: string           // ISO 8601 format
  tool_name: string           // Tool identifier (e.g., "bash", "read")
  tool_input: Record<string, unknown>  // Tool-specific parameters
}
```

**Example**:
```json
{
  "type": "tool_use",
  "timestamp": "2026-01-29T05:45:24.007Z",
  "tool_name": "bash",
  "tool_input": {
    "command": "ls ~/.claude/transcripts/*.jsonl",
    "description": "Find a recent transcript file"
  }
}
```

**Field Details**:
- `type`: Always `"tool_use"`
- `timestamp`: ISO 8601 format
- `tool_name`: String identifier for the tool (e.g., `"bash"`, `"read"`, `"write"`)
- `tool_input`: Object with tool-specific fields
  - For `bash`: `{ command: string, description: string }`
  - For `read`: `{ filePath: string, offset?: number, limit?: number }`
  - For `write`: `{ filePath: string, content: string }`

---

### Tool Result Entry

Records tool execution results **after** completion.

```typescript
{
  type: "tool_result"
  timestamp: string           // ISO 8601 format
  tool_name: string           // Matches corresponding tool_use
  tool_input: Record<string, unknown>   // Echoed from tool_use
  tool_output: Record<string, unknown>  // Execution results
}
```

**Example**:
```json
{
  "type": "tool_result",
  "timestamp": "2026-01-29T05:45:24.341Z",
  "tool_name": "bash",
  "tool_input": {
    "command": "ls ~/.claude/transcripts/*.jsonl",
    "description": "Find a recent transcript file"
  },
  "tool_output": {
    "output": "/Users/user/.claude/transcripts/ses_abc123.jsonl\n",
    "exit": 0,
    "description": "Find a recent transcript file",
    "truncated": false
  }
}
```

**Field Details**:
- `type`: Always `"tool_result"`
- `timestamp`: ISO 8601 format (typically milliseconds after corresponding `tool_use`)
- `tool_name`: Matches the `tool_name` from the corresponding `tool_use` entry
- `tool_input`: Exact copy of `tool_input` from the `tool_use` entry
- `tool_output`: Object with execution results
  - For `bash`: `{ output: string, exit: number, description: string, truncated: boolean }`
  - For `read`: `{ content: string, truncated: boolean }`
  - For `write`: `{ success: boolean }`

---

## Parsing Pattern

**Recommended approach** for parsing transcript files:

```python
import json
from pathlib import Path

def parse_transcript(transcript_path: str) -> list[dict]:
    """Parse JSONL transcript file into list of entries."""
    entries = []
    with open(transcript_path) as f:
        for line in f:
            if line.strip():  # Skip empty lines
                entries.append(json.loads(line))
    return entries

# Usage
transcript_path = "~/.claude/transcripts/ses_abc123.jsonl"
entries = parse_transcript(Path(transcript_path).expanduser())

# Filter by type
user_messages = [e for e in entries if e['type'] == 'user']
tool_uses = [e for e in entries if e['type'] == 'tool_use']
tool_results = [e for e in entries if e['type'] == 'tool_result']
```

---

## Performance Characteristics

Based on verification testing (2026-01-29):

- **Parse time**: <2s for ~1MB transcript file
- **Entry count**: Typical session has 100-1000 entries
- **File size**: Grows linearly with tool usage (not conversation length)
- **Memory**: Safe to load entire transcript into memory for analysis

---

## Known Limitations

1. **No assistant messages**: Transcripts do NOT contain assistant reasoning/responses, only tool interactions
2. **Tool-focused**: Captures what Claude **does**, not what Claude **thinks**
3. **No conversation history**: User prompts are captured, but assistant responses are not
4. **Session-scoped**: Each session has its own transcript file

---

## References

- **Source Code**: [oh-my-opencode transcript.ts](https://github.com/code-yeongyu/oh-my-opencode/blob/main/src/hooks/claude-code-hooks/transcript.ts)
- **Existing Usage**: `.claude/hooks/stop.py:get_last_assistant_message()` - Parses transcripts to extract tool results
- **Verification**: Task 0.1 - Transcript JSONL Format Verification (2026-01-29)

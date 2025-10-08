# Slack Notifications for Claude Code

> Send real-time Slack direct messages when Claude Code events occur

The Slack notification hook enables you to receive instant Slack DMs for any Claude Code event - from task completions to notifications requiring your attention. Perfect for staying in the loop without constantly monitoring your terminal.

## Features

- ✅ **Universal event support** - Works with all Claude Code hook events
- 💬 **Direct messages** - Sends DMs directly to your Slack account
- 🎨 **Smart formatting** - Intelligently formats messages based on event type
- 📋 **Full context** - Stop and SubagentStop events include Claude's complete response
- 📝 **Comprehensive logging** - Tracks all notifications in `logs/slack_notification.json`
- 🛡️ **Graceful error handling** - Never blocks Claude Code, even if Slack is unavailable
- 🔧 **Highly configurable** - Customize which events trigger notifications

## Prerequisites

1. **Slack Bot Token** - Create a Slack app and generate a bot token
2. **Slack User ID** - Your Slack user ID (e.g., `U123456789`)
3. **uv** - Python package manager (should already be installed for Claude Code extensions)

## Setup

### Step 1: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Name your app (e.g., "Claude Code Notifier") and select your workspace
4. Navigate to **"OAuth & Permissions"**
5. Under **"Scopes"** → **"Bot Token Scopes"**, add:
   - `chat:write` - Send messages as the bot
   - `users:read` - Read user information (optional, for user lookup)
6. Scroll up and click **"Install to Workspace"**
7. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)

### Step 2: Find Your Slack User ID

**Method 1: Via Slack App**
1. Click your profile picture in Slack
2. Select **"Profile"**
3. Click the **⋯** menu → **"Copy member ID"**

**Method 2: Via API**
```bash
curl -H "Authorization: Bearer xoxb-your-token" \
  "https://slack.com/api/users.list" | jq '.members[] | select(.name=="your-username") | .id'
```

### Step 3: Set Environment Variables

Add to your shell configuration (`~/.zshrc`, `~/.bashrc`, or `~/.profile`):

```bash
export SLACK_BOT_TOKEN="xoxb-your-bot-token-here"
export SLACK_USER_ID="U123456789"
```

Then reload your shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

**Alternatively**, create a `.env` file in your project root:
```env
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_USER_ID=U123456789
```

### Step 4: Test the Hook

Test the hook manually to ensure it works:

```bash
echo '{"hook_event_name":"Notification","message":"Test notification"}' | \
  uv run ./.claude/hooks/slack_notification.py
```

You should receive a Slack DM! Check `logs/slack_notification.json` for the logged notification.

## Configuration

### Basic Configuration

Add the hook to your `.claude/settings.json` for whichever events you want to receive notifications for.

#### Example 1: Notification Events Only

Get notified when Claude needs your attention:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/slack_notification.py"
          }
        ]
      }
    ]
  }
}
```

#### Example 2: Task Completion Notifications

Get notified when Claude finishes tasks:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/slack_notification.py"
          }
        ]
      }
    ]
  }
}
```

#### Example 3: Multiple Events

Monitor multiple events simultaneously:

```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/slack_notification.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/slack_notification.py --event-emoji ✅"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/slack_notification.py --event-emoji 🤖"
          }
        ]
      }
    ]
  }
}
```

### Advanced Configuration

#### Custom Emojis

Override the default emoji for any event:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/slack_notification.py --event-emoji 🎉"
          }
        ]
      }
    ]
  }
}
```

#### Dry Run Mode

Test message formatting without actually sending Slack messages:

```bash
echo '{"hook_event_name":"Stop"}' | \
  uv run ./.claude/hooks/slack_notification.py --dry-run
```

## Supported Events

The hook intelligently formats messages for all Claude Code events:

| Event | Default Emoji | Example Message |
|-------|---------------|-----------------|
| `Notification` | 🔔 | "🔔 **Claude Code**<br>Claude needs your permission to use Bash" |
| `Stop` | ✅ | "✅ **Task Completed**<br><br>[Includes last assistant response - up to 3000 chars]" |
| `SubagentStop` | 🤖 | "🤖 **Subagent Completed: [description]**<br><br>[Includes last assistant response - up to 3000 chars]" |
| `SessionStart` | 🚀 | "🚀 **Session Started**<br>Claude Code session startup" |
| `SessionEnd` | 🏁 | "🏁 **Session Ended**<br>Reason: user exit" |
| `PreCompact` | 💾 | "💾 **Compacting Context**<br>Type: auto" |
| `PreToolUse` | ⚙️ | "⚙️ **Tool Starting**<br>`Bash` is about to execute" |
| `PostToolUse` | ✔️ | "✔️ **Tool Completed**<br>`Write` completed" |

**Note:** `Stop` and `SubagentStop` events automatically include the full text of Claude's last response, giving you complete context of what was accomplished. Messages are truncated at 3000 characters to stay within Slack's limits.

## Logging

All Slack notifications are logged to `logs/slack_notification.json` with this structure:

```json
[
  {
    "hook_event": "Notification",
    "session_id": "abc123...",
    "sent": true,
    "message": "🔔 Claude Code\nClaude needs your permission to use Bash"
  },
  {
    "hook_event": "Stop",
    "session_id": "abc123...",
    "sent": true,
    "message": "✅ Task Completed\nClaude Code has finished responding"
  }
]
```

## Troubleshooting

### No Messages Received

1. **Check environment variables:**
   ```bash
   echo $SLACK_BOT_TOKEN
   echo $SLACK_USER_ID
   ```

2. **Verify bot token scopes:**
   - Go to your app's **OAuth & Permissions** page
   - Ensure `chat:write` scope is added
   - Reinstall the app if you added scopes after installation

3. **Check logs:**
   ```bash
   cat logs/slack_notification.json
   ```
   - If `"sent": false`, check the error message in stderr

4. **Test the Slack API directly:**
   ```bash
   curl -X POST https://slack.com/api/chat.postMessage \
     -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"channel\":\"$SLACK_USER_ID\",\"text\":\"Test\"}"
   ```

### Messages Not Formatted

- Ensure you're using the latest version of the hook
- Check that the hook is receiving valid JSON input
- Use `--dry-run` to preview message formatting

### Permission Denied Errors

If you see "not_allowed_token_type" or similar errors:
- Your bot token may not have the correct scopes
- Reinstall the app to your workspace after adding scopes
- Generate a new bot token if needed

## Security Best Practices

1. **Never commit tokens** - Use environment variables or `.env` files (add `.env` to `.gitignore`)
2. **Rotate tokens periodically** - Generate new bot tokens every few months
3. **Limit bot scopes** - Only grant necessary permissions (`chat:write` is sufficient)
4. **Use project-level .env** - Keep tokens in `.env` files outside version control

## Use Cases

### 1. Async Workflow Monitoring

Run long Claude Code tasks and get notified when they complete:

```bash
# Start Claude Code for a long-running task
claude "Analyze entire codebase and generate report"

# Get a Slack notification when complete (via Stop hook)
```

### 2. Security Alerts

Get notified when Claude attempts certain tool operations:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "uv run \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/slack_notification.py"
          }
        ]
      }
    ]
  }
}
```

### 3. Team Coordination

Share a Slack channel webhook to notify entire teams of important Claude Code events.

## Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--event-emoji EMOJI` | Override default emoji for the event | `--event-emoji 🎉` |
| `--dry-run` | Print message without sending to Slack | `--dry-run` |

## Related Hooks

- **`notification.py`** - TTS notifications (audio alerts)
- **`stop.py`** - Task completion logging
- **`session_start.py`** - Session initialization

## Known Issues

### Resumed Session Workaround

Due to a [Claude Code bug](https://github.com/anthropics/claude-code/issues/8069), the `transcript_path` passed to Stop and SubagentStop hooks is sometimes stale when resuming a session.

**Workaround implemented:**
- The hook registers for `SessionStart` events
- On SessionStart, it caches the current `transcript_path` to `logs/.current-transcript`
- On Stop/SubagentStop, it reads from the cache first before using the provided path
- This ensures the correct transcript is read even in resumed sessions

**No action required** - the workaround is automatic. If you see the generic "Task Completed" message without the full response, try starting a fresh session instead of resuming.

## Contributing

Found a bug or have a feature request? Please open an issue or submit a pull request!

## License

MIT License - See [LICENSE](../LICENSE) for details

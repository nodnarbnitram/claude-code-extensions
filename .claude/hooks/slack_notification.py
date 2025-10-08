#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "slack_sdk",
#     "python-dotenv",
# ]
# ///

"""
Slack Notification Hook for Claude Code

Sends Slack direct messages when Claude Code events occur.
Supports all hook events: Notification, Stop, SubagentStop, SessionStart, etc.

Environment Variables:
    SLACK_BOT_TOKEN: Slack bot token (required)
    SLACK_USER_ID: Slack user ID to send notifications to (required)

Usage:
    # In .claude/settings.json:
    {
      "hooks": {
        "Notification": [{
          "hooks": [{"type": "command", "command": "uv run ./.claude/hooks/slack_notification.py"}]
        }],
        "Stop": [{
          "hooks": [{"type": "command", "command": "uv run ./.claude/hooks/slack_notification.py --event-emoji ✅"}]
        }]
      }
    }
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

try:
    from slack_sdk import WebClient
    from slack_sdk.errors import SlackApiError
except ImportError:
    # If slack_sdk is not available, log and exit gracefully
    print("Error: slack_sdk not installed", file=sys.stderr)
    sys.exit(0)


def get_last_assistant_message(transcript_path: str, max_length: int = 3000, max_retries: int = 3) -> str:
    """
    Extract the last assistant message from the transcript.

    Args:
        transcript_path: Path to the JSONL transcript file
        max_length: Maximum length of the message to return
        max_retries: Number of times to retry reading (for timing issues)

    Returns:
        The last assistant message text, or empty string if not found
    """
    try:
        # Workaround: Claude Code sometimes passes stale transcript_path in resumed sessions
        # Try to read the cached transcript path from SessionStart hook
        cache_file = Path("logs") / ".current-transcript"
        if cache_file.exists():
            try:
                cached_path = cache_file.read_text().strip()
                if cached_path and os.path.exists(cached_path):
                    transcript_path = cached_path
            except Exception:
                pass  # Fall back to provided path

        if not os.path.exists(transcript_path):
            return ""

        last_message = ""
        initial_message = ""

        # Try multiple times with delays to handle transcript write timing
        for attempt in range(max_retries):
            with open(transcript_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        entry = json.loads(line)

                        # Look for assistant messages (nested under 'message' key)
                        message = entry.get('message', entry)
                        if message.get('role') == 'assistant':
                            # Extract text content from the content array
                            content = message.get('content', [])
                            if isinstance(content, list):
                                # Concatenate all text blocks (skip thinking blocks)
                                text_parts = []
                                for block in content:
                                    if isinstance(block, dict) and block.get('type') == 'text':
                                        text_parts.append(block.get('text', ''))

                                if text_parts:
                                    last_message = '\n'.join(text_parts)
                            elif isinstance(content, str):
                                last_message = content

                    except json.JSONDecodeError:
                        continue

            # Store the first attempt's result
            if attempt == 0:
                initial_message = last_message

            # If message changed from previous attempt, we got a new one - use it
            if last_message and last_message != initial_message:
                break

            # Wait a bit before retrying (except on last attempt)
            if attempt < max_retries - 1:
                time.sleep(0.3)

        # Truncate if too long
        if len(last_message) > max_length:
            last_message = last_message[:max_length] + "\n\n... (message truncated)"

        return last_message

    except Exception as e:
        print(f"Error reading transcript: {e}", file=sys.stderr)
        return ""


def convert_markdown_to_slack(text: str) -> str:
    """
    Convert standard markdown to Slack's markdown format.

    Slack uses different markdown syntax:
    - *text* for bold (not **text**)
    - _text_ for italic (not *text*)
    - Code blocks and inline code are the same

    Args:
        text: Text with standard markdown

    Returns:
        Text with Slack-compatible markdown
    """
    # Convert **text** to *text* (bold)
    # Use a negative lookbehind/lookahead to avoid matching already single asterisks
    text = re.sub(r'(?<!\*)\*\*(?!\*)(.+?)(?<!\*)\*\*(?!\*)', r'*\1*', text)

    return text


def format_message(input_data: dict, event_emoji: str = None) -> str:
    """
    Format a Slack message based on hook event type.

    Args:
        input_data: Hook input data from stdin
        event_emoji: Optional emoji to use instead of default

    Returns:
        Formatted message string
    """
    hook_event = input_data.get('hook_event_name', 'Unknown')

    # Determine emoji
    emoji_map = {
        'Notification': '🔔',
        'Stop': '✅',
        'SubagentStop': '🤖',
        'SessionStart': '🚀',
        'SessionEnd': '🏁',
        'PreCompact': '💾',
        'PreToolUse': '⚙️',
        'PostToolUse': '✔️',
    }
    emoji = event_emoji or emoji_map.get(hook_event, '📬')

    # Format message based on event type
    if hook_event == 'Notification':
        message = input_data.get('message', 'Claude Code notification')
        return f"{emoji} *Claude Code*\n{message}"

    elif hook_event == 'Stop':
        # Include the last assistant response
        transcript_path = input_data.get('transcript_path', '')
        last_response = get_last_assistant_message(transcript_path)

        if last_response:
            # Convert markdown to Slack format
            last_response = convert_markdown_to_slack(last_response)
            return f"{emoji} *Task Completed*\n\n{last_response}"
        else:
            return f"{emoji} *Task Completed*\nClaude Code has finished responding"

    elif hook_event == 'SubagentStop':
        # Include the last assistant response
        transcript_path = input_data.get('transcript_path', '')
        last_response = get_last_assistant_message(transcript_path)

        description = input_data.get('description', 'Subagent task')

        if last_response:
            # Convert markdown to Slack format
            last_response = convert_markdown_to_slack(last_response)
            return f"{emoji} *Subagent Completed: {description}*\n\n{last_response}"
        else:
            return f"{emoji} *Subagent Completed*\n{description}"

    elif hook_event == 'SessionStart':
        source = input_data.get('source', 'startup')
        return f"{emoji} *Session Started*\nClaude Code session {source}"

    elif hook_event == 'SessionEnd':
        reason = input_data.get('reason', 'unknown')
        return f"{emoji} *Session Ended*\nReason: {reason}"

    elif hook_event == 'PreCompact':
        compact_type = input_data.get('compact_type', 'unknown')
        return f"{emoji} *Compacting Context*\nType: {compact_type}"

    elif hook_event == 'PreToolUse':
        tool_name = input_data.get('tool_name', 'unknown')
        return f"{emoji} *Tool Starting*\n`{tool_name}` is about to execute"

    elif hook_event == 'PostToolUse':
        tool_name = input_data.get('tool_name', 'unknown')
        success = input_data.get('tool_response', {}).get('success', True)
        status = 'completed' if success else 'failed'
        return f"{emoji} *Tool {status.title()}*\n`{tool_name}` {status}"

    else:
        # Fallback for unknown events
        message = input_data.get('message', f'Claude Code event: {hook_event}')
        return f"{emoji} *Claude Code*\n{message}"


def send_slack_message(token: str, user_id: str, message: str) -> bool:
    """
    Send a direct message to a Slack user.

    Args:
        token: Slack bot token
        user_id: Slack user ID (e.g., U123456)
        message: Message text to send

    Returns:
        True if message sent successfully, False otherwise
    """
    try:
        client = WebClient(token=token)

        # Send message to user's DM
        response = client.chat_postMessage(
            channel=user_id,
            text=message,
            unfurl_links=False,
            unfurl_media=False
        )

        return response.get('ok', False)

    except SlackApiError as e:
        error_message = e.response.get('error', 'unknown error')
        print(f"Slack API error: {error_message}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error sending Slack message: {e}", file=sys.stderr)
        return False


def log_notification(input_data: dict, sent: bool, message: str):
    """
    Log notification to logs/slack_notification.json.

    Args:
        input_data: Original hook input data
        sent: Whether the Slack message was sent successfully
        message: The formatted message that was sent
    """
    try:
        log_dir = Path(os.getcwd()) / 'logs'
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / 'slack_notification.json'

        # Read existing log data
        if log_file.exists():
            with open(log_file, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new log entry
        log_entry = {
            'hook_event': input_data.get('hook_event_name', 'Unknown'),
            'session_id': input_data.get('session_id', ''),
            'sent': sent,
            'message': message,
        }
        log_data.append(log_entry)

        # Write back to file
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    except Exception as e:
        print(f"Error logging notification: {e}", file=sys.stderr)


def main():
    """Main entry point for the Slack notification hook."""
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(
            description='Send Slack notifications for Claude Code events'
        )
        parser.add_argument(
            '--event-emoji',
            help='Custom emoji to use for this event (overrides default)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Log only, do not send Slack message'
        )
        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Handle SessionStart: only cache the transcript path for later use
        hook_event = input_data.get('hook_event_name', '')
        if hook_event == 'SessionStart':
            transcript_path = input_data.get('transcript_path', '')
            if transcript_path:
                cache_dir = Path("logs")
                cache_dir.mkdir(exist_ok=True)
                cache_file = cache_dir / ".current-transcript"
                cache_file.write_text(transcript_path)
            # Exit early - don't send notifications for SessionStart
            sys.exit(0)

        # Check required environment variables
        slack_token = os.getenv('SLACK_BOT_TOKEN')
        slack_user_id = os.getenv('SLACK_USER_ID')

        if not slack_token or not slack_user_id:
            print(
                "Warning: SLACK_BOT_TOKEN and SLACK_USER_ID environment variables required",
                file=sys.stderr
            )
            # Log the attempt but don't send
            log_notification(input_data, False, "Missing credentials")
            sys.exit(0)

        # Format the message
        message = format_message(input_data, args.event_emoji)

        # Send Slack message (unless dry-run)
        sent = False
        if not args.dry_run:
            sent = send_slack_message(slack_token, slack_user_id, message)
        else:
            print(f"[DRY RUN] Would send: {message}")
            sent = True  # Mark as sent for logging purposes

        # Log the notification
        log_notification(input_data, sent, message)

        # Always exit successfully to not block Claude Code
        sys.exit(0)

    except json.JSONDecodeError:
        print("Error: Invalid JSON input", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()

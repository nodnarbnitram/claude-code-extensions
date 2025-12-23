#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
Discord Notification Hook for Claude Code

Sends Discord messages via webhook when Claude Code events occur.
Works cross-platform (Ubuntu/Mac/Windows) and over SSH.

Environment Variables:
    DISCORD_WEBHOOK_URL: Discord webhook URL (required)
    DISCORD_NOTIFICATIONS_ENABLED: Enable/disable (default: true)

Setup:
    1. Go to your Discord server → Server Settings → Integrations → Webhooks
    2. Create a webhook, copy the URL
    3. Set environment variable: export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

Usage:
    # In .claude/settings.json:
    {
      "hooks": {
        "Notification": [{
          "hooks": [{"type": "command", "command": "uv run ./.claude/hooks/discord_notification.py"}]
        }],
        "Stop": [{
          "hooks": [{"type": "command", "command": "uv run ./.claude/hooks/discord_notification.py --emoji ✅"}]
        }]
      }
    }

Testing:
    echo '{"hook_event_name":"Notification","message":"Test","session_id":"test"}' | \\
      uv run ./.claude/hooks/discord_notification.py
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib import request
from urllib.error import URLError, HTTPError

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def format_notification_message(input_data: dict, emoji: str = None) -> tuple[str, str]:
    """
    Format notification title and message based on event type.

    Args:
        input_data: Hook input data from stdin
        emoji: Optional custom emoji override

    Returns:
        tuple[str, str]: (title, message)
    """
    hook_event = input_data.get('hook_event_name', 'Unknown')

    # Default emoji mapping
    emoji_map = {
        'Notification': '🔔',
        'Stop': '✅',
        'SubagentStop': '🤖',
        'SessionStart': '🚀',
        'SessionEnd': '🛑',
        'PreCompact': '📦',
    }
    icon = emoji or emoji_map.get(hook_event, '📬')

    if hook_event == 'Notification':
        message = input_data.get('message', 'Claude Code notification')
        return (f"{icon} Claude Code", message)

    elif hook_event == 'Stop':
        return (f"{icon} Task Completed", "Claude Code has finished responding")

    elif hook_event == 'SubagentStop':
        description = input_data.get('description', 'Subagent task')
        return (f"{icon} Subagent Complete", description)

    elif hook_event == 'SessionStart':
        source = input_data.get('source', 'unknown')
        return (f"{icon} Session Started", f"Claude Code session started ({source})")

    elif hook_event == 'SessionEnd':
        reason = input_data.get('reason', 'unknown')
        return (f"{icon} Session Ended", f"Claude Code session ended ({reason})")

    else:
        # Fallback for unknown event types
        message = input_data.get('message', f'Event: {hook_event}')
        return (f"{icon} Claude Code", message)


def send_discord_notification(webhook_url: str, title: str, message: str, color: int = 5814783) -> bool:
    """
    Send notification to Discord via webhook.

    Args:
        webhook_url: Discord webhook URL
        title: Notification title
        message: Notification message
        color: Embed color (default: blue 5814783)

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Create Discord embed payload
        payload = {
            "embeds": [{
                "title": title,
                "description": message,
                "color": color,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "footer": {
                    "text": "Claude Code"
                }
            }]
        }

        # Send HTTP POST request
        # Discord requires User-Agent header to prevent blocking
        req = request.Request(
            webhook_url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'ClaudeCode-DiscordNotifier/1.0'
            },
            method='POST'
        )

        with request.urlopen(req, timeout=5) as response:
            if response.status == 204:  # Discord returns 204 No Content on success
                return True
            else:
                print(f"Discord API returned status {response.status}", file=sys.stderr)
                return False

    except HTTPError as e:
        print(f"Discord webhook HTTP error: {e.code} - {e.reason}", file=sys.stderr)
        return False
    except URLError as e:
        print(f"Discord webhook URL error: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error sending Discord notification: {e}", file=sys.stderr)
        return False


def log_notification(
    input_data: dict,
    title: str,
    message: str,
    sent: bool,
    webhook_url: str = None
) -> None:
    """
    Log notification event to logs/discord_notification.json.

    Args:
        input_data: Hook input data from stdin
        title: Notification title
        message: Notification message
        sent: Whether the notification was sent successfully
        webhook_url: Webhook URL (sanitized for logging)
    """
    try:
        # Ensure log directory exists
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / 'discord_notification.json'

        # Read existing log or initialize empty array
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
                    if not isinstance(log_data, list):
                        log_data = []
            except (json.JSONDecodeError, ValueError):
                log_data = []
        else:
            log_data = []

        # Sanitize webhook URL for logging (show only last 10 chars)
        webhook_display = '***' + webhook_url[-10:] if webhook_url else 'not set'

        # Create log entry
        entry = {
            'hook_event': input_data.get('hook_event_name', 'Unknown'),
            'session_id': input_data.get('session_id', ''),
            'title': title,
            'message': message,
            'sent': sent,
            'webhook': webhook_display,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        # Append and write back
        log_data.append(entry)

        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    except Exception as e:
        # Don't block on logging errors
        print(f"Warning: Failed to log notification: {e}", file=sys.stderr)


def main():
    """Main hook execution logic."""
    try:
        # Parse command-line arguments
        parser = argparse.ArgumentParser(
            description='Send Discord notifications for Claude Code events'
        )
        parser.add_argument(
            '--emoji',
            help='Custom emoji to use for this event (overrides default)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Log only, do not send Discord notification'
        )
        parser.add_argument(
            '--color',
            type=int,
            default=5814783,
            help='Discord embed color (default: 5814783 = blue)'
        )
        parser.add_argument(
            '--disable',
            action='store_true',
            help='Disable notifications (log only)'
        )

        args = parser.parse_args()

        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Check if disabled via flag or environment variable
        if args.disable or os.getenv('DISCORD_NOTIFICATIONS_ENABLED', 'true').lower() == 'false':
            sys.exit(0)

        # Get Discord webhook URL
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        if not webhook_url:
            print("Warning: DISCORD_WEBHOOK_URL not set, skipping notification", file=sys.stderr)
            sys.exit(0)

        # Format notification message
        title, message = format_notification_message(input_data, args.emoji)

        # Send notification (unless dry-run)
        sent = False
        if not args.dry_run:
            sent = send_discord_notification(webhook_url, title, message, args.color)
        else:
            print(f"[DRY RUN] Title: {title} | Message: {message}", file=sys.stderr)
            sent = True  # Mark as sent for logging purposes

        # Log the notification
        log_notification(input_data, title, message, sent, webhook_url)

        # Always exit successfully to prevent blocking Claude Code
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error in Discord notification hook: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()

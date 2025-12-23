#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
SSH OSC 777 Notification Hook for Claude Code

Sends notifications over SSH using OSC (Operating System Command) 777 escape sequences.
Automatically detects terminal type (iTerm2, Warp, VS Code) and sends appropriate sequences.

Supports:
- iTerm2: Full OSC 777 notification support
- Warp, VS Code, Generic: Window title + bell fallback

Environment Variables (optional):
    OSC_NOTIFICATIONS_ENABLED: Enable/disable notifications (default: true)
    OSC_TERMINAL_TYPE: Force specific terminal type (iterm2|warp|vscode|generic)
    OSC_EMOJI_NOTIFICATION: Custom emoji for Notification events (default: 🔔)
    OSC_EMOJI_STOP: Custom emoji for Stop events (default: ✅)
    OSC_EMOJI_SUBAGENT: Custom emoji for SubagentStop events (default: 🤖)

Usage:
    # In .claude/settings.json:
    {
      "hooks": {
        "Notification": [{
          "hooks": [{"type": "command", "command": "uv run ./.claude/hooks/ssh_osc777_notification.py"}]
        }],
        "Stop": [{
          "hooks": [{"type": "command", "command": "uv run ./.claude/hooks/ssh_osc777_notification.py --emoji ✅"}]
        }]
      }
    }

Command-Line Arguments:
    --emoji <emoji>: Custom emoji override for this event
    --dry-run: Log only, don't send OSC notification
    --force-terminal <type>: Force specific terminal type (bypass detection)
    --disable: Disable notifications (log only)

Testing:
    # Test with dry-run
    echo '{"hook_event_name":"Notification","message":"Test","session_id":"test"}' | \\
      uv run ./.claude/hooks/ssh_osc777_notification.py --dry-run

    # Test different terminal types
    uv run ./.claude/hooks/ssh_osc777_notification.py --force-terminal iterm2 < test.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def detect_terminal_type() -> str:
    """
    Detect terminal type from environment variables.

    Returns:
        str: Terminal type ('iterm2', 'warp', 'vscode', or 'generic')
    """
    term_program = os.getenv('TERM_PROGRAM', '').lower()
    term = os.getenv('TERM', '').lower()

    # Check for specific terminal programs
    if 'iterm' in term_program:
        return 'iterm2'
    elif 'warp' in term_program:
        return 'warp'
    elif 'vscode' in term_program:
        return 'vscode'
    else:
        return 'generic'


def generate_osc_notification(terminal_type: str, title: str, message: str) -> str:
    """
    Generate appropriate OSC escape sequence for terminal type.

    Args:
        terminal_type: Terminal type from detect_terminal_type()
        title: Notification title
        message: Notification message

    Returns:
        str: OSC escape sequence to write to stdout
    """
    # Sanitize text to prevent OSC injection (remove control characters)
    def sanitize(text: str) -> str:
        # Remove control characters except newline/tab, truncate to 200 chars
        cleaned = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
        cleaned = cleaned.replace('\x1b', '')  # Remove escape sequences
        return cleaned[:200]

    title = sanitize(title)
    message = sanitize(message)

    if terminal_type == 'iterm2':
        # iTerm2 supports full OSC 777 notifications
        # Format: ESC ] 777 ; notify ; title ; message BEL
        return f'\x1b]777;notify;{title};{message}\x07'
    else:
        # Fallback: Use window title change + double bell for emphasis
        # Format: ESC ] 0 ; text BEL
        combined = f"{title}: {message}"
        return f'\x1b]0;{combined}\x07\x07'


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

    # Default emoji mapping (can be overridden by env vars or CLI arg)
    emoji_map = {
        'Notification': os.getenv('OSC_EMOJI_NOTIFICATION', '🔔'),
        'Stop': os.getenv('OSC_EMOJI_STOP', '✅'),
        'SubagentStop': os.getenv('OSC_EMOJI_SUBAGENT', '🤖'),
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

    else:
        # Fallback for unknown event types
        message = input_data.get('message', f'Event: {hook_event}')
        return (f"{icon} Claude Code", message)


def send_osc_notification(terminal_type: str, title: str, message: str) -> bool:
    """
    Send OSC notification by writing to stdout.

    Note: Over SSH, OSC sequences may not work reliably because:
    - TERM_PROGRAM doesn't pass through SSH
    - OSC sequences go to remote stdout, not local terminal
    - Writing to TTY devices can freeze SSH sessions

    For SSH sessions, consider using bell-only mode or the slack_notification.py hook.

    Args:
        terminal_type: Terminal type from detect_terminal_type()
        title: Notification title
        message: Notification message

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Check if we're in an SSH session
        ssh_tty = os.getenv('SSH_TTY')

        if ssh_tty:
            # Over SSH: Just use terminal bell (safest option)
            # OSC sequences don't work reliably over SSH anyway
            sys.stdout.write('\x07')  # Single bell
            sys.stdout.flush()
        else:
            # Local session: Use full OSC sequences
            osc_sequence = generate_osc_notification(terminal_type, title, message)
            sys.stdout.write(osc_sequence)
            sys.stdout.flush()

        return True

    except Exception as e:
        print(f"Error sending OSC notification: {e}", file=sys.stderr)
        return False


def log_notification(
    input_data: dict,
    terminal_type: str,
    title: str,
    message: str,
    sent: bool
) -> None:
    """
    Log notification event to logs/ssh_osc777_notification.json.

    Args:
        input_data: Hook input data from stdin
        terminal_type: Detected terminal type
        title: Notification title
        message: Notification message
        sent: Whether the OSC notification was sent successfully
    """
    try:
        # Ensure log directory exists
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        log_file = log_dir / 'ssh_osc777_notification.json'

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

        # Create log entry
        entry = {
            'hook_event': input_data.get('hook_event_name', 'Unknown'),
            'session_id': input_data.get('session_id', ''),
            'terminal_type': terminal_type,
            'title': title,
            'message': message,
            'sent': sent,
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
            description='Send OSC 777 notifications over SSH for Claude Code events'
        )
        parser.add_argument(
            '--emoji',
            help='Custom emoji to use for this event (overrides default)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Log only, do not send OSC notification'
        )
        parser.add_argument(
            '--force-terminal',
            choices=['iterm2', 'warp', 'vscode', 'generic'],
            help='Force specific terminal type (bypass detection)'
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
        if args.disable or os.getenv('OSC_NOTIFICATIONS_ENABLED', 'true').lower() == 'false':
            sys.exit(0)

        # Detect terminal type (or use forced/env override)
        terminal_type = (
            args.force_terminal or
            os.getenv('OSC_TERMINAL_TYPE') or
            detect_terminal_type()
        )

        # Format notification message
        title, message = format_notification_message(input_data, args.emoji)

        # Send notification (unless dry-run)
        sent = False
        if not args.dry_run:
            sent = send_osc_notification(terminal_type, title, message)
        else:
            print(f"[DRY RUN] Terminal: {terminal_type} | Title: {title} | Message: {message}", file=sys.stderr)
            sent = True  # Mark as sent for logging purposes

        # Log the notification
        log_notification(input_data, terminal_type, title, message, sent)

        # Always exit successfully to prevent blocking Claude Code
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input - {e}", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error in SSH OSC notification hook: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
